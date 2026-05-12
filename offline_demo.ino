#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 7);

const int greenLED = 8;
const int redLED = 9;

String input = "";

void setup() {
  Serial.begin(9600);

  lcd.begin(16, 2);

  pinMode(greenLED, OUTPUT);
  pinMode(redLED, OUTPUT);

  lcd.print("System Ready");

  delay(2000);

lcd.clear();

lcd.setCursor(0,0);
lcd.print("System Ready");
}

void loop() {

  if (Serial.available()) {

    input = Serial.readStringUntil('\n');
    input.trim();

    lcd.clear();

    if (input == "AUTHORIZED") {

      lcd.setCursor(0, 0);
      lcd.print("AUTHORIZED");

      lcd.setCursor(0, 1);
      lcd.print("UNLOCKED");

      digitalWrite(greenLED, HIGH);
      digitalWrite(redLED, LOW);
    }

    else if (input == "THREAT") {

      lcd.setCursor(0, 0);
      lcd.print("THREAT");

      lcd.setCursor(0, 1);
      lcd.print("LOCKED");

      digitalWrite(greenLED, LOW);
      digitalWrite(redLED, HIGH);
    }

    else {

      lcd.setCursor(0, 0);
      lcd.print("UNKNOWN");

      lcd.setCursor(0, 1);
      lcd.print("WAITING");

      digitalWrite(greenLED, LOW);
      digitalWrite(redLED, LOW);
    }
  }
}
