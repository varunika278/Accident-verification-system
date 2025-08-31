import serial
import joblib
import numpy as np
import time
import sys
import smtplib
from email.mime.text import MIMEText
import os
import cv2

# Load ML Model
model = joblib.load(r"D:\Desktop\final_yr_project\python files\RandomForest.pkl")

# Open Serial Connection (Make sure COM port is correct)
ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

def extract_frames(video_path, output_folder):

    cap = cv2.VideoCapture(video_path)


    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


    frame_count = 0
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(frame_filename, frame)

    cap.release()

def get_sensor_data():
    """ Read sensor values from Arduino, ignore GPS data """
    while True:
        try:
            ser.flushInput()  # Clear buffer
            line = ser.readline().decode().strip()
            if line and not line.startswith("GPS"):  # Ignore GPS lines
                values = list(map(float, line.split(",")))
                if len(values) == 5:  # Expecting 5 values
                    return values
        except Exception as e:
            print("Error reading serial:", e)
            time.sleep(1)


# Get sensor data
temperature, humidity, mq3, mq7, mq135 = get_sensor_data()
# temperature = input("Temperature: ")
# humidity = input("humidity: ")
# mq3 = input("Alcohol(mq3): ")
# mq7 = input("CO(mq7): ")
# mq135 = input("Air quality(mq135): ") 

print("Detected values:")
print(f"CO (MQ7): {mq7}")
print(f"Air quality (MQ135): {mq135}")
print(f"Alcohol (MQ3): {mq3}")
print(f"Temp: {temperature} °C")
print(f"Humidity: {humidity} %")

user_data = np.array([[mq7, mq135, mq3, temperature, humidity]])

prediction = model.predict(user_data)
print(f"\nPredicted Drowsiness Cause: {prediction[0]}")

with open("status_report.txt", "a") as file:
    if prediction[0] == "none":
        print("\n=========> Sending Mail <=============")

        sender_email = 'varunika278@gmail.com'
        sender_password = 'bpwq iupt gzyu gdym'
        recipient_emails = 'varunika.2101249@srec.ac.in'

        subject = 'Drowsiness Alert'
        body = 'Drowsy - alert to driver'

        message = MIMEText(body)
        message['Subject'] = subject
        message['From'] = sender_email
        message['To'] = recipient_emails

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_emails, message.as_string())

        print("Drowsiness alert email sent to driver.")
        file.write(f"Cause of drowsiness: {prediction[0]}\n")
        sys.exit(1)

    elif prediction[0] in ["environment", "alcohol", "both"]:
        print("\nDrowsiness detected. Sending the alert to guardian...")

        sender_email = 'varunika278@gmail.com'
        sender_password = 'bpwq iupt gzyu gdym'
        recipient_emails = 'varunika.2101249@srec.ac.in'

        subject = 'Driver consumed alcohol'
        body = 'Drowsy - alert to guardian'

        message = MIMEText(body)
        message['Subject'] = subject
        message['From'] = sender_email
        message['To'] = recipient_emails

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_emails, message.as_string())

        print("\nAlert was sent")
        file.write(f"Cause of drowsiness: {prediction[0]}\n")
        video_path = r"D:\Desktop\final_yr_project\sample videos\accident.mp4"
    
        output_folder = r"D:\Desktop\final_yr_project\accident frames"

        extract_frames(video_path, output_folder)
        
