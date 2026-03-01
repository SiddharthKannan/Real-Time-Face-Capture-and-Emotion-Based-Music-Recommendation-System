/*
  Blink

  Turns an LED on for one second, then off for one second, repeatedly.
*/

// Most ESP32 boards don't define LED_BUILTIN, so we define it ourselves
#define LED_PIN 33  // GPIO33 = onboard red LED on AI Thinker ESP32-CAM

void setup() {
  // initialize digital pin as an output.
  pinMode(LED_PIN, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(LED_PIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);                   // wait for a second
  digitalWrite(LED_PIN, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);                   // wait for a second
}