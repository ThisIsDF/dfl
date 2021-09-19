from imutils.video import FileVideoStream
from imutils.video import FPS
from imutils import face_utils
import numpy as np
import imutils
import time
import cv2
import dlib
from tqdm import tqdm
import os

detector = dlib.cnn_face_detection_model_v1("./mmod_human_face_detector.dat")

count = 0
skip = 0
skipfiles = 0
directory = "Z:\SERIES\Big Sky (2020)\Season 1" 
savepath = "D:\\recycle\\tr\\workspace-KW\\data_src\\frames\\"

for filename in os.listdir(directory):
    skipfiles += 1
    if skipfiles <= 5:
       continue

    print(filename)
    vs = FileVideoStream(directory + '\\' + filename).start()

    framecount = int(vs.stream.get(cv2.CAP_PROP_FRAME_COUNT) ) 
    frameprogress = tqdm(total=framecount, desc="Frame Progress")

    while vs.more():
        frame = vs.read()
        if frame is None: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rects = detector(gray, 0)

        for faceRect in rects:
            x1 = faceRect.rect.left()
            y1 = faceRect.rect.top()
            x2 = faceRect.rect.right()
            y2 = faceRect.rect.bottom()
            h = abs(y2 - y1)
            if h > 400:
                 #print(savepath + 'frame' + str(count) + '.jpg')
                 if skip % 1 == 0:
                    fm = cv2.Laplacian(gray, cv2.CV_64F).var()
                    if fm > 15:
                       cv2.imwrite(savepath + 'frame' + str(count) + '.jpg', frame)
                    count += 1
                 #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                 
                 skip += 1
            else:
                 skip = 0
                      
#        cv2.imshow("Frame", frame)
        frameprogress.update(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vs.stop()
    cv2.destroyAllWindows()
