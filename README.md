# Smart-Face-Recognition-System
Real-time Face Recognition System built for School Science Fair (2026), developed using Python and OpenCV. The project demonstrates a complete computer vision pipeline that includes face detection, dataset creation, model training, and real-time recognition using the LBPH (Local Binary Patterns Histograms) algorithm.
The system captures live video from a webcam, detects faces using Haar Cascade classifiers, and processes them frame-by-frame to identify individuals based on a trained dataset.

It suitable for multiple real-world applications such as attendance systems, basic access control, or identity verification systems. The project also includes Arduino integration via serial communication, enabling interaction with external hardware for automation or physical output control.

The system contains 3 main parts, collecting, training, and finally the main recognition part. In Collecting stage, 30 imgaes of a person is taken. in training, the program is trained and finally and recognition, the trained porgram tries to match the person in front of the camera with collected images and determine who it is.
