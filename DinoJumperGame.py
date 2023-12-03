import pyautogui
import cv2
from HandTrackingModel import HandDetector
import subprocess



width, height = 1280, 720
gestureThreshold = 250
link_opened = False


detector = HandDetector(maxHands=1)

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height) 
gestureThreshold = 100
finger_open = False

while True:
    success, img = cap.read()

    if not link_opened: 
        subprocess.Popen("xdg-open https://offline-dino-game.firebaseapp.com/", shell=True)
        link_opened = True

    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw = False)

    if len(lmlist) != 0:
            if lmlist[8][2] < lmlist[6][2]:
                if not finger_open:
                    print("Index Opened")
                    pyautogui.press('space')
                    finger_open = True
            else:
                finger_open = False

            
     
    
    cv2.imshow("IMAGE", img)
    cv2.waitKey(1)

