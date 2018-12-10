#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 12:38:44 2018

@author: yulizhao
"""

import cv2
import matplotlib.pyplot as plt

img1 = cv2.imread('secchi_segment1.jpg') 
img2 = cv2.imread('secchi_segment.jpg') 
img3 = cv2.imread('secchi_segment2.jpg') 
img4 = cv2.imread('secchi_segment3.jpg') 

figures = []
fig = plt.figure(figsize=(18, 16))
for i in range(1,13):
    figures.append(fig.add_subplot(4,3,i))
count = 0
for img in [img1,img2,img3,img4]:
    figures[count].imshow(img)

    color = ('b','g','r')
    for i,col in enumerate(color):
        histr = cv2.calcHist([img],[i],None,[256],[0,256])
        figures[count+1].plot(histr,color = col)

    figures[count+2].hist(img.ravel(),256,[0,256])

    count += 3

print("Legend")
print("First column = image of Secchi disk")
print("Second column = histogram of colors in image")
print("Third column = histogram of all values")

plt.show() 



def threshold(img):
    ret,thresh = cv2.threshold(img,100,255,cv2.THRESH_BINARY)
    plt.subplot(1,2,1), plt.imshow(img, cmap='gray')
    plt.subplot(1,2,2), plt.imshow(thresh, cmap='gray')

threshold(img4)

