##########################################################################
# mriWorks - Copyright (C) IRMAGE/INSERM, 2020
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# https://cecill.info/licences/Licence_CeCILL_V2-en.html
# for details.
##########################################################################

'''
Last modification on 14 mars 2023
@author: omonti
'''

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics, QAction
from PyQt6.QtWidgets import QDialog, QCheckBox, QVBoxLayout, QHBoxLayout, \
     QPushButton, QScrollArea, QWidget, QMenuBar, \
     QTextEdit
import importlib
import inspect
import os
import yaml


class chOptions(QDialog):

    def __init__(self, pathYaml, nameclass, ports, parent=None):
        super(chOptions, self).__init__(parent)

        self.setWindowTitle(nameclass)
        # self.setWindowFlags(self.windowFlags() &
        #                     Qt.WindowType.WindowCloseButtonHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        
        modul = os.path.splitext(os.path.basename(pathYaml))[0]
        doc = "No description"

        self.nameclass = nameclass
        self.poqs = ports

        self.labels_inputs = self.poqs[0]
        self.values_inputs = self.poqs[1]

        menubar = QMenuBar()
        checkAll = QAction('Check all options', self)
        checkAll.setShortcut('Ctrl+A')
        menubar.addAction(checkAll)
        checkAll.triggered.connect(self.checkAllOptions)

        uncheckAll = QAction('Uncheck all options', self)
        uncheckAll.setShortcut('Ctrl+U')
        menubar.addAction(uncheckAll)
        uncheckAll.triggered.connect(self.uncheckAllOptions)

        self.listCh = []
        listLabels = []

        vbox = QVBoxLayout(self)

        _ss = ports

        self.list1 = []
        self.list2 = []
        self.list3 = []

        for tr in _ss[0]:
            self.list1.append(tr)

        for tr in _ss[1]:
            self.list2.append(tr)
            self.list3.append(tr)

        scrolloptions = QVBoxLayout()

        scrollwidget = QWidget()
        scrollwidget.setLayout(scrolloptions)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMaximumWidth(300)
        scroll.setWidget(scrollwidget)

        desc = QTextEdit()
        desc.setPlainText(doc)
        desc.setReadOnly(True)
        desc.setStyleSheet("background: transparent;")
        desc.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)

        font = desc.document().defaultFont()
        fontMetrics = QFontMetrics(font)
        textSize = fontMetrics.size(0, doc)

        textWidth = textSize.width() + 30
        textHeight = textSize.height() + 30

        desc.setMinimumSize(textWidth, textHeight)
        desc.resize(textWidth, textHeight)

        hbox2 = QHBoxLayout()
        vbox2 = QVBoxLayout()

        with open(pathYaml, 'r', encoding='utf8') as stream:
            try:
                self.dicts = yaml.load(stream, yaml.FullLoader)
                for el in self.dicts[nameclass]:
                    checkedTo = False
                    enableTo = True
                    if el in self.list1:
                        ind = self.list1.index(el)
                        self.list1.remove(el)
                        if 'Node(' in str(self.list2[ind]):
                            enableTo = False
                        vals = self.list2[ind]
                        del self.list2[ind]
                        del self.list3[ind]
                        checkedTo = True
                    b = QCheckBox(el, self)
                    b.setChecked(checkedTo)
                    b.setEnabled(enableTo)
                    self.listCh.append(b)
                    listLabels.append(b.text())
                    vbox2.addWidget(self.listCh[-1])
            except Exception as exc:
                print('yamlerror', exc)
                return

        if 'Nipype' in pathYaml and 'Config_nipype' not in pathYaml:
            modul = 'nipype.' + modul.replace('_', '.', 1).lower()
            clss = nameclass[nameclass.index('_') + 1:]
            desc.clear()
            desc.append(self.getOptionsHelp(modul, clss))
        else:
            with open(pathYaml, 'r', encoding='utf8') as stream:
                rd = stream.readlines()
                rd = rd[rd.index(nameclass + ":\n") + 1:]
    #             rd = rd[:len(self.listCh)]
                doc = ''
                n = len(listLabels)
                for lst in rd:
                    tmp = ''
                    try:
                        tmp = lst.rstrip()
                        tmp = tmp[:tmp.index('#')]
                        tmp = tmp[:tmp.index(':')]
                        if n == 0:
                            break
                        if tmp.strip() in listLabels:
                            n = n - 1
                        doc = doc + "<br><span style=\" font-size:10pt; font-weight:600; color:#222222;\" >" + tmp + " : </span><br>"
                    except Exception as e:
                        pass
                    comm = ''
                    try:
                        comm = lst[lst.index('#') + 1:]
                        doc = doc + "<span style=\" font-size:10pt; font-weight:600; color:#2222ee;\" >" + comm + "</span><br>"
                    except Exception as e:
                        pass

                if len(doc) != 0:
                    desc.clear()
                    desc.append(doc)

        scrolloptions.addLayout(vbox2)

        hbox2.addWidget(scroll)
        hbox2.addWidget(desc)

        vbox.addWidget(menubar)
        vbox.addLayout(hbox2)
        buttonOk = QPushButton('Ok', self)
        buttonCancel = QPushButton('Cancel', self)
        hboxButton = QHBoxLayout()
        hboxButton.addWidget(buttonOk)
        hboxButton.addWidget(buttonCancel)
        vbox.addLayout(hboxButton)

        self.setMinimumWidth(900)
        buttonOk.clicked.connect(self.go)
        buttonCancel.clicked.connect(self.CANCEL)

    def CANCEL(self):
        self.answer = "cancel"
        self.close()

    def go(self):

        for aze in self.listCh:
            if aze.isChecked():
                txt = aze.text()
                self.list1.append(str(txt))

                valueExists = False
                val = ''
                ind = 0

                try:
                    ind = self.labels_inputs.index(txt)
                    if 'Node(' in str(self.values_inputs[ind]):
                        val = self.values_inputs[ind]
                        valueExists = True
                except Exception as e:
                    pass

                if not valueExists:
                    list_val = self.dicts[self.nameclass][aze.text()]
                    if type(list_val).__name__ == 'str':
                        if ('enumerate' in list_val):
                            imb = list_val
                        else:
                            # try:
                            #     imb = "" + eval(list_val)
                            # except Exception as e:
                            #     imb = "" + list_val
                            imb = str(list_val)
                    else:
                        try:
                            imb = eval(list_val)
                        except Exception as e:
                            imb = list_val

                    _imb1 = imb
                    tuple = False
                    try:
                        if type(eval(imb)).__name__ == 'tuple':
                            self.list2.append(eval(imb))
                            tuple = True
                    except Exception as err:
                        tuple = False
                    if not tuple:
                        if type(imb).__name__ == 'str':
                            if 'enumerate' in imb:
                                self.list2.append(list(eval(_imb1))[0][1])
                            else:
                                self.list2.append(_imb1)
                        else:
                            self.list2.append(_imb1)
                    self.list3.append(imb)
                else:
                    self.list2.append(val)

            else:
                if aze.text() in self.list1:
                    ind = self.list1.index(aze.text())
                    self.list1.remove(aze.text())
                    del self.list2[ind]
                    del self.list3[ind]

        self.newports = (self.list1, self.list2, self.poqs[2], self.poqs[3])
        self.close()
        self.answer = "ok"

    def getNewValues(self):
        return self.newports, list(self.list3)

    def getAnswer(self):
        return self.answer

    def checkAllOptions(self):
        for aze in self.listCh:
            aze.setChecked(True)

    def uncheckAllOptions(self):
        for aze in self.listCh:
            if aze.isEnabled():
                aze.setChecked(False)

    def getOptionsHelp(self, modules, nameClass):
        try:
            imp = importlib.import_module(modules)
            MyClass = getattr(imp, nameClass)
            doc_help = MyClass.help(True)
            doc_help = doc_help[doc_help.index('[Optional]') + 11: doc_help.index('Outputs::')]
        except Exception as err:
            doc_help = 'error : {}'.format(str(err))
        return doc_help

    def closeEvent(self, closeEvent):
        self.answer = "cancel"
        self.close()
