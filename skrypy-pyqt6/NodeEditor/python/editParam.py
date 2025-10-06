##########################################################################
# mriWorks - Copyright (C) IRMAGE/INSERM, 2020
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# https://cecill.info/licences/Licence_CeCILL_V2-en.html
# for details.
##########################################################################

from NodeEditor.python.tools import DefinitType
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QDialog, QLabel, \
    QPushButton, QWidget, QGroupBox, QComboBox, QScrollArea, QLineEdit
import os


class editParam(QDialog):

    def __init__(self, nameBlock, unit, inout, valInit, parent=None):
        super(editParam, self).__init__(parent)

        self.inout = inout
        self.setWindowTitle('Input parameters')
        self.setWindowFlags(self.windowFlags() &
                            Qt.WindowType.WindowCloseButtonHint)
        self.setMinimumWidth(280)

        nIn = len(inout[0])
        self.listField = {}
        for i in range(0, nIn):
            try:
                self.listField[inout[0][i]] = DefinitType(eval(valInit[i])).returntype()
            except Exception as err:
                self.listField[inout[0][i]] = DefinitType(valInit[i]).returntype()

        vbox = QVBoxLayout(self)

        hbox = QHBoxLayout()
        label = QLabel("Block Name : ")
        hbox.addWidget(label)
        label = QLineEdit(nameBlock)
        label.setDisabled(True)
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        hbox.addWidget(label)
        hbox2 = QHBoxLayout()
        label = QLabel("Block Unit : ")
        hbox2.addWidget(label)
        label = QLineEdit(unit)
        label.setDisabled(True)
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        hbox2.addWidget(label)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)

        scrolllayout = QVBoxLayout()

        scrollwidget = QWidget()
        scrollwidget.setLayout(scrolllayout)

        scroll = QScrollArea()
#         scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(scrollwidget)
        scroll.setMinimumWidth(200)

        self.label = []
        self.zoneline = []
        palette = QPalette()
        font = QFont("Times", 10)
        font.setBold(True)
        for i in range(len(inout[0])):
            hbox3 = QHBoxLayout()
            label = QLabel(inout[0][i])
            if ('enumerate' not in self.listField[inout[0][i]] and
                self.listField[inout[0][i]] != 'bool') or (
                    'Node(' in str(inout[1][i])):
                lab = QLineEdit()
                lab.setText(str(inout[1][i]))
                lab.setFont(font)
                if 'Node(' in lab.text():
                    lab.setReadOnly(True)
                    self.listField[inout[0][i]] = 'str'
                    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.darkGray)
                else:
                    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.blue)
                lab.setPalette(palette)
                self.label.append(inout[0][i])
                self.zoneline.append(lab)
                hbox3.addWidget(label)
                hbox3.addWidget(self.zoneline[i])
                scrolllayout.addLayout(hbox3)
            else:
                lab = QComboBox()
                lab.setMinimumWidth(int(self.size().width() / 4))
                if self.listField[inout[0][i]] == 'bool':
                    lab.addItem('True')
                    lab.addItem('False')
                else:
                    for it in list(eval(valInit[i])):
                        lab.addItem(it[1])
#                         lab.addItem(str(it))
                index = lab.findText(str(inout[1][i]), Qt.MatchFlag.MatchFixedString)
                if index >= 0:
                    lab.setCurrentIndex(index)
                lab.setFont(font)
                palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.blue)
                lab.setPalette(palette)
                self.label.append(inout[0][i])
                self.zoneline.append(lab)
                hbox3.addWidget(label)
                hbox3.addWidget(self.zoneline[i])
                scrolllayout.addLayout(hbox3)
        vbox.addWidget(scroll)

        self.info = QLabel()
        vbox.addWidget(self.info)

        buttonOk = QPushButton('Ok', self)
        buttonCancel = QPushButton('Cancel', self)
        hbox4 = QHBoxLayout()
        hbox4.addWidget(buttonOk)
        hbox4.addWidget(buttonCancel)

        vbox.addLayout(hbox4)
        self.adjustSize()

        buttonOk.clicked.connect(self.OK)
        buttonCancel.clicked.connect(self.CANCEL)

    def CANCEL(self):
        self.listVal = self.inout[1]
        self.close()

    def OK(self):
        self.listVal = []

        for index, i in enumerate(self.zoneline):
            if type(i) is QComboBox:
                try:
                    self.listVal.append(eval(i.currentText()))
                except (SyntaxError,
                        NameError,
                        TypeError,
                        ZeroDivisionError):
                    self.listVal.append(i.currentText())

            else:
                if i.text():
                    if i.text() in ['float', 'int', 'complex', 'bool', 'str', 'input']:
                        tmpd = i.text()
                    else:
                        try:
                            tmpd = eval(i.text())
                        except (SyntaxError,
                                NameError,
                                TypeError,
                                ZeroDivisionError):
                            tmpd = i.text()
                else:
                    tmpd = ''

                if 'list' in self.listField[self.label[index]] or 'array' in self.listField[self.label[index]]:
                    if not tmpd:
                        self.info.setText("<span style=\" \
                                            font-size:10pt; \
                                            color:#cc0000;\" > error :"
                                          + self.label[index] +
                                          " must be not empty </span>")
                        return
                if 'array' in self.listField[self.label[index]]:
                    if not tmpd[0]:
                        self.info.setText("<span style=\" \
                                            font-size:10pt; \
                                            color:#cc0000;\" > error :"
                                          + self.label[index] +
                                          " must be not empty </span>")
                        return
                ############################################################################################

                if (self.listField[self.label[index]] == 'path' and
                        tmpd not in 'path'):
                    if not os.path.exists(tmpd):
                        self.info.setText("<span style=\" \
                                            font-size:10pt; \
                                            color:#cc0000;\" > error :"
                                          + self.label[index] +
                                          " does't seems exist </span>")
                        return
                    else:
                        self.listVal.append(tmpd)

                elif self.listField[self.label[index]] == 'str':
                    self.listVal.append(str(tmpd))

                elif (DefinitType(tmpd).returntype() !=
                        self.listField[self.label[index]]):
                    self.info.setText("<span style=\" \
                                        font-size:10pt; \
                                        color:#cc0000;\" > error : "
                                      + self.label[index] + " must be "
                                      + self.listField[self.label[index]]
                                      + "</span>")
                    return
                else:
                    self.listVal.append(tmpd)
        self.close()

    def closeEvent(self, event):
        return QDialog.closeEvent(self, event)

    def getNewValues(self):
        return self.listVal
