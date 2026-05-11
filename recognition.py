import serial # imports library for Serial communication
import cv2 # camera
import numpy as np # numbers and arrays 
import time # time library for delays

arduino = None
send_enabled = False

try:
    arduino = serial.Serial('COM11', 9600)
    time.sleep(2)
    print("Arduino connected")
except:
    print("Arduino NOT connected (PC mode only)")

recognizer = cv2.face.LBPHFaceRecognizer_create() # creates LBPH face recognizer
recognizer.read("trainer.yml") # loads the trained model

labels = np.load("labels.npy", allow_pickle=True).item() # loads lebels ie person names used in the trained model

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml" # loads Haard Cascade for detecting faces
)

cam = cv2.VideoCapture(0) # default camera


CONFIDENCE_THRESHOLD = 50 # confidence treshold, below that, faces will be considered UNKNOWN

while True:

    ret, frame = cam.read() # continous images from camera creates live video

    # mirror webcam
    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # converts to grayscale to make detection easier

    faces = face_cascade.detectMultiScale(gray, 1.3, 5) # Haar Cascade searches for face and returns x, y, w and h

    for (x, y, w, h) in faces: # loops through each and every face found

        face = gray[y:y+h, x:x+w] # extracts only the face area
        face = cv2.resize(face, (200, 200)) # resizes to the trained images size

        label_id, confidence = recognizer.predict(face)  # prediction part ising LBPH, returns confidence and lable_id, the name of the person it thinks it is

        # default UNKNOWN
        name = "Unknown"
        role = "Unknown"

        # yellow, default for unknown faces
        color = (0, 255, 255)

        # recognized properly
        if confidence < CONFIDENCE_THRESHOLD:

            person_data = labels[label_id] # defines person_data to label_id

            name = person_data["name"]
            role = person_data["role"]
            if arduino is not None:
                arduino.write(b'UNKNOWN\n')

            # Authorized = green
            if role.lower() == "authorized":

                color = (0, 255, 0)
                if arduino is not None:
                    arduino.write(b'AUTHORIZED\n')

            # Threat = red 
            elif role.lower() == "threat":

                color = (0, 0, 255)
                if arduino is not None:
                    arduino.write(b'THREAT\n')

        # rectangle
        cv2.rectangle(frame,
                      (x, y),
                      (x+w, y+h),
                      color,
                      2) # puts rectangle around the face, using the defined color

        # text
        text = f"{name} - {role}"

        cv2.putText(frame,
                    text,
                    (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    color,
                    2) # puts text over the face
                    
    key = cv2.waitKey(1) & 0xFF

    # press 's' to toggle sending ON/OFF
    if key == ord('s'):
        send_enabled = not send_enabled
        print("SEND MODE:", send_enabled)

    # press 'q' to quit
    if key == ord('q'):
        break                

    cv2.imshow("Smart Face Recognition System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'): # if Q pressed in Keyboard, the program is stopped
        break

cam.release()
cv2.destroyAllWindows()