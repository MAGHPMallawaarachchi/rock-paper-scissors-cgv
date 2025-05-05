import cv2
import os

def capture_image(save_path="../images/input.jpg"):
    os.makedirs(os.path.dirname(save_path), exist_ok=True) 

#initialize the webcam
cam = cv2.VideoCapture(0) 
if not cam.isOpened():
    raise IOError("Cannot open webcam")

