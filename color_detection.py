import cv2
import numpy as np

hmin=0
hmax=0
smin=0
smax=0
vmin=0
vmax=0
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
    vmax= x

lower_green = np.array([hmin,smin,vmin])
upper_green = np.array([hmax,smax,vmax])
cv2.namedWindow("frame1",50)
cv2.createTrackbar("hmin","frame1",50,255,hminc)
cv2.createTrackbar("hmax","frame1",50,255,hmaxc)
cv2.createTrackbar("smin","frame1",50,255,sminc)
cv2.createTrackbar("smax","frame1",50,255,smaxc)
cv2.createTrackbar("vmin","frame1",50,255,vminc)
cv2.createTrackbar("vmax","frame1",50,255,vmaxc)
cap = cv2.VideoCapture('green.mp4')
largest_area = 0
cX,cY = 0,0
while True:
    ret, frame = cap.read()
    if not ret:
        cap = cv2.VideoCapture('green.mp4')
        ret, frame = cap.read()
        continue

    hmin = cv2.getTrackbarPos("hmin","frame1")
    hmax = cv2.getTrackbarPos("hmax","frame1")
    smin = cv2.getTrackbarPos("smin","frame1")
    smax = cv2.getTrackbarPos("smax","frame1")
    vmin = cv2.getTrackbarPos("vmin","frame1")
    vmax = cv2.getTrackbarPos("vmax","frame1")
    lower_green = np.array([hmin, smin, vmin])
    upper_green = np.array([hmax, smax, vmax])

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
    '''
    for cnt in cnts:
        #approx = cv2.approxPolyDP(cnt,0.005*cv2.arcLength(cnt,True),True)
        cv2.drawContours(frame,(cnt),-1,(255,0,0),5)
        #area = cv2.contourArea(cnt,None)
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:

            cX,cY=0,0

        # draw the contour and center of the shape on the image
        cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
        cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(frame, "center", (cX - 20, cY - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        #cv2.putText(frame,"Area = "+str(area),)
        '''
    frameY, frameX = frame.shape[0], frame.shape[1]
    cntFrameX, cntFrameY = int(frameX // 2), int(frameY // 2)
    print(cntFrameX, cntFrameY)
    cv2.circle(frame, (cntFrameX, cntFrameY), 6, (0, 255, 0), -1)
    cv2.putText(frame, "Frame center", (cntFrameX, cntFrameY),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imshow('thresh', thrshed)
    cv2.imshow('res', res)
    cv2.imshow('hsv', hsv)
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)

    k = cv2.waitKey(30) & 0xFF
    if k == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
