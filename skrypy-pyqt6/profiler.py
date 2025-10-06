##########################################################################
# mriWorks - Copyright (C) IRMAGE/INSERM, 2020
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# https://cecill.info/licences/Licence_CeCILL_V2-en.html
# for details.
##########################################################################

from PyQt6.QtWidgets import QApplication
import cProfile
from main import Project_Irmage
import re
import sys


if __name__ == '__main__':

    app = QApplication(sys.argv)
    cProfile.run(Project_Irmage(), '')
    if imageViewer.state:
        sys.exit(app.exec())
