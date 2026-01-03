import socket

print("Socket Quiz Client")

HOST = '127.0.0.1'
PORT = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    data = client.recv(1024)
    if not data:
        break
    print(data.decode(), end="")

    msg = input()
    client.send(msg.encode())

client.close()
