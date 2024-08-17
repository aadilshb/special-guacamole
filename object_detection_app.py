import cv2 # type: ignore
import numpy as np # type: ignore
import tensorflow as tf # type: ignore
import requests # type: ignore
import os
import time
import threading
from object_detection.utils import label_map_util # type: ignore
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = 'mail_server'#replace with your mail server
SMTP_PORT = 587
SENDER_EMAIL = 'mail_id'#replace with your mail id
SENDER_PASSWORD = 'PASSWORD'  
RECIPIENT_EMAIL = 'mail_id'#replace with your mail id

last_email_time = 0
EMAIL_THROTTLE_TIME = 20  

def send_email_alert(subject, body):
    global last_email_time
    current_time = time.time()
    if current_time - last_email_time < EMAIL_THROTTLE_TIME:
        return  

    last_email_time = current_time
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    def send_email_thread():
        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            text = msg.as_string()
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, text)
            server.quit()
            print(f"Email alert sent to {RECIPIENT_EMAIL}")
        except Exception as e:
            print(f"Failed to send email alert: {e}")

    email_thread = threading.Thread(target=send_email_thread)
    email_thread.start()

FASTAPI_URL = "http://localhost:8000/send_whatsapp_message/"
FASTAPI_ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"  # Replace with your actual access token

last_message_time = datetime.min

def send_whatsapp_message(object_label, body_parameters):
    payload = {
        "body_parameters": body_parameters
    }
    try:
        response = requests.post(FASTAPI_URL, json=payload)
        response.raise_for_status()  
        print(f"WhatsApp message about '{object_label}' sent successfully")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send WhatsApp message: {e}")

model_path = r'C:\Users\aadil\OneDrive\Desktop\mini_proj_6\jetsonProject\Model\ssd_mobilenet_v2_fpnlite_320x320\ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8\saved_model'
model = tf.saved_model.load(model_path)

def load_labels(path='C:/Users/aadil/OneDrive/Desktop/mini_proj_6/jetsonProject/mscoco_label_map.pbtxt'):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Label map file '{path}' not found.")
    category_index = label_map_util.create_category_index_from_labelmap(path, use_display_name=True)
    return category_index

def detect_objects(image_np):
    input_tensor = tf.convert_to_tensor(image_np)
    input_tensor = input_tensor[tf.newaxis, ...]
    detections = model(input_tensor)

    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
    detections['num_detections'] = num_detections

    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
    return detections

def draw_bounding_boxes(image_np, detections, category_index):
    global last_message_time
    detected_labels = set()
    
    for i in range(detections['num_detections']):
        if detections['detection_scores'][i] > 0.5:
            class_id = detections['detection_classes'][i]
            box = detections['detection_boxes'][i]
            ymin, xmin, ymax, xmax = box
            (left, right, top, bottom) = (xmin * image_np.shape[1], xmax * image_np.shape[1], ymin * image_np.shape[0], ymax * image_np.shape[0])
            cv2.rectangle(image_np, (int(left), int(top)), (int(right), int(bottom)), (0, 255, 0), 2)
            label = category_index[class_id]['name']
            cv2.putText(image_np, label, (int(left), int(top)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            
            if label not in detected_labels:
                now = datetime.now()
                
                if now - last_message_time >= timedelta(seconds=20):
                    
                    send_whatsapp_message(
                        object_label=label,
                        body_parameters=[f"A {label} has been detected by the surveillance system."]
                    )
                    last_message_time = now
                detected_labels.add(label)
            if label:
                send_email_alert(f"{label} detected", f"A {label} has been detected by the surveillance system.")

                
    return image_np

category_index = load_labels()


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    image_np = np.array(frame)
    detections = detect_objects(image_np)
    image_np = draw_bounding_boxes(image_np, detections, category_index)

    cv2.imshow('Object Detection', image_np)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
