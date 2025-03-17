import cv2


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
print(face_cascade)
# image = cv2.imread(r"C:\Users\Administrator\OneDrive\Desktop\90789301.jpeg")
image = cv2.imread(r"C:\Users\Administrator\work\faceblur\core\download.jpg")
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5)
print(faces)

for (x,y,w,h) in faces:
    face_region = image[y:y+h,x:x+w]
    blurred_face = cv2.GaussianBlur(face_region,(99,99),30)
    image[y:y+h,x:x+w] = blurred_face
    cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
    # print(x)

cv2.imshow('frame',image)
cv2.waitKey(0)
cv2.destroyAllWindows()