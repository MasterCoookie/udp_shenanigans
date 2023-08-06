import time
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QLineEdit, QWidget
from PyQt5.QtCore import QSize, QObject, pyqtSignal, QThread

class UdpClient(QObject):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(2.0)
        self.results_queue = []

    def send_message(self):
        start = time.time()


        self.client_socket.sendto(self.message, self.addr)
        try:
            data, server = self.client_socket.recvfrom(1024)
            data = int.from_bytes(data, 'big')
            end = time.time()
            elapsed = end - start
            self.results_queue.append(f'{data} in {elapsed}s')
        except socket.timeout:
            self.results_queue.append('REQUEST TIMED OUT')
        self.finished.emit()

    def set_addr_msg(self, _addr, _message):
        self.addr = (_addr, 12000)
        self.message = _message.to_bytes(2, 'big')

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
        self.address_input.setText('127.0.0.1')

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

    def on_finished(self):
        print("dupa")
        self.button.setEnabled(True)
        result = self.client.results_queue.pop(0)
        self.result_label.setText(result)
    
    def on_click(self):
        self.button.setEnabled(False)
        
        value = int(self.value_input.text())
        address = self.address_input.text()

        self.client.set_addr_msg(address, value)

        self.thred = QThread()
        self.client.moveToThread(self.thred)

        self.thred.started.connect(self.client.send_message)
        self.thred.finished.connect(self.on_finished)
        self.thred.finished.connect(self.thred.deleteLater)

        self.client.finished.connect(self.thred.quit)

        self.thred.start()

        
        self.client.finished.connect(self.client.deleteLater)

    

if __name__ == '__main__':
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec_()
