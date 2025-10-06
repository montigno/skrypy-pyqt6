##########################################################################
# mriWorks - Copyright (C) IRMAGE/INSERM, 2020
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# https://cecill.info/licences/Licence_CeCILL_V2-en.html
# for details.
##########################################################################

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton


class setLimits(QDialog):
    def __init__(self, format, limits, parent=None):
        super(setLimits, self).__init__(parent)

        self.format = format[format.index('_') + 1:] if '_' in format else format
        self.limits = limits
        self.new_limits = []

        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout()
        label = QLabel("Minimal value : ")
        hbox.addWidget(label)
        label = QLineEdit(str(limits[0]))
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.new_limits.append(label)
        hbox.addWidget(label)

        hbox2 = QHBoxLayout()
        label = QLabel("Maximal value : ")
        hbox2.addWidget(label)
        label = QLineEdit(str(limits[1]))
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.new_limits.append(label)
        hbox2.addWidget(label)

        self.info = QLabel()

        buttonOk = QPushButton('Ok', self)
        buttonCancel = QPushButton('Cancel', self)
        hbox3 = QHBoxLayout()
        hbox3.addWidget(buttonOk)
        hbox3.addWidget(buttonCancel)

        buttonOk.clicked.connect(self.OK)
        buttonCancel.clicked.connect(self.CANCEL)

        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.info)
        vbox.addLayout(hbox3)

    def OK(self):
        for index, i in enumerate(self.new_limits):
            if type(eval(i.text())).__name__ != self.format:
                self.info.setText("<span style=\" \
                                  font-size:10pt; \
                                  color:#cc0000;\" > error : \
                                  values must be " + self.format + "</span>")
                return
        self.close()
        self.answer = 'ok'

    def CANCEL(self):
        self.answer = "cancel"
        self.close()

    def getNewValues(self):
        if self.format == 'int':
            return (int(self.new_limits[0].text()),
                    int(self.new_limits[1].text()))
        else:
            return (float(self.new_limits[0].text()),
                    float(self.new_limits[1].text()))

    def getAnswer(self):
        return self.answer
