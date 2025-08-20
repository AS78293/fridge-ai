from ultralytics import YOLO
import cv2
import numpy as np

# Load YOLO model
model = YOLO("runs/detect/merged_v1_m2/weights/best.pt")

def detect_food_from_cv2(cv2_img):
    results = model(cv2_img)
    labels = []
    for r in results:
        for c in r.boxes.cls:
            labels.append(model.names[int(c)])
    return list(set(labels))
