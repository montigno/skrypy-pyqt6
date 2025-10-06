from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import (QApplication, QGridLayout, QPushButton,
                             QWidget, QLabel, QVBoxLayout, QFrame, QSizePolicy)


class buildLibrary(QWidget):

    menu_choosen = pyqtSignal(str)

    def __init__(self, listModules, parent=None):
        super(buildLibrary, self).__init__(parent)
        ncol = 3
        self.setMinimumWidth(120 + ncol * 40)
        self.setMaximumWidth(120 + ncol * 40)
        # self.setMaximumHeight(100)

        row_number = int(len(listModules) / ncol) + (len(listModules) % ncol > 0)
        # Create a QGridLayout instance
        glayout = QGridLayout()
        Separator = QFrame()
        Separator.setFrameShape(QFrame.Shape.HLine)
        Separator.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        # Separator.setLineWidth(1)
        # Separator.setFrameShadow(QFrame.Shadow.Sunken)

        for i in range(row_number):
            for j in range(ncol):
                try:
                    vbox = QVBoxLayout()
                    if i == -1 and j == -1:
                        Separador = QFrame()
                        Separador.Shape(QFrame.Shape.HLine)
                        Separador.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
                        Separador.setLineWidth(3)
                        # vbox.addWidget(Separador)
                    else:
                        lab = list(listModules)[i*ncol + j]
                        lab = lab.replace('_', '\n')
                        ico = list(listModules.values())[i*ncol + j]
                        label = QLabel()
                        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        # label.setWordWrap(True)
                        label.setStyleSheet("QLabel{font-size: 8pt;}")
                        label.setMinimumHeight(10)
                        label.setMaximumHeight(20)
                        label.setText(lab)
                        label.updateGeometry()
                        button = QPushButton(self.parent())
                        button.setObjectName(label.text())
                        # button.setFixedHeight(50)
                        button.clicked.connect(self.buttonClik)
                        button.setIcon(QIcon(ico))
                        button.setIconSize(QSize(40, 40))
                        # button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
                        button.setMinimumWidth(70)
                        button.setMinimumHeight(70)
                        button.setMaximumWidth(70)
                        button.setMaximumWidth(70)
                        vbox.addWidget(button)
                        vbox.addWidget(label)
                        # vbox.addWidget(Separator)
                    # vbox.insertSpacing(50, 5)
                    glayout.addLayout(vbox, i, j)
                except Exception as err:
                    pass
        self.setFixedHeight(row_number*100)
        self.setLayout(glayout)

    def buttonClik(self, txt):
        self.menu_choosen.emit(self.sender().objectName())
