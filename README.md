# special-guacamole
Object Detection and Notification System
Overview
The Object Detection and Notification System is a surveillance application that uses a pre-trained TensorFlow object detection model to identify objects in real-time from a webcam feed. When a specific object (e.g., a person) is detected, the system sends a WhatsApp message via a FastAPI server every 10 seconds.

Features
Real-time object detection using TensorFlow's SSD MobileNet model.
Sends a WhatsApp message through FastAPI when objects are detected.
Message dispatches are limited to every 10 seconds for each detected object.
Uses OpenCV for video capture and display.

Requirements
Python 3.7 or higher
TensorFlow 2.x
OpenCV
Requests
FastAPI
Object Detection API (TensorFlow models and label maps)
