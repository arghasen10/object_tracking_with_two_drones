import socket
from threading import *
import time

host = '127.0.0.1'
port = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen(2)
print('waiting for first client')
conn1, addr1 = server.accept()
print('Connected by client: %s' % repr(addr1))
print('waiting for second client')
conn2, addr2 = server.accept()
print('Connected by client: %s' % repr(addr1))


class Receive1(Thread):
    def run(self):
        while True:
            data = conn1.recv(1024)
            if not data:
                break
            print('Received from client1: %s' % data.decode())
            time.sleep(0.2)


class Receive2(Thread):
    def run(self):
        while True:
            data = conn2.recv(1024)
            if not data:
                break
            print('Received from client2: %s' % data.decode())
            time.sleep(0.2)



R1 = Receive1()
R2 = Receive2()

R1.start()
time.sleep(0.2)
R2.start()

        
