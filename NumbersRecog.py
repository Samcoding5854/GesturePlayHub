import cv2
import time
import os
import HandTrackingModel as htm
from Utils import play_inning, generate_computer_number

wCam, hCam = 640, 480

pTime = 0

# cap = cv2.VideoCapture(0)
# cap.set(3, wCam)
# cap.set(4, hCam)


detector = htm.HandDetector(detectionConf=0.7, maxHands = 1)

cTime = 0
pTime = 0

tipIds = [4, 8, 12, 16, 20]



def NumberGiver(img):
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw = False)

    user_score = 0
    computer_score = 0
    

    if len(lmlist) != 0 :
        fingers = []

        # Thumb
        if lmlist[tipIds[0]][1] > lmlist[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):
            if lmlist[tipIds[id]][2] < lmlist[tipIds[id]-2][2]:
                fingers.append(1)
            
            else:
                fingers.append(0)

        # print(fingers)

        totalFingers = fingers.count(1)
        # print(totalFingers)

        # # cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        # cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
        #             10, (255, 0, 0), 25)
        
        totalFingersint = int(totalFingers)


        return (totalFingersint)
    
    else:
        # Handle the case when lmlist is empty
        return 0

