import cv2
import mediapipe as mp
import numpy as np
import Hand_tracking as htm
# from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = htm.handDetector(detectionCon=0.8)
# detector = HandDetector(detectionCon=0.8)

colorR = (255, 0, 255)
cx, cy, w, h = 100, 100, 150, 150

class DragRect():
    def __init__(self, posCenter, size=[200,200]):
        self.posCenter = posCenter
        self.size = size

    def Update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        if cx - w//2<cursor[0]<cx + w//2 and cy - h//2<cursor[1]<cy + h//2:
            self.posCenter = cursor

            
rectList = []
for x in range(5):
    rectList.append(DragRect([x*250+150,150]))

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = detector.findHands(frame)
    # hands, frame = detector.findHands(frame)
    lmList = detector.findPosition(frame)
    # if len(lmList) != 0:
    #     print(lmList[8])

    # if hands:
    #     hand1 = hands[0]
    #     lmList = hand1["lmList"]
    #     cursor = lmList[8]

        # length,info,frame = detector.findDistance(lmList[8], lmList[12], frame)
        # print(length)
        # if length<30:

    #     print(cursor)
    if lmList:
        cursor = lmList[8]
        # length,info,frame = detector.findDistance(lmList[8], lmList[12], frame)
        length,info,frame = detector.findDistance(8, 12, frame)
        print(length)
        if length<50:
            for rect in rectList:
                rect.Update(cursor[1:])
    for rect in rectList:   
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(frame, (cx - w//2, cy - h//2), (cx + w//2, cy + h//2), colorR, cv2.FILLED)
    cv2.imshow("Image", frame)
    if cv2.waitKey(1) & 0xFF == ord("e"):
        break 

cap.release()
cv2.destroyAllWindows()