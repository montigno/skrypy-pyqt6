##########################################################################
# mriWorks - Copyright (C) IRMAGE/INSERM, 2020
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# https://cecill.info/licences/Licence_CeCILL_V2-en.html
# for details.
##########################################################################

'''
Created on 06 oct. 2025
@author: omonti
'''

from Config import Config
from NodeEditor.python.Diagram_Editor import NodeEdit
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, \
      QLineEdit, QMainWindow, QMessageBox, QCheckBox

import os
import shutil
import subprocess
import sys
import tempfile
import time
from dirsync import sync


class Project_Irmage(QMainWindow):
    def __init__(self, self_dir_path):

        os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

        Manag_cpu()
        self.state = True
        self.self_dir_path = self_dir_path

        # synchronize submodules ################################
        Synchronize_submod_tree(self.self_dir_path)

        # Main Window ###########################################
        super(Project_Irmage, self).__init__()

        # initial setting #######################################
        config_mr = Config()
        title = "skrypy " + config_mr.getVersion()

        # system control ########################################
        time.sleep(0.1)
        current_dir_path = os.path.dirname(os.path.realpath(__file__))
        source_disp = os.path.join(current_dir_path, 'NodeEditor', 'python', 'systemControl.py')
        self.sysctrl = subprocess.Popen([sys.executable,
                                         source_disp,
                                         'skrypy control',
                                         str(os.getpid())])

        # Createwidgets ##########################################
        self.t = CreateWidget()
        self.setCentralWidget(self.t)

        # Window Main ###########################################
        self.setWindowTitle(title)
        self.showNormal()
        self.statusBar().showMessage('Ready')

        # tempfile directory ####################################
        self.tmp_dir = os.path.join(os.path.expanduser('~'), '.skrypy', 'temp_file')
        if not os.path.exists(self.tmp_dir):
            os.mkdir(self.tmp_dir)
        else:
            tmp = tempfile.NamedTemporaryFile(delete=False).name
            d = os.path.join(os.path.expanduser('~'), '.skrypy', os.path.basename(str(tmp)))
            shutil.copytree(self.tmp_dir, d, symlinks=False, ignore=None)
            os.remove(tmp)

    def closeEvent(self, event):
        msg = QMessageBox(self)
        msg.setWindowTitle("Exit skrypy")
        msg.setMinimumWidth(400)
        msg.setMaximumWidth(500)
        # msg.setFixedSize(400, 200)
        msg.setText("Have you saved your projects ?")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)
        cb = QCheckBox("Clear shared memory")
        msg.setCheckBox(cb)
        event.ignore()
        # msg.setDetailedText("Extra details.....")
        # msg.setInformativeText("This is some extra informative text")
        x = msg.exec()

        if x == QMessageBox.StandardButton.Yes:
            if cb.isChecked():
                ClearSharedMemory()
            Synchronize_submod_tree(self.self_dir_path)
            self.sysctrl.kill()
            event.accept()

    def __del__(self):
        try:
            shutil.rmtree(self.tmp_dir)
        except Exception as err:
            pass


class CreateWidget(QWidget):
    def __init__(self):
        super(CreateWidget, self).__init__()

        textInfo = QLineEdit(self)
        textInfo.setReadOnly(True)
        textInfo.resize(500, 40)
        textInfo.setText('Welcome to Irmage')

        self.wdg = NodeEdit(textInfo)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addWidget(self.wdg)
        self.verticalLayout.addWidget(textInfo)


class Copy_submod_tree():
    def __init__(self, self_dir_path):
        s = os.path.join(self_dir_path, 'NodeEditor', 'submodules')
        d = os.path.join(os.path.expanduser('~'), '.skrypy', 'submodules')
        if os.path.exists(d):
            try:
                shutil.rmtree(d)
            except Exception as err:
                print(err)
                os.unlink(d)
        shutil.copytree(s, d, symlinks=False, ignore=None)


class Synchronize_submod_tree():
    def __init__(self, self_dir_path):
        s = os.path.join(self_dir_path, 'NodeEditor', 'submodules')
        d = os.path.join(os.path.expanduser('~'), '.skrypy', 'submodules')
        if os.path.exists(d):
            sync(s, d, 'sync')
            sync(d, s, 'sync')
        else:
            shutil.copytree(s, d, symlinks=False, ignore=None)


class Manag_cpu():

    def __init__(self):
        super(Manag_cpu, self).__init__()
        cpu_cnt = Config().getCpuCount()
        if cpu_cnt > os.cpu_count():
            Config().setCpuCount(os.cpu_count())


class ClearSharedMemory():

    def __init__(self):
        self.file_shm = os.path.join(os.path.expanduser('~'), '.skrypy', 'list_shm.yml')
        self.clearMemory()

    def clearMemory(self):
        if os.path.exists(self.file_shm):
            os.remove(self.file_shm)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    with open("styles.css", "r") as file:
        app.setStyleSheet(file.read())
    self_dir_path = os.path.dirname(os.path.realpath(__file__))
    imageViewer = Project_Irmage(self_dir_path)
    mri_icon = os.path.join(self_dir_path, 'ressources', 'skrypy.png')
    app.setWindowIcon(QIcon(mri_icon))
    os.chdir(os.path.expanduser('~'))
    imageViewer.show()
    if imageViewer.state:
        sys.exit(app.exec())
