import os
import sys

# Suppress TensorFlow Logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress INFO and WARNING logs
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Temporarily redirect stdout and stderr to suppress logs
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

import logging
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import smtplib
from email.mime.text import MIMEText
from datetime import datetime


# Restore stdout and stderr for normal print statements
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

# Disable TensorFlow Logging
logging.getLogger("tensorflow").setLevel(logging.ERROR)
print("\nDetecting Drowsiness\n")

def get_images_drowsy(dir):
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

image_directory_drowsy = r"D:\Desktop\final_yr_project\drowsiness frames"
# image_directory = sys.argv[1]
images = get_images_drowsy(image_directory_drowsy)

model_drowsy=load_model(r'D:\Desktop\final_yr_project\drowsiness detection\drowsiness_model.h5', compile=False)
predictions = model_drowsy.predict(images)
#model.summary()

# Select image to display
img_index = 0
# Get predicted class label
class_label = np.argmax(predictions[img_index])

labels_drowsy = ['drowsy', 'non_drowsy']
count_drowsy=0
count_non_drowsy=0

for i in range(len(images)):
    predicted_class = np.argmax(predictions[i])
    class_probability = predictions[i, predicted_class]
    # print(f'Predicted class for {i+1}.jpg : {labels_drowsy[predicted_class]}')
    if(labels_drowsy[predicted_class]=="drowsy"):
        count_drowsy+=1
    elif(labels_drowsy[predicted_class]=="non_drowsy"):
        count_non_drowsy+=1
    # print('Class probability:', class_probability)
    
print()
print("Drowsy = ",count_drowsy)
print("Non Drowsy = ",count_non_drowsy)
with open("status_report.txt", "a") as file:
    if count_non_drowsy > count_drowsy:
        drowsiness_status = "non_drowsy"
        print("\nThe driver is not drowsy.\n")
        file.write(f"Drowsiness: {drowsiness_status}\n")
        sys.exit(1)
    else:
        drowsiness_status = "drowsy"
        print("\nThe driver is drowsy\n")
        file.write(f"Drowsiness: {drowsiness_status}\n")
        # Get current date and time
        now = datetime.now()
        formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"Time_of_Drowsiness: {formatted_datetime}\n")

if count_drowsy>count_non_drowsy:
    print("")
    print("=========>Sending Mail<=============")
    sender_email = 'varunika278@gmail.com'
    sender_password = 'bpwq iupt gzyu gdym'
    recipient_email = 'pepperpotts0508@gmail.com'
    subject = 'Alert'
    body = 'Drowsy'
    print("Drowsy")
    
    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = recipient_email
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
    print("=============>Drowsy Alert Sent<=============")
