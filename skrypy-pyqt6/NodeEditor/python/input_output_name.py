##########################################################################
# mriWorks - Copyright (C) IRMAGE/INSERM, 2020
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# https://cecill.info/licences/Licence_CeCILL_V2-en.html
# for details.
##########################################################################

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, \
    QPushButton, QComboBox


class input_output_setName(QDialog):

    def __init__(self, unit, typeport, ports, defaultName, parent=None):
        super(input_output_setName, self).__init__(parent)
        self.newName = ''

        self.typeport = typeport
        self.defaultName = defaultName
        self.listPorts = []

        currentFormat = ''
        for prts in ports:
            self.listPorts.append(prts.name)

        self.vbox = QVBoxLayout(self)

        hbox = QHBoxLayout()
        label = QLabel("Script Unit : ")
        hbox.addWidget(label)
        label = QLineEdit(unit)
        label.setDisabled(True)
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        hbox.addWidget(label)

        hbox2 = QHBoxLayout()
        label = QLabel("Name " + typeport + " port : ")
        hbox2.addWidget(label)
        self.portName = QLineEdit(defaultName)
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        hbox2.addWidget(self.portName)

        hbox3 = QHBoxLayout()
        buttonOk = QPushButton('Ok', self)
        buttonCancel = QPushButton('Cancel', self)
        hbox4 = QHBoxLayout()
        hbox4.addWidget(buttonOk)
        hbox4.addWidget(buttonCancel)

        buttonOk.clicked.connect(self.OK)
        buttonCancel.clicked.connect(self.CANCEL)

        self.vbox.addLayout(hbox)
        self.vbox.addLayout(hbox2)
        self.vbox.addLayout(hbox3)
        self.vbox.addLayout(hbox4)
        self.info = QLabel()
        self.vbox.addWidget(self.info)

    def OK(self):
        self.newName = ''
        if not self.portName.text():
            self.info.setText("<span style=\" \
                              font-size:10pt; \
                              color:#cc0000;\" > error : name " + self.typeport + " port  is empty </span>")
            return
        if self.portName.text() in self.listPorts and self.portName.text() != self.defaultName:
            self.info.setText("<span style=\" \
                              font-size:10pt; \
                              color:#cc0000;\" > error : name " + self.typeport + " is already taken ! </span>")
            return
        self.newName = self.portName.text()
        self.close()

    def CANCEL(self):
        self.newName = ''
        self.close()

    def getNewValues(self):
        return self.newName
