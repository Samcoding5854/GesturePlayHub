import cv2 
import time
import webbrowser
import subprocess
from Utils import EmotionDetector


############################################################


cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)

link_opened = False
cTime = 0
start_time = None
tracking_duration = 5
current_emotion = None
pTime = 0
emotion_actions = {
    "happy": "xdg-open https://youtube.com/shorts/T8bO1iKu76g?feature=share",
    "sad": "xdg-open https://www.youtube.com/watch?v=u0w-s6yid38",
    "angry": "xdg-open https://www.youtube.com/watch?v=WcIcVapfqXw",
    "neutral": "xdg-open https://i.imgflip.com/7wclr3.jpg",
    "shocked": "https://www.youtube.com/shorts/yvBYSfb1-GE"
}

#############################################################

while True:
    success, img = cap.read()
    emotion = EmotionDetector(img) #Emotion Detector 
    print(emotion)

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


        ### Showing the FPS ###
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX, 3, (255,0,255), 3)


    cv2.imshow("IMAGE", img)
    cv2.waitKey(1)