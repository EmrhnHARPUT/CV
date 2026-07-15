import cv2
import numpy as np

class CV:

    def __init__(self):
        self.bounds = {
            "blue": [np.array([100, 150, 50]), np.array([140, 255, 255])],
            "green": [np.array([40, 70, 70]), np.array([80, 255, 255])],
            "red": [np.array([0, 120, 70]), np.array([10, 255, 255])]
        }

    def target(self,color_name:str,cnt_area:int,square_color:tuple,square_thickenss:int,
               line_color:tuple,line_thickenss:int,text:str,text_color:tuple,text_thickenss:int,
               project_name:str):
        
        points = []
        max_point = 50
        current_center = None

        if color_name in self.bounds:

            color_min = self.bounds[color_name][0]
            color_max = self.bounds[color_name][1]
            cam = cv2.VideoCapture(0)

            while True:
                ret , square = cam.read()
                if not ret:
                    break

                hsv = cv2.cvtColor(square,cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv,color_min,color_max)
                mask = cv2.dilate(mask,None,iterations=2)
                mask = cv2.erode(mask,None,iterations=2)

                contours , _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                    if cv2.contourArea(cnt) > cnt_area:
                        x,y,w,h = cv2.boundingRect(cnt)

                        CenterX = x + (w // 2)
                        CenterY = y + (h // 2)
                        current_center = (CenterX,CenterY)

                        cv2.rectangle(square,(x,y),(x+w,y+h),square_color,square_thickenss)
                        cv2.line(square,(CenterX-10,CenterY),(CenterX+10,CenterY),line_color,line_thickenss)
                        cv2.line(square,(CenterX,CenterY-10),(CenterX,CenterY+10),line_color,line_thickenss)
                        cv2.putText(square,text,(x,y+h+20),cv2.FONT_ITALIC,0.5,(255,0,0),text_thickenss)
                        cv2.putText(square,f"X:{CenterX} Y:{CenterY}",(x,y+h+40),cv2.FONT_ITALIC,0.5,text_color,text_thickenss)

                    if len(points) > max_point:
                        points.pop(0)
                
                    if current_center is not None:
                        points.append(current_center)

                cv2.imshow(project_name,square)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            cam.release()
            cv2.destroyAllWindows()

görüntü = CV()
görüntü.target("blue",1000,(255,0,0),2,(255,255,255),2,"BLUE TARGET",(0,255,0),2,"TARGET SYSTEM")
