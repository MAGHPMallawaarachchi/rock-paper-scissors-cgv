import cv2
import os

def capture_image(save_path="../images/input.jpg"):
    os.makedirs(os.path.dirname(save_path), exist_ok=True) 

#initialize the webcam
    cam = cv2.VideoCapture(0) 
    if not cam.isOpened():
        raise IOError("Cannot open webcam")

#read frame and save 
    ret, frame = cam.read()
    if ret:
        cv2.imwrite(save_path, frame)
        cam.release()
        return save_path
    else:
        cam.release()
        raise ValueError("Failed to capture image")