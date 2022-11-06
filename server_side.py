from PyQt5.QtWidgets import QGridLayout, QPushButton, QLineEdit, QTextEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication
from PyQt5.QtCore import QRunnable, pyqtSlot, QThreadPool, pyqtSignal
from PyQt5.QtCore import QObject
import sys
import socket
import datetime


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread
    execute function with given arguments
    and signals
    '''
    def __init__(self, arg, f):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.arg = arg
        self.f = f
        self.signals = WorkerSignals()
        # Add the callback to our kwargs

    @pyqtSlot()
    def run(self):
        '''
        Your code goes in this function
        '''
        print("Thread start")
        self.f(self.signals, self.arg)
        print("Thread stop")


def fun_to_run(signals, arg):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            port = int(arg.port_num.text())
            s.bind(('localhost', port))
            print('Listening...')
            s.listen(100)
            s.settimeout(0.2 * 1000)
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    try:
                        data = conn.recv(1024)
                    except socket.error as e:
                        print("Error: %s" % e)
                        break
                    if data:
                        print(data.decode('utf-8'))
                        now = datetime.datetime.now()
                        msg = now.strftime('%H:%M:%S  ')
                        msg = msg + data.decode('utf-8')
                    if not data:
                        break
            print("Thread complete")
            signals.result.emit(msg)
    except socket.error as e:
        print("Error: %s" % e)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.worker = None

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads"
              % self.threadpool.maxThreadCount())

        layout = QGridLayout()

        self.input_label = QLabel()
        self.input_label.setText("Port number: ")
        layout.addWidget(self.input_label, 0, 0)

        self.port_num = QLineEdit()
        self.port_num.setText("1")
        self.port_num.setMaximumWidth(40)
        layout.addWidget(self.port_num, 1, 0)

        self.start_button = QPushButton("Start server")
        self.start_button.pressed.connect(self.start)
        layout.addWidget(self.start_button, 0, 1)

        self.message_box = QTextEdit()
        self.message_box.setReadOnly(True)
        self.message_box.setDisabled(True)
        layout.addWidget(self.message_box, 2, 1)

        self.status = QLineEdit()
        self.status.setReadOnly(True)
        self.status.setDisabled(True)
        layout.addWidget(self.status, 1, 1)

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)
        self.setWindowTitle("Server side")
        self.show()

    def start(self):
        self.status.setText("Running")
        self.worker = Worker(self, fun_to_run)
        self.worker.signals.result.connect(self.update_text)
        self.threadpool.start(self.worker)
        self.start_button.setDisabled(True)

    def update_text(self, new):
        print('in update')
        self.message_box.append(new)
        self.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
