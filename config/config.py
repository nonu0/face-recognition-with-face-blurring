import os
import json
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings loaded from environment variables."""

    # Application settings
    APP_NAME = os.getenv("APP_NAME", "YOLOv8 Face Blur API")
    VERSION = os.getenv("VERSION", "1.0.0")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true" 

    # Model paths
    YOLO_MODEL_PATH = os.getenv("YOLO_MODEL_PATH", "C:/Users/Administrator/work/faceblur/core/yolov8n-face.pt")
    TEST_SOURCE1 = os.getenv('TEST_SOURCE1',r'C:\Users\Administrator\work\yolo_v8_realtime_face_blur\tests\walk.mp4')
    # Video streaming settings
    DEFAULT_VIDEO_SOURCE = os.getenv("DEFAULT_VIDEO_SOURCE", "0")
    FRAME_WIDTH = int(os.getenv("FRAME_WIDTH", 1000))
    FRAME_HEIGHT = int(os.getenv("FRAME_HEIGHT", 700))
    MAX_QUEUE_SIZE = int(os.getenv("MAX_QUEUE_SIZE", 5))
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", 10))
    DEFAULT_NAME = os.getenv("DEFAULT_NAME", "Camera")

    COLORS = json.loads(os.getenv("COLORS", '{"1": [255,0,255], "2": [0,255,0], "3": [255,0,0]}'))

    # Face blur settings
    BLUR_INTENSITY = int(os.getenv("BLUR_INTENSITY", 10))
    BLUR_SETTINGS = json.loads(os.getenv('BLUR_SETTINGS', '{"light": 25, "strong": 95}'))
    BLUR = os.getenv("BLUR", "True").lower() == "true" 
    # Logging settings
    LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "app.log")

    # Threading settings
    MAX_BLUR_THREADS = int(os.getenv("MAX_BLUR_THREADS", 4))

config = Config()
