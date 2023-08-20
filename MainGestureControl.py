import cv2 
import time
import numpy as np
import HandTrackingModel as htm
import math
import alsaaudio
import subprocess
from HandInfoDetector import HandInfo
from Utils import EmotionDetector
from cvzone.HandTrackingModule import HandDetector
from NumberGiverGest import NumberGiver


############################################################


cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)

m = alsaaudio.Mixer()
pmin_default, pmax_default = m.getrange()
minVol = pmin_default
maxVol = pmax_default


tipIds = [4, 8, 12, 16, 20] #Finger Tips Id for Mediapipe


detectorInd = HandDetector(detectionCon=0.8, maxHands=2)


link_opened = False
cTime = 0
start_time = None
tracking_duration = 50
current_emotion = None
pTime = 0
emotion_actions = {
    "happy": "xdg-open https://youtube.com/shorts/T8bO1iKu76g?feature=share",
    "sad": "xdg-open http://google.com",
    "angry": "xdg-open http://google.com",
    "neutral": "xdg-open http://google.com"
}

#############################################################

while True:
    success, img = cap.read()
    emotion = EmotionDetector(img) #Emotion Detector 
    # print(emotion)
    hands, img =detectorInd.findHands(img)

    if emotion in emotion_actions:
        if current_emotion != emotion:
            current_emotion = emotion
            start_time = time.time()

        elapsed_time = time.time() - start_time
        if elapsed_time >= tracking_duration and not link_opened:
            action = emotion_actions[current_emotion]
            subprocess.Popen(action, shell=True)
            link_opened = True
            current_emotion = None

    else:
        current_emotion = None
        start_time = None

    numberOfHands= HandInfo(hands)
    


    if len(hands) != 0:
    
        print(f' Number Of Hands: {numberOfHands}')

        ### Volume Adjustment Code ###
        if numberOfHands == '2':
            print("Volume Activated")
    
            hand1 = hands[1]
            lmlist = hand1["lmList"]
            
            x1, y1= lmlist[4][1], lmlist[4][2]
            x2, y2= lmlist[8][1], lmlist[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.circle(img, (x1,y1), 6, (255,0,255), cv2.FILLED)
            cv2.circle(img, (x2,y2), 6, (255,0,255), cv2.FILLED)
            cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3)
            cv2.circle(img, (cx,cy), 10, (255,0,255), cv2.FILLED)
            length = math.hypot(x2 - x1, y2 - y1)
            # print(length)

            if length < 15:
                cv2.circle(img, (cx,cy), 10, (0, 255, 0), cv2.FILLED)
            
            volu = np.interp(length,[15,140],[0,100])
            print(volu)
            m.setvolume(int(volu))
           
        ### Play Pause Activation Code ###
        elif numberOfHands == '1':
            fingers = []
            hand1 = hands[0]
            lmlist = hand1["lmList"]
            print("Play/Pause Activated")

            ### Counting the Number Displayed on Hand ###

            if lmlist[tipIds[0]][1] > lmlist[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1,5):
                if lmlist[tipIds[id]][2] < lmlist[tipIds[id]-2][2]:
                    fingers.append(1)
                
                else:
                    fingers.append(0)

   
            totalFingers = fingers.count(1)
       
            print(f'Number of Fingers : {totalFingers}')

            ### Running Commands for next / previous / play / pause ###
            if totalFingers == 1:
                if fingers == [0, 0, 0, 0, 1]:
                    subprocess.Popen('playerctl --all-players next', shell=True)
            
                elif fingers == [1, 0, 0, 0, 0]:
                        subprocess.Popen('playerctl --all-players previous', shell=True)


            elif totalFingers == 0:
                subprocess.Popen('playerctl --all-players pause', shell=True)
            
            elif totalFingers == 5:
                subprocess.Popen('playerctl --all-players play', shell=True)

        ### Showing the FPS ###
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX, 3, (255,0,255), 3)


    cv2.imshow("IMAGE", img)
    cv2.waitKey(1)

