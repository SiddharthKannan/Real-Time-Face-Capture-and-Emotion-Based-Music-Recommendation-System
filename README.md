# Emotion-Based Music Recommendation System v2.0

An updated version of the Emotion-Based Music Recommendation System, now featuring a **live ESP32-CAM feed** for real-time facial emotion detection — replacing the previous version which only supported static image uploads.

---

## What's New in v2.0
The original system required users to manually upload stock photos or images to detect emotions. This updated version integrates an **ESP32-CAM** module that streams a live camera feed directly to the web interface, allowing real-time face capture and emotion analysis at the click of a button.

---

## How It Works
1. The ESP32-CAM streams a live video feed to the web interface
2. When you click **"Analyze Live Face Now"**, the stream pauses and a snapshot is captured
3. The image is sent to the Flask server, which detects the face and predicts the emotion using a trained CNN model
4. Based on the detected emotion, 5 song recommendations are returned and displayed in the interface
5. The live stream resumes automatically after a few seconds

---

## Emotion to Mood Mapping
| Detected Emotion | Music Mood |
|-----------------|------------|
| Happy, Sad | Happy |
| Fear, Angry | Calm |
| Surprise, Neutral | Energetic |
| Disgust | Sad |

---

## Hardware Requirements
- ESP32-CAM module (AI Thinker board)
- FTDI programmer or USB-to-TTL adapter (for flashing the ESP32)
- A PC/laptop on the same WiFi network as the ESP32-CAM

---

## Software Requirements
- Python 3.x with the following libraries:
```
  pip install flask opencv-python tensorflow pandas numpy requests
```
- Arduino IDE with the following board/library support:
  - ESP32 board package installed
  - `esp_camera.h` library

---

## Project Structure
```
EmotionBasedMusicRecommendationSystem/
│
├── app1.py                  # Flask backend
├── templates/
│   └── index.html           # Web interface
├── haar/
│   └── haarcascade_frontalface_default.xml  # Face detection classifier
├── uploads/                 # Temporary image storage
└── arduino/
    └── realflaskupload/
        └── realflaskupload.ino  # ESP32-CAM Arduino code
```

---

## Setup & Running

### 1. Flash the ESP32-CAM
- Open `arduino/realflaskupload/realflaskupload.ino` in Arduino IDE
- Update the WiFi credentials:
```cpp
  const char* ssid     = "YOUR_WIFI_NAME";
  const char* password = "YOUR_WIFI_PASSWORD";
```
- Update the Flask server IP to match your PC's local IP:
```cpp
  const char* serverUrl = "http://YOUR_PC_IP:8080/predict";
```
- Select board: **AI Thinker ESP32-CAM**
- Flash the code and restart the ESP32

### 2. Run the Flask Server
- Navigate to the project folder in your terminal/Anaconda prompt
- Run:
```
  python app1.py
```
- The server will start at `http://0.0.0.0:8080`

### 3. Open the Web Interface
- On any device on the same WiFi network, open your browser and go to:
```
  http://YOUR_PC_IP:8080
```

---

## Using the System

### Option 1 — Upload Image (original feature)
- Click **Choose File**, select any photo with a face, and hit **Submit**
- The system will detect the emotion and recommend songs

### Option 2 — Live ESP32-CAM (new feature)
- Point the ESP32-CAM at your face
- Click **Analyze Live Face Now**
- The stream will briefly pause, capture your face, analyze the emotion, and display song recommendations
- The live stream resumes automatically after a few seconds

---

## Notes
- The ESP32-CAM can only handle one connection at a time, so the live stream is paused during capture — this is expected behavior
- Make sure your PC and ESP32-CAM are on the same WiFi network
- The `CNN_Model.h5` file may be too large for GitHub — use Git LFS or host it separately if needed
