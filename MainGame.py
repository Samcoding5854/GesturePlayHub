import cv2
import cvzone
import HandTrackingModel as htm
import random
from NumbersRecog import NumberGiver
import pyautogui
import time

detector = htm.HandDetector(detectionConf=0.7, maxHands = 1)

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)


timer = 0
StateResult = False
StartGame = False
PlayerOut = False
outMessageTime = None
BattingScore1inn = 00
BowlPlayed1inn = 0
BattingScore2inn = 0
BowlPlayed2inn = 0
showImgAI = False
Target = 0
InningPlayer = 0
GameEnd = False
gameEndTime = None
Ballsleft = 0
RunsLeft = 0

while True:

    imgB = cv2.imread("Resources/samarth@martian.png")
    imgB = cv2.resize(imgB, (0,0), None, 0.67,0.67)
    success, img = cap.read()
    
    imgScaled = cv2.resize(img,(0,0), None, 0.73,0.73)
    imgScaled = imgScaled[:,80:415] 
    imgScaled = cv2.flip(imgScaled, 1)
    # imgScaled = detector.findHands(imgScaled)
    imgB[358:708, 910:1245] = imgScaled
    # cv2.imshow("Scaled", imgScaled)


    
    if StartGame:

        if StateResult is False:
            timer = time.time() - initialTime
            if InningPlayer == 0:
                Batsman = "Samarth"
                Bowler = "AI"
                cv2.putText(imgB,str(int(timer)),(620,605),cv2.FONT_HERSHEY_PLAIN, 10, (255,0,255), 7)
                cv2.putText(imgB,f'1st INNING',(400,110),cv2.FONT_HERSHEY_PLAIN, 6, (255,0,255), 6)
                cv2.putText(imgB,f'Batsman: {Batsman}',(100,780),cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255), 2)
                cv2.putText(imgB,f'Bowler: {Bowler}',(100,810),cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255), 2)
                cv2.putText(imgB,f'{BattingScore1inn}',(93,300),cv2.FONT_HERSHEY_PLAIN, 6, (255,0,255), 5)
                cv2.putText(imgB,f'{BowlPlayed1inn}',(1135,300),cv2.FONT_HERSHEY_PLAIN, 6, (255,0,255), 5)
                cv2.putText(imgB,f'Runs Made: {BattingScore1inn}',(930,780),cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255), 2)
                cv2.putText(imgB,f'Balls Played: {BowlPlayed1inn}',(930,820),cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255), 2)

            ### Show stats when the first innings end ###
            if PlayerOut and outMessageTime is not None:
                    cv2.putText(imgB, "You are out", (400,110),cv2.FONT_HERSHEY_PLAIN, 6, (255,0,255), 6)
                    cv2.putText(imgB,f'{BattingScore1inn}',(93,300),cv2.FONT_HERSHEY_PLAIN, 6, (255,0,255), 5)
                    cv2.putText(imgB,f'{BowlPlayed1inn}',(1135,300),cv2.FONT_HERSHEY_PLAIN, 6, (255,0,255), 5)
                

                    if time.time() - outMessageTime >= 3:  # Display for 2 seconds
                        PlayerOut = False
                        outMessageTime = None

            elif InningPlayer == 1:
                Batsman = "AI"
                Bowler = "Samarth"      

                cv2.putText(imgB,str(int(timer)),(620,605),cv2.FONT_HERSHEY_PLAIN, 10, (255,0,255), 7)
                # if not GameEnd:  # Display only if the game hasn't ended
                cv2.putText(imgB, f'2nd INNING', (400, 110), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 6)
                cv2.putText(imgB,f'Batsman: {Batsman}',(100,780),cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255), 2)
                cv2.putText(imgB,f'Bowler: {Bowler}',(100,810),cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255), 2)
                cv2.putText(imgB,f'{BattingScore2inn}',(93,300),cv2.FONT_HERSHEY_PLAIN, 6, (255,0,255), 5)
                cv2.putText(imgB,f'{BowlPlayed2inn}',(1135,300),cv2.FONT_HERSHEY_PLAIN, 6, (255,0,255), 5)
                cv2.putText(imgB,f'Target: {Target}',(930,760),cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255), 2)
                cv2.putText(imgB,f'Balls Left: {Ballsleft}',(930,800),cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255), 2)
                cv2.putText(imgB,f'Runs Left: {RunsLeft}',(930,840),cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255), 2)

                   
              
            if timer > 3:    
                timer = 0
        
                UserNumber = NumberGiver(imgScaled)
                randomNumber = random.randint(1,5)  

                imgAI = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                
                
                # cv2.putText(imgB,f'{randomNumber}',(835,400),cv2.FONT_HERSHEY_PLAIN, 10, (255,0,255), 5)
                print(f'PC Played: {randomNumber}')
                
                if UserNumber == 0:
                    print("Zero is not a valid play")
                else:
                    print(f'You Played: {UserNumber}')

                
                showImgAI = True 

                if UserNumber != randomNumber:
                    if InningPlayer == 0:
                        BattingScore1inn = BattingScore1inn + UserNumber
                        BowlPlayed1inn += 1
                        Ballsleft += 1
                        Target = BattingScore1inn
                        RunsLeft = Target
                        print(f'Runs Made: {BattingScore1inn}')
                        print(f'Balls Played: {BowlPlayed1inn}\n\n')
                        

                    elif InningPlayer == 1:
                        BattingScore2inn = BattingScore2inn + randomNumber
                        BowlPlayed2inn = BowlPlayed2inn + 1
                        Ballsleft -=1
                        RunsLeft = RunsLeft - randomNumber
                        print(f'Runs Made: {BattingScore1inn}')
                        print(f'Runs Left: {RunsLeft}')
                        print(f'Balls Played: {BowlPlayed1inn}')
                        print(f'Balls Left: {Ballsleft}\n\n')

                        if RunsLeft <=0 or Ballsleft<0:
                            RunsLeft = 0
                            GameEnd = True
                            gameEndTime = time.time()
                            print("PC Wins\n\n")
                            break

                    
                elif UserNumber == randomNumber:

                    if InningPlayer == 0:
                        print('\n\n2nd INNING\n\n')
                        PlayerOut = True
                        outMessageTime = time.time()
                        InningPlayer = 1


                    else:
                        GameEnd = True
                        gameEndTime = time.time()
                        print("You Win!\n\n")
                        break
  
                pyautogui.press('s')

        if showImgAI:  # Display imgAI when showImgAI is True
            imgAI = cv2.resize(imgAI, (295,295))
            imgB = cvzone.overlayPNG(imgB, imgAI, (110, 410))   

    # if GameEnd:
    #     if RunsLeft <= 0:
    #         cv2.putText(imgB, "PC Wins", (400,110),cv2.FONT_HERSHEY_PLAIN, 6, (255,0,255), 6)
    #     else:
    #         cv2.putText(imgB, "You Win!", (400,110),cv2.FONT_HERSHEY_PLAIN, 6, (255,0,255), 6)
    #     if time.time() - gameEndTime >= 2:  # Display for 2 seconds
    #         GameEnd = False
    #         gameEndTime = None
        
    cv2.imshow("BG", imgB)

    key = cv2.waitKey(1)
    if key == ord('s'):
        StartGame = True
        initialTime = time.time()
        StateResult = False

    
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break