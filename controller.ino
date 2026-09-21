#include "Keyboard.h"
#include "Mouse.h"

int button = 12;
int joy_b = 2;
int joy_x = A0;
int joy_y = A1;


void setup() {
  // put your setup code here, to run once:
  pinMode(button, INPUT);
  pinMode(joy_b, INPUT_PULLUP);
  Mouse.begin();
  Keyboard.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
  if (digitalRead(button)) {
    Keyboard.press('a');
  } else {
    Keyboard.release('a');
  };

  int x = analogRead(joy_x);
  int y = analogRead(joy_y);

  int mouseX = map(x, 0, 1023, -10, 10);
  int mouseY = map(y, 0, 1023, -10, 10);

  if (abs(mouseX) < 2) mouseX = 0;
  if (abs(mouseY) < 2) mouseY = 0;


  Mouse.move(mouseX, mouseY);

  // Joystick button = left mouse button
  if (digitalRead(joy_b) == LOW) {
    Mouse.press(MOUSE_LEFT);
  } else {
    Mouse.release(MOUSE_LEFT);
  }

  delay(10);
}