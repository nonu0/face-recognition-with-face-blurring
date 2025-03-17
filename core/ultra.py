import cv2
import pandas as pd
from ultralytics import YOLO

# print(YOLO)

video = r'C:\Users\Administrator\work\faceblur\core\walk.mp4'
cap = cv2.VideoCapture(video)
model = YOLO(model='yolo11n.pt')
# print(model)
while cap.isOpened():
    ret,frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame,(1000,700))
    detections = model(frame)
    # print(detections)
    for det in detections:
        boxes = det.boxes
        for box in boxes:
            cls = box.cls
            conf = box.conf
            cx,cy,w,h = box.xywh.numpy()[0]
            # print(type(x))
            x1 = int(cx - w / 2)
            y1 = int(cy - h / 2)
            x2 = int(cx + w / 2)
            y2 = int(cy + h / 2)
            # for cods in xywh:
                # x,y,w,h = cods[0],cods[1],cods[2],cods[3]
                # x,y,w,h = int(x),int(y),int(w),int(h)
                # # print(x)
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,0),2)
    
    cv2.imshow('Frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()