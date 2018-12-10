#! /usr/bin/env python

import cv2
import sys
import os

def video_frame(video_name):
    cap = cv2.VideoCapture(video_name)
    capture,image = cap.read()
    count = 0
    capture = True
    while capture:
        capture,image = cap.read()
        cv2.imwrite('images/frame%d.jpg' % count, image)
        print("Creating frame: ", count, capture)
        count += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()

# main
if __name__== "__main__":
    filename = sys.argv[1]
    os.system("mkdir images")
    video_frame(filename)
