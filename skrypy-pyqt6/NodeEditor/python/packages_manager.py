from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QTextCursor
from PyQt6.QtWidgets import QDialog, QPlainTextEdit, QHBoxLayout, QPushButton, \
    QLineEdit, QVBoxLayout, QTextEdit, QCompleter
from subprocess import Popen, PIPE, STDOUT, DEVNULL


class manage_pck(QDialog):

    def __init__(self, parent=None):

        super(manage_pck, self).__init__(parent)
        self.setMinimumWidth(800)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        self.histories = []

        a = QTextEdit()
        a.setMinimumHeight(100)
        a.setReadOnly(True)
        a.insertHtml('-- to list the packages already installed in your virtual environment, type : <b>pip3 list</b><br> ')
        a.insertHtml('-- to install your package, type : <b>pip3 install <i>package_name</i></b> (ex: pip3 install numpy)<br>')
        a.insertHtml('-- to install your package with version, type : <b>pip3 install <i>package_name==version</i></b> (ex: pip3 install numpy==1.21.0)<br>')
        a.insertHtml('-- to uninstall a package, type: <b>pip3 uninstall <i>package_name</i></b> (ex : pip3 uninstall numpy) <br>')
        a.insertHtml('-- to update a package, type: <b>pip3 install <i>package_name</i> --upgrade</b> (ex : pip3 install numpy --upgrade) <br>')

        self.b = QPlainTextEdit()
        fixed_font = QFont("monospace")
        fixed_font.setStyleHint(QFont.StyleHint.TypeWriter)
        self.b.setStyleSheet("""QPlainTextEdit {background-color: #333;
                             color: #00FF00;
                             font-family: Courier;}""")
        self.b.setReadOnly(True)
        self.b.setMinimumSize(600, 500)
        self.b.setFont(fixed_font)
        self.b.resize(500, 800)
        self.b.move(10, 20)

        vlayout = QVBoxLayout(self)

        hlayout = QHBoxLayout()

        self.cmd = QLineEdit('pip3 install package_name')
        self.cmd.setMinimumWidth(400)

        self.button_run = QPushButton('run', self)
        self.button_run.setMaximumSize(200, 30)
        self.button_run.clicked.connect(self.install_package)

        hlayout.addWidget(self.button_run)
        hlayout.addWidget(self.cmd)

        vlayout.addWidget(a)
        vlayout.addLayout(hlayout)
        vlayout.addSpacing(2)
        vlayout.addWidget(self.b)

        self.setLayout(vlayout)

    def install_package(self):
        self.cmd.setEnabled(False)
        self.button_run.setEnabled(False)
        command = self.cmd.text()
        if 'uninstall' in command:
            if '-y' not in command:
                command = "pip3 uninstall -y " + command[command.find("uninstall") + 10:]
        self.b.clear()
        self.b.insertPlainText(command + "\n")
        self.b.update()

        self.setCursor(Qt.CursorShape.WaitCursor)

        # p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=STDOUT, shell=True, bufsize=1)
        p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=STDOUT, shell=True)

        while p.stdout is not None:
            line = p.stdout.readline()
            if not line:
                break
            txt = line.decode("utf-8")
            self.b.insertPlainText(txt)
            self.b.verticalScrollBar().setValue(self.b.verticalScrollBar().maximum())
            self.b.repaint()
            if self.b.blockCount() > 5000:
                break
            if not line:
                p.stdout.flush()
                break

        self.unsetCursor()

        if command not in self.histories:
            self.histories.append(command)
            completer = QCompleter(self.histories)
            self.cmd.setCompleter(completer)
        self.cmd.setEnabled(True)
        self.button_run.setEnabled(True)
