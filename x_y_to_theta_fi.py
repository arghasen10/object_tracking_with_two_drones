import cv2
import numpy as np
import time
import math
import matplotlib.pyplot as plt
import csv
hmin = 0
hmax = 0
smin = 0
smax = 0
vmin = 0
vmax = 0
max_index = 0

def hminc(x):
    hmin = x


def hmaxc(x):
    hmax = x


def sminc(x):
    smin = x


def smaxc(x):
    smax = x


def vminc(x):
    vmin = x


def vmaxc(x):
    vmax = x


lower_hsv = np.array([hmin, smin, vmin])
upper_hsv = np.array([hmax, smax, vmax])
##cv2.namedWindow("frame1", 50)
##cv2.createTrackbar("hmin", "frame1", 50, 255, hminc)
##cv2.createTrackbar("hmax", "frame1", 50, 255, hmaxc)
##cv2.createTrackbar("smin", "frame1", 50, 255, sminc)
##cv2.createTrackbar("smax", "frame1", 50, 255, smaxc)
##cv2.createTrackbar("vmin", "frame1", 50, 255, vminc)
##cv2.createTrackbar("vmax", "frame1", 50, 255, vmaxc)
cap = cv2.VideoCapture('bluebox_drone.MP4')
largest_area = 0
theta =[0]
fi = [0]
timestamp = [0]
X = [0]
Y = [0]
cX, cY = 0, 0
areas = []
starttime = time.time()
previoustime = starttime
ret,frame = cap.read()
hframe,wframe = frame.shape[0],frame.shape[1]
#fourcc = cv2.VideoWriter_fourcc(*'XVID')

#out = cv2.VideoWriter('output_processe.avi', fourcc, 32.0, (wframe,hframe))


#csv file for storing yaw pitch with timestamp

with open('orientation_data.csv', 'w+') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Yaw","Pitch","Timestamp"])


while True:
    ret, frame = cap.read()
    if not ret:
        cap = cv2.VideoCapture('bluebox_drone.MP4')
        ret, frame = cap.read()
        continue
    hframe,wframe = frame.shape[0],frame.shape[1]
    cntFrameX,cntFrameY = wframe//2,hframe//2
    #print(cntFrameX,cntFrameY)
    #hmin = cv2.getTrackbarPos("hmin", "frame1")
    #hmax = cv2.getTrackbarPos("hmax", "frame1")
    #smin = cv2.getTrackbarPos("smin", "frame1")
    #smax = cv2.getTrackbarPos("smax", "frame1")
    #vmin = cv2.getTrackbarPos("vmin", "frame1")
    #vmax = cv2.getTrackbarPos("vmax", "frame1")
    #lower_green = np.array([hmin, smin, vmin])
    #upper_green = np.array([hmax, smax, vmax])
    lower_hsv = np.array([86,122,117])
    upper_hsv = np.array([176,215,255])
    # frame = cv2.rotate(frame,0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    kernel = np.ones((5,5), np.int)
    dilated = cv2.dilate(mask, kernel)
    morphed = cv2.morphologyEx(dilated,cv2.MORPH_OPEN,kernel)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    ret, thrshed = cv2.threshold(cv2.cvtColor(res, cv2.COLOR_BGR2GRAY), 3, 255, cv2.THRESH_BINARY)
    _,cnts,_ = cv2.findContours(morphed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) != 0:
        # draw in blue the contours that were founded
        #cv2.drawContours(frame, cnts, -1, 255, 3)

        # find the biggest area
        cnt = max(cnts, key=cv2.contourArea)

        M = cv2.moments(cnt)

        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:

            cX, cY = 0, 0
        ##
        ##    # draw the contour and center of the shape on the image
        cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
        cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(frame, "center of Obj", (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.circle(frame,(cntFrameX,cntFrameY),5,(255,255,255),-1)
    cv2.putText(frame, "center of frame", (cntFrameX - 10, cntFrameY - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    delx = cntFrameX-cX
    dely = cntFrameY-cY
    X.append(delx)
    Y.append(dely)
    #Need to find actual value of angle of view of camera
    delfi = -math.atan(math.tan(1.134)*delx/320)*180/3.14
    deltheta = -math.atan(math.tan(1.134)*dely/240)*180/3.14

    cv2.putText(frame,'Pitch :'+str.format('{0:.3f}', deltheta)+'Yaw :'+str.format('{0:.3f}', delfi),(wframe-240,80),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
    theta.append(deltheta)
    fi.append(delfi)
    timenow = time.time()
    timeval = timenow-starttime
    timeframe = timenow-previoustime
    previoustime=timenow
    timestamp.append(timeval)
    #print("Delx: ",delx,"Dely: ",dely,"Deltheta: ",deltheta)
    #print("Dely: ",dely)
    #print("Deltheta: ",deltheta)
    #print("Delfi: ",delfi)
    #print("Time: ",timeval)
    print("TimeFrame :",timeframe)
    #csv file store output
    with open('orientation_data.csv', 'a') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(
            [delfi,deltheta,timenow])

    #cv2.imshow('hsv', hsv)
    cv2.imshow('frame', frame)
    #out.write(frame)
    #cv2.imshow('mask', mask)
    #cv2.imshow('morphological transformation',morphed)
    #cv2.imshow('res',res)
    #cv2.imshow('threshold',thrshed)
    k = cv2.waitKey(30) & 0xFF
    if k == ord('q'):
        fig, axs= plt.subplots(4)
        fig.suptitle('Change of X,Y,theta,phy wrt time')
        #axs.plot(timestamp,delX)
        axs[0].plot(timestamp,X)
        axs[1].plot(timestamp,Y)
        axs[2].plot(timestamp,theta)
        axs[3].plot(timestamp,fi)
        axs[0].set(xlabel = 'time',ylabel = 'delX')
        axs[1].set(xlabel = 'time',ylabel = 'delY')
        axs[2].set(xlabel = 'time',ylabel = 'deltheta')
        axs[3].set(xlabel = 'time',ylabel = 'delfy')
        plt.show()
        break
#out.release()
cap.release()
cv2.destroyAllWindows()
