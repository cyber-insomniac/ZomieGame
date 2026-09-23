#include "HX711.h"
#include "Keyboard.h"
#include "Mouse.h"

#define HX711_DOUT 6
#define HX711_SCK  7
#define HEAL 12
#define JOY_X A0
#define JOY_Y A1

HX711 scale;

// --- Calibration ---
// Get this properly: tare with no weight, place a known weight,
// calibration_factor = raw_reading_with_weight / known_weight
const float calibration_factor = 2469.0;

// --- Hit detection tuning ---
// These are in "scale units" (whatever your calibration_factor produces,
// e.g. kg or lbs) - tune with Serial output first before trusting them.
const float HIT_TRIGGER_THRESHOLD = 2.0;   // force needed to start counting this as a "hit"
const float RESET_THRESHOLD       = 0.5;   // must drop back below this before a new hit can register
const unsigned long CAPTURE_WINDOW_MS = 120; // how long to watch for the peak after a hit starts
const unsigned long MIN_HIT_INTERVAL_MS = 200; // hard debounce floor between hits

// --- Damage thresholds (tune to your load cells / game feel) ---
const float LIGHT_HIT_MIN = 2.0;
const float MEDIUM_HIT_MIN  = 8.0;
const float HARD_HIT_MIN = 15.0;

unsigned long lastMouseMove = 0;
const unsigned long MOUSE_INTERVAL_MS = 15; // higher = slower cursor

bool waitingForReset = false;
unsigned long lastHitTime = 0;
bool healButtonLastState = false;

void setup() {
    Serial.begin(9600);

    scale.begin(HX711_DOUT, HX711_SCK);
    scale.set_scale(calibration_factor);

    Serial.println("Remove all weight...");
    delay(3000);

    scale.tare();
    Serial.println("Scale ready!");

    pinMode(HEAL, INPUT_PULLUP);

    Keyboard.begin();
}

void loop() {

    int x = analogRead(JOY_X);
    int y = analogRead(JOY_Y);

    int mouseX = map(x, 0, 1023, -10, 10);
    int mouseY = map(y, 0, 1023, -10, 10);

    if (abs(mouseX) < 2) mouseX = 0;
    if (abs(mouseY) < 2) mouseY = 0;

  if (millis() - lastMouseMove >= MOUSE_INTERVAL_MS) {
    if (mouseX != 0 || mouseY != 0) {
        Mouse.move(mouseX, mouseY);
    }
    lastMouseMove = millis();
  }

    bool pressed = (digitalRead(HEAL) == LOW);

    if (pressed && !healButtonLastState) {
        Serial.println("Using Item");
        Keyboard.press('g');
        delay(30);
        Keyboard.release('g');
    }

    healButtonLastState = pressed;

    if (!scale.is_ready()) return; // don't block waiting for a conversion

    float reading = scale.get_units(1); // single fast sample, not an average of 10

    unsigned long now = millis();

    // If we're in cooldown, wait for force to settle before allowing another hit
    if (waitingForReset) {
        if (reading < RESET_THRESHOLD) {
            waitingForReset = false;
        }
        return;
    }

    // Detect the start of a hit
    if (reading >= HIT_TRIGGER_THRESHOLD && (now - lastHitTime) > MIN_HIT_INTERVAL_MS) {
        float peak = reading;
        unsigned long captureStart = now;

        // Watch for the true peak over a short window (the impact spike)
        while (millis() - captureStart < CAPTURE_WINDOW_MS) {
            if (scale.is_ready()) {
                float sample = scale.get_units(1);
                if (sample > peak) peak = sample;
            }
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