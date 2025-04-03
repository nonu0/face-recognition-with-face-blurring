import cv2
from ultralytics import YOLO
from fastapi import HTTPException

import urllib.parse

import sys
import os
import logging
# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.models.model_loader import load_model  # Now it should work
from config.config import config


class CustomVideoCapture:
    def __init__(self,src:str=config.DEFAULT_VIDEO_SOURCE,name:str=config.DEFAULT_NAME,blur:bool=config.BLUR):
        self.src = self._decode_src(src)
        logging.info(f"Opening video source: {self.src}")
        self.cap = cv2.VideoCapture(self.src)
        self.name = name
        self.model = load_model()
        self.running = True
        
        if not self.cap.isOpened():
            raise HTTPException(status_code=400, detail="Could not open video source")

    # def _decode_src(self, src):
    #     source = urllib.parse.unquote(src).strip()
    #     if source.isdigit():  
    #         return int(source)  # Convert "0" to integer for webcam
    #     elif os.path.isfile(source):  # Check if file exists
    #         return source
    #     else:
            # raise HTTPException(status_code=400, detail=f"Invalid video source: {source}")
    def _decode_src(self, src):
        source = os.path.normpath(urllib.parse.unquote(src)).strip()
        if source.isdigit():
            return int(source)  # Convert "0" to integer for webcam
        elif os.path.isfile(source):  # Check if file exists
            return source
        else:
            raise HTTPException(status_code=400, detail=f"Invalid video source: {source}")


    def video_stream(self):
        try:
            while self.running and self.cap.isOpened():
                ret,frame = self.cap.read()
                if not ret or frame is None:
                    break
                frame = cv2.resize(frame,(config.FRAME_WIDTH,config.FRAME_HEIGHT))
                detections = self.model.track(frame,persist=True)[0]
                if detections and detections.boxes:
                    from app.services.face_blur import roi_blur
                    roi_blur(detections,frame)
                    
                    for box in detections.boxes:
                        id = int(box.id.item()) if box.id is not None else -1
                        x1,y1,x2,y2 = map(int,box.xyxy[0].tolist())
                        color = config.COLORS.get('3')
                        cv2.putText(frame,f'ID:{id}',(x1,y1-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,color,1)
                        
                _,buffer = cv2.imencode('.jpg',frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' +
                       buffer.tobytes() + b'\r\n')
        finally:
            self.running = False
            self.cap.release()
            
