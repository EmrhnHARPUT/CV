import cv2 
import numpy as np 

BLUE_MİN = np.array([100, 150, 50])
BLUE_MAX = np.array([140, 255, 255])

cam = cv2.VideoCapture(0)

while True:
    ret , square = cam.read()
    if not ret:
        break
    
    hsv_square = cv2.cvtColor(square,cv2.COLOR_BGR2HSV)
    blue_mask = cv2.inRange(hsv_square,BLUE_MİN,BLUE_MAX)

    blue_contours , _ = cv2.findContours(blue_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in blue_contours:
        if cv2.contourArea(cnt) > 800:
            x,y,w,h = cv2.boundingRect(cnt)

            centerX = x + (w // 2)
            centerY = y + (h // 2)

            cv2.rectangle(square,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.line(square,(centerX-10,centerY),(centerX+10,centerY),(255,255,255),2)
            cv2.line(square,(centerX,centerY-10),(centerX,centerY+10),(255,255,255),2)
            cv2.putText(square,"BLUE TARGET",(x,y+h+20),cv2.FONT_ITALIC,0.5,(255,0,0),2)
            cv2.putText(square,f"X:{centerX} Y:{centerY}",(x,y+h+40),cv2.FONT_ITALIC,0.5,(0,255,0),2)
        
    cv2.imshow("DetectionSystem",square)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()