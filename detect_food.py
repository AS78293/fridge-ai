from ultralytics import YOLO
import cv2
import numpy as np
import os

# Path to your trained model (update this!)
MODEL_PATH = "runs/detect/fast_train/weights/best.pt"

# Check if weights exist
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model weights not found at {MODEL_PATH}. Train first or update path.")

# Load YOLO model
model = YOLO(MODEL_PATH)

def detect_food_from_cv2(cv2_img):
    """
    Detect food items from an OpenCV image using YOLOv8.
    
    Args:
        cv2_img (numpy.ndarray): Input image in OpenCV format (BGR).
    
    Returns:
        list[str]: Unique detected food item names.
    """
    results = model(cv2_img)  # Run inference
    labels = []

    for r in results:
        for c in r.boxes.cls:   # class IDs of detections
            labels.append(model.names[int(c)])  # map ID -> label name
    
    return list(set(labels))  # remove duplicates
