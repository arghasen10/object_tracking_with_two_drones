import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
cap = cv2.VideoCapture('green.mp4')
cX,cY = 0,0
delX = []
delY = []
timestamp = []
starttime = time.time()
while True:
    ret, frame = cap.read()
    if not ret:
        cap = cv2.VideoCapture('green.mp4')
        ret, frame = cap.read()
        continue

    lower_green = np.array([63,121,103])
    upper_green = np.array([253,250,204])
    frame = cv2.rotate(frame,0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green, upper_green)
    kernel = np.ones((15, 15), np.int)
    dilated = cv2.dilate(mask, kernel)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    ret, thrshed = cv2.threshold(cv2.cvtColor(res, cv2.COLOR_BGR2GRAY), 3, 255, cv2.THRESH_BINARY)
    _,cnts,_  = cv2.findContours(thrshed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    areas = [cv2.contourArea(cnt) for cnt in cnts]
    max_index = np.argmax(areas)
    cnt = cnts[max_index]
    M = cv2.moments(cnt)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:

        cX, cY = 0, 0

    # draw the contour and center of the shape on the image
    cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
    cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
    cv2.putText(frame, "center", (cX - 20, cY - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    frameY, frameX = frame.shape[0], frame.shape[1]
    cntFrameX, cntFrameY = int(frameX // 2), int(frameY // 2)
    #print(cntFrameX, cntFrameY)
    cv2.circle(frame, (cntFrameX, cntFrameY), 6, (0, 255, 0), -1)
    cv2.putText(frame, "Frame center", (cntFrameX, cntFrameY),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    delX.append(cntFrameX-cX)
    delY.append(cntFrameY-cY)
    timenow = time.time()
    timestamp.append(timenow-starttime)
    cv2.imshow('thresh', thrshed)
    #cv2.imshow('res', res)
    #cv2.imshow('hsv', hsv)
    cv2.imshow('frame', frame)
    #cv2.imshow('mask', mask)

    k = cv2.waitKey(30) & 0xFF
    if k == ord('q'):
        print("DelX ",delX)
        print("dely = ",delY)
        print("timestamp ",timestamp)
        fig, axs = plt.subplots(1)
        fig.suptitle('delX w.r.t. center of frame')
        axs.plot(timestamp,delX)
        #axs[0].plot(timestamp,delX)
        #axs[1].plot(timestamp,delY)
        axs.set(xlabel = 'time',ylabel = 'delX')
        plt.show()
        break
cap.release()
cv2.destroyAllWindows()
