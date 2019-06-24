import socket
from time import sleep
s = socket.socket()
host = socket.gethostname()
port = 8000
s.connect((host,port))
#msg = "Hello world from client 1\n"
glat=21.063546748
glng=43.769998453
galt=5.094645
pitch=0.9756352
yaw = 0.67689585
delfi = 20.979685
deltheta = 9.0979853
msg = "Lat:"+str(glat)+",Lng:"+str(glng)+",Alt:"+str(galt)+",Pitch:"+str(pitch)+",Yaw:"+str(yaw)+",yawo:"+str(delfi)+",Pitcho:"+str(deltheta)+",id:1\n"
msg = msg.encode()
while 1:
    s.send(msg)
    sleep(0.3)
