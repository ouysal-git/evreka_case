import socket  # Import socket module
import threading
from struct import pack
from time import sleep

import logging

HOST = "127.0.0.1"
PORT = 4001
logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().setLevel(logging.DEBUG)


def on_new_client(clientsocket, addr):
    logging.info(f'Client connected: {addr}')
    while True:
        lat = 34.2
        long = 42.1
        data_to_send = pack("@ff", lat, long)
        try:
            clientsocket.send(data_to_send)
        except Exception as e:
            logging.warning(f'Exception on Client :{addr} ex:{e}')
            break
        sleep(5)
    clientsocket.close()
    logging.info(f'Client disconnected: {addr}')


s = socket.socket()  # Create a socket object
logging.error(f'Server started on: {HOST}:{PORT}')

s.bind((HOST, PORT))
s.listen(5)
# Now wait for client connection.
while True:
    c, addr = s.accept()  # Establish connection with client.
    threading.Thread(target=on_new_client, args=(c, addr)).start()
s.close()
logger.error(f'Server closed')
