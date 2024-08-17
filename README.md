# special-guacamole
Object Detection and Notification System
---------------------------------------------------------------------------------------------------------
Overview:
The Object Detection and Notification System is a surveillance application that uses a pre-trained TensorFlow object detection model to identify objects in real-time from a webcam feed. When a specific object (e.g., a person) is detected, the system sends a WhatsApp message via a FastAPI server every 10 seconds.

Features:
Real-time object detection using TensorFlow's SSD MobileNet model.
Sends a WhatsApp message through FastAPI when objects are detected.
Message dispatches are limited to every 10 seconds for each detected object.
Uses OpenCV for video capture and display.

Requirements:
Python 
TensorFlow 2.x
OpenCV
Requests
FastAPI
Object Detection API (TensorFlow models and label maps)
------------------------------------------------------------------------------------------------------------------
Project Environment Requirements
--------------------------------------
Operating System:
Windows 10/11, Linux, or macOS
Python Version
Python 3.x (e.g., Python 3.8)
Python Packages
opencv-python
numpy
tensorflow
requests
object-detection (if using a specific package for object detection utilities)

Installation Instructions:
Navigate to the Project Directory:
Change into the project directory where the code is located.

Set Up a Virtual Environment (Optional but Recommended):
Create and activate a virtual environment to manage dependencies.

Install Required Packages:
Use pip to install the required Python packages.

Model and Label Map Files
Model Path: Download the pre-trained model and place it in the specified directory.
Label Map Path: Download the label map file and place it in the specified directory.

Running the Project:
Start the FastAPI Server:
Run the FastAPI server to handle WhatsApp messaging requests.

Run the Object Detection Script:
Execute the object detection script to start detecting objects and sending messages.

Configuration:
Access Token: Replace the placeholder access token in the script with your actual access token.
Webcam: Ensure the webcam is properly connected and accessible for object detection.
Additional Notes:
Keep any API keys or tokens confidential and secure.

-----------------------------------------------------------------------------------------------------------------------------------------
In the provided codes, the object_detection_app.py file contains the main code and email logic.
The mini_proj.py file contains the logic for FastApi Whatsapp message sending.
