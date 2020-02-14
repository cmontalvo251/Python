
 
import cv2
from scipy.spatial import Delaunay
import numpy as np 
import matplotlib.pyplot as plt


cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    cv2.imshow("test", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1
        cap=cv2.imread(img_name)        
        cv2.imshow('capture', cap)
        #originalImage = cv2.imread('starpractice2')
        grayImage = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
        (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
        # Taking a matrix of size 5 as the kernel 
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)) 
  
 
        img_erosion = cv2.erode(blackAndWhiteImage, kernel, iterations=5)
        ret,thresh = cv2.threshold(img_erosion,127,255,0)
        cx=[]
        cy=[]

        # find contours in the binary image
        ret,thresh = cv2.threshold(img_erosion,127,255,0)
        contours, hierarchy = cv2.findContours(thresh,1,2)
        for c in contours:
   
           # calculate moments for each contour
           M = cv2.moments(c)
 
           # calculate x,y coordinate of center
           if M["m00"] != 0:
             cX = int(M["m10"] / M["m00"])
             cY = int(M["m01"] / M["m00"])
             cx.append(cX)
             cy.append(cY)
     
    
         
           else:
             cX, cY = 0, 0
           cv2.circle(img_erosion, (cX, cY), 5, (255, 255, 255), -1)

        x=np.size(cx)
        points=np.zeros((x,2))
        for k in range(0,x):
          points[k,0]=cx[k]
          points[k,1]=-cy[k]
  


        tri = Delaunay(points)
#print(points)


 


        plt.triplot(points[:,0], points[:,1], tri.simplices.copy())
        plt.plot(points[:,0], points[:,1], 'o')

 
#cv2.imshow('Input', originalImage)
        cv2.imshow('Erosion', img_erosion)
        plt.show()

#cv2.imwrite('/home/mrgpl/Documents/Capstone/erosion.jpg'/img_erosion)
#cv2.waitKey(0)


cam.release()
cv2.destroyAllWindows()
cv2.waitKey(0)