from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, \
    QCheckBox


class setPreferences(QDialog):

    def __init__(self, checkedTo, parent=None):
        super(setPreferences, self).__init__(parent)
        self.setWindowTitle('Appearance')
        self.setWindowFlags(self.windowFlags() & Qt.WindowType.WindowCloseButtonHint)
        self.setMinimumWidth(280)

        vbox = QVBoxLayout(self)

        self.itemlab = QCheckBox("Show items label", self)
        self.itemlab.setChecked(checkedTo[0])
        self.linkText = QCheckBox("Show links text", self)
        self.linkText.setChecked(checkedTo[1])
        self.linkArray = QCheckBox("Show links array", self)
        self.linkArray.setChecked(checkedTo[2])

        vbox.addWidget(self.itemlab)
        vbox.addWidget(self.linkText)
        vbox.addWidget(self.linkArray)

        buttonOk = QPushButton('Ok', self)
        buttonCancel = QPushButton('Cancel', self)
        hbox = QHBoxLayout()
        hbox.addWidget(buttonOk)
        hbox.addWidget(buttonCancel)

        vbox.addLayout(hbox)

        self.setLayout(vbox)

        buttonOk.clicked.connect(self.OK)
        buttonCancel.clicked.connect(self.CANCEL)

        self.answer = 'cancel'

    def CANCEL(self):
        self.close()

    def OK(self):
        self.answer = 'ok'
        self.listVal = [self.itemlab.isChecked(),
                        self.linkText.isChecked(),
                        self.linkArray.isChecked()]
        self.close()

    def getNewValues(self):
        return self.listVal, self.answer
