# SafeFall: Fall Detection Web App

SafeFall is an innovative web application designed to detect falls in real-time using computer vision. It leverages the power of YOLO (You Only Look Once) object detection models to analyze video streams from a smartphone camera and alert caregivers when a fall is detected. The application is user-friendly, allowing for easy setup and management of caregiver information.

## Features

- **Real-time Fall Detection**: Utilizes a YOLO model to detect falls in real-time from a live video stream.
- **2 Alert System**: Sends a Whatsapp message to caregiver's number and sends a signal to an Arduino to activate an LED and buzzer when a fall is detected.
- **Caregiver Management**: Allows for adding and removing caregiver contact information.
- **Fall History Log**: Maintains a log of all detected falls with date, time, confidence score, and a snapshot of the incident.

## Requirements

- Python 3.8 or higher
- Streamlit
- OpenCV
- Pandas
- Ultralytics
- pySerial
- IP Webcam App (for Android)
