import time,psutil,matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axis3d,Axes3D
import random

x1=[]
y1=[]
z1 = []
x2=[]
y2=[]
z2=[]
i=0
while True:
   fig = plt.figure()
   ax = fig.add_subplot(111, projection='3d')
   #ax = Axes3D(fig)

   x1.append(random.randint(23,35))
   y1.append(random.randint(56,77))
   z1.append(random.randint(0,10))
   x2.append(random.randint(23, 35))
   y2.append(random.randint(56, 77))
   z2.append(random.randint(0, 10))
   label = i
   ax.scatter(x1,y1,z1)
   ax.scatter(x2,y2,z2)
   plt.plot(x1,y1,z1,'g--')
   plt.plot(x2,y2,z2,'b--')
   xline1 = [x1[-1],30]
   yline1 = [y1[-1],65]
   zline1 = [z1[-1],0]
   print(x1[-1],y1[-1],z1[-1])
   plt.plot(xline1,yline1,zline1,'ro-')
   xline2 = [x2[-1], 30]
   yline2 = [y2[-1], 65]
   zline2 = [z2[-1], 0]
   print(x2[-1],y2[-1],z2[-1])
   plt.plot(xline2, yline2, zline2, 'yo-')

   ax.set_xlabel("x")
   ax.set_ylabel("y")
   ax.set_zlabel("z")
   fig.show()
   plt.show()
   time.sleep(0.1)
   plt.close()
   i+=1


