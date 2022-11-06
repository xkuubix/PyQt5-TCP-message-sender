from PyQt5.QtWidgets import QGridLayout, QPushButton, QLineEdit, QTextEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication
import sys
import socket


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.is_running = False

        layout = QGridLayout()

        # LABEL
        self.input_label = QLabel()
        self.input_label.setText("Port number: ")
        layout.addWidget(self.input_label, 0, 0)

        # IP IN LABEL
        self.ip_label = QLabel()
        self.ip_label.setText("Send message to [IP]: ")
        layout.addWidget(self.ip_label, 0, 1)

        # IP IN LABEL
        self.ip_input = QLineEdit()
        self.ip_input.setText("127.0.0.1")
        layout.addWidget(self.ip_input, 1, 1)

        # PORT NUM IN
        self.port_num = QLineEdit()
        self.port_num.setText("1")
        self.port_num.setMaximumWidth(40)
        layout.addWidget(self.port_num, 1, 0)

        # START BUTTON
        self.start_button = QPushButton("Send")
        self.start_button.pressed.connect(self.send)
        layout.addWidget(self.start_button, 3, 1)

        # MESSAGE BOX
        self.message_box = QTextEdit()
        self.message_box.setReadOnly(False)
        self.message_box.setDisabled(False)
        layout.addWidget(self.message_box, 2, 1)

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)
        self.setWindowTitle("Client side")
        self.show()

    def send(self):
        """
        SEND BUTTON LINK
        """
        print(self.message_box.toPlainText())
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            ip = self.ip_input.text()
            port = int(self.port_num.text())
            s.connect((ip, port))
            s.sendall(bytes(self.message_box.toPlainText(), 'utf-8'))
        self.message_box.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
