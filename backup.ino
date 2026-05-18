#include <Keypad.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>
#include <Servo.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);
Servo doorServo;

// =========================
// PASSWORD VARIABLES
// =========================
String enteredPassword = "";
String given_pwd = "";
bool enteringPassword = false;

// =========================
// KEYPAD SETUP
// =========================
const byte ROWS = 4;
const byte COLS = 4;

char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};

byte rowPins[ROWS] = {2, 3, 4, 5};
byte colPins[COLS] = {6, 7, 8, 10};

Keypad keypad = Keypad(
  makeKeymap(keys),
  rowPins,
  colPins,
  ROWS,
  COLS
);

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

  // LOCKED POSITION
  doorServo.write(0);

  // Create custom chars
  lcd.createChar(0, smiley);
  lcd.createChar(1, warning);
  lcd.createChar(2, question);
  lcd.createChar(3, lockClosed);
  lcd.createChar(4, lockOpen);
  lcd.createChar(5, deniedIcon);

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("Assalamu Alaikum");

  lcd.setCursor(0, 1);
  lcd.print("System Ready...");
}

// =========================
// LOOP
// =========================
void loop() {

  char key = keypad.getKey();

  if (key) {

    // =========================
    // REQUEST ACCESS
    // =========================
    if (key == 'A') {

      Serial.println("A_PRESSED");

      lcd.clear();

      lcd.setCursor(0, 0);
      lcd.print("PLEASE WAIT");

      lcd.setCursor(0, 1);
      lcd.print("OWNER VERIFY");

      enteringPassword = false;
    }

    // =========================
    // START PASSWORD MODE
    // =========================
    else if (key == 'B') {

      enteringPassword = true;

      enteredPassword = "";

      lcd.clear();

      lcd.setCursor(0, 0);
      lcd.print("PASSWORD:");

      lcd.setCursor(0, 1);
      lcd.print("---");
    }

    // =========================
    // PASSWORD INPUT
    // =========================
    else if (
      enteringPassword &&
      key >= '0' &&
      key <= '9'
    ) {

      if (enteredPassword.length() < 3) {

        enteredPassword += key;

        lcd.setCursor(
          enteredPassword.length() - 1,
          1
        );

        lcd.print(key);
      }
    }

    // =========================
    // CONFIRM PASSWORD
    // =========================
    else if (
      enteringPassword &&
      key == 'C'
    ) {

      if (enteredPassword.length() == 3) {

        given_pwd = enteredPassword;

        lcd.clear();

        lcd.setCursor(0, 0);
        lcd.print("ENTERED:");

        lcd.setCursor(0, 1);
        lcd.print(given_pwd);

        Serial.print("Password: ");
        Serial.println(given_pwd);

        // =========================
        // CHECK PASSWORD
        // =========================
        if (given_pwd == "679") {

          lcd.clear();

          lcd.setCursor(0, 0);
          lcd.write(byte(0));
          lcd.print(" ACCESS OK");

          lcd.setCursor(0, 1);
          lcd.write(byte(4));
          lcd.print(" UNLOCKED");

          doorServo.write(90);
        }

        else {

          lcd.clear();

          lcd.setCursor(0, 0);
          lcd.write(byte(5));
          lcd.print(" WRONG PASSWORD");

          lcd.setCursor(0, 1);
          lcd.write(byte(3));
          lcd.print(" LOCKED");

          doorServo.write(0);
        }

        enteringPassword = false;
      }
    }

    // =========================
    // CLEAR PASSWORD
    // =========================
    else if (
      enteringPassword &&
      key == '*'
    ) {

      enteredPassword = "";

      lcd.clear();

      lcd.setCursor(0, 0);
      lcd.print("PASSWORD:");

      lcd.setCursor(0, 1);
      lcd.print("---");
    }
  }
   
      

  // =========================
  // SERIAL COMMANDS
  // =========================
  if (Serial.available()) {

    String msg = Serial.readStringUntil('\n');

    msg.trim();

    Serial.print("Received: ");
    Serial.println(msg);

    // =========================
    // AUTHORIZED
    // =========================
    if (msg == "AUTHORIZED") {

      lcd.clear();

      lcd.setCursor(0, 0);
      lcd.write(byte(0));
      lcd.print(" AUTHORIZED");

      lcd.setCursor(0, 1);
      lcd.write(byte(4));
      lcd.print(" UNLOCKED");

      doorServo.write(90);
    }

    // =========================
    // THREAT
    // =========================
    else if (msg == "THREAT") {

      lcd.clear();

      lcd.setCursor(0, 0);
      lcd.write(byte(1));
      lcd.print(" THREAT");

      lcd.setCursor(0, 1);
      lcd.write(byte(3));
      lcd.print(" LOCKED");

      doorServo.write(0);
    }

    // =========================
    // WAITING
    // =========================
    else if (msg == "WAITING") {

      lcd.clear();

      lcd.setCursor(0, 0);
      lcd.write(byte(2));
      lcd.print(" UNKNOWN");

      lcd.setCursor(0, 1);
      lcd.print("WAITING...");
    }

    // =========================
    // ALLOW
    // =========================
    else if (msg == "ALLOW") {

      lcd.clear();

      lcd.setCursor(0, 0);
      lcd.write(byte(0));
      lcd.print(" ACCESS OK");

      lcd.setCursor(0, 1);
      lcd.write(byte(4));
      lcd.print(" UNLOCKED");

      doorServo.write(90);
    }

    // =========================
    // DENY
    // =========================
    else if (msg == "DENY") {

      lcd.clear();

      lcd.setCursor(0, 0);
      lcd.write(byte(5));
      lcd.print(" ACCESS DENY");

      lcd.setCursor(0, 1);
      lcd.write(byte(3));
      lcd.print(" LOCKED");

      doorServo.write(0);
    }

    // =========================
    // RESET
    // =========================
    else if (msg == "Reset") {

      lcd.clear();

      lcd.setCursor(0, 0);
      lcd.print("Asslamu Alaikum");

      lcd.setCursor(0, 1);
      lcd.print("System Ready...");

      doorServo.write(0);
    }
  }
}
