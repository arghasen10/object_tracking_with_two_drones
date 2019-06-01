from sympy import Point3D,Line3D,Segment3D
import math,numpy as np
pitch1 = 100.47
yaw1 = 56.31
pt1 = [24,56,2]
pt2 = [27,57,10]
l1 = math.cos(math.radians(yaw1))*math.sin(math.radians(pitch1))
l2 = math.sin(math.radians(yaw1))*math.sin(math.radians(pitch1))
l3 = math.cos(math.radians(pitch1))

dir1 = [l1,l2,l3]
pitch2 = 139.1
yaw2 = 67.45
l11 = math.cos(math.radians(yaw2))*math.sin(math.radians(pitch2))
l22 = math.sin(math.radians(yaw2))*math.sin(math.radians(pitch2))
l33 = math.cos(math.radians(pitch2))


dir2 = [l11,l22,l33]
print(dir1,dir2)
b = np.array([pt2[0]-pt1[0],pt2[1]-pt1[1]])
a = np.array([[l1,-l11],[l2,-l22]])
kt = np.linalg.solve(a,b)
print(kt)
print(pt1[0]+kt[0]*l1)
print(pt1[1]+kt[0]*l2)
print(pt1[2]+kt[0]*l3)


L1 = Line3D(Point3D(pt1),direction_ratio=dir1)
L2 = Line3D(Point3D(pt2),direction_ratio=dir2)

print(L1.intersection(L2))