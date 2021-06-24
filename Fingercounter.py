import cv2
import time
import HandModule as htm


wcam,hcam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,wcam)
pTime=0

detector = htm.handDetector()

tipId=[4,8,12,16,20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
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

       # print(fingers)
        count=0
        if fingers[0] == 0:
            cv2.putText(img, 'Thumb finger: closed',(5,70),cv2.FONT_HERSHEY_PLAIN,1.5,(255,0,0),1)
        else:
            cv2.putText(img, 'Thumb finger: open',(5,70),cv2.FONT_HERSHEY_PLAIN,1.5,(255,0,0),1)
            count=count+1
        if fingers[1] == 0:
            cv2.putText(img, 'Index finger: closed',(5,100),cv2.FONT_HERSHEY_PLAIN,1.5,(255,0,0),1)
        else:
            cv2.putText(img, 'Index finger: open',(5,100),cv2.FONT_HERSHEY_PLAIN,1.5,(255,0,0),1)
            count=count+1
        if fingers[2] == 0:
            cv2.putText(img, 'Middle finger: closed',(5,130),cv2.FONT_HERSHEY_PLAIN,1.5,(255,0,0),1)
        else:
            cv2.putText(img, 'Middle finger: open',(5,130),cv2.FONT_HERSHEY_PLAIN,1.5,(255,0,0),1)
            count=count+1
        if fingers[3] == 0:
            cv2.putText(img, 'Ring finger: closed',(5,160),cv2.FONT_HERSHEY_PLAIN,1.5,(255,0,0),1)
        else:
            cv2.putText(img, 'Ring finger: open',(5,160),cv2.FONT_HERSHEY_PLAIN,1.5,(255,0,0),1)
            count=count+1
        if fingers[4] == 0:
            cv2.putText(img, 'Little finger: closed',(5,190),cv2.FONT_HERSHEY_PLAIN,1.5,(255,0,0),1)
        else:
            cv2.putText(img, 'Little finger: open',(5,190),cv2.FONT_HERSHEY_PLAIN,1.5,(255,0,0),1)
            count=count+1

        
        cv2.putText(img, f'Fingers open:',(5,250),cv2.FONT_HERSHEY_PLAIN,1.5,(255,0,0),1)
        cv2.putText(img, f'{int(count)}',(5,300),cv2.FONT_HERSHEY_PLAIN,4,(255,0,0),2)
        
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime 
    cv2.putText(img, f'FPS:{int(fps)}',(5,25),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)
    cv2.imshow("Nazeer", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
