import cv2

def video_frame(video_name):
    cap = cv2.VideoCapture(video_name)
    capture,image = cap.read()
    count = 0
    capture = True
    while capture:
        capture,image = cap.read()
        cv2.imwrite('frame%d.jpg' % count, image)
        print("Creating frame: ", capture)
        count += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()

# main
video_frame("DSCN0003.AVI")
