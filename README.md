# Smart-Face-Recognition-System
Real-time Face Recognition System built for School Science Fair (2026), developed using Python and OpenCV. The project demonstrates a complete computer vision pipeline that includes face detection, dataset creation, model training, and real-time recognition using the LBPH (Local Binary Patterns Histograms) algorithm.
The system captures live video from a webcam, detects faces using Haar Cascade classifiers, and processes them frame-by-frame to identify individuals based on a trained dataset.

It suitable for multiple real-world applications such as attendance systems, basic access control, or identity verification systems. The project also includes Arduino integration via serial communication, enabling interaction with external hardware for automation or physical output control.

The system contains 3 main parts, collecting, training, and finally the main recognition part. In Collecting stage, 30 imgaes of a person is taken. in training, the program is trained and finally and recognition, the trained porgram tries to match the person in front of the camera with collected images and determine who it is.

# Project Structure:

Create a folder structure like this:
```
Project Folder
├── collecting_faces.py
├── training.py
├── recognition.py
└── dataset
    ├── Authorized
    └── Threat
```

# Setup Instructions (Windows)

## 1. Install Python

Download and install Python from:

https://www.python.org/downloads/

IMPORTANT:
During installation, make sure to check:

* ✅ "Add Python to PATH"

After installation, open Command Prompt and test:

```bash
python --version
```

or

```bash
py --version
```

---

## 2. Download the Project

Download or clone the project folder from GitHub.

Example using Git:

```bash
git clone https://github.com/abrar2011/Smart-Face-Recognition-System
```

Or simply download the ZIP and extract it.

---

## 3. Open Project Folder

Open Command Prompt inside the project folder.

Example:

```bash
cd Desktop
cd Smart-Face-Recognition-System
```

---

## 4. Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

You should now see:

```bash
(venv)
```

in the terminal.

---

## 5. Install Required Libraries

Run:

```bash
pip install -r requirements.txt
```

## Notes

* Webcam is required
* If no faces are detected, verify camera permissions
* Re-train the model every time after adding new faces
