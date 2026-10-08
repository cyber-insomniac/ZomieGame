#include "Keyboard.h"
#include "Mouse.h"

#define attack_button   A4
#define up              2
#define left            3
#define right           4
#define down            5
#define use_button      7
#define pick_up_button  6

const int MOVE_SPEED = 5;

const unsigned long MOUSE_INTERVAL_MS = 15;
unsigned long lastMouseMove = 0;

const int HIT_TRIGGER_THRESHOLD = 100;
const int RESET_THRESHOLD       = 30;
const int LIGHT_HIT_MIN         = 750;
const int MEDIUM_HIT_MIN        = 805;
const int HARD_HIT_MIN          = 810;

const unsigned long CAPTURE_WINDOW_MS   = 120; // how long to watch for the peak after a hit starts
const unsigned long MIN_HIT_INTERVAL_MS = 200; // hard debounce floor between hits


bool waitingForReset = false;
unsigned long lastHitTime = 0;

void setup() {
    Serial.begin(9600);

    pinMode(up, INPUT);
    pinMode(left, INPUT);
    pinMode(right, INPUT);
    pinMode(down, INPUT);
    pinMode(use_button, INPUT);
    pinMode(pick_up_button, INPUT);

    Keyboard.begin();
    Mouse.begin();
}

void loop() {

    if (millis() - lastMouseMove >= MOUSE_INTERVAL_MS) {
        int mouseX = 0;
        int mouseY = 0;

        if (digitalRead(right))     mouseX += MOVE_SPEED;
        if (digitalRead(left))      mouseX -= MOVE_SPEED;
        if (digitalRead(down))      mouseY += MOVE_SPEED; // screen Y grows downward
        if (digitalRead(up))        mouseY -= MOVE_SPEED;

        if (mouseX != 0 || mouseY != 0) {
            Mouse.move(mouseX, mouseY);
        }

        lastMouseMove = millis();

    }

    if (digitalRead(use_button)){
        Keyboard.press('a');
        delay(30);
        Keyboard.release('a');
    } 
    if (digitalRead(pick_up_button)){
        Keyboard.press('e');
        delay(30);
        Keyboard.release('e');
    } 
    int reading = analogRead(attack_button);
    unsigned long now = millis();

    if (waitingForReset) {
      if (reading < RESET_THRESHOLD) {
        waitingForReset = false;
      }
    } else if (reading >= HIT_TRIGGER_THRESHOLD && (now - lastHitTime) > MIN_HIT_INTERVAL_MS) {
      int peak = reading;
      unsigned long captureStart = now;

      while (millis() - captureStart < CAPTURE_WINDOW_MS) {
        int sample = analogRead(attack_button);
        if (sample > peak) peak = sample;
      }

      registerHit(peak);

      lastHitTime = millis();
      waitingForReset = true;
  }
}

void registerHit(float peakForce) {
    Serial.print("Hit! Peak force: ");
    Serial.println(peakForce, 2);

    if (peakForce >= HARD_HIT_MIN) {
        Serial.println("-> HARD hit (h)");
        Keyboard.press('h');
        delay(30);
        Keyboard.release('h');
    } else if (peakForce >= MEDIUM_HIT_MIN) {
        Serial.println("-> MEDIUM hit (m)");
        Keyboard.press('m');
        delay(30);
        Keyboard.release('m');
    } else if (peakForce >= LIGHT_HIT_MIN) {
        Serial.println("-> light hit (l)");
        Keyboard.press('l');
        delay(30);
        Keyboard.release('l');
    } else {
        Serial.println("-> below light threshold, ignored");
    }
}