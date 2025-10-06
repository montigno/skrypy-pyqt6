import GPUtil
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QPlainTextEdit, \
                            QVBoxLayout, QDialog, QHBoxLayout, QPushButton, \
                            QCheckBox, QTextEdit
from PyQt6.QtGui import QFont

import os
import psutil
import signal
import sys


class controlSys(QDialog):
    def __init__(self, text, proid, parent=None):
        super(controlSys, self).__init__(parent)

        self.proid = int(proid)

        # self.setWindowFlags(Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowTitleHint | Qt.WindowType.CustomizeWindowHint)
        self.txt = '\n'

        self.top = 0
        self.left = 0
        self.width = 400
        self.height = 400
        self.setWindowTitle(text)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMinimumHeight(self.height)
        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout()
        self.plainText = QPlainTextEdit()
        self.plainText.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.plainText.setReadOnly(True)
        self.plainText.setMaximumHeight(200)
        # self.plainText.setStyleSheet("background-color: #303030; color: #ffffff")
        self.plainText.appendPlainText(text)
        self.plainText.appendPlainText('ID main process :' + proid)
        button_thread = QPushButton('processes')
        button_thread.clicked.connect(self.buttonProcess)
        button_stop = QPushButton('force stop')
        button_stop.clicked.connect(self.buttonStop)
        button_stop_restart = QPushButton('force stop and restart')
        button_stop_restart.clicked.connect(self.buttonStopRestart)
        vbox.addWidget(self.plainText)
        hbox.addWidget(button_thread)
        hbox.addWidget(button_stop)
        hbox.addWidget(button_stop_restart)
        vbox.addLayout(hbox)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Monospace"))
        self.console.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.console.setStyleSheet("background-color: #303030; color: #ffffff")
        vbox.addWidget(self.console)

        # self.box = QCheckBox("Keep above",self)
        # self.box.stateChanged.connect(self.clickBox)
        # vbox.addWidget(self.box)

        self.setLayout(vbox)

        self.monitor = Monitor()
        self.monitor.cpuPercent.connect(self.setValueCPU)
        self.monitor.start()

    def buttonProcess(self, text):
        with open(os.path.join(os.path.expanduser('~'), '.skrypy', 'list_process.tmp'), 'r') as f:
            list_proc = f.read()
            self.plainText.appendPlainText(list_proc)
            self.plainText.setUndoRedoEnabled(False)

    def buttonStop(self):
        try:
            os.kill(self.proid, signal.SIGKILL)
        except Exception as err:
            pass
        self.close()

    def buttonStopRestart(self):
        os.kill(self.proid, signal.SIGKILL)
        self.close()

        fp = open(os.path.join(os.path.expanduser('~'), '.bashrc'))
        txt = fp.read()
        try:
            txt = txt[txt.index('cmd_sk'):]
            self.txt = txt[txt.index('source'): txt.index('\n')-1]
            os.system(self.txt)
        except Exception as err:
            print('restart error : ', err)
            self.close()

    def clickBox(self, state):
        if state == Qt.CheckState.Checked:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
        self.show()

    def setValueCPU(self, valuesCPU, list_gpu):
        tmp = ''
        bar_len = 18
        total = 100

        val = valuesCPU[0]
        filled_len = int(bar_len * val / float(total))
        bar = ('=' * filled_len) + (' ' * (bar_len - filled_len))
        total_ram = int(psutil.virtual_memory().total / (1024.**3))
        tmp += 'RAM({}Go) :{:>4d}% : {}|\n'.format(total_ram, val, bar)

        val = valuesCPU[1]
        filled_len = int(bar_len * val / float(total))
        bar = ('=' * filled_len) + (' ' * (bar_len - filled_len))
        total_swap = int(psutil.swap_memory().total / (1024.**3))
        tmp += 'SWAP({}Go):{:>4d}% : {}|\n\n'.format(total_swap, val, bar)

        for i, val in enumerate(valuesCPU[2:]):
            filled_len = int(bar_len * val / float(total))
            bar = ('=' * filled_len) + (' ' * (bar_len - filled_len))
            tmp += 'CPU{} : {: >4d}% : {}|\n'.format(i, val, bar)

        tmp += '\nGPUs:\n'
        for i, lst in enumerate(list_gpu):
            tmp += 'GPU[{}] : {}\n'.format(i, lst)

        self.console.setPlainText(tmp)

    def keyPressEvent(self, event):
        if event.key() != Qt.Key.Key_Escape:
            QDialog.keyPressEvent(self, event)
        else:
            pass


class Monitor(QThread):
    cpuPercent = pyqtSignal(list, list)

    def run(self):
        self._stopped = False
        while not self._stopped:
            per_cpu = psutil.cpu_percent(interval=None, percpu=True)
            per_gpu = []
            try:
                per_gpu = GPUtil.getGPUs()
            except Exception as err:
                pass
            value = []
            txt = []
            value.append(int(psutil.virtual_memory().percent))
            value.append(int(psutil.swap_memory().percent))
            for idx, usage in enumerate(per_cpu):
                value.append(int(psutil.cpu_percent(interval=0.2)))
            for idx, usage in enumerate(per_gpu):
                txt.append(float(usage.load))
            self.cpuPercent.emit(value, txt)

    def stop(self):
        self._stopped = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dispInfo = controlSys(*sys.argv[1:])
    dispInfo.show()
    sys.exit(app.exec())
