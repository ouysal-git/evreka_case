import socket
from struct import unpack

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        data = s.recv(1024)
        lat, long = unpack("@ff", data)
        print(f"Received lat: {lat}, long: {long}")