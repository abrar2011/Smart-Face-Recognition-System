import cv2 # library used for camera features
import os # folder and file navigations
import numpy as np # numerical data and arrays

DATASET_PATH = r"C:\Users\abrar_l03\Desktop\Abrar\Science Fair 2026\Smart Face Recognition System\dataset" # defines the dataset path that contains all the faces

recognizer = cv2.face.LBPHFaceRecognizer_create() # creates LBPH recognizer

faces = []
labels = []

label_map = {}

current_label = 0

# Authorized / Threat
for role in os.listdir(DATASET_PATH):

    role_path = os.path.join(DATASET_PATH, role)

    if not os.path.isdir(role_path):
        continue

    # person folders
    for person_name in os.listdir(role_path):

        person_path = os.path.join(role_path, person_name)

        if not os.path.isdir(person_path):
            continue

        label_map[current_label] = {
            "name": person_name,
            "role": role
        }

        for img_name in os.listdir(person_path):

            img_path = os.path.join(person_path, img_name)

            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            if img is None:
                continue

            faces.append(img)
            labels.append(current_label)

        current_label += 1

faces = np.array(faces)
labels = np.array(labels)

recognizer.train(faces, labels)

recognizer.save("trainer.yml")

np.save("labels.npy", label_map)

print("\nTraining complete!")