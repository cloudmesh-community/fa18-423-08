import os  
import sys
import cv2
import threading
from progressbar import ProgressBar, Percentage, Bar

#seperate videos into frames
#folder for each video stored under capture folder
#frames stored under each folder
def MainRange(start, stop):
    for i in range(start, stop):
        try:
            folder = 'capture/' + videoname_list[i]
            
            cap = cv2.VideoCapture(video_list[i])
            if cap.isOpened():
                if not os.path.exists(folder):
                    os.makedirs(folder)
            else:
                print("%s cannot be opened" % videoname_list[i])
                continue
                
            length =  int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) 
            width =  int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height =  int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps =  int(cap.get(cv2.CAP_PROP_FPS))        
            print (videoname_list[i], length, width, height, fps)
            
            pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=length+1).start()
            
            for count in range(length):
                cap.set(cv2.CAP_PROP_POS_FRAMES, count)
                capture, image = cap.read()
                if capture == True:
                    path = folder + '/frame{count:04}.jpg'.format(count=count)
                    cv2.imwrite(path, image)
                    pbar.update(count)
                else:
                    continue
            cap.release()                
        
        except:
            continue

#start running python script
#take a folder path as an argument
#take a number of cores as an argument
#video_list includes video paths
#videoname_list includes parsed video names
#root: current directory path, dirs: folders under current directory, files: videos under current directory


if __name__== "__main__":
    videos_path = sys.argv[1] 
    threads_num = int(sys.argv[2])
    
    video_list = []
    videoname_list = []
    for root, dirs, files in os.walk(videos_path):
        for file in files:
            video_list.append(os.path.join(root, file))
            videoname_list.append(os.path.splitext(file)[0])
    
    if threads_num > len(video_list):
        threads_num = len(video_list)

    cut = round(len(video_list)/threads_num)
    threads = []
    for j in range(threads_num-1):
        threads.append(threading.Thread(target=MainRange,args=(j*cut,(j+1)*cut)))        
    threads.append(threading.Thread(target=MainRange,args=((threads_num-1)*cut,len(video_list))))
     
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    print("Done!")


    
    

    
    
    


    
    
    
    
    
    