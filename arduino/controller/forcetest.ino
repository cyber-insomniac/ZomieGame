#define FORCE_SENSOR_PIN A4

void setup() {
  Serial.begin(9600);
}

void loop() {
  int analogReading = analogRead(FORCE_SENSOR_PIN);

  Serial.println(analogReading);

  delay(100);
}
