#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 14:00:34 2018

@author: yulizhao
"""

import cv2
import glob

x0,x1,y0,y1 = 1280, 640, 180, 400
delta_x = -1

def image_segments(image):
    img = cv2.imread(image)
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
            axis = x
            break
    mini_secchi = img[:,axis-400:axis-90,:]



# main
if __name__== "__main__":
    files = sorted(glob.glob("images/*.jpg"))
    print (files)
    for file in files:
        print (file)
        data = image_segments(file)
        print (file, data)
    
