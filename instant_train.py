# instant_train.py - JUST TRAIN FAST, NO COMPLICATIONS
from ultralytics import YOLO

# Smallest model, smallest images, no validation, no plots
model = YOLO("yolov8n.pt")

print("TRAINING WITH MAXIMUM SPEED SETTINGS...")
print("YOLOv8n (2.6M params vs your 25M)")
print("320px images (vs your 640px = 4x faster)")
print("No validation during training")
print("Expected: 5-10 minutes total vs your hours")

model.train(
    data="dataset/data.yaml",
    imgsz=320,              # Small images = fast
    epochs=20,              # Fewer epochs
    batch=-1,               # Auto batch size
    workers=0,              # No multiprocessing issues
    cache=False,            # No caching complications
    val=False,              # NO validation during training
    plots=False,            # NO plots
    verbose=False,          # Less output
    save_period=-1,         # No intermediate saves
    patience=5,             # Quick early stopping
    name="fast_train",
    exist_ok=True,
)

print("TRAINING DONE! Running quick validation...")
model.val(data="dataset/data.yaml", imgsz=320)