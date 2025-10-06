from PyQt6.QtCore import QThread, pyqtSlot, Qt, QObject
from PyQt6.QtWidgets import QProgressBar, QVBoxLayout, QHBoxLayout, QPushButton, \
    QApplication, QWidget, QLabel
import sys
import time


class StartDiagram(QThread):

    # def __init__(self, name, args, wind):
    def __init__(self, name):
        super(StartDiagram, self).__init__()
        self.name = name
        self.window_progressBar()

    def window_progressBar(self):
        self.winBar = QWidget()
        self.winBar.setWindowTitle('test')
        self.winBar.setStyleSheet("background-color:white;")
        self.winBar.resize(400, 80)
        self.winBar.setWindowFlags(Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.label = QLabel()
        self.pbar = QProgressBar(self.winBar)
        self.pbar.setGeometry(-100, 0, 350, 30)
        self.pbar.setValue(0)
        self.button_stop = QPushButton('Stop')
        self.button_stop.clicked.connect(self.buttonStop)
        # self.args += (self.button_stop,)
        # self.button_stop.clicked.connect(self.runner.kill)
        vbx = QVBoxLayout()
        hbx = QHBoxLayout()
        hbx.addWidget(self.pbar)
        hbx.addWidget(self.button_stop)
        vbx.addWidget(self.label)
        vbx.addLayout(hbx)
        self.winBar.setLayout(vbx)
        self.winBar.move(500, 500)
        self.winBar.show()
        time.sleep(0.1)

    def buttonStop(self):
        print('stopped !')
        self.terminate()

    def update_winBar(self):
        print('update win bar !!')


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     dispInfo = StartDiagram(sys.argv[1])
#     sys.exit(app.exec())
