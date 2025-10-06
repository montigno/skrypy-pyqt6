from PyQt6.Qt import pyqtSlot, QProcess, QTextCodec
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont, QTextCursor
from PyQt6.QtWidgets import QDialog, QPlainTextEdit, QHBoxLayout, QPushButton, \
    QGridLayout, QTextEdit, QLineEdit, QVBoxLayout


class manage_pck(QDialog):

    def __init__(self, parent=None):

        super(manage_pck, self).__init__(parent)
        self.setMinimumWidth(800)

        self.b = Console()
        self.reader = ProcessOutputReader()
        self.reader.produce_output.connect(self.b.append_output)

        vlayout = QVBoxLayout(self)

        self.list_package()

        hlayout = QHBoxLayout()

        self.cmd = QLineEdit('pip3 install package')
        self.cmd.setMinimumWidth(400)

        button = QPushButton('run')
        button.setMaximumSize(200, 30)
        button.clicked.connect(self.install_package)

        hlayout.addWidget(self.cmd)
        hlayout.addWidget(button)

        vlayout.addLayout(hlayout)
        vlayout.addSpacing(2)
        vlayout.addWidget(self.b)

        self.setLayout(vlayout)

    def list_package(self):
        command = 'pip3 list'
        self.reader.start(command)

    def install_package(self):
        command = self.cmd.text()
        self.b.clear()
        self.reader.terminate()
        self.reader.start('echo', [command])
        self.reader.waitForFinished(1000)
        self.reader.kill()
        self.reader.start(command)
        self.reader.waitForFinished(-1)
        self.reader.kill()
        self.list_package()


class Console(QPlainTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        fixed_font = QFont("monospace")
        fixed_font.setStyleHint(QFont.StyleHint.TypeWriter)

        self.setReadOnly(True)
        self.setMaximumBlockCount(10000)  # limit console to 10000 lines
        self.setStyleSheet(
                        """QPlainTextEdit {background-color: #333;
                           color: #00FF00;
                           font-family: Courier;}""")
        self.setMinimumSize(600, 800)
        self.setFont(fixed_font)
        self.resize(500, 800)
        self.move(10, 20)
        # self.moveCursor(QTextCursor.MoveOperation.Start)

        self._cursor_output = self.textCursor()

    @pyqtSlot(str)
    def append_output(self, text):
        self._cursor_output.insertText(text)
        self.scroll_to_last_line()

    def scroll_to_last_line(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.movePosition(QTextCursor.MoveOperation.Up if cursor.atBlockStart() else
                            QTextCursor.MoveOperation.StartOfLine)
        self.setTextCursor(cursor)


class ProcessOutputReader(QProcess):
    produce_output = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        codec = QTextCodec.codecForLocale()
        self._decoder_stdout = codec.makeDecoder()
        self.readyReadStandardOutput.connect(self._ready_read_standard_output)

    @pyqtSlot()
    def _ready_read_standard_output(self):
        raw_bytes = self.readAllStandardOutput()
        text = self._decoder_stdout.toUnicode(raw_bytes)
        self.produce_output.emit(text)
