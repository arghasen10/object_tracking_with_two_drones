from __future__ import print_function
import cv2
import numpy as np
import time
import math
import socket
#import csv
from dronekit import connect, VehicleMode
import datetime,csv

#Set up option parsing to get connection string
import argparse  
parser = argparse.ArgumentParser(description='Print out vehicle state information. Connects to SITL on local PC by default.')
parser.add_argument('--connect', 
                   help="vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None


#Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()

host = '192.168.1.104'
port = 2004
BUFFER_SIZE = 2000 
tcpClientB = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpClientB.connect((host, port))
# Connect to the Vehicle. 
#   Set `wait_ready=True` to ensure default attributes are populated before `connect()` returns.
print("\nConnecting to vehicle on: %s" % connection_string)
vehicle = connect(connection_string, wait_ready=True)

vehicle.wait_ready('autopilot_version')


# Get all vehicle attributes (state)
print("\nGet all vehicle attribute values:")
print(" Autopilot Firmware version: %s" % vehicle.version)
print("   Major version number: %s" % vehicle.version.major)
print("   Minor version number: %s" % vehicle.version.minor)
print("   Patch version number: %s" % vehicle.version.patch)
print("   Release type: %s" % vehicle.version.release_type())
print("   Release version: %s" % vehicle.version.release_version())
print("   Stable release?: %s" % vehicle.version.is_stable())
print(" Autopilot capabilities")

#Create a file to store data
currenttime = datetime.datetime.now()
currenttime = str(currenttime)
currenttime_array = currenttime.split(' ')
date = currenttime_array[0]
Time = currenttime_array[1][:8]
mode = Time.split(':')
s1 = int(mode[0])
s2 = int(mode[1])
s3 = int(mode[2])
s1 = s1*10000+s2*100+s3
Time = s1
mode = date.split('-')
s1 = int(mode[0])
s2 = int(mode[1])
s3 = int(mode[2])
s1 = s1*10000+s2*100+s3
date = s1
filename = 'output'+str(Time)+'_'+str(date)
filename+='.csv'

print('Name of File created :',filename)
header_name = ["Date","Time","Lat","Lng","Alt","Yawd","Pitchd","Yawo","Pitch0","Timestamp"]
with open(filename, 'w+') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(header_name)


cap = cv2.VideoCapture(0)
largest_area = 0
theta =[0]
fi = [0]
timestamp = [0]
X = [0]
Y = [0]
objX, objY = 0, 0

starttime = time.time()
previoustime = starttime
print(cap)
ret,frame = cap.read()
print(ret)
hframe,wframe = frame.shape[0],frame.shape[1]
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_take1.avi',fourcc,32.0,(wframe,hframe))
while True:
    ret, frame = cap.read()
    if not ret:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        continue
    currenttime = datetime.datetime.now()
    currenttime = str(currenttime)
    currenttime_array = currenttime.split(' ')
    date = currenttime_array[0]
    Time = currenttime_array[1][:8]
    hframe,wframe = frame.shape[0],frame.shape[1]
    cntFrameX,cntFrameY = wframe//2,hframe//2
    lower_hsv = np.array([86,122,117])
    upper_hsv = np.array([176,215,255])
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    kernel = np.ones((5,5), np.int)
    dilated = cv2.dilate(mask, kernel)
    morphed = cv2.morphologyEx(dilated,cv2.MORPH_OPEN,kernel)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    ret, thrshed = cv2.threshold(cv2.cvtColor(res, cv2.COLOR_BGR2GRAY), 3, 255, cv2.THRESH_BINARY)
    _,cnts,_ = cv2.findContours(morphed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) != 0:
        cnt = max(cnts, key=cv2.contourArea)

        M = cv2.moments(cnt)

        if M["m00"] != 0:
            objX = int(M["m10"] / M["m00"])
            objY = int(M["m01"] / M["m00"])
        else:
            objX,objY = 0, 0
        cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
        cv2.circle(frame, (objX, objY), 7, (255, 255, 255), -1)
        cv2.putText(frame, "center of Obj", (objX - 20, objY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        
    cv2.circle(frame,(cntFrameX,cntFrameY),5,(255,255,255),-1)
    cv2.putText(frame, "center of frame", (cntFrameX - 10, cntFrameY - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    delx = cntFrameX-objX
    dely = cntFrameY-objY
    delfi = -math.atan(math.tan(1.134)*delx/320)*180/3.14
    deltheta = -math.atan(math.tan(1.134)*dely/240)*180/3.14
    gloc = str(vehicle.location.global_frame)
    rloc = str(vehicle.location.global_relative_frame)
    gloc = gloc.split(',')
    rloc = rloc.split(',')
    glat = gloc[0][19:]
    glng = gloc[1][4:]
    galt = gloc[2][4:]
    rlat = rloc[0][27:]
    rlng = rloc[1][4:]
    ralt = rloc[2][4:]
    attitude = str(vehicle.attitude)
    pitch,yaw,roll = attitude.split(',')
    pitch = pitch.split(':')[1][6:]
    yaw = yaw[4:]
    roll = roll[5:]
    print("Glat: ",glat,"Glng: ",glng,"Galt: ",galt)
    #print("Rlat: ",rlat,"Rlng: ",rlng,"Ralt: ",ralt)
    print("Pitch: ",pitch,"Yaw: ",yaw,"Roll: ",roll)
    timestampd = time.time()
    data_list = [date,Time,glat,glng,galt,yaw,pitch,delfi,deltheta,timestampd]
    
    with open(filename, 'a') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(data_list)
    
    MESSAGE = "Lat:"+str(glat)+",Lng:"+str(glng)+",Alt:"+str(galt)+",Pitch:"+str(pitch)+",Yaw:"+str(yaw)+",yawo:"+str(delfi)+",Pitcho:"+str(deltheta)
    tcpClientB.send(MESSAGE.encode())  
    cv2.putText(frame,'Pitch :'+str.format('{0:.3f}', deltheta)+'Yaw :'+str.format('{0:.3f}', delfi),(wframe-240,80),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
    theta.append(deltheta)
    fi.append(delfi)
    timenow = time.time()
    timeval = timenow-starttime
    timeframe = timenow-previoustime
    previoustime=timenow
    timestamp.append(timeval)
    print("TimeFrame :",timeframe)
    cv2.imshow('frame', frame)
    out.write(frame)                                #Save video for later purpose
    
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
out.release()
cap.release()
cv2.destroyAllWindows()

