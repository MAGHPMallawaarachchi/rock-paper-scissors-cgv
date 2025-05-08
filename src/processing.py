import cv2
import mediapipe as mp
import numpy as np
import os

def remove_background(image_path, save_path="../images/no_bg.jpg"):
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
    return gray