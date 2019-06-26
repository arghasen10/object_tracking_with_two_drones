from math import sin,cos,radians,atan2,sqrt,degrees
import numpy as np

from vpython import *

import socket, csv, datetime



class visualize():

    def __init__(self, x1, y1, z1, x2, y2, z2, tpx, tpy, tpz):
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        self.tpx = tpx
        self.tpy = tpy
        self.tpz = tpz

        screen = canvas(x=0, y=0, width=1325, height=750, center=vector(5, 0, 0), background=vector(0, 0, 0))
        screen.forward = vector(-1, 0, 0)
        screen.up = vector(0, 0, 1)

        axis_x = arrow(pos=vector(0, 0, 0), axis=vector(500, 0, 0), shaftwidth=5, color=color.red)
        axis_y = arrow(pos=vector(0, 0, 0), axis=vector(0, 500, 0), shaftwidth=5, color=color.green)
        axis_z = arrow(pos=vector(0, 0, 0), axis=vector(0, 0, 500), shaftwidth=5, color=color.blue)

        xy_plane = box(pos=vector(0, 0, 0), size=vector(1000, 1000, 2), color=vector(0.35, 0.35, 0.35))
        origin = sphere(pos=vector(0, 0, 0), radius=10, color=color.white)

        self.a1 = arrow(pos=vector(0, 0, 0), axis=vector(x1, y1, z1), shaftwidth=3, color=color.white)
        self.a2 = arrow(pos=vector(0, 0, 0), axis=vector(x2, y2, z2), shaftwidth=3, color=color.white)

        self.drone_1 = sphere(pos=vector(x1, y1, z1), radius=10, color=color.magenta)
        self.drone_2 = sphere(pos=vector(x2, y2, z2), radius=10, color=color.orange)

        self.skew1 = curve(pos=[(x1, y1, z1), (tpx, tpy, tpz)])
        self.skew2 = curve(pos=[(x2, y2, z2), (tpx, tpy, tpz)])

        self.trail1 = points(pos=[(x1, y1, z1)])
        self.trail2 = points(pos=[(x2, y2, z2)])
        self.trail3 = points(pos=[(tpx, tpy, tpz)])

    def update(self, x1: object, y1: object, z1: object, x2: object, y2: object, z2: object, tpx: object, tpy: object, tpz: object) -> object:
        self.a1.axis = vector(x1, y1, z1)
        self.a2.axis = vector(x2, y2, z2)

        self.drone_1.pos = vector(x1, y1, z1)
        self.drone_2.pos = vector(x2, y2, z2)

        self.skew1.visible = 0
        self.skew2.visible = 0
        self.skew1 = curve(pos=[(x1, y1, z1), (tpx, tpy, tpz)])
        self.skew2 = curve(pos=[(x2, y2, z2), (tpx, tpy, tpz)])

        self.trail1.append((x1, y1, z1))
        self.trail2.append((x2, y2, z2))
        self.trail3.append((tpx, tpy, tpz))


def triangulate(glatval, glngval, galtval, lat1val,lng1val,alt1val,yaw1val,pitch1val,lat2val,lng2val,alt2val,yaw2val,pitch2val,v):
    print("Called")
    yaw1val = degrees(yaw1val)
    pitch1val = degrees(pitch1val)
    yaw2val = degrees(yaw2val)
    pitch2val = degrees(pitch2val)
    x1, y1, z1, l1, m1, n1 = find_lenpara(glatval,glngval,galtval,lat1val,lng1val,alt1val,yaw1val,pitch1val)
    x2, y2, z2, l2, m2, n2 = find_lenpara(glatval,glngval,galtval,lat2val,lng2val,alt2val,yaw2val,pitch2val)

    #h1 = (l1 * l1) + (m1 * m1) + (n1 * n1)
    #h2 = (l2 * l2) + (m2 * m2) + (n2 * n2)
    h1 = 1
    h2 = 1
    k4 = ((-2*x1*n1*n1 - 2*x1*m1*m1 + 2*n1*l1*z1 + 2*m1*l1*y1)/h1) + ((-2*x2*n2*n2 - 2*x2*m2*m2 + 2*n2*l2*z2 + 2*m2*l2*y2)/h2)
    k5 = ((-2*y1*l1*l1 - 2*y1*n1*n1 + 2*n1*m1*z1 + 2*m1*l1*x1)/h1) + ((-2*y2*l2*l2 - 2*y2*n2*n2 + 2*n2*m2*z2 + 2*m2*l2*x2)/h2)
    k6 = ((-2*z1*m1*m1 - 2*z1*l1*l1 + 2*n1*m1*y1 + 2*n1*l1*x1)/h1) + ((-2*z2*m2*m2 - 2*z2*l2*l2 + 2*n2*m2*y2 + 2*n2*l2*x2)/h2)

    k7 = (2*m1*l1/h1) + (2*m2*l2/h2)
    k8 = (2*n1*l1/h1) + (2*n2*l2/h2)
    k9 = (2*n1*m1/h1) + (2*n2*m2/h2)

    k1 = (((n1*n1) + (m1*m1))/h1) + (((n2*n2) + (m2*m2))/h2)
    k2 = (((l1*l1) + (n1*n1))/h1) + (((n2*n2) + (l2*l2))/h2)
    k3 = (((m1*m1) + (l1*l1))/h1) + (((m2*m2) + (l2*l2))/h2)

    A = np.array([[2*k1,-k7,-k8],[-k7,2*k2,-k9],[-k8,-k9,2*k3]])
    B = np.array([-k4,-k5,-k6])
    A_inv = np.linalg.inv(A)
    P = A_inv.dot(B)
    #print([k1,k2,k3],[k4,k5,k6],[k7,k8,k9])
    #print('A: ',A)
    #print('B: ',B)
    #print('A_inv:',A_inv)
    #print('P: ',P)
    pX = P[0]
    pY = P[1]
    pZ = P[2]
    #v.update(x1,y1,z1,x2,y2,z2,pX,pY,pZ)
    v.update(x1,)
    print(pX,pY,pZ)
    plat,plng = getlatlng(pX,pY,glatval,glngval)
    print("Object Location: ",plat,plng,pZ)


def getlatlng(pX,pY,glatval,glngval):
    brng =
    return plat,plng


def find_lenpara(glat,glng,galt,lat,lng,alt,yaw,pitch):
    print("lenpara Called")
    x,y = find_dist(glat,glng,lat,lng)
    z = galt - alt
    sinp = sin(pitch)
    l = sinp*cos(yaw)
    m = sinp*sin(yaw)
    n = cos(pitch)

    return x,y,z,l,m,n


def find_dist(lat1,lng1,lat2,lng2):                   #Find distance between two lat,lng

    #print(geopy.distance.vincenty((lat1, lng1), (lat2, lng2)), "in KM found with geopy")

    # dlat,dlng method

    R = 6371
    dlat = lat2 - lat1
    dlat = radians(dlat)
    dlng = lng2 - lng1
    dlng = radians(dlng)
    a = sin(dlat / 2) * sin(dlat / 2) + cos(radians(lat1)) * cos(
        radians(lat2)) * sin(dlng / 2) * sin(dlng / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d = R * c
    print("Distance measured with dlatdlng is ", d)

    print("Finding X,Y: ")
    R = 6371
    dlat = lat2 - lat1
    dlat = radians(dlat)
    dlng = 0
    dlng = radians(dlng)
    a = sin(dlat / 2) * sin(dlat / 2) + cos(radians(lat1)) * cos(
        radians(lat2)) * sin(dlng / 2) * sin(dlng / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d1 = R * c
    print("Projection Distance is ", d1)

    x = d1
    y = sqrt(pow(d, 2) - pow(x, 2))

    return x, y


glat = input("Enter Ground Latitude  ")
glng = input("Enter Ground Longitude ")
galt = input("Enter Ground Altitude  ")
glat = float(glat)
glng = float(glng)
galt = float(galt)

s = socket.socket()

host = '192.168.1.101'
port = 8000


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(2)
print('waiting for first client')
conn1, addr1 = server.accept()
print('Connected by client: %s' % repr(addr1))
print('waiting for second client')
conn2, addr2 = server.accept()
print('Connected by client: %s' % repr(addr1))


def connrun():
    data = conn1.recv(1024)
    return data


def conn1run():
    data = conn2.recv(1024)
    return data


currenttime = datetime.datetime.now()
currenttime = str(currenttime)
currenttime_array = currenttime.split(' ')
date = currenttime_array[0]
time = currenttime_array[1][:8]
mode = time.split(':')
s1 = int(mode[0])
s2 = int(mode[1])
s3 = int(mode[2])
s1 = s1 * 10000 + s2 * 100 + s3
time = s1
mode = date.split('-')
s1 = int(mode[0])
s2 = int(mode[1])
s3 = int(mode[2])
s1 = s1 * 10000 + s2 * 100 + s3
date = s1
filename = 'output' + str(time) + '_' + str(date)
filename += '.csv'
print('Name of File created :', filename)
header_name = ["Date", "Time", "lat1", "lng1", "alt1", "pitchd1", "yawd1", "yawo1", "pitcho1", "lat2", "lng2", "alt2",
               "pitchd2", "yawd2", "yawo2", "pitcho2"]

with open(filename, 'w+') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(header_name)
flag=0
v = visualize(0, 0, 0, 0, 0, 0, 0, 0, 0)
while True:
    data1 = connrun()
    data2 = conn1run()
    data1 = data1.decode()
    data2 = data2.decode()
    data1 = data1.split('\n')
    data1 = data1[-2]
    data2 = data2.split('\n')
    data2 = data2[-2]
    data1 = data1.split(',')
    data2 = data2.split(',')
    currenttime = datetime.datetime.now()
    currenttime = str(currenttime)
    currenttime_array = currenttime.split(' ')
    date = currenttime_array[0]
    Time = currenttime_array[1][:8]
    if (len(data1) != 8):
        continue
    if (len(data2) != 8):
        continue
    if data1[-1].split(':')[1] == '1':
        lat1 = data1[0].split(':')[1]
        lng1 = data1[1].split(':')[1]
        alt1 = data1[2].split(':')[1]
        pitchd1 = data1[3].split(':')[1]
        yawd1 = data1[4].split(':')[1]
        yawo1 = data1[5].split(':')[1]
        pitcho1 = data1[6].split(':')[1]
        print(lat1, lng1, alt1, pitchd1, yawd1, yawo1, pitcho1)
        lat2 = data2[0].split(':')[1]
        lng2 = data2[1].split(':')[1]
        alt2 = data2[2].split(':')[1]
        pitchd2 = data2[3].split(':')[1]
        yawd2 = data2[4].split(':')[1]
        yawo2 = data2[5].split(':')[1]
        pitcho2 = data2[6].split(':')[1]
        print(lat2, lng2, alt2, pitchd2, yawd2, yawo2, pitcho2)
        data_list = [date, Time, lat1, lng1, alt1, pitchd1, yawd1, yawo1, pitcho1, lat2, lng2, alt2, pitchd2, yawd2,
                     yawo2, pitcho2]
        with open(filename, 'a') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(data_list)

    else:
        lat2 = data1[0].split(':')[1]
        lng2 = data1[1].split(':')[1]
        alt2 = data1[2].split(':')[1]
        pitchd2 = data1[3].split(':')[1]
        yawd2 = data1[4].split(':')[1]
        yawo2 = data1[5].split(':')[1]
        pitcho2 = data1[6].split(':')[1]
        lat1 = data2[0].split(':')[1]
        lng1 = data2[1].split(':')[1]
        alt1 = data2[2].split(':')[1]
        pitchd1 = data2[3].split(':')[1]
        yawd1 = data2[4].split(':')[1]
        yawo1 = data2[5].split(':')[1]
        pitcho1 = data2[6].split(':')[1]
        print(lat1, lng1, alt1, pitchd1, yawd1, yawo1, pitcho1)
        print(lat2, lng2, alt2, pitchd2, yawd2, yawo2, pitcho2)
        data_list = [date, Time, lat1, lng1, alt1, pitchd1, yawd1, yawo1, pitcho1, lat2, lng2, alt2, pitchd2, yawd2,
                     yawo2, pitcho2]
        with open(filename, 'a') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(data_list)
    data_list = data_list[2:]
    floatedlist = []
    lat1 = float(lat1)
    lng1 = float(lng1)
    alt1 = float(alt1)
    yawd1 = float(yawd1)
    pitchd1 = float(pitchd1)
    yawo1 = float(yawo1)
    pitcho1 = float(pitcho1)
    lat2 = float(lat2)
    lng2 = float(lng2)
    alt2 = float(alt2)
    yawd2 = float(yawd2)
    pitchd2 = float(pitchd2)
    yawo2 = float(yawo2)
    pitcho2 = float(pitcho2)

    yaw1 = yawd1+yawo1
    pitch1 = pitchd1+pitcho1
    yaw2 = yawo2+yawd2
    pitch2 = pitchd2+pitcho2
    print("Hi")
    if flag ==0:
        print("Inside flag = 0")
        flag=1

    triangulate(glat, glng, galt, lat1, lng1, alt1, yaw1, pitch1, lat2, lng2, alt2, yaw2, pitch2,v)


