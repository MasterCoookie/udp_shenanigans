import time
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QLineEdit, QWidget
from PyQt5.QtCore import QSize

class UdpClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(2.0)

    def send_message(self, _message, _addr):
        start = time.time()

        addr = (_addr, 12000)
        message = _message.to_bytes(2, 'big')

        self.client_socket.sendto(message, addr)
        try:
            data, server = self.client_socket.recvfrom(1024)
            data = int.from_bytes(data, 'big')
            end = time.time()
            elapsed = end - start
            return f'{data} in {elapsed}s'
        except socket.timeout:
            return 'REQUEST TIMED OUT'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.client = UdpClient()

        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle('UDP Client')
        self.setMinimumSize(QSize(480, 100))

        self.value_label = QLabel('Enter a number to send to the server', self)
        self.value_input = QLineEdit(self)

        self.address_label = QLabel('Enter the server address', self)
        self.address_input = QLineEdit(self)

        self.result_label = QLabel('Result: ', self)
        
        self.button = QPushButton('Send', self)
        self.button.clicked.connect(self.on_click)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.value_label)
        self.layout.addWidget(self.value_input)
        self.layout.addWidget(self.address_label)
        self.layout.addWidget(self.address_input)
        self.layout.addWidget(self.result_label)
        self.layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
    
    def on_click(self):
        value = int(self.value_input.text())
        address = self.address_input.text()
        result = self.client.send_message(value, address)
        self.result_label.setText(f'Result: {result}')



app = QApplication([])

window = MainWindow()
window.show()

app.exec_()
