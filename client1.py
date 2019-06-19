import socket
from time import sleep
s = socket.socket()
host = socket.gethostname()
port = 8000
s.connect((host,port))
msg = "Hello world from client 2\n"
msg = msg.encode()
while 1:
    s.send(msg)
    print("Messege sent to server ")
    #sleep(1)
