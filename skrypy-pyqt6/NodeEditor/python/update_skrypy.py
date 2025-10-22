import os
import git
import shutil
import yaml

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton, \
    QHBoxLayout


class skrypy_update(QDialog):
    def __init__(self, parent=None):
        super(skrypy_update, self).__init__(parent)
        self.setWindowTitle("Skrypy Updater")
        self.setMinimumWidth(400)
        self.setAutoFillBackground(True)
        self.answer = 'cancel'
        dest = "/tmp/"
        skrypy_current = os.path.realpath(__file__)
        skrypy_current = skrypy_current[:skrypy_current.index('NodeEditor')]
        config_current = os.path.join(skrypy_current, 'config.yml')
        with open(config_current, 'r', encoding='utf8') as stream:
            dicts = yaml.load(stream, yaml.FullLoader)
            self.version_current = dicts['version']
        self.skrypy_current = skrypy_current
        skrypy_new = os.path.join(dest, "skrypy-pyqt6")
        if os.path.exists(skrypy_new):
            shutil.rmtree(skrypy_new)
        try:
            git.Git(dest).clone("https://github.com/montigno/skrypy-pyqt6.git")
            skrypy_new = os.path.join(skrypy_new, "skrypy-pyqt6")
            config_new = os.path.join(skrypy_new, 'config.yml')
            with open(config_new, 'r', encoding='utf8') as stream:
                dicts = yaml.load(stream, yaml.FullLoader)
                self.version_new = dicts['version']
            self.skrypy_new = skrypy_new
            self.confirmation_dialog()
        except Exception as err:
            self.error_message()

    def error_message(self):
        label1 = QLabel("fatal: unable to access 'https://github.com/montigno/skrypy.git/': \nCould not resolve host: github.com' ")
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
        buttonCancel.clicked.connect(self.close)
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

    def upgrading(self):
        shutil.rmtree(self.skrypy_current)
        shutil.copytree(self.skrypy_new, self.skrypy_current, dirs_exist_ok=True)
        self.answer = 'YES'
        self.close()

    def getAnswer(self):
        return self.answer
