# imports OpenCV for camera usage, OS for creating folders and Time for the delays
import cv2
import os
import time

# paths
AUTHORIZED_PATH = r"C:\Users\abrar_l03\Desktop\Abrar\Science Fair 2026\Smart Face Recognition System\dataset\Authorized"

THREAT_PATH = r"C:\Users\abrar_l03\Desktop\Abrar\Science Fair 2026\Smart Face Recognition System\dataset\Threat"

# asks for name and role
name = input("Enter person's name: ")
role = input("Enter role (Authorized/Threat): ")

# choose role folder
if role.lower() == "authorized":

    base_path = AUTHORIZED_PATH

elif role.lower() == "threat":

    base_path = THREAT_PATH

else:

    print("Invalid role.")
    exit()

# role folders must already exist
if not os.path.exists(base_path):

    print("\nRole folder does not exist:")
    print(base_path)

    exit()

# person folder
person_path = os.path.join(base_path, name)

# create persona folder automatically
os.makedirs(person_path, exist_ok=True)

# imports Haar Cascade, widely used algorithm to find faces in images
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cam = cv2.VideoCapture(0) # uses default webcam 

count = 0 # sets image counter to 0
last_capture_time = 0 # sets last capture time to 0

while True:

    ret, frame = cam.read() # takes images from camera, since it is in a while loop, images are taken repeatedly creating a live video

    # mirror webcam
    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # sets images to grayscale

    faces = face_cascade.detectMultiScale(gray, 1.3, 5) # Haar Cascade returning coordinate of faces

    for (x, y, w, h) in faces: # loops through all faces if mutiple exists

        cv2.rectangle(frame,
                      (x, y),
                      (x+w, y+h),
                      (0, 255, 0),
                      2) # creates rectangle frame around each face

        # capture every 0.5 sec
        if time.time() - last_capture_time > 0.5:

            count += 1

            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (200, 200)) # crops so only the face is in the image

            cv2.imwrite(f"{person_path}/{count}.jpg", face) # saves image in proper path with proper name

            last_capture_time = time.time()

    cv2.putText(frame,
                f"Collected: {count}/30",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2) # shows the progress, ie how many images taken

    cv2.imshow("Collect Faces", frame) # creates a window  and shows the live camera feed

    if cv2.waitKey(1) & 0xFF == ord('q') or count >= 30: 
        break # if letter Q is pressed in keyboard or 30 images are taken, the loop is broken and the program stops running

cam.release()
cv2.destroyAllWindows()
