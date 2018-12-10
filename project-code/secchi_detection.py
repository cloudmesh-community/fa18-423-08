# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 14:53:47 2018

@author: yulizhao
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
#https://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/
image = cv2.imread("frame264.jpg")
output = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

circle = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.95, 1000)
if circle is not None:
    circle = np.round(circle[0,:]).astype("int")
    for (x,y,r) in circle:
        cv2.circle(output, (x,y),r,(0,255,0),4)
        cv2.rectangle(output,(x-5,y-5),(x+5,y+5),(0,128,255),-1)
    cv2.imshow('output',np.hstack([image,output]))
    cv2.waitKey(0)



#https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html
img = cv2.imread("frame264.jpg",0)

ret,thresh = cv2.threshold(img,150,255,cv2.THRESH_BINARY)
plt.subplot(1,2,1),plt.imshow(img,cmap='gray')
plt.subplot(1,2,2),plt.imshow(thresh,cmap='gray')

edges = cv2.Canny(thresh,100,200)
plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'),plt.xticks([]),plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'),plt.xticks([]),plt.yticks([])
plt.show()

#https://www.learnopencv.com/image-recognition-and-object-detection-part1/

#rubic test code
img = cv2.imread("two-cubes.png")
RGB = [40,158,16]
thresh = 40 
minRGB = np.array([RGB[0]-thresh,RGB[1]-thresh,RGB[2]-thresh])
maxRGB = np.array([RGB[0]+thresh,RGB[1]+thresh,RGB[2]+thresh])

maskRGB = cv2.inRange(img, minRGB, maxRGB)
resultRGB = cv2.bitwise_and(img,img,mask = maskRGB)
plt.imshow(resultRGB)

#code RGB
img = cv2.imread("frame5.jpg")
RGB = [125,162,82]
thresh = 50
minRGB = np.array([RGB[0]-thresh,RGB[1]-thresh,RGB[2]-thresh])
maxRGB = np.array([RGB[0]+thresh,RGB[1]+thresh,RGB[2]+thresh])

maskRGB = cv2.inRange(img, minRGB, maxRGB)
resultRGB = cv2.bitwise_and(img,img,mask = maskRGB)
plt.imshow(resultRGB)

#code HSV
img = cv2.imread("frame5.jpg")
RGB = [150,170,200]
thresh = 80
hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
hsv = cv2.cvtColor(np.uint8([[RGB]]),cv2.COLOR_BGR2HSV)[0][0]
minHSV = np.array([hsv[0]-thresh,hsv[1]-thresh,hsv[2]-thresh])
maxHSV = np.array([hsv[0]+thresh,hsv[1]+thresh,hsv[2]+thresh])
maskHSV = cv2.inRange(hsv_img,minHSV,maxHSV)
resultHSV = cv2.bitwise_and(hsv_img,hsv_img,mask = maskHSV)
plt.imshow(resultHSV)
image = Image.fromarray(resultHSV)
image.save('hsv_img.png')


#code LAB
img = cv2.imread("frame5.jpg")
RGB = [180,225,217]
thresh = 200
lab_img = cv2.cvtColor(img,cv2.COLOR_BGR2LAB)
lab = cv2.cvtColor(np.uint8([[RGB]]),cv2.COLOR_BGR2LAB)[0][0]
minLAB = np.array([lab[0]-thresh,lab[1]-thresh,lab[2]-thresh])
maxLAB = np.array([lab[0]+thresh,lab[1]+thresh,lab[2]+thresh])
maskLAB = cv2.inRange(hsv_img,minHSV,maxHSV)
resultLAB = cv2.bitwise_and(lab_img,lab_img,mask = maskLAB)
plt.imshow(resultLAB)