import time
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import QSize

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle('UDP Client')
        self.setMinimumSize(QSize(480, 80))
        
        self.button = QPushButton('Send', self)
        self.button.move(190, 20)


client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1.0)
message = 2
addr = ("127.0.0.1", 12000)

app = QApplication([])

window = MainWindow()
window.show()

app.exec_()

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