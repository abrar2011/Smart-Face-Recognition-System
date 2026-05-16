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

// Warning ⚠
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

// Question ❓
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

// Lock Closed 🔒
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

// Lock Open 🔓
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

// X mark ❌
byte deniedIcon[8] = {
  B10001,
  B01010,
  B00100,
  B00100,
  B00100,
  B01010,
  B10001,
  B00000
};

// =========================
// SETUP
// =========================
void setup() {

  Serial.begin(9600);

  lcd.begin(16, 2);

  // Create custom chars
  lcd.createChar(0, smiley);
  lcd.createChar(1, warning);
  lcd.createChar(2, question);
  lcd.createChar(3, lockClosed);
  lcd.createChar(4, lockOpen);
  lcd.createChar(5, deniedIcon);

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("System Ready");

  lcd.setCursor(0, 1);
  lcd.print("Waiting...");
}

// =========================
// LOOP
// =========================
void loop() {

  if (Serial.available()) {

    String msg = Serial.readStringUntil('\n');

    msg.trim();

    Serial.print("Received: ");
    Serial.println(msg);

    lcd.clear();

    // =========================
    // AUTHORIZED
    // =========================
    if (msg == "AUTHORIZED") {

      lcd.setCursor(0, 0);
      lcd.write(byte(0));
      lcd.print(" AUTHORIZED");

      lcd.setCursor(0, 1);
      lcd.write(byte(4));
      lcd.print(" UNLOCKED");
    }

    // =========================
    // THREAT
    // =========================
    else if (msg == "THREAT") {

      lcd.setCursor(0, 0);
      lcd.write(byte(1));
      lcd.print(" THREAT");

      lcd.setCursor(0, 1);
      lcd.write(byte(3));
      lcd.print(" LOCKED");
    }

    // =========================
    // WAITING APPROVAL
    // =========================
    else if (msg == "WAITING") {

      lcd.setCursor(0, 0);
      lcd.write(byte(2));
      lcd.print(" UNKNOWN");

      lcd.setCursor(0, 1);
      lcd.print("WAITING APPROV");
    }

    // =========================
    // ALLOW
    // =========================
    else if (msg == "ALLOW") {

      lcd.setCursor(0, 0);
      lcd.write(byte(0));
      lcd.print(" ACCESS OK");

      lcd.setCursor(0, 1);
      lcd.write(byte(4));
      lcd.print(" UNLOCKED");
    }

    // =========================
    // DENY
    // =========================
    else if (msg == "DENY") {

      lcd.setCursor(0, 0);
      lcd.write(byte(5));
      lcd.print(" ACCESS DENY");

      lcd.setCursor(0, 1);
      lcd.write(byte(3));
      lcd.print(" LOCKED");
    }

    // =========================
    // RESET
    // =========================
    else if (msg == "Reset") {

      lcd.setCursor(0, 0);
      lcd.print("System Ready");

      lcd.setCursor(0, 1);
      lcd.print("Waiting...");
    }

    // =========================
    // UNKNOWN MESSAGE
    // =========================
    else {

      lcd.setCursor(0, 0);
      lcd.print("Unknown Cmd");
a
      lcd.setCursor(0, 1);
      lcd.print(msg);
    }
  }
}
