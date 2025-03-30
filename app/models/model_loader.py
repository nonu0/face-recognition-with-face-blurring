from ultralytics import YOLO
from config.config import config

def load_model():
    try:
        model = YOLO(config.YOLO_MODEL_PATH)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")