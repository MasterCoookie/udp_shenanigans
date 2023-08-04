import time
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1.0)
message = 2
addr = ("127.0.0.1", 12000)

start = time.time()
client_socket.sendto(message.to_bytes(2, 'big'), addr)
try:
    data, server = client_socket.recvfrom(1024)
    data = int.from_bytes(data, 'big')
    end = time.time()
    elapsed = end - start
    print(f'Recieved response:{data} in {elapsed}s')
except socket.timeout:
    print('REQUEST TIMED OUT')