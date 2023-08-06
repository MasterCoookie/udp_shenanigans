import time
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import QSize

class UdpClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(1.0)
        self.message = 2
        self.addr = ("127.0.0.1", 12000)

    def send_message(self):
        start = time.time()

        self.client_socket.sendto(self.message.to_bytes(2, 'big'), self.addr)
        try:
            data, server = self.client_socket.recvfrom(1024)
            data = int.from_bytes(data, 'big')
            end = time.time()
            elapsed = end - start
            print(f'Recieved response:{data} in {elapsed}s')
        except socket.timeout:
            print('REQUEST TIMED OUT')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle('UDP Client')
        self.setMinimumSize(QSize(480, 80))
        
        self.button = QPushButton('Send', self)
        self.button.move(190, 20)


app = QApplication([])

window = MainWindow()
window.show()

app.exec_()
