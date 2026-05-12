import serial
import cv2
import numpy as np
import time

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
# LAST DETECTED PERSON
# =========================
current_role = "UNKNOWN"


# =========================
# MAIN LOOP
# =========================
while True:

    ret, frame = cam.read()

    if not ret:
        break

    # mirror webcam
    frame = cv2.flip(frame, 1)

    # grayscale
    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    # detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        1.3,
        5
    )

    # default if nobody detected
    current_role = "UNKNOWN"

    # =========================
    # LOOP THROUGH FACES
    # =========================
    for (x, y, w, h) in faces:

        # crop face
        face = gray[y:y+h, x:x+w]

        # resize
        face = cv2.resize(face, (200, 200))

        # predict
        label_id, confidence = recognizer.predict(face)

        # defaults
        name = "Unknown"
        role = "UNKNOWN"

        # yellow
        color = (0, 255, 255)

        # =========================
        # RECOGNIZED
        # =========================
        if confidence < CONFIDENCE_THRESHOLD:

            person_data = labels[label_id]

            name = person_data["name"]
            role = person_data["role"]

            # AUTHORIZED
            if role.lower() == "authorized":

                color = (0, 255, 0)
                role = "AUTHORIZED"

            # THREAT
            elif role.lower() == "threat":

                color = (0, 0, 255)
                role = "THREAT"

        # save current role
        current_role = role

        # =========================
        # DRAW RECTANGLE
        # =========================
        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            color,
            2
        )

        # =========================
        # DRAW TEXT
        # =========================
        text = f"{name} - {role}"

        cv2.putText(
            frame,
            text,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

    # =========================
    # SHOW WINDOW
    # =========================
    cv2.imshow(
        "Smart Face Recognition System",
        frame
    )

    # =========================
    # KEYBOARD CONTROLS
    # =========================
    key = cv2.waitKey(1) & 0xFF

    # PRESS S TO SEND ONCE
    if key == ord('s'):

        if arduino is not None:

            arduino.write(
                (current_role + '\n').encode()
            )

            print("SENT:", current_role)

        else:
            print("Arduino not connected")

    # PRESS Q TO QUIT
    if key == ord('q'):
        break


# =========================
# CLEANUP
# =========================
cam.release()
cv2.destroyAllWindows()
