import serial
import cv2
import numpy as np
import time
from datetime import datetime

# =========================
# SERIAL
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

labels = np.load(
    "labels.npy",
    allow_pickle=True
).item()


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


# =========================
# STATUS
# =========================
current_role = "UNKNOWN"
default = "Reset"

prev_time = 0
fps = 0


# =========================
# MAIN LOOP
# =========================
while True:

    ret, frame = cam.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    # =========================
    # FPS CALCULATION
    # =========================
    current_time = time.time()
    fps = 1 / (current_time - prev_time) if prev_time != 0 else 0
    prev_time = current_time

    # timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    current_role = "UNKNOWN"

    # =========================
    # FACE LOOP
    # =========================
    for (x, y, w, h) in faces:

        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (200, 200))

        label_id, confidence = recognizer.predict(face)

        name = "Unknown"
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
    # TOP STATUS BAR
    # =========================
    status_color = (0, 255, 255)

    if current_role == "AUTHORIZED":
        status_color = (0, 255, 0)

    elif current_role == "THREAT":
        status_color = (0, 0, 255)

    # dark bar
    cv2.rectangle(frame, (0, 0), (800, 40), (30, 30, 30), -1)

    cv2.putText(frame, f"Time: {timestamp}",
                (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1)

    cv2.putText(frame, f"FPS: {int(fps)}",
                (300, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1)

    cv2.putText(frame, f"STATUS: {current_role}",
                (450, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                status_color,
                2)

    # =========================
    # SHOW WINDOW
    # =========================
    cv2.imshow("Smart Face Recognition System", frame)

    # =========================
    # KEYBOARD CONTROLS
    # =========================
    key = cv2.waitKey(1) & 0xFF

    # send once
    if key == ord('s'):

        if arduino is not None:
            try:
                arduino.write((current_role + '\n').encode())
                print("SENT:", current_role)
            except Exception as e:
                print("Serial error:", e)

        else:
            print("Arduino not connected")
            
    # reset LCD 
    if key == ord('r'):
        arduino.write((default + '\n').encode())
        print ("Reset")

    # quit
    if key == ord('q'):
        break


# =========================
# CLEANUP
# =========================
cam.release()
cv2.destroyAllWindows()
