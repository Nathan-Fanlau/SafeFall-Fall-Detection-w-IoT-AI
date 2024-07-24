import cv2
import streamlit as st
from ultralytics import YOLO
from datetime import datetime, timedelta
import pandas as pd
import os
import serial

def app():
    st.header('SafeFall: Fall Detection Web App')
    st.subheader('Made by SIC5 - Kelompok 32')
    st.write('To use: Install "IP Webcam" from the playstore in your smartphone. Then, choose the bottom-most option "Start server"')
    st.write('An IPv4 URL will appear i.e. (https://xxx.xxx.xxx.xxx:8080). Optionally, you can open the URL in your browser.')
    st.write('Next, input URL to streamlit with the format (https://xxx.xxx.xxx.xxx:8080/video). Click "Start streaming". Done!')
    st.write('')

    custom_model_path = 'best.pt'
    model = YOLO(custom_model_path)
    object_names = list(model.names.values())

    min_confidence = st.slider('Minimum confidence score', 0.0, 1.0, value=0.75)

    st.write('Select the minimum confidence score the model must have for its predictions. The default minimum confidence score is set to 0.75. Lower confidence score (near 0) means the model can be more uncertain about its predictions. While, a higher confidence score (near 1) means the model is more certain about its prediction.')
    
    # URL Kamera HP
    mobile_stream_url = st.text_input("Mobile Camera Stream URL. (Format: https://xxx.xxx.xxx.xxx:8080/video)")

    # Button to start and stop streaming
    start_button = st.button('Start Streaming')
    stop_button = st.button('Stop Streaming')
    
    # TAMBAHAN: Inisialisasi koneksi ESP32
    ESP32 = serial.Serial('COM3', 9600)

    # Initialize fall history in session state if not already
    if 'fall_history' not in st.session_state:
        st.session_state.fall_history = []

    # Initialize last fall detection time in session state if not already
    if 'last_fall_time' not in st.session_state:
        st.session_state.last_fall_time = datetime.min
        
    if start_button and mobile_stream_url:
        # Access video mobile camera via URL
        cap = cv2.VideoCapture(mobile_stream_url)

        # Placeholder video frame
        frame_placeholder = st.empty()

        # Start video capture loop
        while cap.isOpened():
            ret, frame = cap.read()
            
            if not ret:
                st.write("Failed to capture image")
                break
            
            # Boolean untuk cek jatuh atau tidak
            isfall = False

            result = model(frame)
            for detection in result[0].boxes.data:
                x0, y0 = (int(detection[0]), int(detection[1]))
                x1, y1 = (int(detection[2]), int(detection[3]))
                score = round(float(detection[4]), 2)
                cls = int(detection[5])
                object_name = model.names[cls]
                label = f'{object_name} {score:.2f}'

                if score > min_confidence:
                    cv2.rectangle(frame, (x0, y0), (x1, y1), (255, 0, 0), 2)
                    cv2.putText(frame, label, (x0, y0 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    
                    # If a fall is detected, log the date, time, & confidence score (with a 10-second interval)
                    if object_name == 'Fall Detected':
                        # Update boolean untuk arduino menjadi true
                        isfall = True
                        
                        current_time = datetime.now()
                        
                        if current_time - st.session_state.last_fall_time > timedelta(seconds=10):
                            fall_date = current_time.strftime('%Y-%m-%d')
                            fall_time = current_time.strftime('%H-%M-%S')
                            
                            frame_filename = f'fall_frame_{fall_date}_{fall_time}_{score:.2f}.png'
                            frame_path = os.path.join('fall_frames', frame_filename)
                            os.makedirs('fall_frames', exist_ok=True)
                            cv2.imwrite(frame_path, frame)
                            
                            st.session_state.fall_history.append({
                                'No': len(st.session_state.fall_history) + 1,
                                'Date': fall_date,
                                'Time (WIB)': fall_time.replace(':', '-'),
                                'Confidence Score': f'{score:.2f}',
                                'Image': frame_path
                            })
                            
                            # Switch case arduino
                            if isfall:
                                ESP32.write('1'.encode())
                            else:
                                ESP32.write('0'.encode())
                            
                            st.session_state.last_fall_time = current_time
                                          
            # Display frame in Streamlit
            frame_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            if stop_button:
                break

        cap.release()

    # Display Fall history
    st.subheader('Fall History')
    if st.session_state.fall_history:
        df_fall_history = pd.DataFrame(st.session_state.fall_history)
        df_fall_history.set_index('No', inplace=True)
        
        # Display the table with images
        for index, row in df_fall_history.iterrows():
            st.write(f"**No:** {index}")
            st.write(f"**Date:** {row['Date']}")
            st.write(f"**Time (WIB):** {row['Time (WIB)']}")
            st.write(f"**Confidence Score:** {row['Confidence Score']}")
            st.image(row['Image'])
            st.write("---")

    else:
        st.write('No falls detected yet.')

    # Display Caregiver data
    
    st.subheader('Caregiver Information')
    caregiver_data = {
        'No': ['1', '2', '3'],
        'Name': ['Lebron James', 'Stephen Curry', 'Lionel Messi'],
        'Phone Number': ['+62 812-3456-7890', '+62 811-2345-6789', '+62 813-4567-8901']
    }
    df_caregivers = pd.DataFrame(caregiver_data)
    df_caregivers.set_index('No', inplace=True)
    st.table(df_caregivers)

if __name__ == "__main__":
    app()