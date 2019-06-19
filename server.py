import socket
s = socket.socket()
#host = socket.gethostname()
host = '192.168.43.39'
port = 8000
s.bind((host,port))
s.listen(1)
print("Waiting for 2 connections")
conn,addr = s.accept()
print("Client 1 is connected")
conn1,addr1 = s.accept()
print("Client2 is connected")
while 1:
    recv_msg = conn.recv(1024)
    print("Message received: ",recv_msg.decode())
    recv_msg = conn1.recv(1024)
    print("Messege Received: ",recv_msg.decode())

