import socket
s = socket.socket()

host = '192.168.43.39'
port = 8000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
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


while True:
    data1=connrun()
    data2 = conn1run()
    data1 = data1.decode()
    data2 = data2.decode()
    data1 = data1.split('\n')
    data1 = data1[-2]
    data2 = data2.split('\n')
    data2 = data2[-2]
    print(data1)
    print(data2)
