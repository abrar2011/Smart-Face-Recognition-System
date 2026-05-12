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

# 2. Download the Project

Download or clone the project folder from GitHub.

Example using Git:

```bash
git clone https://github.com/abrar2011/Smart-Face-Recognition-System
```

Or simply download the ZIP and extract it.

---

# 3. Open Project Folder

Open Command Prompt inside the project folder.

Example:

```bash
cd Desktop
cd Smart-Face-Recognition-System
```

---

# 4. Create Virtual Environment (Recommended)

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

# 5. Install Required Libraries

Run:

```bash
pip install opencv-contrib-python numpy pyserial
```

(Optional UI support)

```bash
pip install pillow
```

---

# 7. Collect Face Data

Run:

```bash
python collecting_faces.py
```

Follow the instructions to collect face images.

---

# 8. Train the Model

Run:

```bash
python training.py
```

This creates:

* trainer.yml
* labels.npy

---

# 9. Start Recognition System

Run:

```bash
python recognition.py
```

Controls:

* Press `S` → Send current detection to Arduino
* Press `Q` → Quit program

---

# 10. Arduino Connection (Optional)

Make sure Arduino is connected to the correct COM port.

Example:

```python
arduino = serial.Serial('COM11', 9600)
```

Change COM port if needed.

---

# Notes

* Webcam is required
* Good lighting improves recognition accuracy
* If no faces are detected, verify camera permissions
* Re-train the model after adding new faces
