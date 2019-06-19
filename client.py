import socket
host = '127.0.0.1'
port = 8080
msg = "2"
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((host,port))

    while True:
        
        client.send(msg.encode())

print("Added")

