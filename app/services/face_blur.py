import cv2
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


import concurrent.futures

from config.config import config

blur_executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)


def face_roi(frame,x1,y1,x2,y2,blur_level='strong'):
    blur_ksize = config.BLUR_SETTINGS.get(blur_level,25)
    blur_ksize = max(5,blur_ksize // 5*2+1)
    roi = frame[y1:y2, x1:x2]
    if roi.size == 0:
        return None
    blur = cv2.GaussianBlur(roi,(blur_ksize,blur_ksize),30)
    return (x1,y1,x2,y2,blur)

def roi_blur(detections,frame):
    future_blurs = [blur_executor.submit(face_roi,frame, *map(int,box.xyxy.tolist()[0])) for box in detections.boxes]
    for future in concurrent.futures.as_completed(future_blurs):
        result = future.result()
        if result:
            x1,y1,x2,y2,blur = result
            frame[y1:y2,x1:x2] = blur
            
