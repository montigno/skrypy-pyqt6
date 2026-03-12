##########################################################################
# mriWorks - Copyright (C) IRMAGE/INSERM, 2020
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# https://cecill.info/licences/Licence_CeCILL_V2-en.html
# for details.
##########################################################################

'''
Created on 26 déc. 2023

@author: omonti
'''

from Config import Config
from PyQt6.QtWidgets import QMessageBox
import os
import platform


class AboutSoft(QMessageBox):

    def __init__(self, parent=None):
        QMessageBox.__init__(self, parent)
        self.about(self,
                   "About main",
                   "skrypy version: " + Config().getVersion() + "<br>"
                   "Python version: " + platform.python_version() + "<br>"
                   "OS: " + platform.system() + " " + platform.release() + "<br>"
                   "number of CPUs in the system: " + str(os.cpu_count()) + "<br><br>"
                   "<b>skrypy</b> developped by :"
                   "<br>Olivier MONTIGON "
                   " "
                   "<p>omontigon@yahoo.fr</p>")
