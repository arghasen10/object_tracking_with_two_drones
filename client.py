import socket
from time import sleep
s = socket.socket()
host = socket.gethostname()
port = 8000
s.connect((host,port))
msg = "Hello world from client 1\n"
msg = msg.encode()
while 1:
    s.send(msg)
    sleep(0.3)
