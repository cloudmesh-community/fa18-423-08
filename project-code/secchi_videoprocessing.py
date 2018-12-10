#! /usr/bin/env python

# from multiprocessing import Pool
import cv2
import sys
import os
from progressbar import ProgressBar, Percentage, Bar

def video_frame(video_name):
    cap = cv2.VideoCapture(video_name)
    length =  int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) 
    width =  int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height =  int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps =  int(cap.get(cv2.CAP_PROP_FPS))    

    filler = len(str(length))

    
    
    print (length, width, height, fps)

    pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=length+1).start()

    
    capture,image = cap.read()
    count = 0
    capture = True
    while capture:
        capture,image = cap.read()
        cv2.imwrite('images/frame{count:04}.jpg'.format(count=count), image)
        #print("Creating frame: ", count, capture)
        count += 1
        pbar.update(count)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()

# main
if __name__== "__main__":
    filename = sys.argv[1]
    os.system("mkdir images")
    video_frame(filename)
