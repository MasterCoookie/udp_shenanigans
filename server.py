import socket
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 12000))

while True:
    data, address = server_socket.recvfrom(1024)
    data = int.from_bytes(data, 'big')
    data *= 2
    time.sleep(1)
    server_socket.sendto(data.to_bytes(2, 'big'), address)
    