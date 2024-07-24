#define LED 4
#define BUZZER 5

void setup() {
  pinMode(LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    char data = Serial.read();
    if (data == '1') {
      while (true) {
        if (Serial.available()) {
          char input = Serial.read();
          if (input == '0') {
            digitalWrite(LED, LOW);
            digitalWrite(BUZZER, LOW);
            break;
          }
        }
        
        digitalWrite(LED, HIGH);
        digitalWrite(BUZZER, HIGH);
        delay(500);
        digitalWrite(LED, LOW);
        digitalWrite(BUZZER, LOW);
        delay(500);
      }
    } else if (data == '0') {
      digitalWrite(LED, LOW);
      digitalWrite(BUZZER, LOW);
    }
  }
}

