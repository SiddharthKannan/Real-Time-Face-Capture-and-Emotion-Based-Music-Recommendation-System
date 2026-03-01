from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import pandas as pd
import os
import requests
import traceback

app = Flask(__name__)

# Load the trained model
model = load_model("./model/CNN_Model.h5")

# Define emotion classes
Emotion_Classes = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# Load the music player data
Music_Player = pd.read_csv("./dataset/data_moods.csv")

# Preprocess the image
def load_and_prep_image(filename, img_shape=48):

    img = cv2.imread(filename)

    if img is None:
        raise ValueError("Image could not be loaded")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier(
        "./haar/haarcascade_frontalface_default.xml"
    )

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=4
    )

    # If face detected, crop first face
    if len(faces) > 0:
        x, y, w, h = faces[0]
        face_img = img[y:y+h, x:x+w]
    else:
        # Fallback: use entire image
        face_img = img

    # Convert to RGB
    face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)

    # Resize to model input size
    face_img = cv2.resize(face_img, (img_shape, img_shape))

    # Normalize
    face_img = face_img / 255.0

    return face_img

# Predict emotion and recommend songs
def predict_emotion_and_recommend(filename):
    img = load_and_prep_image(filename)
    pred = model.predict(np.expand_dims(img, axis=0))
    pred_class = Emotion_Classes[np.argmax(pred)]
    recommendations = recommend_songs(pred_class)
    return pred_class, recommendations

# Recommend songs based on predicted emotion
def recommend_songs(pred_class):
    recommendations = []

    if pred_class == 'Disgust':
        recommendations = get_music_recommendations('Sad')
    elif pred_class in ['Happy', 'Sad']:
        recommendations = get_music_recommendations('Happy')
    elif pred_class in ['Fear', 'Angry']:
        recommendations = get_music_recommendations('Calm')
    elif pred_class in ['Surprise', 'Neutral']:
        recommendations = get_music_recommendations('Energetic')

    return recommendations

# Get music recommendations for a given mood
def get_music_recommendations(mood):
    songs = Music_Player[Music_Player['mood'] == mood]
    songs = songs.sort_values(by="popularity", ascending=False)[:5]
    recommendations = songs[['album', 'artist', 'name', 'popularity', 'release_date']].to_dict(orient='records')
    return recommendations

@app.route('/')
def home():
    return render_template('index.html')

# Proxy route to capture image from ESP32-CAM (avoids browser CORS issues)
@app.route('/capture_from_esp', methods=['GET'])
def capture_from_esp():
    esp_url = "http://192.168.1.212/capture"
    try:
        print(f"Attempting to connect to ESP32 at {esp_url}")
        response = requests.get(esp_url, timeout=10)
        print(f"ESP32 responded with status: {response.status_code}, size: {len(response.content)} bytes")
        return response.content, 200, {'Content-Type': 'image/jpeg'}
    except Exception as e:
        traceback.print_exc()
        print(f"Error connecting to ESP32: {str(e)}")
        return jsonify({'error': str(e)}), 500

# API endpoint for prediction and recommendations
@app.route('/predict', methods=['POST'])
def predict():
    # Support both FormData (file upload) and raw bytes
    if 'file' in request.files:
        file = request.files['file']
        image_bytes = file.read()
    else:
        image_bytes = request.data

    if image_bytes is None or len(image_bytes) == 0:
        return jsonify({'error': 'No image data received'}), 400

    # Convert bytes to OpenCV image
    img_array = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({'error': 'Invalid image data'}), 400

    # Save temporarily
    temp_path = "./uploads/esp32.jpg"
    cv2.imwrite(temp_path, img)

    emotion, recommendations = predict_emotion_and_recommend(temp_path)

    return jsonify({
        'emotion': emotion,
        'recommendations': recommendations
    }), 200

@app.route('/trigger_analysis', methods=['POST'])
def trigger_analysis():
    return jsonify({'status': 'Trigger received - waiting for next capture'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)