from sympy import Point3D,Line3D,Segment3D
import math,numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axis3d

def parse(lat1,lon1,alt1,pitch1,yaw1,lat2,lon2,alt2,pitch2,yaw2):
    pt1 = [float(lat1),float(lon1),float(alt1)]
    pt2 = [float(lat2),float(lon2),float(alt2)]
    pitch1 = float(pitch1)
    yaw1 = float(pitch2)
    '''
    pitch1 = 100.47
    yaw1 = 56.31
    pt1 = [24,56,2]
    pt2 = [27,57,10]
    '''
    l1 = math.cos(math.radians(yaw1))*math.sin(math.radians(pitch1))
    l2 = math.sin(math.radians(yaw1))*math.sin(math.radians(pitch1))
    l3 = math.cos(math.radians(pitch1))
    '''
    dir1 = [l1,l2,l3]
    pitch2 = 139.1
    yaw2 = 67.45
    '''
    l11 = math.cos(math.radians(yaw2))*math.sin(math.radians(pitch2))
    l22 = math.sin(math.radians(yaw2))*math.sin(math.radians(pitch2))
    l33 = math.cos(math.radians(pitch2))

    b = np.array([pt2[0]-pt1[0],pt2[1]-pt1[1]])
    a = np.array([[l1,-l11],[l2,-l22]])
    kt = np.linalg.solve(a,b)
    print(kt)
    pt3 = []
    pt3.append(pt1[0]+kt[0]*l1)
    pt3.append(pt1[1]+kt[0]*l2)
    pt3.append(pt1[2]+kt[0]*l3)

    print(pt3)


    #Plotting in MatplotLib

    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    X1 = [pt1[0],pt3[0]]
    Y1 = [pt1[1],pt3[1]]
    Z1 = [pt1[2],pt3[2]]
    X2 = [pt2[0],pt3[0]]
    Y2 = [pt2[1],pt3[1]]
    Z2 = [pt2[2],pt3[2]]
    plt.plot(X1,Y1,Z1,'ro-')

    plt.plot(X2,Y2,Z2,'yo-')
    ax.text(pt1[0],pt1[1],pt1[2],"Drone1",color = 'red')
    ax.text(pt2[0],pt2[1],pt2[2],"Drone2",color = 'red')
    ax.text(pt3[0],pt3[1],pt3[2],"Object",color = 'red')
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    plt.show()