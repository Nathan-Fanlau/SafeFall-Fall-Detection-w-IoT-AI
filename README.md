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
- pywhatkit
- IP Webcam App (for Android)

## Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/Nathan-Fanlau/SafeFall-Fall-Detection-w-IoT-AI.git
    cd SafeFall-Fall-Detection-w-IoT-AI
    ```

2. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## Setup

1. **IP Webcam Setup**
   - Install the [IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam) app from the Google Play Store on your Android device.
   - Open the app and start the server. Note the IPv4 URL (e.g., `http://xxx.xxx.xxx.xxx:8080/video`).

2. **Connect to Arduino**
   - Ensure your Arduino is connected to your computer.
   - Update the `ESP32 = serial.Serial('COM3', 9600)` line in the code with the correct port for your setup.

## Usage

1. **Run the Application**
    ```bash
    streamlit run app_phonecam.py
    ```

2. **Configure the Web App**
   - Open the web app in your browser.
   - Enter the mobile camera stream URL (from IP Webcam).
   - Click "Start Streaming" to begin fall detection.

3. **Manage Caregivers**
   - Navigate to the "Caregiver Management" section.
   - Add or remove caregivers as needed.

---

Made by SIC5 - Kelompok 32
