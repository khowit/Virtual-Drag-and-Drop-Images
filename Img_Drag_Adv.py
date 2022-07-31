import cv2
import numpy as np
import Hand_tracking as htm
import cvzone
import os
# from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = htm.handDetector(detectionCon=0.8)

class DragImg():
    def __init__(self, path, posOrigin, imgType):

        self.path = path
        self.posOrigin = posOrigin
        self.imgType = imgType

        if self.imgType == 'png':
            self.img = cv2.imread(self.path,cv2.IMREAD_UNCHANGED)
        else:
            self.img = cv2.imread(self.path)

        self.size = self.img.shape[:2]

    def Update(self, cursor):
        ox, oy = self.posOrigin
        w, h = self.size

        if ox<cursor[0]<ox + w and oy<cursor[1]<oy + h:
            self.posOrigin = cursor[0]-w//2, cursor[1]-h//2
        

path = "Virtual Drag and Drop/images"
myList = os.listdir(path)
imgList = []

for x, imgPath in enumerate(myList):
    if 'png' in imgPath:
        imgType = 'png'
    else:
        imgType = 'jpg'

    imgList.append(DragImg(f'{path}/{imgPath}', [50+x*300, 50], imgType))
    

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame)

    if lmList:

        length,info,frame = detector.findDistance(8, 12, frame)
        print(length)
        if length < 50:
            cursor = lmList[8]
            for imgObj in imgList:
                imgObj.Update(cursor[1:])

    try:     
        for imgObj in imgList:
            h, w = imgObj.size
            ox, oy = imgObj.posOrigin
            if imgObj.imgType == 'png':
                frame = cvzone.overlayPNG(frame, imgObj.img, [ox, oy])
            else:
                frame[oy:oy + h, ox:ox + w] = imgObj.img
    except:
        pass

    cv2.imshow("Image", frame)
    if cv2.waitKey(1) & 0xFF == ord("e"):
        break 

cap.release()
cv2.destroyAllWindows()