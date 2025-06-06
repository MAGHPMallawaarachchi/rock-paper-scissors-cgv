import cv2
import mediapipe as mp
import numpy as np
import os
import time

def remove_background(image_path, save_path="images/no_bg.jpg"):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)  # Ensure folder exists

    mp_selfie = mp.solutions.selfie_segmentation
    selfie = mp_selfie.SelfieSegmentation(model_selection=1)
    
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Error reading image from {image_path}")
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = selfie.process(img_rgb)
    
    mask = result.segmentation_mask > 0.1
    bg_removed = np.zeros(img.shape, dtype=np.uint8)
    bg_removed[mask] = img[mask]
    
    cv2.imwrite(save_path, bg_removed)
    
    if not os.path.exists(save_path) or os.path.getsize(save_path) == 0:
        raise ValueError(f"Failed to save background removed image to {save_path}")
    
    return save_path

def greyscale(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Greyscale", gray)
    _auto_close_windows(1)
    return gray

def threshold(gray_img):
    _, thresh = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
    cv2.imshow("Threshold", thresh)
    _auto_close_windows(1)
    return thresh

def binarize(gray_img):
    binarized = cv2.adaptiveThreshold(gray_img, 255,
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY, 11, 2)
    cv2.imshow("Binarized", binarized)
    _auto_close_windows(1)
    return binarized

def _auto_close_windows(seconds):
    """Wait for `seconds` then close all OpenCV windows."""
    start_time = time.time()
    while True:
        if time.time() - start_time > seconds:
            cv2.destroyAllWindows()
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break