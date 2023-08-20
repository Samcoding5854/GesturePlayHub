import cv2
import mediapipe as mp
import time

class HandDetector():
    def __init__(self, mode = False, maxHands = 2, model_complexity=1, detectionConf = 0.5, trackingConf = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.model_complexity = model_complexity
        self.detectionConf = detectionConf
        self.trackingConf = trackingConf
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,
                                        self.maxHands,
                                        self.model_complexity,
                                        self.detectionConf,
                                        self.trackingConf)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLMS in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLMS, self.mpHands.HAND_CONNECTIONS)
    
        return img

        
    def findPosition(self, img, handNo = 0, draw = False):
        lmList = []


        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        # print(id, cx, cy)
                        lmList.append([id,cx,cy])
                        if draw:
                            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return lmList


def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    cTime = 0
    detector = HandDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        
        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX, 3, (255,0,255), 3)
        cv2.imshow("IMAGE", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()