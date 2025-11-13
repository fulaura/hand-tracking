#include <CapacitiveSensor.h>

CapacitiveSensor cs_2_4 = CapacitiveSensor(2,4); // 1M resistor between pins 2 & 4

int inPin = 2; 
int outPin = 4;  
int r;           
int p = LOW;    
long time = 0;       
long debounce = 200;
// bool prev=0;

// LED pins
int ledTouch = 5;   // lights when touched
int ledRelease = 6; // lights when not touched
int ledDummy = 7;   // dummy LED, not used for now

void setup() {
  pinMode(outPin, INPUT);

  pinMode(ledTouch, OUTPUT);
  pinMode(ledRelease, OUTPUT);
  pinMode(ledDummy, OUTPUT);

  digitalWrite(ledDummy, LOW); // keep dummy LED off

  Serial.begin(9600);
}

void loop() {
  r = digitalRead(outPin);

  // Optional: send touch status over serial
  if (r == HIGH) {
    Serial.println("TOUCHED");
  } else {
    Serial.println("RELEASED");
  }

  // LED logic
  if (r == HIGH) {
    digitalWrite(ledTouch, HIGH);
    digitalWrite(ledRelease, LOW);
  } else {
    digitalWrite(ledTouch, LOW);
    digitalWrite(ledRelease, HIGH);
  }

  // Dummy LED stays off for now
  // digitalWrite(ledDummy, LOW);

  p = r; // store previous state

  delay(10); // stabilize readings
}
