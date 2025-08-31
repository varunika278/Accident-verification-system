import os
import sys

# Suppress TensorFlow Logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress INFO and WARNING logs
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Redirect stdout and stderr to suppress unwanted logs
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

import logging
import tensorflow as tf
from tensorflow.keras.models import load_model
from email.mime.text import MIMEText
from PIL import Image
import requests
import smtplib
import numpy as np
# Restore stdout and stderr for normal print statements
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

# Disable TensorFlow Logging
logging.getLogger("tensorflow").setLevel(logging.ERROR)

import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

def get_device_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        loc = data.get("loc", "Unknown")  
        return loc
    except Exception as e:
        print(f"Error getting location: {e}")
        return "Unknown"

def get_images_accident(dir):
    img_size = 224
    images = []
    for filename in os.listdir(dir):
        path = os.path.join(dir, filename)
        img = Image.open(path)
        img = img.resize((img_size, img_size))
        images.append(img)

    images = np.array([np.array(img) for img in images])
    images = images / 255.0
    return images

image_directory_accident = r"D:\Desktop\final_yr_project\accident frames"
images = get_images_accident(image_directory_accident)

model_accident = load_model(r'D:\Desktop\final_yr_project\accident detection\accident_model.h5', compile=False)
predictions = model_accident.predict(images)

labels_accident = ['accident', 'non_accident']
count_accident = 0
count_non_accident = 0

accident_detected = False  # Flag to check if an accident occurred
with open("status_report.txt", "a") as file:
    for i in range(len(images)):
        predicted_class = np.argmax(predictions[i])
        class_probability = predictions[i, predicted_class]

        if labels_accident[predicted_class] == "accident":
            print("\n=========> Sending Mail <=============")

            sender_email = 'varunika278@gmail.com'
            sender_password = 'bpwq iupt gzyu gdym'  
            recipient_emails = ['varunika.2101249@srec.ac.in', 'pepperpotts0508@gmail.com']
            subject = 'Accident Alert! for both guardian and police'
            
            device_location = get_device_location()

            body = f"**Accident Detected!**\n\n" \
                f"Location: {device_location}\n\n" \
                f"Take immediate action!"

            print("Accident detected. Sending location")

            message = MIMEText(body)
            message['Subject'] = subject
            message['From'] = sender_email
            message['To'] = ", ".join(recipient_emails)

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_emails, message.as_string())

            print("Accident Alert Sent with Location")
            cause = 'accident'
            file.write(f"Accident: {cause}\n")
            file.write(f"Accident_or_not: {"yes"}\n")                 
            accident_detected = True
            break  # Exit loop after sending the email

    if not accident_detected:
        print("No accident detected. Exiting...")
        cause = 'not_accident'
        file.write(f"Accident: {cause}\n")  
        sys.exit(1)  # Exit if no accident is detected

    #     count_accident += 1
    # else:
    #     count_non_accident += 1

# print("\nAccident =", count_accident)
# print("Non-Accident =", count_non_accident)

# # If accident detected, send alert with location
# if count_accident > count_non_accident:
#     print("\n=========> Sending Mail <=============")
    
#     sender_email = 'varunika278.gmail.com'
#     sender_password = 'bpwq iupt gzyu gdym'  
#     recipient_emails = ['ur_team_mates_email_gaurdian','ur_team_mates_email_police']
#     subject = 'Accident Alert! for both gaurdian and police'
    
#     # Get device location
#     device_location = get_device_location()
#     location_link = f"https://www.google.com/maps?q={device_location}"

#     # Email body with location
#     body = f" **Accident Detected!** \n\n" \
#            f"Location: {device_location}\n\n" \
#            f"View on Google Maps: {location_link}\n\n" \
#            f"Take immediate action!"

#     print("Accident detected. Sending location:", location_link)

#     # Construct email message
#     message = MIMEText(body)
#     message['Subject'] = subject
#     message['From'] = sender_email
#     message['To'] = recipient_email

#     # Send email
#     with smtplib.SMTP('smtp.gmail.com', 587) as server:
#         server.starttls()
#         server.login(sender_email, sender_password)
#         server.sendmail(sender_email, recipient_email, message.as_string())

#     print("------------> Email Sent <------------")
#     print("=============> Accident Alert Sent with Location <=============")
#     print("whole process done")
