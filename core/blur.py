import cv2
import threading
from ultralytics import YOLO



model = YOLO(r'C:\Users\Administrator\work\faceblur\core\yolov8n-face.pt')
# print(model)


def face_blur_effect(frame,x1,x2,y1,y2,blur_effect=True,blur_density='heavy'):
    if not blur_effect:
        return frame
    
    blur_settings = {
        'light':25,
        'heavy':75
    }
    ksize = blur_settings.get(blur_density)
    ksize = max(15,ksize // 5 * 2 + 1)
    # print(ksize)
    roi = frame[y1:y2,x1:x2]
    blur = cv2.GaussianBlur(roi,(ksize,ksize),30)
    frame[y1:y2,x1:x2] = blur
    return frame

def process_frames():
    cap = cv2.VideoCapture(0)
    blur_effect = True
    while cap.isOpened():
        ret,frame = cap.read()
        if not ret:
            print('Failed to retrieve frames.')
            break
        try:
            detections = model.predict(frame)
            
            # if detections is None:
            #     print('No detections!!')
            for det in detections:
                boxes = det.boxes
                confidence = boxes.conf
                cx,cy,w,h = boxes.xywh.tolist()[0]
                # cls = boxes.cls
                x1,y1 = int(cx - w / 2), int(cy - h / 2)
                x2,y2 = int(cx + w / 2), int(cy + h / 2 )
                
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,0),2)
                frame = face_blur_effect(frame,x1,x2,y1,y2,blur_effect)
                
                
        except:
            print('No detections!!')
            # print(x2)
        # print(detections)
        
        key = cv2.waitKey(1)  & 0xFF
        cv2.imshow('Frame',frame)
        if key == ord('q'):
            break
        elif key == ord('b'):
            blur_effect = not blur_effect
    cap.release()
    cv2.destroyAllWindows()
    
sources = [0,r'C:\Users\Administrator\work\faceblur\core\walk.mp4']
thread = [threading.Thread(target=process_frames) for _ in sources]
for t in thread:
    t.start()
for t in thread:
    t.join()
# print(thread)
        