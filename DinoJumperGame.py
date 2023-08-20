import pyautogui
import cv2



width, height = 1280, 720
gestureThreshold = 250

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height) 

# pyautogui.press('space')

while True:
    success, img = cap.read()

    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)
    
    
    cv2.imshow("IMAGE", img)
    cv2.waitKey(1)