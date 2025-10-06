from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QDialogButtonBox, \
    QVBoxLayout


class log_pwd_dialog(QDialog):

    def __init__(self, parent=None):
        super(log_pwd_dialog, self).__init__(parent)
        self.dial()

    def dial(self):
        self.setWindowModality(True)
        self.setWindowFlags(Qt.WindowType.WindowContextHelpButtonHint)
        self.username = QLineEdit(self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        loginLayout = QFormLayout()
        loginLayout.addRow("Username", self.username)
        loginLayout.addRow("Password", self.password)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self._control)
        buttons.rejected.connect(self._reject)
        layout = QVBoxLayout(self)
        layout.addLayout(loginLayout)
        layout.addWidget(buttons)
        self.setLayout(layout)
        self.open()

        # set window title & stylesheet
        self.setWindowTitle('Login Box')
        # self.setStyleSheet((qdarkstyle.load_stylesheet_pyqt5()))
        # ###lock resize
        self.setSizeGripEnabled(False)
        # self.setFixedSize(self.sizeHint())

    def _control(self):
        self.answer = 'ok'
        self.close()

    def _reject(self):
        self.answer = 'cancel'
        self.close()

    def getPwd(self):
        return self.password.text()

    def getLogin(self):
        return self.username.text()

    def getAnswer(self):
        return self.answer
