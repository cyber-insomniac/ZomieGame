#include "Keyboard.h"
#include "Mouse.h"
#include <EEPROM.h>

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

// ----- Calibratable thresholds (no longer const - calibration overwrites these) -----
int HIT_TRIGGER_THRESHOLD = 100;
int RESET_THRESHOLD       = 30;
int LIGHT_HIT_MIN         = 450;
int MEDIUM_HIT_MIN        = 800;
int HARD_HIT_MIN          = 850;

const unsigned long CAPTURE_WINDOW_MS   = 120; // how long to watch for the peak after a hit starts
const unsigned long MIN_HIT_INTERVAL_MS = 200; // hard debounce floor between hits

// Minimum reading that counts as "a stomp started" during calibration -
// deliberately low/generic since we don't know the real thresholds yet.
const int CALIBRATION_NOISE_FLOOR = 50;

bool waitingForReset = false;
unsigned long lastHitTime = 0;

// Edge-detection state for use/pickup buttons
bool useLastState    = false;
bool pickupLastState = false;
bool bothLastState    = false;

// EEPROM layout
const int EEPROM_MAGIC_ADDR = 0;
const byte EEPROM_MAGIC_VALUE = 0xA5; // marks "valid calibration saved"
const int EEPROM_DATA_ADDR = 1;

struct CalibrationData {
    int hitTrigger;
    int reset;
    int light;
    int medium;
    int hard;
};

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

    loadCalibration();
}

void loop() {

    // ----- Mouse movement -----
    if (millis() - lastMouseMove >= MOUSE_INTERVAL_MS) {
        int mouseX = 0;
        int mouseY = 0;

        if (digitalRead(right)) mouseX += MOVE_SPEED;
        if (digitalRead(left))  mouseX -= MOVE_SPEED;
        if (digitalRead(down))  mouseY += MOVE_SPEED; // screen Y grows downward
        if (digitalRead(up))    mouseY -= MOVE_SPEED;

        if (mouseX != 0 || mouseY != 0) {
            Mouse.move(mouseX, mouseY);
        }

        lastMouseMove = millis();
    }

    // ----- Use / pick up buttons (single press) + calibration combo -----
    bool useState    = digitalRead(use_button);
    bool pickupState = digitalRead(pick_up_button);
    bool bothPressed = useState && pickupState;

    if (bothPressed && !bothLastState) {
        // Rising edge of "both held together" - enter calibration.
        runCalibration();
        // Clear edge states so releasing the buttons afterward doesn't
        // immediately fire a stray 'g' or 'e'.
        useState = false;
        pickupState = false;
    } else if (!bothPressed) {
        if (useState && !useLastState) {
            Keyboard.press('g');
            delay(30);
            Keyboard.release('g');
        }
        if (pickupState && !pickupLastState) {
            Keyboard.press('e');
            delay(30);
            Keyboard.release('e');
        }
    }

    useLastState    = useState;
    pickupLastState = pickupState;
    bothLastState   = bothPressed;

    // ----- Attack / hit detection -----
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

void registerHit(int peakForce) {
    Serial.print("Hit! Peak force: ");
    Serial.println(peakForce);

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

// ---------------------------------------------------------------------
// Calibration
// ---------------------------------------------------------------------

// Blocks until a stomp is detected on attack_button, captures its peak
// over CAPTURE_WINDOW_MS, then waits for the sensor to settle back down
// before returning - so three separate stomps don't bleed into each other.
int waitForStomp(const char* label) {
    Serial.print("Do a ");
    Serial.print(label);
    Serial.println(" stomp now...");

    // Wait for the stomp to start
    int reading;
    do {
        reading = analogRead(attack_button);
    } while (reading < CALIBRATION_NOISE_FLOOR);

    // Capture the peak
    int peak = reading;
    unsigned long captureStart = millis();
    while (millis() - captureStart < CAPTURE_WINDOW_MS) {
        int sample = analogRead(attack_button);
        if (sample > peak) peak = sample;
    }

    Serial.print(label);
    Serial.print(" peak: ");
    Serial.println(peak);

    // Wait for release before accepting the next stomp
    do {
        reading = analogRead(attack_button);
    } while (reading > CALIBRATION_NOISE_FLOOR);

    delay(300); // brief pause so the player can reset their stance
    return peak;
}

void runCalibration() {
    Serial.println("=== CALIBRATION MODE ===");
    Serial.println("Release both buttons, then stomp as prompted.");
    delay(1000);

    int lightPeak  = waitForStomp("LIGHT");
    int mediumPeak = waitForStomp("NORMAL");
    int hardPeak   = waitForStomp("HARD");

    if (!(hardPeak > mediumPeak && mediumPeak > lightPeak)) {
        Serial.println("Warning: stomps weren't in increasing order (light < normal < hard).");
        Serial.println("Calibration will still be applied, but double-check your results.");
    }

    HIT_TRIGGER_THRESHOLD = lightPeak * 0.4;
    RESET_THRESHOLD        = lightPeak * 0.15;
    LIGHT_HIT_MIN           = lightPeak * 0.7;
    MEDIUM_HIT_MIN          = (lightPeak + mediumPeak) / 2;
    HARD_HIT_MIN            = (mediumPeak + hardPeak) / 2;

    Serial.println("=== New thresholds ===");
    Serial.print("HIT_TRIGGER_THRESHOLD: "); Serial.println(HIT_TRIGGER_THRESHOLD);
    Serial.print("RESET_THRESHOLD: ");       Serial.println(RESET_THRESHOLD);
    Serial.print("LIGHT_HIT_MIN: ");         Serial.println(LIGHT_HIT_MIN);
    Serial.print("MEDIUM_HIT_MIN: ");        Serial.println(MEDIUM_HIT_MIN);
    Serial.print("HARD_HIT_MIN: ");          Serial.println(HARD_HIT_MIN);

    saveCalibration();
    Serial.println("Calibration saved. Ready to play!");
}

void saveCalibration() {
    CalibrationData data = { HIT_TRIGGER_THRESHOLD, RESET_THRESHOLD, LIGHT_HIT_MIN, MEDIUM_HIT_MIN, HARD_HIT_MIN };
    EEPROM.put(EEPROM_DATA_ADDR, data);
    EEPROM.write(EEPROM_MAGIC_ADDR, EEPROM_MAGIC_VALUE);
}

void loadCalibration() {
    if (EEPROM.read(EEPROM_MAGIC_ADDR) != EEPROM_MAGIC_VALUE) {
        Serial.println("No saved calibration found - using defaults.");
        return; // nothing saved yet, keep the compiled-in defaults above
    }

    CalibrationData data;
    EEPROM.get(EEPROM_DATA_ADDR, data);

    HIT_TRIGGER_THRESHOLD = data.hitTrigger;
    RESET_THRESHOLD        = data.reset;
    LIGHT_HIT_MIN           = data.light;
    MEDIUM_HIT_MIN          = data.medium;
    HARD_HIT_MIN            = data.hard;

    Serial.println("Loaded saved calibration.");
}