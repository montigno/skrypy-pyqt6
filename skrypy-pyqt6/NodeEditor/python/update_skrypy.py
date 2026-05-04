import os
# import git
import shutil
import yaml
import tempfile
import stat

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, \
    QHBoxLayout


class skrypy_update(QDialog):
    def __init__(self, parent=None):
        try:
            import git
        except ImportError:
            print("Git is not installed on your system. Please install it with the command 'sudo apt-get install git-all'.")
        super(skrypy_update, self).__init__(parent)
        self.setWindowTitle("Skrypy Updater")
        self.setMinimumWidth(400)
        self.setAutoFillBackground(True)
        self.answer = 'cancel'
        dest = tempfile.gettempdir()
        self.skrypy_current = os.path.realpath(__file__)
        self.skrypy_current = self.skrypy_current[:self.skrypy_current.index('NodeEditor')]
        config_current = os.path.join(self.skrypy_current, 'config.yml')
        with open(config_current, 'r', encoding='utf8') as stream:
            dicts = yaml.load(stream, yaml.FullLoader)
            self.version_current = dicts['version']
        self.skrypy_new_dir = os.path.join(dest, "skrypy-pyqt6")
        if os.path.exists(self.skrypy_new_dir):
            shutil.rmtree(self.skrypy_new_dir, onerror=self.remove_readonly)
        try:
            git.Git(dest).clone("https://github.com/montigno/skrypy-pyqt6.git")
            self.skrypy_new = os.path.join(self.skrypy_new_dir, "skrypy-pyqt6")
            config_new = os.path.join(self.skrypy_new, 'config.yml')
            with open(config_new, 'r', encoding='utf8') as stream:
                dicts = yaml.load(stream, yaml.FullLoader)
                self.version_new = dicts['version']
            self.confirmation_dialog()
        except Exception:
            self.error_message()

    def error_message(self):
        label1 = QLabel("fatal: unable to access 'https://github.com/montigno/skrypy-pyqt6.git/': \nCould not resolve host: github.com' ")
        buttonOk = QPushButton('OK', self)
        vbox = QVBoxLayout(self)
        vbox.addWidget(label1)
        vbox.addWidget(buttonOk)
        buttonOk.clicked.connect(self.close)
        self.setLayout(vbox)

    def confirmation_dialog(self):

        label1 = QLabel("The latest version available is " + self.version_new)
        label2 = QLabel("Your current version is " + self.version_current)
        label3 = QLabel("Do you want to update ? If you click YES, you will need to restart Skrypy to take effect.")
        label3.setWordWrap(True)

        buttonCancel = QPushButton('NO', self)
        buttonCancel.clicked.connect(self.closeDialog)
        buttonOk = QPushButton('YES', self)
        buttonOk.clicked.connect(self.upgrading)
        hbox = QHBoxLayout()
        hbox.addWidget(buttonCancel)
        hbox.addWidget(buttonOk)

        vbox = QVBoxLayout(self)
        vbox.addWidget(label1)
        vbox.addWidget(label2)
        vbox.addWidget(label3)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def remove_readonly(self, func, path, _):
        "Clear the readonly bit and reattempt the removal"
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def upgrading(self):
        shutil.rmtree(self.skrypy_current, onerror=self.remove_readonly)
        shutil.copytree(self.skrypy_new, self.skrypy_current, dirs_exist_ok=True)
        shutil.rmtree(self.skrypy_new_dir, onerror=self.remove_readonly)
        self.answer = 'YES'
        self.close()

    def closeDialog(self):
        shutil.rmtree(self.skrypy_new_dir, onerror=self.remove_readonly)
        self.close()

    def getAnswer(self):
        return self.answer
