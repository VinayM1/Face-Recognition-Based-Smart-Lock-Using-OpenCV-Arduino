#include <Servo.h>
Servo myServo;

void setup() {
  Serial.begin(9600);
  myServo.attach(9); // Connect to D9
  myServo.write(0);  // Locked
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();
    if (command == 'U') {
      myServo.write(90);  // Unlock
      delay(5000);
      myServo.write(0);   // Lock again
    } else if (command == 'L') {
      myServo.write(0);   // Force lock
    }
  }
}
