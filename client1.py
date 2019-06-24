import socket
from time import sleep
host = socket.gethostname()
port = 8000
glat=22.7365897309
glng=42.7547812689
galt=3.624579
pitch=0.4895892
yaw = 0.51247561
delfi = 12.35578923
deltheta = 45.490732
msg = "Lat:"+str(glat)+",Lng:"+str(glng)+",Alt:"+str(galt)+",Pitch:"+str(pitch)+",Yaw:"+str(yaw)+",yawo:"+str(delfi)+",Pitcho:"+str(deltheta)+",id:2\n"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((host,port))

    while True:
        sleep(0.3)
        client.send(msg.encode())
