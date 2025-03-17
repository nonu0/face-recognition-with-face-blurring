import cv2
from ultralytics import YOLO


model = YOLO(r'C:\Users\Administrator\work\faceblur\core\yolov8n-face.pt')
video = r'C:\Users\Administrator\work\faceblur\core\walk.mp4'
cap = cv2.VideoCapture(0)

def face_blur(frame,x1,y1,x2,y2):
    roi = frame[y1:y2,x1:x2]
    blur = cv2.GaussianBlur(roi,(99,99),30)
    frame[y1:y2,x1:x2] = blur
    return frame

while cap.isOpened():
    ret,frame = cap.read()
    if not ret:
        break
    
    frame = cv2.resize(frame,(1000,700))
    detections = model(frame)
    for result in detections:
        for det in result.boxes:
            cls = det.cls
            confidence = det.conf
            # print(xywh)
            # print(confidence)
            cx,cy,w,h = det.xywh.numpy()[0]
            x1 = int(cx - w / 2)
            y1 = int(cy - h / 2)
            x2 = int(cx + w / 2)
            y2 = int(cy + h / 2)
            # print(cx)
            frame = cv2.rectangle(frame, (x1, y1), (x2,y2),(255,255,0),2)
            frame = face_blur(frame,x1,y1,x2,y2)
    
    cv2.imshow('Frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()

# print(model)