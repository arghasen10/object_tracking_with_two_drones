import socket
from time import sleep
host = socket.gethostname()
port = 8000
msg = "2\n"
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((host,port))

    while True:
        sleep(0.3)
        client.send(msg.encode())
