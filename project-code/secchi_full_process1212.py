import sys
import cv2
import pytesseract
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
                break
        else:
            continue
    cap.release()

    if flag == True:
        return image, 'Succeed'
    else:
        return image, 'Failed'


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
            axis = x
            break

    if flag == True:
        mini_secchi = image_catch[y0:y1,axis:(axis+160),:]
        measurement = pytesseract.image_to_string(mini_secchi)

        return measurement, mini_secchi, 'Succeed'
    else:
        return measurement, mini_secchi, 'Failed'

if __name__== "__main__":

    video_path = sys.argv[1]
    model = load_model('secchi_classification.h5')
    image_catch, stat = frame_catch(video_path, model)
    cv2.imwrite("image_catch.jpg",image_catch)
    if stat == 'Failed':
        print("Something bad happened.")
    else:
        measurement, mea_pic, stat2 = depth_reco(image_catch)
        if stat2 == 'Failed':
            print("Recognition failed")
        else:
            cv2.imwrite('mea_pic.jpg', mea_pic)
            print(measurement)
