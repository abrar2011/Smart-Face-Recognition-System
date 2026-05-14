#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 7);

// =========================
// CUSTOM CHARACTERS
// =========================

// Smiley 🙂
byte smiley[8] = {
  B00000,
  B01010,
  B01010,
  B00000,
  B10001,
  B01110,
  B00000,
  B00000
};

// Warning ⚠️ (simple triangle)
byte warning[8] = {
  B00100,
  B01110,
  B01110,
  B01110,
  B00100,
  B00100,
  B00000,
  B00100
};

// Question mark ❓
byte question[8] = {
  B01110,
  B10001,
  B00010,
  B00100,
  B00100,
  B00000,
  B00100,
  B00000
};

// Lock closed 🔒
byte lockClosed[8] = {
  B01110,
  B10001,
  B10001,
  B11111,
  B11011,
  B11011,
  B11111,
  B00000
};

// Lock open 🔓
byte lockOpen[8] = {
  B01110,
  B10000,
  B10000,
  B11111,
  B11011,
  B11011,
  B11111,
  B00000
};

// =========================
// SETUP
// =========================
void setup() {

  Serial.begin(9600);

  lcd.begin(16, 2);

  // create characters
  lcd.createChar(0, smiley);
  lcd.createChar(1, warning);
  lcd.createChar(2, question);
  lcd.createChar(3, lockClosed);
  lcd.createChar(4, lockOpen);

  lcd.setCursor(0, 0);
  lcd.print("System Ready");
}

// =========================
// LOOP
// =========================
void loop() {

  if (Serial.available()) {

    String msg = Serial.readStringUntil('\n');
    msg.trim();

    lcd.clear();

    // =========================
    // AUTHORIZED
    // =========================
    if (msg == "AUTHORIZED") {

      lcd.setCursor(0, 0);
      lcd.write(byte(0)); // smiley
      lcd.print(" AUTHORIZED");

      lcd.setCursor(0, 1);
      lcd.write(byte(4)); // open lock
      lcd.print(" UNLOCKED");
    }

    // =========================
    // THREAT
    // =========================
    else if (msg == "THREAT") {

      lcd.setCursor(0, 0);
      lcd.write(byte(1)); // warning
      lcd.print(" THREAT");

      lcd.setCursor(0, 1);
      lcd.write(byte(3)); // closed lock
      lcd.print(" LOCKED");
    }

    // =========================
    // RESET
    // =========================
    else if (msg == "Reset") {

      lcd.setCursor(0,0);
      lcd.print("System Ready")
    }

    // =========================
    // UNKNOWN
    // =========================
    else {

      lcd.setCursor(0, 0);
      lcd.write(byte(2)); // question mark
      lcd.print(" UNKNOWN");

      lcd.setCursor(0, 1);
      lcd.print(" ACCESS DENIED");
    }
  }
}
