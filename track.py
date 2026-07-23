import numpy as np
import cv2 

track_points = []
max_track_length = 100

BLUE_MİN = np.array([100, 150, 50])
BLUE_MAX = np.array([140, 255, 255])

cam = cv2.VideoCapture(0)

while True:
    ret , square = cam.read()
    if not ret:
        break

    
    square = cv2.resize(square,(640,480))
    hsv = cv2.cvtColor(square,cv2.COLOR_BGR2HSV)
    blue_mask = cv2.inRange(hsv,BLUE_MİN,BLUE_MAX)
    blue_mask = cv2.erode(blue_mask,None,iterations=2)
    blue_mask = cv2.dilate(blue_mask,None,iterations=2)

    contours , _ = cv2.findContours(blue_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    current_center = None

    for cnt in contours:
        if cv2.contourArea(cnt) > 1000:
            x,y,w,h = cv2.boundingRect(cnt)

            CenterX = x + (w // 2)
            CenterY = y + (h // 2)
 
            current_center = (CenterX,CenterY)

            cv2.rectangle(square,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.putText(square,"BLUE TARGET",(x,y+h+20),cv2.FONT_ITALIC,0.5,(255,255,255),2)
            cv2.line(square,(CenterX-10,CenterY),(CenterX+10,CenterY),(255,255,255),2)
            cv2.line(square,(CenterX,CenterY-10),(CenterX,CenterY+10),(255,255,255),2)
            cv2.putText(square,f"X:{CenterX} Y:{CenterY}",(x,y+h+40),cv2.FONT_ITALIC,0.5,(0,255,0),2)
    
    if current_center is not None:
        track_points.append(current_center)

    if len(track_points) > max_track_length:
        track_points.pop(0)


    for i in range(1,len(track_points)):
        cv2.line(square,track_points[i-1],track_points[i],(0,0,255),2)

    cv2.imshow("SYSTEM",square)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()