#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

Servo doorServo;

// =========================
// CUSTOM CHARACTERS
// =========================

// 🙂 Smiley
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

// ⚠ Warning
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

// ❓ Question
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

// 🔒 Lock Closed
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

// 🔓 Lock Open
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

// ❌ Denied
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

  lcd.init();
  lcd.backlight();

  // Servo
  doorServo.attach(9);

  // LOCKED position
  doorServo.write(0);

  // Create chars
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

      doorServo.write(90);

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

      doorServo.write(0);

      lcd.setCursor(0, 0);
      lcd.write(byte(1));
      lcd.print(" THREAT");

      lcd.setCursor(0, 1);
      lcd.write(byte(3));
      lcd.print(" LOCKED");
    }

    // =========================
    // WAITING
    // =========================
    else if (msg == "WAITING") {

      doorServo.write(0);

      lcd.setCursor(0, 0);
      lcd.write(byte(2));
      lcd.print(" UNKNOWN");

      lcd.setCursor(0, 1);
      lcd.print("WAIT...");
    }

    // =========================
    // ALLOW
    // =========================
    else if (msg == "ALLOW") {

      doorServo.write(90);

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

      doorServo.write(0);

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

      doorServo.write(0);

      lcd.setCursor(0, 0);
      lcd.print("ed
      ");

      lcd.setCursor(0, 1);
      lcd.print("Alaikum");
    }

    // =========================
    // UNKNOWN CMD
    // =========================
    else {

      lcd.setCursor(0, 0);
      lcd.print("Unknown Cmd");

      lcd.setCursor(0, 1);
      lcd.print(msg);
    }
  }
}
