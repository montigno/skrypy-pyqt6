##########################################################################
# mriWorks - Copyright (C) IRMAGE/INSERM, 2020
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# https://cecill.info/licences/Licence_CeCILL_V2-en.html
# for details.
##########################################################################

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, \
    QButtonGroup, QCheckBox, QPushButton, QLineEdit

import time
import os
import yaml


class multiple_execution_altern(QDialog):
    def __init__(self, listDiagram, parent=None):
        super(multiple_execution_altern, self).__init__(parent)
        self.setWindowTitle('Order of processes - alternation')
        self.setWindowFlags(self.windowFlags() & Qt.WindowType.WindowCloseButtonHint)
        self.listVal = []
        self.adjustSize()
        vbox = QVBoxLayout(self)
        self.zonecombo = []
        list_clust = ['local']
        list_clust.extend(self.get_clusters_list())
        for i, lst in enumerate(listDiagram):
            lab = QLabel('Diagram '+str(i))
            comb = QComboBox(self)
            comb.addItems(listDiagram)
            comb.addItem('None')
            comb.setCurrentIndex(i)
            checkb = QCheckBox('threading mode')
            clust = QComboBox(self)
            clust.addItems(list_clust)
            clust.setCurrentIndex(0)
            self.zonecombo.append((comb, checkb, clust))
            hbox = QHBoxLayout()
            hbox.addWidget(lab)
            hbox.addWidget(comb)
            hbox.addWidget(checkb)
            hbox.addWidget(clust)
            vbox.addLayout(hbox)
        self.a = QCheckBox('run sequentially')
        self.a.setChecked(True)
        self.b = QCheckBox('run in multiprocessing mode (available in the next version)')
        self.b.stateChanged.connect(self.info_mu)
        cs = QButtonGroup(self)
        cs.addButton(self.a)
        cs.addButton(self.b)
        vbox.addWidget(self.a)
        vbox.addWidget(self.b)

        buttonGo = QPushButton('Go!', self)
        buttonCancel = QPushButton('Cancel', self)
        # buttonSaveProj = QPushButton('Save project', self)
        # buttonOpenProj = QPushButton('Open project', self)
        hboxbutton = QHBoxLayout()
        hboxbutton.addWidget(buttonGo)
        hboxbutton.addWidget(buttonCancel)
        # hboxbutton.addWidget(buttonSaveProj)
        # hboxbutton.addWidget(buttonOpenProj)
        vbox.addLayout(hboxbutton)

        buttonGo.clicked.connect(self.GO)
        buttonCancel.clicked.connect(self.CANCEL)
        # buttonSaveProj.clicked.connect(self.SaveProj)
        # buttonOpenProj.clicked.connect(self.OpenProj)

    def CANCEL(self):
        self.close()

    def GO(self):
        for lst_comb in self.zonecombo:
            self.listVal.append((lst_comb[0].currentText(), lst_comb[1].isChecked(), lst_comb[2].currentText()))
        self.listVal.append(self.a.isChecked())
        self.listVal.append(self.b.isChecked())
        self.close()

    def info_mu(self):
        self.a.setChecked(True)

    def get_clusters_list(self):
        lst_clust = []
        clust_file = os.path.expanduser('~')
        clust_file = os.path.join(clust_file, '.skrypy', 'list_servers.yml')
        if os.path.exists(clust_file):
            with open(clust_file, 'r') as stream:
                lst_clust = yaml.load(stream, yaml.FullLoader)
                lst_clust = list(lst_clust.keys())
                lst_clust.remove('template')
        return lst_clust

    def onTimeout(self):
        self.info.setText('')

    def closeEvent(self, event):
        return QDialog.closeEvent(self, event)

    def getNewValues(self):
        return self.listVal
