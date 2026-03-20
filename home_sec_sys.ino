#include <Servo.h>

const int pirPin = 2; 
const int ldrPin = A0; 
const int redLedPin = 10;      // RED LED (Face not recognized) 
const int greenLedPin = 11;    // GREEN LED (face recognized) 
const int buzzerPin = 4; 
const int ldrLedPin = 8;       //LED next to LDR ( if low light ) 
const int lightThreshold = 100; 

Servo myServo;

void setup() {
  pinMode(pirPin, INPUT); 
  pinMode(redLedPin, OUTPUT); 
  pinMode(greenLedPin, OUTPUT); 
  pinMode(buzzerPin, OUTPUT); 
  pinMode(ldrLedPin, OUTPUT);    
  Serial.begin(9600); 
}

void loop() {
  int pirValue = digitalRead(pirPin);
  int ldrValue = analogRead(ldrPin);

  
  // LDR control for its own LED (independent of motion) 
  if (ldrValue < lightThreshold) { 
    digitalWrite(ldrLedPin, HIGH); 
    }
  else { 
    digitalWrite(ldrLedPin, LOW); 
    }
  
  // PIR Motion Detection 
  if (pirValue == HIGH) { 
    Serial.println("MOTION"); 
    digitalWrite(redLedPin, HIGH); // Red LED ON for motion 
    unsigned long startTime = millis(); 
    while (millis() - startTime < 10000) { 
      if (Serial.available() > 0) { 
        char cmd = Serial.read(); 
        if (cmd == 'G') { 
          digitalWrite(greenLedPin, HIGH); 
          digitalWrite(redLedPin, LOW); 
          noTone(buzzerPin); 
          Serial.println("GREEN_ON"); 
          delay(5000); 
          digitalWrite(greenLedPin, LOW); 
          Serial.println("GREEN_OFF"); 
          break; 
        } 
        else if (cmd == 'B') { 
          tone(buzzerPin, 1000); 
          digitalWrite(redLedPin, HIGH); 
          Serial.println("BUZZED"); 
          delay(3000); 
          noTone(buzzerPin); 
          digitalWrite(redLedPin, LOW); 
          Serial.println("BUZZ_OFF"); 
          break; 
        } 
      } 
    } 
  }
  else { 
    digitalWrite(redLedPin, LOW); 
    digitalWrite(greenLedPin, LOW); 
    noTone(buzzerPin); 
  } 

delay(100); 
} 