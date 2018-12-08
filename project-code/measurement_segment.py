# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 14:00:34 2018

@author: yulizhao
"""

import cv2
import matplotlib.pyplot as plt

x0,x1,y0,y1 = 960, 640, 180, 400
delta_x = -40

img = cv2.imread('frame802.jpg')

flag = False

for x in range(x0,x1, delta_x):
    mini_img = img[y0:y1,x:(x+160),:]
    count = 0
    for i in range(mini_img.shape[0]):
        for j in range(mini_img.shape[1]):
            b = mini_img[i,j,0]
            g = mini_img[i,j,1]
            r = mini_img[i,j,2]
            if b> 240 and g > 240 and r >240:
                count = count + 1
    if count/(160*220) > 0.2:
        flag = True
        break
        