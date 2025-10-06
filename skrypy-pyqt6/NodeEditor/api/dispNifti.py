from PyQt5.Qt import QKeySequence
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPalette
from PyQt5.QtWidgets import QSlider, QLabel, QSizePolicy, \
    QLineEdit, QGroupBox, QGridLayout, QVBoxLayout, QDialog, QWidget, \
    QApplication
import numpy as np
import os
from random import randrange
from scipy.ndimage import rotate
import sys


class DispNifti(QDialog):

    def __init__(self, imgf, title='', del_fil='no', parent=None):
        super(DispNifti, self).__init__(parent)
        # QDialog.__init__(self, parent)

        NiftiFile = Open_Nifti(imgf)
        img = NiftiFile.image()
        pixdim = NiftiFile.pixdim()[1:4]
        # pixdim=(1.0, 1.0)

        self.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint, True)
#         self.setWindowModality(Qt.WindowModality.NonModal)

        try:
            img[np.isnan(img)] = 0.0
        except:
            pass

        self.img = np.array(img)
        self.dim = len(self.img.shape)

        if (self.dim == 2):
            tmpimg = self.img.copy()
        elif (self.dim == 3):
            tmpimg = self.img[:, :, 0].copy()
        elif (self.dim == 4):
            tmpimg = self.img[:, :, 0, 0].copy()       
        elif (self.dim == 5):
            tmpimg = self.img[:, :, 0, 0, 0].copy()

        self.w, self.h = tmpimg.shape
        self.interl = self.w
        self.rx, self.ry = self.w, self.h

        self.scaleFactor = 2
        if self.w >= 512:
            self.scaleFactor = round(self.w / 256)
        elif self.w >= 256:
            self.scaleFactor = round(self.w / 128)
        elif self.w >= 128:
            self.scaleFactor = round(self.w / 64)
        elif self.w >= 64:
            self.scaleFactor = round(self.w / 16)
        elif self.w >= 32:
            self.scaleFactor = round(self.w / 4)

        if self.w >= self.h:
            if (self.h * pixdim[1] < self.w * pixdim[0]):
                self.rx = int(self.w * pixdim[0] / pixdim[1])
                self.ry = self.h
                self.interl = self.h
            elif (self.h * pixdim[1] > self.w * pixdim[0]):
                self.rx = self.w
                self.ry = int(self.h * pixdim[1] / pixdim[0])
                self.interl = self.w
        else:
            if (self.h * pixdim[1] > self.w * pixdim[0]):
                self.rx = int(self.w * pixdim[0] / pixdim[1])
                self.ry = self.h
                self.interl = self.h
            elif (self.h * pixdim[1] < self.w * pixdim[0]):
                self.rx = self.w
                self.ry = int(self.h * pixdim[1] / pixdim[0])
                self.interl = self.w
               
        self.boxSliders() 
        self.enableSliders()
        self.imgqLabel()
        self.navigImage()
        
        self.info = QLabel()
        self.info.setText("<span style=\" \
                          font-size:10pt; \
                          color:#101010;\"> {:.2f}x{:.2f}mm ({}x{})</span>"
                          .format(self.w * pixdim[0], self.h * pixdim[1], self.w, self.h))
          
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addWidget(self.imageLabel)
        self.verticalLayout.addWidget(self.layoutSlide)
        self.verticalLayout.addWidget(self.info)
         
        self.setWindowTitle(title)
#         self.resize((10 + self.rx) * self.scaleFactor, (50 + self.ry) * self.scaleFactor)
        self.setLayout(self.verticalLayout)
        self.move(self.pos().x() + 20 * randrange(10), self.pos().y() + 20 * randrange(10))
        
        if del_fil == 'yes':
            try:
                os.remove(imgf)
            except OSError as e:
                print("Error : %s : %s" % (input_file, e.strerror))

    def imgqLabel(self):
        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.ColorRole.Base)
#         self.imageLabel.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
    def navigImage(self):
        self.indexImage()
        self.displayPosValue()
        totalBytes = self.x.data.nbytes
        bytesPerLine = int(totalBytes / self.interl)
        image = QImage(self.x.data, self.w , self.h, bytesPerLine, QImage.Format.Format_Grayscale8)
        # image = QImage(self.x.repeat(4), self.w, self.h, QImage.Format.Format_RGB32)

        self.pixm = QPixmap.fromImage(image)
        self.pixm = self.pixm.scaled(self.rx * (self.scaleFactor - 1),
                                     self.ry * (self.scaleFactor - 1),
                                     Qt.AspectRatioMode.IgnoreAspectRatio)
        self.imageLabel.setPixmap(self.pixm)
#         self.imageLabel.adjustSize()

    def indexImage(self):
        sl1 = self.a1.value()
        sl2 = self.a2.value()
        sl3 = self.a3.value()
        if (self.dim == 2):
            x = self.img.copy()
            self.a1.setMaximum(0)
            self.a2.setMaximum(0)
            self.a3.setMaximum(0)
        elif (self.dim == 3):
            x = self.img[:, :, sl1].copy()
            self.a1.setMaximum(self.img.shape[2] - 1)
            self.a2.setMaximum(0)
            self.a3.setMaximum(0)
        elif (self.dim == 4):
            x = self.img[:, :, sl1, sl2].copy()
            self.a1.setMaximum(self.img.shape[2] - 1)
            self.a2.setMaximum(self.img.shape[3] - 1)
            self.a3.setMaximum(0)
        elif (self.dim == 5):
            x = self.img[:, :, sl1, sl2, sl3].copy()
            self.a1.setMaximum(self.img.shape[2] - 1)
            self.a2.setMaximum(self.img.shape[3] - 1)
            self.a3.setMaximum(self.img.shape[4] - 1)
        x = rotate(x, -90, reshape=True)
        x = np.uint8((x - x.min()) / np.ptp(x) * 255.0)
        self.x = x
        
    def displayPosValue(self):
        self.txta1.setText(str(self.a1.value() + 1) + ' / ' + str(self.a1.maximum() + 1))
        self.txta2.setText(str(self.a2.value() + 1) + ' / ' + str(self.a2.maximum() + 1))
        self.txta3.setText(str(self.a3.value() + 1) + ' / ' + str(self.a3.maximum() + 1))

    def boxSliders(self):
        self.k1 = QLabel('Sl 1    ')
        self.k2 = QLabel('Sl 2')
        self.k3 = QLabel('Sl 3')
 
        self.a1 = self.createSlider(0, 0, 0)
        self.a2 = self.createSlider(0, 0, 0)
        self.a3 = self.createSlider(0, 0, 0)
 
        self.a1.valueChanged.connect(self.changePosValue)
        self.a2.valueChanged.connect(self.changePosValue)
        self.a3.valueChanged.connect(self.changePosValue)
 
        self.txta1 = self.createFieldValue()
        self.txta2 = self.createFieldValue()
        self.txta3 = self.createFieldValue()
 
        self.controlsGroup = QGroupBox('Slice Controls')
        gridCtrl = QGridLayout()
        gridCtrl.addWidget(self.k1, 0, 0)
        gridCtrl.addWidget(self.a1, 0, 1)
        gridCtrl.addWidget(self.txta1, 0, 2)
        gridCtrl.addWidget(self.k2, 1, 0)
        gridCtrl.addWidget(self.a2, 1, 1)
        gridCtrl.addWidget(self.txta2, 1, 2)
        gridCtrl.addWidget(self.k3, 2, 0)
        gridCtrl.addWidget(self.a3, 2, 1)
        gridCtrl.addWidget(self.txta3, 2, 2)
        self.controlsGroup.setLayout(gridCtrl)
         
        self.layoutSliders = QVBoxLayout()
        self.layoutSliders.addWidget(self.controlsGroup)
 
        self.layoutSlide = QWidget()
        self.layoutSlide.setLayout(self.layoutSliders)
        
    def enableSliders(self):
        self.a1.setEnabled(True)
        self.a2.setEnabled(True)
        self.a3.setEnabled(True)
         
    def createSlider(self, maxm=0, minm=0, pos=0):
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        # slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        slider.setTickInterval(1)
        # slider.setSingleStep(1)
        slider.setMaximum(maxm)
        slider.setMinimum(minm)
        slider.setValue(pos)
        slider.setEnabled(False)
        return slider
     
    def createFieldValue(self):
        fieldValue = QLineEdit()
        fieldValue.setEnabled(False)
        fieldValue.setFixedWidth(80)
        fieldValue.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        return fieldValue
     
    def changePosValue(self):
        self.navigImage()
        
    def keyPressEvent(self, event):
        if (QKeySequence(event.key() + int(event.modifiers())) ==
                QKeySequence("Ctrl+W")):
            self.close()
        return QDialog.keyPressEvent(self, event)


class Open_Nifti:
    def __init__(self, fileSource='path'):
        import os.path
        import nibabel as nib
        self.fileSource = fileSource
        self.dim = 0
        self.img = [[0.0]]
        self.pxd = (1.0, 1.0)
        if (os.path.splitext(fileSource)[1] == '.nii') or \
           ('.nii.gz' in fileSource):
            img = nib.load(fileSource)
            self.img = img.get_fdata()
            self.dim = len(img.shape)
            self.pxd = img.header._structarr['pixdim']
        else:
            print('no Nifti file')

    def image(self: 'array_float'):
        return self.img

    def dim(self: 'int'):
        return self.dim

    def pixdim(self: 'list_float'):
        return self.pxd

    def filePath(self: 'path'):
        return self.fileSource


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dispNifti = DispNifti(sys.argv[1], sys.argv[2], sys.argv[3])
    dispNifti.show()
    sys.exit(app.exec())
