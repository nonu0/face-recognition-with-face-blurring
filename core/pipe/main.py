import cv2
from ultralytics import YOLO

import time
import threading


class VideoCapture(threading.Thread):
    def __init__(self,src=0,name='Camera'):
        super().__init__()
        self.src = src
        self.cap = cv2.VideoCapture(self.src)
        self.running = True
        self.name = name
        
    def run(self):
        global captured_frames
        while self.running and self.cap.isOpened():
            ret,frame = self.cap.read()
            if not ret:
                print('Failed to capture frame.')
                break
            # print(type(frame))
            # print(type(ret))
            frame = cv2.resize(frame,(1000,700))
            with lock:
                captured_frames[self.name] = frame
            # print(captured_frames)
            # ddd = captured_frames.items()
            # for name,framess in ddd:
            #     print('items',name)
            
            # time.sleep(0.01)
            # for name,frame in captured_frames:
                # cv2.imshow(name,frame)
            
        # self.cap.release()
        
    def stop(self):
        self.running = False
        self.cap.release()
        cv2.destroyAllWindows()
        
            
            
captured_frames = {}
lock = threading.Lock()
model = YOLO(r'C:\Users\Administrator\work\faceblur\core\yolov8n-face.pt')
sources = [0,r'C:\Users\Administrator\work\faceblur\core\walk.mp4']
# sources = [0,r'C:\Users\Administrator\work\faceblur\core\walk.mp4',r'C:\Users\Administrator\work\faceblur\core\black_room.mp4']
streams = [VideoCapture(source,f'Camera_{i}')for i,source in enumerate(sources)]
for stream in streams:
    stream.start()
    
def face_blur(detections,frame):
        for det in detections:
            # boxes = det.boxes
            for box in det.boxes:
                # print(box)
                cx,cy,w,h = box.xywh.tolist()[0]
                # confidence = boxes
                # cls = boxes.cls
                x1,y1 = int(cx - w / 2), int(cy - h / 2)
                x2,y2 = int(cx + w / 2), int(cy + h / 2)
                frame = cv2.rectangle(frame,(x1,y1),(x2,y2),(98,54,232),2)
                roi = frame[y1:y2,x1:x2]
                blur = cv2.GaussianBlur(roi,(99,99),10)
                frame[y1:y2,x1:x2] = blur
                # print('dfg',roi)
                # frame = face_blur(frame,x1,x2,y1,y2)
    

def display():
    blur_effect = False
    while True:
        with lock:
            captured_frames_copy = captured_frames.copy()
        for name,frame in captured_frames_copy.items():
            # print(type(name))
            detections = model.predict(frame)
            if blur_effect:
                face_blur(detections,frame)
            cv2.imshow(name,frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    for stream in streams:
        stream.stop()
        
print(display())
# print()