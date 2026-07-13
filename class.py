import numpy as np
import cv2

class CV:
    def __init__(self):

        self.bounds = {
            "blue": [np.array([100, 150, 50]), np.array([140, 255, 255])],
            "green": [np.array([40, 70, 70]), np.array([80, 255, 255])],
            "red": [np.array([0, 120, 70]), np.array([10, 255, 255])]
        }
    
        
    def target(self,color_name:str,square_color:tuple,square_thickness:int,line_color:tuple,line_thickness:
               int,text:str,text_thickness:int,text_color:tuple):

        color_name = color_name.lower()
        if color_name in self.bounds:
            color_min = self.bounds[color_name][0]
            color_max = self.bounds[color_name][1]

            cam = cv2.VideoCapture(0)
            while True:
                ret , square = cam.read()
                if not ret:
                    break
                
                square = cv2.resize(square, (640, 480))
                hsv = cv2.cvtColor(square,cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv,color_min,color_max)
                contours , _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                    if cv2.contourArea(cnt) > 1000:
                        x,y,w,h = cv2.boundingRect(cnt)

                        CenterX = x + (w // 2)
                        CenterY = y + (h // 2)

                        cv2.rectangle(square,(x,y),(x+w,y+h),square_color,square_thickness)
                        cv2.line(square,(CenterX-10,CenterY),(CenterX+10,CenterY),line_color,line_thickness)
                        cv2.line(square,(CenterX,CenterY-10),(CenterX,CenterY+10),line_color,line_thickness)
                        cv2.putText(square,text,(x,y+h+20),cv2.FONT_ITALIC,0.5,text_color,text_thickness)
                        cv2.putText(square,f"X:{CenterX} Y:{CenterY}",(x,y+h+40),cv2.FONT_ITALIC,0.5,text_color,text_thickness)
            
                cv2.imshow("SYSTEM",square)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            
            cam.release()
            cv2.destroyAllWindows()

        else:
            print(f"{color_name} not found!")

video = CV()
video.target("green",(0,255,0),2,(255,255,255),2,"GREEN TARGET",2,(0,255,0))
