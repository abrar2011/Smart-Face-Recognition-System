import cv2
import numpy as np
import time
import requests
import os

# =========================
# SEND EVENT TO BOT
# =========================
def send_event(event_type, data):

    try:
        requests.post(
            "http://127.0.0.1:5000/event",
            json={
                "type": event_type,
                "data": data
            },
            timeout=2
        )
        print("EVENT SENT:", event_type)

    except Exception as e:
        print("Flask Error:", e)


# =========================
# FACE SYSTEM
# =========================
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

labels = np.load(
    "labels.npy",
    allow_pickle=True
).item()

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

cam = cv2.VideoCapture(0)

CONFIDENCE_THRESHOLD = 50

cooldown = 5
last_detection = 0

# =========================
# RESET FLAG
# =========================
system_reset = False

os.makedirs("snapshots", exist_ok=True)

print("System Running")
print("S = Send | R = Reset | Q = Quit")


# =========================
# LOOP
# =========================
while True:

    ret, frame = cam.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    detected_role = None
    detected_name = None

    # =========================
    # RESET HANDLER (LOCAL)
    # =========================
    if system_reset:
        detected_role = None
        detected_name = None
        last_detection = 0
        system_reset = False
        print("SYSTEM RESET DONE")

    # =========================
    # FACE DETECTION
    # =========================
    for (x, y, w, h) in faces:

        face = cv2.resize(gray[y:y+h, x:x+w], (200, 200))

        label, confidence = recognizer.predict(face)

        role = "UNKNOWN"
        name = "Unknown"

        if confidence < CONFIDENCE_THRESHOLD:
            person = labels[label]
            name = person["name"]
            role = person["role"].upper()

        detected_role = role
        detected_name = name

        # =========================
        # COLOR SETTINGS
        # =========================
        if role == "AUTHORIZED":
            color = (0, 255, 0)   # GREEN
        elif role == "THREAT":
            color = (0, 0, 255)   # RED
        else:
            color = (0, 255, 255) # YELLOW

        # =========================
        # DRAW BOX
        # =========================
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

        cv2.putText(
            frame,
            f"{name}",
            (x, y-25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

        cv2.putText(
            frame,
            f"{role}",
            (x, y-5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

    # =========================
    # TOP BAR
    # =========================
    cv2.rectangle(frame, (0, 0), (900, 40), (30, 30, 30), -1)

    cv2.putText(
        frame,
        "S = Send | R = Reset | Q = Quit",
        (10, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.imshow("Smart Security System", frame)

    key = cv2.waitKey(1) & 0xFF

    # =========================
    # SEND
    # =========================
    if key == ord('s'):

        if detected_role is None:
            print("No face detected")

        elif time.time() - last_detection < cooldown:
            print("Cooldown active")

        else:

            if detected_role == "AUTHORIZED":

                send_event(
                    "AUTHORIZED",
                    {"message": f"{detected_name} authorized"}
                )

            elif detected_role == "THREAT":

                path = f"snapshots/{int(time.time())}.jpg"
                cv2.imwrite(path, frame)

                send_event(
                    "THREAT",
                    {
                        "message": "Threat detected",
                        "image": path
                    }
                )

            else:

                path = f"snapshots/{int(time.time())}.jpg"
                cv2.imwrite(path, frame)

                send_event(
                    "UNKNOWN",
                    {
                        "message": "Unknown person",
                        "image": path
                    }
                )

            last_detection = time.time()

    # =========================
    # RESET (KEY R)
    # =========================
    if key == ord('r'):

        system_reset = True
        last_detection = 0

        send_event(
            "RESET",
            {"message": "System reset"}
        )

        print("RESET SENT")

    # =========================
    # QUIT
    # =========================
    if key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
