import cv2
import numpy as np
import time
from datetime import datetime
import requests
import os

# =========================
# FLASK SEND FUNCTION
# =========================
def send_event(event_type, data):

    print("SENDING →", event_type, data)

    try:
        requests.post(
            "http://127.0.0.1:5000/event",
            json={
                "type": event_type,
                "data": data
            },
        )
    except Exception as e:
        print("Flask send error:", e)



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
last_sent = 0
cooldown = 2  # seconds

# =========================
# SAVE FOLDER
# =========================
os.makedirs("snapshots", exist_ok=True)


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
    # FACE DETECTION
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
    # UI BAR
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

    if key == ord('s'):

        now = time.time()
        if now - last_sent < cooldown:
            continue

        last_sent = now
        print("SEND TRIGGERED")

        image_path = None

        # =========================
        # SAVE IMAGE ONLY FOR THREAT / UNKNOWN
        # =========================
        if current_role in ["THREAT", "UNKNOWN"]:
            image_path = f"snapshots/{int(time.time())}.jpg"
            cv2.imwrite(image_path, frame)
            print("IMAGE SAVED:", image_path)

        # =========================
        # LOG EVENT (ALWAYS)
        # =========================
        send_event(
            "log",
            {
                "message": f"{name} detected as {current_role} at {timestamp}"
            }
        )
        
        send_event(
            "log",
            {
                "log": f"{current_role}"
            }
        )

        # =========================
        # THREAT ALERT
        # =========================
        if current_role == "THREAT":
            send_event(
                "alert",
                {
                    "message": f"🚨 THREAT: {name} detected at {timestamp}",
                    "image": image_path
                }
            )

        # =========================
        # UNKNOWN PERSON
        # =========================
        elif current_role == "UNKNOWN":

            print("UNKNOWN detected")

            send_event(
                "manual_verification",
                {
                    "message": f"UNKNOWN person detected at {timestamp}",
                    "image": image_path
                }
            )

    # RESET
    if key == ord('r'):

        send_event(
            "reset",
        {
            "message": "System Reset"
        }
    )

        print("RESET")
        

    if key == ord('q'):
        cam.release()
        cv2.destroyAllWindows()


# =========================
# CLEANUP
# =========================
cam.release()
cv2.destroyAllWindows()
