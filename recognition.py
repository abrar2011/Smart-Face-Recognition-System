import serial
import cv2
import numpy as np
import time
from datetime import datetime
import requests

# =========================
# FLASK SEND FUNCTION
# =========================
def send_event(event_type, message):

    print("SENDING →", event_type, message)

    try:
        requests.post(
            "http://127.0.0.1:5000/event",
            json={
                "type": event_type,
                "message": message
            }
        )
    except Exception as e:
        print("Flask send error:", e)


# =========================
# SERIAL (ARDUINO)
# =========================
arduino = None

print("System Starting...")

try:
    arduino = serial.Serial('COM13', 9600)
    time.sleep(2)
    print("Arduino connected")

except:
    print("Arduino NOT connected (PC mode only)")


# =========================
# FACE RECOGNIZER
# =========================
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

labels = np.load("labels.npy", allow_pickle=True).item()


# =========================
# FACE DETECTOR
# =========================
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


# =========================
# CAMERA
# =========================
cam = cv2.VideoCapture(0)


# =========================
# SETTINGS
# =========================
CONFIDENCE_THRESHOLD = 50

# prevent spam
last_sent = 0
cooldown = 2  # seconds


# =========================
# MAIN LOOP
# =========================
while True:

    ret, frame = cam.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    current_role = "UNKNOWN"
    name = "Unknown"

    # =========================
    # FACE LOOP
    # =========================
    for (x, y, w, h) in faces:

        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (200, 200))

        label_id, confidence = recognizer.predict(face)

        role = "UNKNOWN"
        color = (0, 255, 255)

        if confidence < CONFIDENCE_THRESHOLD:

            person_data = labels[label_id]

            name = person_data["name"]
            role = person_data["role"]

            if role.lower() == "authorized":
                role = "AUTHORIZED"
                color = (0, 255, 0)

            elif role.lower() == "threat":
                role = "THREAT"
                color = (0, 0, 255)

        current_role = role

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

        cv2.putText(
            frame,
            f"{name} - {role}",
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

    # =========================
    # TOP BAR
    # =========================
    cv2.rectangle(frame, (0, 0), (800, 40), (30, 30, 30), -1)

    cv2.putText(frame, f"Time: {timestamp}",
                (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255), 1)

    cv2.putText(frame, f"STATUS: {current_role}",
                (450, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0) if current_role == "AUTHORIZED"
                else (0, 0, 255) if current_role == "THREAT"
                else (0, 255, 255),
                2)

    cv2.imshow("Smart Face Recognition System", frame)

    # =========================
    # KEY INPUT
    # =========================
    key = cv2.waitKey(1) & 0xFF

    # SEND ON S PRESS
    if key == ord('s'):

        now = time.time()

        if now - last_sent > cooldown:

            last_sent = now

            print("SEND TRIGGERED")

            # =========================
            # LOGS
            # =========================
            send_event(
                "log",
                f"{name} detected as {current_role} at {timestamp}"
            )

            # =========================
            # ALERT
            # =========================
            if current_role == "THREAT":
                send_event(
                    "alert",
                    f"🚨 THREAT: {name} detected at {timestamp}"
                )
                
                
            # =========================
            # UNKNOWN PERSON
            # =========================
            if current_role == "UNKNOWN":

                state = input("Do you want to inform the home owner? (Y/N): ")

                if state.upper() == 'Y':

                    send_event( "manual_verification", f"UNKNOWN person detected at {timestamp}")

            
            # =========================
            # ARDUINO
            # =========================
            if arduino is not None:
                try:
                    arduino.write((current_role + '\n').encode())
                except Exception as e:
                    print("Serial error:", e)

    # RESET
    if key == ord('r'):
        if arduino:
            arduino.write(("Reset\n").encode())
        print("RESET")

    # QUIT
    if key == ord('q'):
        break


# =========================
# CLEANUP
# =========================
cam.release()
cv2.destroyAllWindows()
