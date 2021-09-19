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

directory = r"C:\path\to\video\files"
savepath = r"C:\path\to\workspace\for\frames"
facesize = 400    # minimum face size to save frame
blur = 15         # maximum blurriness to save frame (lower value is higher frame blur)

detector = dlib.cnn_face_detection_model_v1("./mmod_human_face_detector.dat")

count = 0
skip = 0
skipfiles_count = 0
skipfiles = -1

for filename in os.listdir(directory):
    skipfiles_count += 1
    if skipfiles_count <= skipfiles:
       continue

    print(filename)
    vs = FileVideoStream(os.path.join(directory, filename)).start()

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
            if h >= facesize:
                 #print(savepath + 'frame' + str(count) + '.jpg')
                 if skip % 1 == 0:
                    fm = cv2.Laplacian(gray, cv2.CV_64F).var()
                    if fm > blur:
                       cv2.imwrite(fsavepath + '\\' + 'frame' + str(count) + '.jpg', frame)
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
