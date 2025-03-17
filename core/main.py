import cv2
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
            print(type(frame))
            print(type(ret))
            captured_frames[self.name] = frame
            print(captured_frames)
            
            time.sleep(0.01)
            
        # self.cap.release()
        
    def stop(self):
        self.running = False
        self.cap.release()
        cv2.destroyAllWindows()
            
            
captured_frames = {}
sources = [0,r'C:\Users\Administrator\work\faceblur\core\walk.mp4']
streams = [VideoCapture(source,i) for i,source in enumerate(sources)]