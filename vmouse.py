import cv2
import time
import autopy
import HandModule as htm
import numpy as np
import math

wCam,hCam = 640, 480
frameR=100
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,wCam)
pTime=0
smoothening=5
plocx,plocy = 0,0
clocx,clocy = 0,0

detector = htm.handDetector()
wScr,hScr = autopy.screen.size()

print(wScr,hScr)

tipId=[4,8,12,16,20]
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[4][1:]
        x3,y3 = lmList[5][1:]
        

        fingers=[]
        if lmList[tipId[0]][1]>lmList[tipId[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1,5):
            if lmList[tipId[id]][2]<lmList[tipId[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        cv2.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,255),2)

        if fingers[1]==1 and fingers[2]==0:
            x3=np.interp(x1,(frameR,wCam-frameR),(0,wScr))
            y3=np.interp(y1,(frameR,hCam-frameR),(0,hScr))
            clocx=plocx + (x3-plocx)/smoothening
            clocy=plocy + (y3-plocy)/smoothening
            autopy.mouse.move(wScr-clocx,clocy)
            cv2.circle(img,(x1,y1),15,(0,0,0),cv2.FILLED)
            plocx,plocy = clocx,clocy
        if fingers[2]==1:
            
            cv2.line(img,(x3,y3),(x2,y2),(255,0,0),2)
            cx,cy = (x3+x2)//2,(y3+y2)//2
            cv2.circle(img, (cx,cy),7,(255,0,0),cv2.FILLED)
            length=math.hypot(x2-x3,y2-y3)

            #Hand range 25 - 165
            #Vol range -65 - 0

            if length <50:
                autopy.mouse.click()
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime 
    cv2.putText(img, f'FPS:{int(fps)}',(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3)
    cv2.imshow("Nazeer", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
