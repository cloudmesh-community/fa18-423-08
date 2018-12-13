# Running the code

## Installation

First install the code with

```bash
git clone https://github.com/cloudmesh-community/fa18-423-08.git
cd fa18-423-08/project-code
```
### Install Anaconda

### Install CV2

On OSX

```bash
brew brew tap homebrew/science
```
### Install Progressbar
```bash
pip install progressbar
```

### Install tensorflow
```bash
pip install tensorflow
```

or

```conda
conda install -c conda-forge tensorflow
```

### Install Keras
```bash
pip install keras
```

or

```conda
conda install -c conda-forge keras
```

### Install pytesseract

```bash
pip install pytesseract
```
and

```bash
brew install tesseract
```


## Fetching the data

The Secchi Disk Data is located at 

https://drive.google.com/drive/folders/1W0EwjAcmZKgC-qEUosWNuUNwP4lOZ8fr

We have chose from that data the following video

https://drive.google.com/drive/folders/1KwldcJzSA-96bthUlFQD2yk8iOorBLDo

Please download it with the usual download button or use gdrive

Thei file is called. [DSCN0003.avi](https://drive.google.com/drive/folders/1KwldcJzSA-96bthUlFQD2yk8iOorBLDo) 

## Execution of the code


To run the program please do the following

Make sure secchi_full_process1212.py, secchi_classfication.h5, and the video file under the same directory.

Run the program at the command line with

```bash
python secchi_full_process1212.py DSCN0003.avi
```

where the file takes one argument for the video name



```python
import sys
import cv2
import pytesseract
import numpy as np
from keras.models import load_model

def frame_catch(video_path, model):

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("%s cannot be opened" % video_path)

    length =  int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    flag = False
    for count in range(length):
        print("Frame %i processing..." % count)
        cap.set(cv2.CAP_PROP_POS_FRAMES, count)
        capture, image = cap.read()
        if capture == True:
            image_mini = image[:,290:690,:] # 720*400
            image_mini = cv2.cvtColor(image_mini, cv2.COLOR_BGR2GRAY)
            image_mini = cv2.resize(image_mini,(90,50),interpolation=cv2.INTER_CUBIC)
            data = image_mini.reshape(1,90,50,1)
            softmax_output = model.predict(data)
            y_predict = (-softmax_output).argsort(axis=1)[:,0][0]
            if y_predict == 0:
                flag = True
                cv2.imwrite('image_catch.jpg', image)
                break
        else:
            continue

    if flag == True:
        for i in range(1, 10):
            cap.set(cv2.CAP_PROP_POS_FRAMES, count-i)
            capture, image = cap.read()
            if capture == True:
                cv2.imwrite('frame{count:04}.jpg'.format(count=count-i),image)
        return image, 'Succeed'
    else:
        return image, 'Failed'
    cap.release()


def depth_reco(image):

    print("Measurement processing...")
    x0, x1, y0, y1 = 1280, 640, 180, 400
    delta_x = -5

    flag = False
    for x in range(x0, x1, delta_x):
        mini_img = image[y0:y1, x:(x+160), :]
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

    if flag == True:
        cv2.imwrite('mea_pic.jpg', mini_img)
        # only keep yellow
        hsv = cv2.cvtColor(cv2.imread('mea_pic.jpg'), cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array([26,43,150]), np.array([38,255,255]))
        measurement = pytesseract.image_to_string(mask, config='--psm 7 -c tessedit_char_whitelist=0123456789')
        cv2.imwrite('mea_pic_after.jpg', mask)
        return measurement, 'Succeed'
    else:
        return "", 'Failed'

if __name__== "__main__":

    video_path = sys.argv[1]
    model = load_model('secchi_classification.h5')
    image_catch, stat = frame_catch(video_path, model)

    if stat == 'Failed':
        print("secchi can be detected through out the video.")
    else:
        measurement, stat2 = depth_reco(image_catch)
        if stat2 == 'Failed':
            print("Recognition failed")
        else:
            print("Measurement: %s" % measurement)
```

The frame_catch function first read each frame in a video

find the secchi disk segment, grayscale the image

resize the image to 90*50, then run the "h5" model on the image.

The program will keep analyzing each frame until the result from h5 model returns 0

meaning secchi disk is no longer detected in the frame.

if secchi disk is no longer detected, depth_reco function will be ran

depth_reco takes the frame as input, then run a mask from the right side of the frame to the left

when the count of white pixels reaches 20% of the total pixel count in the mask

The mask is returned in a variable.

Then pytesseract OCR will run on the mask, if number can be read, return number

if number cannot be read, save the mask.


## Training model steps

1. Seperate video into frames

2. Extract secchi segment from the frames

3. Label the visibility of each frame in filenames

4. Reshape the images and put all images into a CSV file

5. CNN training


### 1. Seperate video into frames

Define a function to seperate the video into frames. There will be a main directory called "capture".

Inside capture, each video will have a folder to store the frames in.

This code is stored under:

https://github.com/cloudmesh-community/fa18-423-08/blob/master/project-code/secchi_videoprocessing.py

It should run in the command line in the format of:

```bash
python secchi_videoprocessing.py video 2
```

where the file takes two arguments, first one is the path of the videos, second one takes the number of cores to utilize

```python
import os  
import sys
import cv2
import threading
from progressbar import ProgressBar, Percentage, Bar

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

#main section
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
```

An example frame would look like this:

![Original](frame527.jpg)


### 2. extract the secchi disk from the frames.

The secchi disk is taken out of the frame by the pixel position of 290 < x < 690

The secchi disk segment image is then put into grayscale

Last, the secchi disk segment image is resized to  90*50.

The code is stored under:

https://github.com/cloudmesh-community/fa18-423-08/blob/master/project-code/secchi_segment.py

The command line:
```bash
python secchi_segment.py capture
```
where it takes one argument, the folder where the frames are stored.

```python
import os  
import sys
import cv2
from progressbar import ProgressBar, Percentage, Bar

def secchi_segment(frame):
    img = cv2.imread(frame)
    video_name = frame.split('\\')[1]
    frame_number = frame.split('\\')[2].split('.')[0]
    if not os.path.exists(video_name):
        os.makedirs(video_name)
    secchi = img[:,290:690,:]
    secchi = cv2.cvtColor(secchi, cv2.COLOR_BGR2GRAY)
    secchi = cv2.resize(secchi,(90,50),interpolation = cv2.INTER_CUBIC)
    path = video_name + '/frame_secchi_{number}.jpg'.format(number = frame_number)
    cv2.imwrite(path,secchi)
#main
if __name__== "__main__":
    frame_path = sys.argv[1]

    frame_list = []
    for root, dirs, files in os.walk(frame_path):
        for file in files:
            frame_list.append(os.path.join(root,file))
    for frame in frame_list:
        data = secchi_segment(frame)
        print(frame)
```

### 3. label the visibility of each frame in filenames

This step has to be done by the researcher, to identify to which frame is the secchi disk

no longer visible. Add a "_1" behind the filename if the frame still has secchi disk,

add a "_0" behind the filename if the frame does not have secchi disk.


```python
import os

files = os.listdir('DSCN0003')

count = 0
for file in files[0:701]:
    new_file = os.path.splitext(file)[0]+'_1'+".jpg"
    os.rename(os.path.join('DSCN0003',file),os.path.join('DSCN0003',new_file))
    

for file in files[701:1466]:
    new_file = os.path.splitext(file)[0]+'_0'+".jpg"
    os.rename(os.path.join('DSCN0003',file),os.path.join('DSCN0003',new_file))

for file in files[1466:]:
    new_file = os.path.splitext(file)[0]+'_1'+".jpg"
    os.rename(os.path.join('DSCN0003',file),os.path.join('DSCN0003',new_file))
```

### 4. Reshape the images and put all images into a CSV file

Reshape each image into one array, and then add the label value to the "label" column

Then add each array into a pandas DataFrame, then save the dataframe as a csv file.

```python
import os
import cv2
import pandas as pd
import time


start = time.time()

folder_name = 'DSCN0003'

data_X = pd.DataFrame()
y_list = []
for _,_,files in os.walk(folder_name):
    i = 0
    for file in files:
        filepath = os.path.join(folder_name, file)
        
        try:
            im = cv2.imread(filepath)
            im = pd.DataFrame(im[:,:,0].reshape(1,-1))
            data_X = pd.concat([data_X, im], axis=0)
            y = os.path.splitext(file)[0].split('_')[-1]
            y_list.append(y)
            print("Pic %i" % i)
            i += 1
        
        except:
            continue

runtime = time.time() - start
print("Runtime is %f s." % runtime)

data = data_X.copy()
data['label'] = y_list
data.to_csv('DSCN0003.csv',index = False)
```

### 5. CNN training

Read the csv file

have a training set and a testing set

seperate the label column and store it into a seperate variable

One-hot encoding process the label values.

The neural network structure is already designed

model at last will be saved as a "h5" file.


```python
import numpy as np
import pandas as pd
from keras.models import *
from keras.layers import *
from keras.utils import np_utils

train_size = 1600
img_cols, img_rows = 50, 90
n_class = 2

data = pd.read_csv('DSCN0003.csv')
data_y = np_utils.to_categorical(data['label'],2)
data_X = np.array(data.iloc[:,:(data.shape[1]-1)])

train_X = data_X[:train_size,:]
train_X = train_X.reshape(train_X.shape[0], img_rows, img_cols, 1)
test_X = data_X[train_size:,:]
test_X = test_X.reshape(test_X.shape[0], img_rows, img_cols, 1)
train_y = data_y[:train_size,:]
test_y = data_y[train_size:,:]

inputs = Input((img_rows, img_cols, 1))
x = inputs

for i in range(3):
    x = Convolution2D(8*2**i, (3,3), activation='relu')(x)
    x = Convolution2D(8*2**i, (3,3), activation='relu')(x)
    x = BatchNormalization()(x)
    x = MaxPooling2D((2,2))(x)

x = Flatten()(x)
x = Dropout(0.05)(x)
x = Dense(n_class, activation='softmax')(x)

model = Model(inputs=inputs, outputs=x)
model.summary()

model.compile(optimizer='Adam',loss='categorical_crossentropy',metrics=['accuracy'])
model.fit(train_X, train_y, epochs=5, batch_size=128, validation_data=(test_X,test_y))

model.save('secchi_classification.h5')
```


## Potential limitations and Problems

1. The position of items needs to be similar to DSCN0003.avi for other video.

2. segment of secchi disk is designed to be at a fixed range of positions where x axis is between 290 - 690

3. The model is trained only based on DSCN0003.avi file, the adaptive and accuracy still needs to be improved

   by having more data.
   
4. Pytesseract OCR has trouble reading numbers from the image provided

## Possible solution for measurement reading

1. Build an OCR model based on the data, but will require people to label each frame measurement for training purpose

   The tape measurement should be replaced with other tapes, since this tape does not tell feet information on frames.

2. Replace tape measurement with other types of measurement, for example, light sensor or pressure measurement. 




