##########################################################################
# mriWorks - Copyright (C) IRMAGE/INSERM, 2020
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# https://cecill.info/licences/Licence_CeCILL_V2-en.html
# for details.
##########################################################################

'''
Created on 26 December 2023
Last modification on 07 august 2025
@author: Olivier Montigon
'''

from PyQt6.QtCore import QByteArray, Qt, QStringListModel, QLineF, QPointF, \
    QMimeData, QRectF, pyqtSlot, QRunnable, QTimer, pyqtSignal, QEvent
from PyQt6.QtGui import QStandardItemModel, QPixmap, QPainterPath, QCursor, \
    QBrush, QStandardItem, QPainter, QImage, QTransform, QColor, QFont, QPen, \
    QPolygonF, QLinearGradient, QKeySequence, QIcon, QFontMetrics, QPalette, \
    QPainterPathStroker, QAction
from PyQt6.QtWidgets import QMenuBar, QTextEdit, QGraphicsScene, QDialog, \
    QGraphicsView, QGraphicsPathItem, QGraphicsPolygonItem, \
    QGraphicsRectItem, QSpinBox, QDoubleSpinBox, QComboBox, \
    QTreeView, QWidget, QVBoxLayout, QTabBar, QSplitter, \
    QFileDialog, QSizePolicy, QGraphicsItem, QMessageBox, QMenu, \
    QHBoxLayout, QLabel, QPushButton, QGraphicsProxyWidget, QGraphicsTextItem, \
    QGridLayout, QCheckBox, QLineEdit, QCompleter, QToolBar, QToolButton, \
    QProgressBar, QApplication, QScrollArea, QProgressDialog, \
    QMdiArea, QMdiSubWindow, QTabWidget

from collections import deque
from enum import Enum
from functools import partial
import gc
import importlib
import inspect
from math import atan, cos, sin
import os
import subprocess
import sys
import re
import time
import webbrowser
import yaml
from random import randint
from threading import Timer

from . import Config, Plugin, AboutSoft
from . import DefinitType, ReorderList, diagramInfo
from . import GetValueInBrackets, SetValueInBrackets
from . import PythonHighlighter, skrypy_update
from . import multiple_execution, multiple_execution_altern
from . import analyze2, execution2, servers_window
from . import buildLibrary, SubWindow
from . import changeLabel, changeTitle, chOptions
from . import defineTunnels, define_inputs_outputs
from . import input_output_setName
from . import editCombobox, errorHandler
from . import editParam, editParamLoopFor
from . import getlistModules, getlistSubModules
from . import seeCode, getDocString, manage_pck
from . import setPreferences, setLimits

# report_diagram = False
# showGrid = True


class ArrowDynamicDown(QGraphicsPolygonItem):

    def __init__(self, parent=None):
        super(ArrowDynamicDown, self).__init__(QPolygonF([QPointF(14, -9),
                                                          QPointF(22, -9),
                                                          QPointF(22, -7),
                                                          QPointF(14, -7)]),
                                               parent)
        self.setBrush(QBrush(Qt.GlobalColor.red))
        self.setCursor(QCursor(ItemMouse.HANDLETOPITEM.value))
        self.answer = False

    def mousePressEvent(self, event):
        super(ArrowDynamicDown, self).mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self.answer = True

    def mouseReleaseEvent(self, event):
        self.answer = False


class ArrowDynamicUp(QGraphicsPolygonItem):

    def __init__(self, parent=None):
        super(ArrowDynamicUp, self).__init__(QPolygonF([QPointF(3, -9),
                                                        QPointF(6, -9),
                                                        QPointF(6, -12),
                                                        QPointF(8, -12),
                                                        QPointF(8, -9),
                                                        QPointF(11, -9),
                                                        QPointF(11, -7),
                                                        QPointF(8, -7),
                                                        QPointF(8, -4),
                                                        QPointF(6, -4),
                                                        QPointF(6, -7),
                                                        QPointF(3, -7)]),
                                             parent)
        self.setBrush(QBrush(Qt.GlobalColor.green))
        self.setCursor(QCursor(ItemMouse.HANDLETOPITEM.value))
        self.answer = False

    def mousePressEvent(self, event):
        super(ArrowDynamicUp, self).mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self.answer = True

    def mouseReleaseEvent(self, event):
        self.answer = False


class ArrowOptions(QGraphicsPolygonItem):

    def __init__(self, parent=None):
        super(ArrowOptions, self).__init__(QPolygonF([QPointF(5, -9),
                                                      # QPointF(10, -15),
                                                      QPointF(15, -9),
                                                      QPointF(10, -3)]),
                                           parent)
        self.setBrush(QBrush(Qt.GlobalColor.yellow))
        self.setCursor(QCursor(ItemMouse.HANDLETOPITEM.value))
        self.answer = False

    def mousePressEvent(self, event):
        super(ArrowOptions, self).mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self.answer = True

    def mouseReleaseEvent(self, event):
        self.answer = False


class BlockCreate(QGraphicsRectItem):

    def __init__(self, name='', unit='', category=None, w=150, h=100, listValIn=(), isMod=True, *inout, parent=None):
        super(BlockCreate, self).__init__(parent)
        self.name = name
        self.unit = unit
        self.category = category
        self.listValIn = listValIn
        self.inout = inout
        self.isMod = isMod
        self.w, self.h = w, h
        self.wmin, self.hmin = 0.0, 0.0
        self.setZValue(0)
        self.link = ''
        # self.path = QPainterPath()

        self.preview = False
        self.moved = False

        self.setAcceptHoverEvents(True)

        if self.category:
            self.editBlock(ItemColor.PROCESS_TOP.value, ItemColor.PROCESS_BOT.value, ItemColor.FRAME_PROCESS.value)
        else:
            self.editBlock(ItemColor.SUBPROCESS_TOP.value, ItemColor.SUBPROCESS_BOT.value, ItemColor.FRAME_SUBPROCESS.value)

        self.caseFinal = False
        self.currentLoop = None

    def addProbesOutputs(self):
        height = self.boundingRect().height() / 2
        i = 0
        for outp in self.outputs:
            posY = (((len(self.outputs) - 1) / 2) - i) * height / len(self.outputs)
            probe = Probes('new', outp.format, 'Value', True)
            probe.setPos(self.mapToScene(outp.pos()).x() + 100, self.mapToScene(outp.pos()).y() - 4 * posY)
            editor.diagramScene[editor.currentTab].addItem(probe)
            startConnection = Connection('', probe.inputs[0], outp, outp.format)
            startConnection.setEndPos(outp.scenePos())
            startConnection.setToPort(outp)
            nt = startConnection.link.name
            nc = probe.unit
            editor.listNodes[editor.currentTab][nt] = self.unit + ':' + outp.name + '#Node#' + nc + ':' + probe.label
            editor.listItems[editor.currentTab][nc] = probe
            i += 1
        UpdateUndoRedo()

    def addConnectorInputs(self):
        height = self.boundingRect().height() / 2
        i, k = 0, 0
        for inp in self.inputs:
            inputTaken = False
            for key, val in editor.listNodes[editor.currentTab].items():
                val = val[val.index("#Node") + 6:]
                inputTaken = (self.unit + ":" + inp.name) == val
                if inputTaken:
                    break
            if not inputTaken:
                posY = (((len(self.inputs) - 1) / 2) - i) * height / len(self.inputs)
                self.conn = ConnectorItem(inp.name, '', 80, 20, 'in', inp.format, self.listValIn[k], True)
                self.conn.setPos(self.mapToScene(inp.pos()).x() - 200, self.mapToScene(inp.pos()).y() - 4 * posY)
                editor.diagramScene[editor.currentTab].addItem(self.conn)
                startConnection = Connection('', self.conn.outputs, inp, inp.format)
                startConnection.setEndPos(inp.scenePos())
                startConnection.setToPort(inp)
                nt = startConnection.link.name
                nc = self.conn.connct
                editor.listNodes[editor.currentTab][nt] = nc + ':' + self.conn.name + '#Node#' + self.unit + ':' + inp.name
                editor.listItems[editor.currentTab][nc] = self.conn
                i += 1

                if 'U' in self.unit:
                    listVal = editor.listBlocks[editor.currentTab][self.unit]
                    ind = listVal[2][0].index(inp.name)
                    newList = []
                    for j in range(len(listVal[2][1])):
                        if j == ind:
                            oldVal = listVal[2][1][j]
                            newList.append('Node(' + nt + ')')
                        else:
                            newList.append(listVal[2][1][j])
                    del editor.listBlocks[editor.currentTab][self.unit]
                    editor.listBlocks[editor.currentTab][self.unit] = (listVal[0], listVal[1], (listVal[2][0], newList, listVal[2][2], listVal[2][3]))

                if 'M' in self.unit:
                    listVal = editor.listSubMod[editor.currentTab][self.unit]
                    ind = listVal[1][0].index(inp.name)
                    newList = []
                    for j in range(len(listVal[1][1])):
                        if j == ind:
                            oldVal = listVal[1][1][j]
                            newList.append('Node(' + nt + ')')
                        else:
                            newList.append(listVal[1][1][j])
                    del editor.listSubMod[editor.currentTab][self.unit]
                    editor.listSubMod[editor.currentTab][self.unit] = (listVal[0], (listVal[1][0], newList, listVal[1][2], listVal[1][3]), listVal[2])
            k += 1
        UpdateUndoRedo()

    def addConnectorOutputs(self):
        height = self.boundingRect().height() / 2
        i = 0
        for outp in self.outputs:
            posY = (((len(self.outputs) - 1) / 2) - i) * height / len(self.outputs)
            self.conn = ConnectorItem(outp.name, '', 70, 26, 'out', outp.format, '', True)
            self.conn.setPos(self.mapToScene(outp.pos()).x() + 100, self.mapToScene(outp.pos()).y() - 4 * posY)
            editor.diagramScene[editor.currentTab].addItem(self.conn)
            startConnection = Connection('', self.conn.inputs, outp, outp.format)
            startConnection.setEndPos(outp.scenePos())
            startConnection.setToPort(outp)
            nt = startConnection.link.name
            nc = self.conn.connct
            editor.listNodes[editor.currentTab][nt] = self.unit + ':' + outp.name + '#Node#' + nc + ':' + self.conn.name
            editor.listItems[editor.currentTab][nc] = self.conn
            i += 1
        UpdateUndoRedo()

    def addinput(self):
        UpdateUndoRedo()
        tmpnameEnters, tmpvalEnters = [], []
        tmpnameEnters = editor.listBlocks[editor.currentTab][self.unit][2][0].copy()
        tmpvalEnters = editor.listBlocks[editor.currentTab][self.unit][2][1].copy()
        tmplastEnter = tmpnameEnters[-1]
        tmplastVal = editor.getlib()[self.name][1][1][-1]

        try:
            sg = [int(s) for s in tmplastEnter.split('_') if s.isdigit()]
            newb = str(int(sg[-1]) + 1)
            tmplastEnter = tmplastEnter.replace(str(sg[-1]), newb)
        except Exception as e:
            tmplastEnter += '_0'

        tmpnameEnters.append(tmplastEnter)
        tmpvalEnters.append(tmplastVal)
        ase = ((tmpnameEnters, tmpvalEnters, editor.listBlocks[editor.currentTab][self.unit][2][2],
                editor.listBlocks[editor.currentTab][self.unit][2][3]),)
        self.updateBlock(ase, True)

    def contextMenuEvent(self, event):
        menu = QMenu()
        activ = False
        if self.name[len(self.name) - 2:] == '_d':
            activ = True

        if self.isMod:
            ac = menu.addAction('')
#             ci = menu.addAction('Add constants to all inputs')
#             ci.triggered.connect(self.addConstantsInputs)
#             menu.addSeparator()
            ap = menu.addAction('Add probes to all outputs')
            ap.triggered.connect(self.addProbesOutputs)
            menu.addSeparator()
            ac = menu.addAction('Add connectors to all inputs')
            ac.triggered.connect(self.addConnectorInputs)
            ad = menu.addAction('Add connectors to all outputs')
            ad.triggered.connect(self.addConnectorOutputs)
            menu.addSeparator()
            de = menu.addAction('Delete')
            de.triggered.connect(self.deleteItem)
            pa = menu.addAction('Parameters')
            if self.category:
                pa.triggered.connect(self.editParametersProcess)
#                 er = menu.addAction('Error handler')
#                 er.triggered.connect(self.errorHandl)
                sc = menu.addAction('See code')
                sc.triggered.connect(self.seeCode)
                ao = menu.addAction('Input options')
                ao.triggered.connect(self.inputOptions)
                if '_dyn' in self.name:
                    menu.addSeparator()
                    dya = menu.addAction('Add input dyn (+)')
                    dya.triggered.connect(self.addinput)
                    dys = menu.addAction('Remove input dyn (-)')
                    dys.triggered.connect(self.subinput)
            else:
                pa.triggered.connect(self.editParametersSubProcess)
                su = menu.addAction('See submodul')
                su.triggered.connect(self.seeSubMod)
        else:
            if self.category:
                sc = menu.addAction('See code')
                sc.triggered.connect(self.seeCode)
            else:
                su = menu.addAction('See submodul')
                su.triggered.connect(self.seeSubMod)

        menu.exec(event.screenPos())

    def editBlock(self, colorGradient1, colorGradient2, colorPen):
        # self.colorGradient1 = colorGradient1
        # self.colorGradient2 = colorGradient2
        # self.colorPen = colorPen
        gradient = QLinearGradient(QPointF(0, 0), QPointF(0, 50))
        gradient.setColorAt(0, colorGradient1)
        gradient.setColorAt(1, colorGradient2)
        
        self.setPen(QPen(colorPen, 4))
        self.setBrush(QBrush(gradient))

        if self.isMod:
            self.setFlags(self.GraphicsItemFlag.ItemIsSelectable | self.GraphicsItemFlag.ItemIsMovable | self.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setFlag(self.GraphicsItemFlag.ItemIsFocusable, True)

        self.setCursor(QCursor(ItemMouse.HANDLETOPITEM.value))
        # Label:
        self.label = QGraphicsTextItem(self.name, self)
        self.label.setDefaultTextColor(ItemColor.TEXT_LABEL_PROCESS.value)
        self.label.setFont(QFont("Times", 16, QFont.Weight.Bold))

        self.nameUnit = QGraphicsTextItem(self.unit, self)
        self.nameUnit.setDefaultTextColor(ItemColor.DEFAULTTEXTCOLOR.value)
        self.nameUnit.setFont(QFont("Times", 12, QFont.Weight.Bold))

        self.box_title = QGraphicsRectItem(self)
        # self.box_title.setBrush(QBrush(ItemColor.BACKGROUND.value))
        self.box_title.setPen(QPen(Qt.PenStyle.NoPen))
        self.box_title.setZValue(-2)
        self.box_title.setParentItem(self)

        wminIn = 0.0
        self.inputs, self.outputs = [], []
        i = 0
        if self.listValIn:
            for i, j in enumerate(self.listValIn):
                typ = 'str'
                # if type(j).__name__ not in 'str' or type(j).__name__ not in 'tuple' or j == 'path' or 'enumerate' in j:
                if type(j).__name__ not in 'str' or j == 'path' or 'enumerate' in j:
                    try:
                        typ = DefinitType(eval(j)).returntype()
                    except Exception as e:
                        typ = DefinitType(j).returntype()
                portIn = Port(self.inout[0][0][i], 'in', typ, self.unit, True, self.isMod, 4, -16, self)
                self.inputs.append(portIn)
                if wminIn < portIn.label.boundingRect().width():
                    wminIn = portIn.label.boundingRect().width()
                i += 1

        wminOut = 0.0
        for i in range(len(self.inout[0][2])):
            portOut = Port(self.inout[0][2][i], 'out', self.inout[0][3][i], self.unit, True, self.isMod, 4, -16, self)
            self.outputs.append(portOut)
            if wminOut < portOut.label.boundingRect().width():
                wminOut = portOut.label.boundingRect().width()

        gridSize = ItemGrid.SPACEGRID.value
        self.wmin = wminIn + 20 + wminOut
        self.wmin = round(self.wmin / gridSize) * gridSize

        factorh = 20
        self.hmin = factorh * len(self.inputs)
        if self.hmin < factorh * len(self.outputs):
            self.hmin = factorh * len(self.outputs)

        self.wmin, self.hmin = round(self.wmin / gridSize) * gridSize, gridSize + round(self.hmin / gridSize) * gridSize

        x, y = self.newSize(self.w, self.h)
        # self.path.addRoundedRect(0.0, 0.0, x, y, 10, 10)

        if '_dyn' in self.name:
            self.polUp = ArrowDynamicUp(self)
            self.polUp.setPos(0, y)

            self.polDown = ArrowDynamicDown(self)
            self.polDown.setPos(0, y)

        if self.category:
            cat = self.category.split('.')
            pathYml = os.path.dirname(os.path.realpath(__file__))
            pathYml = os.path.join(pathYml, '../modules', cat[0], cat[1] + ".yml")
            if os.path.exists(pathYml):
                with open(pathYml, 'r', encoding='utf8') as stream:
                    dicts = yaml.load(stream, yaml.FullLoader)
                    if self.name in dicts:
                        self.polOp = ArrowOptions(self)
                        self.polOp.setPos(0, y)

        if self.isMod:
            self.resize = Slide(self)
            self.resize.setPos(x, y)
            self.ongrid = True
            self.resize.posChangeCallbacks.append(self.newSize)  # Connect the callback
            self.resize.setFlag(self.resize.GraphicsItemFlag.ItemIsSelectable, True)
            self.resize.wmin = self.wmin
            self.resize.hmin = self.hmin

    def newSize(self, w, h):
        # Limit the block size:
        if h < self.hmin:
            h = self.hmin + 2
        if w < self.wmin:
            w = self.wmin

        gridSize = ItemGrid.SPACEGRID.value
        w, h = round(w / gridSize) * gridSize, round(h / gridSize) * gridSize

        self.setRect(0.0, 0.0, w, h)
        self.box_title.setRect(-1, -24, w + 2, 22)

        # center label:
        rect = self.label.boundingRect()
        lw, lh = rect.width(), rect.height()
        lx, ly = (w - lw) / 2, (-30)
        self.label.setPos(lx, ly - 5)
        # bottom name unit:
        rect = self.nameUnit.boundingRect()
        lw, lh = rect.width(), rect.height()
        lx, ly = (w - lw) / 2, (h)
        self.nameUnit.setPos(lx, ly)
        # Update port positions:
        if len(self.inputs) == 1:
            self.inputs[0].setPos(0, h / 2)
        elif len(self.inputs) > 1:
            y = (h) / (len(self.inputs) + 1)
            dy = (h) / (len(self.inputs) + 1)
            for inp in self.inputs:
                inp.setPos(0, y)
                y += dy

        if len(self.outputs) == 1:
            self.outputs[0].setPos(w, h / 2)

        elif len(self.outputs) > 1:
            y = (h) / (len(self.outputs) + 1)
            dy = (h) / (len(self.outputs) + 1)
            for outp in self.outputs:
                outp.setPos(w, y)
                y += dy

        try:
            self.polUp.setPos(0, h)
            self.polDown.setPos(0, h)
        except Exception as e:
            pass

        try:
            self.polOp.setPos(0, h)
        except Exception as err:
            pass

        return w, h

    def hoverEnterEvent(self, event):
        # self.setFocus(True)
        # pos = event.screenPos()
        if self.category:
            self.showToolTip()
        event.accept()

    def itemChange(self, *args, **kwargs):
        gridSize = ItemGrid.SPACEGRID.value
        if args[0] == self.GraphicsItemChange.ItemPositionHasChanged:
            xV = round(args[1].x() / gridSize) * gridSize
            yV = round(args[1].y() / gridSize) * gridSize
            self.setPos(QPointF(xV, yV))
        return QGraphicsRectItem.itemChange(self, *args, **kwargs)

    def editParametersProcess(self):
        cat = self.category.split('.')
        listValDefault = editor.getlib()[self.name][1][1]
        if not listValDefault:
            listValDefault = ()
        if '_dyn' in self.name:
            tmplistVal = self.inout[0][1]
            tmpList = []
            for indDef in listValDefault:
                tmpList.append(indDef)
            for i in range(len(listValDefault), len(tmplistVal)):
                tmpList.append(tmpList[-1])
            listValDefault = tmpList
        else:
            pathYml = os.path.dirname(os.path.realpath(__file__))
            pathYml = os.path.join(pathYml, '../modules', cat[0], cat[1] + ".yml")
            if os.path.exists(pathYml):
                with open(pathYml, 'r', encoding='utf8') as stream:
                    dicts = yaml.load(stream, yaml.FullLoader)
                    try:
                        for el in dicts[self.name]:
                            if el in editor.listBlocks[editor.currentTab][self.unit][2][0]:
                                if type(dicts[self.name][el]).__name__ == 'str':
                                    if 'enumerate' in dicts[self.name][el]:
                                        listValDefault = (*listValDefault, dicts[self.name][el])
                                    else:
                                        try:
                                            listValDefault = (*listValDefault, eval(dicts[self.name][el]))
                                        except Exception as e:
                                            listValDefault = (*listValDefault, dicts[self.name][el])
                                else:
                                    try:
                                        listValDefault = (*listValDefault, eval(dicts[self.name][el]))
                                    except Exception as e:
                                        listValDefault = (*listValDefault, dicts[self.name][el])
                    except Exception as er:
                        pass
                        # print('error 1 :', er)
        c = editParam(self.name, self.unit, editor.listBlocks[editor.currentTab][self.unit][2], listValDefault)
        c.exec()
        listVal = editor.listBlocks[editor.currentTab][self.unit]
        try:
            del editor.listBlocks[editor.currentTab][self.unit]
            editor.listBlocks[editor.currentTab][self.unit] = (listVal[0], listVal[1], (listVal[2][0], c.getNewValues(), listVal[2][2], listVal[2][3]))
        except Exception as e:
            editor.listBlocks[editor.currentTab][self.unit] = listVal

    def editParametersSubProcess(self):
        c = editParam(self.name, self.unit, editor.listSubMod[editor.currentTab][self.unit][1], editor.libSubMod[self.name][1])
        c.exec()
        listVal = editor.listSubMod[editor.currentTab][self.unit]
        try:
            del editor.listSubMod[editor.currentTab][self.unit]
            editor.listSubMod[editor.currentTab][self.unit] = (listVal[0], (listVal[1][0], c.getNewValues(), listVal[1][2], listVal[1][3]), listVal[2])
        except Exception as e:
            editor.listSubMod[editor.currentTab][self.unit] = listVal

    def errorHandl(self):
        c = errorHandler(self.name, self.unit)
        c.exec()

    def seeCode(self):
        c = seeCode(self.category, self.name, editor)
        c.exec()

    def foncedBlock(self, fcd):
        if fcd:
            self.setOpacity(0.4)
        else:
            self.setOpacity(1.0)

    def mouseMoveEvent(self, mouseEvent):
        mouseEvent.accept()
        editor.loopMouseMoveEvent(self, mouseEvent.scenePos())
        return QGraphicsRectItem.mouseMoveEvent(self, mouseEvent)

    def mouseReleaseEvent(self, event):
        editor.loopMouseReleaseEvent(self, True)
        return QGraphicsRectItem.mouseReleaseEvent(self, event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            try:
                editor.diagramScene[editor.currentTab].clearSelection()
            except Exception as err:
                pass
            self.setSelected(True)

        if event.button() == Qt.MouseButton.LeftButton and self.isMod:
            if not self.isSelected():
                editor.diagramScene[editor.currentTab].clearSelection()
                self.setSelected(True)
            else:
                for lstLoop, ItemsLoop in editor.listTools[editor.currentTab].items():
                    if self.unit in ItemsLoop:
                        editor.diagramScene[editor.currentTab].clearSelection()
                        self.setSelected(True)
                        break

            try:
                if self.polUp.answer:
                    self.addinput()
                if self.polDown.answer:
                    self.subinput()
                    self.polUp.answer = False
                    self.polDown.answer = False
            except Exception as err:
                pass

            try:
                if self.polOp.answer:
                    self.inputOptions()
                    self.polOp.answer = False
            except Exception as err:
                pass

            if 'U' in self.unit:
                b1 = BlockCreate(self.name, '', editor.getlib()[self.name][0], 150, 100, editor.getlib()[self.name][1][1], False, editor.getlib()[self.name][1])
                b1.preview = True
                textSource = 'Source : ' + editor.getlib()[self.name][0]
                TreeLibrary().showModel(b1, textSource)
            else:
                bm = BlockCreate(self.name, '', None, 150, 100, editor.libSubMod[self.name][1], False, editor.libSubMod[self.name])
                TreeLibrary().showModel(bm, '')

        event.accept()
#         if event.button() == 1 and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
#             editor.blockSelection(self)
#         return QGraphicsRectItem.mousePressEvent(self, event)

    def mouseDoubleClickEvent(self, event):
        if self.isMod:
            if self.category:
                self.editParametersProcess()
            else:
                self.editParametersSubProcess()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            self.setPos(self.x(), self.y() - 1)
        elif event.key() == Qt.Key.Key_Down:
            self.setPos(self.x(), self.y() + 1)
        elif event.key() == Qt.Key.Key_Left:
            self.setPos(self.x() - 1, self.y())
        elif event.key() == Qt.Key.Key_Right:
            self.setPos(self.x() + 1, self.y())
        elif event.key() == Qt.Key.Key_Plus and '_dyn' in self.name:
            self.addinput()
        elif event.key() == Qt.Key.Key_Minus and '_dyn' in self.name:
            self.subinput()
        elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_U:
            if self.link:
                webbrowser.open(self.link)

    def showToolTip(self):
        self.link = ''
        c = getDocString(self.category, self.name)
        txt = c.getComment()
        numbLines = len(txt.split("\n"))
        sizefont = "9"
        if numbLines > 40:
            sizefont = "8"
        if numbLines > 80:
            sizefont = "6"
        if 'link_web' in txt:
            tmp = txt[txt.index('link_web:')+9:]
            if 'http' in tmp:
                try:
                    self.link += tmp[0:tmp.index('\n')].strip()
                except Exception as err:
                    self.link += tmp.strip()
            elif 'Nipype' in self.category and 'Config_nipype' not in self.category:
                self.link = 'https://nipype.readthedocs.io/en/latest/api/generated/'
                modul = self.category.replace('_', '.').lower()
                modul += '.html#'
                clss = self.name[self.name.index('_') + 1:].lower()
                self.link += modul + clss

        txt = txt.replace('<', '&lt;')
        txt = txt.replace('>', '&gt;')
        txt_html = "<pre><p style=\"background-color: #ffffff;\">"
        txt_html += "<span style=\" \
                     font-size:11pt; \
                     font-family:Calibri; \
                     font-weight:1000; \
                     color:#000000; \" > " + self.name + ":</span><br>"
        txt_html += "<span style=\" \
                     font-size:" + sizefont + "pt; \
                     font-family:Calibri; \
                     font-weight:1000; \
                     color:#3060EE; \" > " + txt + "</span>"
        txt_html += "</p></pre>"
        self.setToolTip(txt_html)

    def inputOptions(self):
        cat = self.category.split('.')
        pathYml = os.path.dirname(os.path.realpath(__file__))
        pathYml = os.path.join(pathYml, '../modules', cat[0], cat[1] + ".yml")

        if os.path.exists(pathYml):
            lvl = editor.listBlocks.copy()[editor.currentTab][self.unit]
            with open(pathYml, 'r', encoding='utf8') as stream:
                dicts = yaml.load(stream, yaml.FullLoader)
            try:
                dicts[self.name]
                c = chOptions(pathYml, self.name, lvl[2], editor)
                c.exec()
                if c.getAnswer() == "cancel":
                    return
                UpdateUndoRedo()
                asq = (c.getNewValues()[0],)
                self.updateBlock(asq, True)
            except (OSError, KeyError) as err:
                editor.editText("No options available", 10, 600, 'ff0000', False, True)
        else:
            editor.editText("No options available", 10, 600, 'ff0000', False, True)

        # UpdateUndoRedo()

    def subinput(self):
        UpdateUndoRedo()
        tmpnameEnters = []
        tmpvalEnters = []
        tmpnameEnters = editor.listBlocks[editor.currentTab][self.unit][2][0].copy()
        tmpvalEnters = editor.listBlocks[editor.currentTab][self.unit][2][1].copy()
        tmplastEnter = tmpnameEnters[-1]
        tmplastVal = tmpvalEnters[-1]

        tmpListLink = []
        for key, val in editor.listNodes[editor.currentTab].items():
            tmpListLink.append(val[val.index('#Node#') + 6:len(val)])

        if len(tmpnameEnters) > len(editor.getlib()[self.name][1][0]):
            if tmpListLink:
                if self.unit + ':' + tmplastEnter in tmpListLink:
                    return
            del tmpnameEnters[-1]
            del tmpvalEnters[-1]
            ase = ((tmpnameEnters, tmpvalEnters, editor.listBlocks[editor.currentTab][self.unit][2][2],
                    editor.listBlocks[editor.currentTab][self.unit][2][3]),)
            self.updateBlock(ase, True)

    def updateBlock(self, newListVal, resize_bl):
        try:
            diagram = editor.undoredoTyping[editor.currentTab][len(editor.undoredoTyping[editor.currentTab]) - 1]
        except Exception as e:
            try:
                diagram = editor.undoredoTyping[editor.currentTab][0]
            except Exception as e:
                diagram = SaveDiagram().toPlainText()

        unddiagram = diagram[diagram.index("block=[" + self.unit + "]"):]

        try:
            unddiagram = unddiagram[0:unddiagram.index("\n") + 1]
        except Exception as e:
            pass

        diagram = diagram.replace(unddiagram, "")

        for item in editor.diagramScene[editor.currentTab].items():
            editor.diagramScene[editor.currentTab].removeItem(item)
        if resize_bl:
            x, y = self.sceneBoundingRect().width() - 2, self.sceneBoundingRect().height() - 2
        else:
            x, y = 150, 80
        block = ProcessItem(self.unit, self.name, self.category, x, y, *newListVal).getBlocks()
        block.setPos(self.scenePos())

        coord = block.sceneBoundingRect()
        rect = block.rect()
        diagram += '\nblock=[' + self.unit + \
                   '] category=[' + self.category + \
                   '] class=[' + self.name + \
                   '] valInputs=[' + str(editor.listBlocks[editor.currentTab][self.unit][2]) + \
                   '] RectF=[' + str((coord.x() + 2, coord.y() + 2, rect.width() - 2, rect.height() - 2)) + \
                   ']'
        LoadDiagram(diagram.splitlines())
        UpdateList(diagram)
        editor.undoredoTyping[editor.currentTab][len(editor.undoredoTyping[editor.currentTab])] = diagram

    def deleteItem(self):
        for elem in editor.diagramView[editor.currentTab].items():
            if type(elem) is LinkItem:
                if editor.listNodes[editor.currentTab][elem.name].find(self.unit + ':') != -1:
                    self.deletelink(elem, self.unit)
        editor.diagramScene[editor.currentTab].removeItem(self)
        del editor.listItems[editor.currentTab][self.unit]
        if self.category:
            del editor.listBlocks[editor.currentTab][self.unit]
            # editor.listBlocks[editor.currentTab] = ReorderList(editor.listBlocks[editor.currentTab]).getNewList()
        else:
            del editor.listSubMod[editor.currentTab][self.unit]
            # editor.listSubMod[editor.currentTab] = ReorderList(editor.listSubMod[editor.currentTab]).getNewList()
        editor.deleteItemsLoop(self)
        # editor.listNodes[editor.currentTab] = ReorderList(editor.listNodes[editor.currentTab]).getNewList()
#         UpdateUndoRedo()

    def deletelink(self, linkEle, unt):
        nameItem = editor.listNodes[editor.currentTab][linkEle.name]
        nameItemTmp0 = nameItem[0:nameItem.index('#Node#')]
        unitTmp0 = nameItemTmp0[0:nameItemTmp0.index(':')]
        nameItemTmp0 = nameItemTmp0[nameItemTmp0.index(':') + 1:len(nameItemTmp0)]
        if 'C' in unitTmp0:
            for elem in editor.diagramView[editor.currentTab].items():
                if type(elem) is Port:
                    if elem.unit == unitTmp0:
                        other = False
                        for lstNode in editor.listNodes[editor.currentTab]:
                            if not lstNode == linkEle.name:
                                tmpq = editor.listNodes[editor.currentTab][lstNode]
                                tmpq = tmpq[0:tmpq.index(':')]
                                if tmpq == unitTmp0:
                                    other = True
                                    break
                        if not other:
                            elem.setBrush(QBrush(TypeColor.unkn.value))
                            elem.label.setPlainText('unkn')
                            elem.format = 'unkn'
                            elem.name = 'unkn'
                            elem.label.setPos(elem.pos().x() - 160 - elem.label.boundingRect().size().width(), elem.label.pos().y())
                            tmp = editor.listConnects[editor.currentTab][elem.unit]
                            del editor.listConnects[editor.currentTab][elem.unit]
                            if 'in' in tmp[0]:
                                editor.listConnects[editor.currentTab][elem.unit] = (tmp[0], 'unkn', 'unkn', '')

        nameItem = editor.listNodes[editor.currentTab][linkEle.name]
        nameItemTmp = nameItem[0:nameItem.index('#Node#')]
        unitTmp = nameItemTmp[0:nameItemTmp.index(':')]
        if unitTmp == unt:
            nameItemTmp = nameItem[nameItem.index('#Node#') + 6:len(nameItem)]
            unitTmp = nameItemTmp[0:nameItemTmp.index(':')]
            nameItemTmp = nameItemTmp[nameItemTmp.index(':') + 1:len(nameItemTmp)]
            if 'C' in unitTmp:
                for elem in editor.diagramView[editor.currentTab].items():
                    if type(elem) is Port:
                        if elem.unit == unitTmp:
                            elem.setBrush(QBrush(TypeColor.unkn.value))
                            elem.label.setPlainText('unkn')
                            elem.format = 'unkn'
                            elem.name = 'unkn'
                            tmp = editor.listConnects[editor.currentTab][elem.unit]
                            del editor.listConnects[editor.currentTab][elem.unit]
                            editor.listConnects[editor.currentTab][elem.unit] = (tmp[0], 'unkn', 'unkn')
            if 'P' in unitTmp:
                for elem in editor.diagramView[editor.currentTab].items():
                    if type(elem) is Port:
                        if elem.unit == unitTmp:
                            elem.setBrush(QBrush(TypeColor.unkn.value))
                            elem.format = 'unkn'
                            tmp = editor.listProbes[editor.currentTab][elem.unit]
                            del editor.listProbes[editor.currentTab][elem.unit]
                            editor.listProbes[editor.currentTab][elem.unit] = ('unkn', tmp[1])
            if 'U' in unitTmp:
                listVal = editor.listBlocks[editor.currentTab][unitTmp]
                mod = listVal[0]
                category = listVal[1]
                cat = category.split('.')
                listEnter = editor.getlib()[mod][1][0]
                listValDefault = editor.getlib()[mod][1][1]
                if not listValDefault:
                    listValDefault = ()
                if len(listEnter) != len(listVal[2][1]):
                    if '_dyn' in mod:
                        listEnter = listVal[2][0]
                        tmplistVal = listVal[2][1]
                        tmpList = []
                        for indDef in listValDefault:
                            tmpList.append(indDef)
                        for i in range(len(listValDefault), len(tmplistVal)):
                            tmpList.append(tmpList[-1])
                        listValDefault = tmpList
                    else:
                        pathYml = os.path.dirname(os.path.realpath(__file__))
                        pathYml = os.path.join(pathYml, '../modules', cat[0], cat[1] + ".yml")
                        if os.path.exists(pathYml):
                            with open(pathYml, 'r', encoding='utf8') as stream:
                                dicts = yaml.load(stream, yaml.FullLoader)
                                for el in dicts[mod]:
                                    if el in listVal[2][0]:
                                        listEnter = (*listEnter, el)
                                        if type(dicts[mod][el]).__name__ == 'str':
                                            if 'enumerate' in dicts[mod][el]:
                                                listValDefault = (*listValDefault, dicts[mod][el])
                                            else:
                                                try:
                                                    listValDefault = (*listValDefault, eval(dicts[mod][el]))
                                                except Exception as e:
                                                    listValDefault = (*listValDefault, dicts[mod][el])
                                        else:
                                            try:
                                                listValDefault = (*listValDefault, eval(dicts[mod][el]))
                                            except Exception as e:
                                                listValDefault = (*listValDefault, dicts[mod][el])
                ###############################################################################
                newList = []
                for i in range(len(listEnter)):
                    if listEnter[i] == nameItemTmp:
                        newValfromModules = listValDefault[i]

                        if type(newValfromModules).__name__ == 'str':
                            if 'enumerate' in newValfromModules:
                                newValfromModules = list(eval(newValfromModules))[0][1]
                        newList.append(newValfromModules)
                    else:
                        newList.append(listVal[2][1][i])
                ###############################################################################

                del editor.listBlocks[editor.currentTab][unitTmp]
                editor.listBlocks[editor.currentTab][unitTmp] = (listVal[0], listVal[1], (listVal[2][0], newList, listVal[2][2], listVal[2][3]))

            elif 'M' in unitTmp:
                listVal = editor.listSubMod[editor.currentTab][unitTmp]
                mod = listVal[0]
                ind = listVal[1][0].index(nameItemTmp)
                newValfromModules = editor.libSubMod[mod][1][ind]

                if type(newValfromModules).__name__ == 'str':
                    if 'enumerate' in newValfromModules:
                        newValfromModules = list(eval(newValfromModules))[0][1]

                newList = []
                for i in range(len(listVal[1][1])):
                    if i == ind:
                        newList.append(newValfromModules)
                    else:
                        newList.append(listVal[1][1][i])

                del editor.listSubMod[editor.currentTab][unitTmp]
                editor.listSubMod[editor.currentTab][unitTmp] = (listVal[0], (listVal[1][0], newList, listVal[1][2], listVal[1][3]), listVal[2])

        editor.deleteLinksLoop(linkEle)

        editor.diagramScene[editor.currentTab].removeItem(linkEle)
        editor.diagramScene[editor.currentTab].removeItem(linkEle.getlinkTxt())
        editor.diagramScene[editor.currentTab].removeItem(linkEle.getlinkShow())
        editor.diagramScene[editor.currentTab].removeItem(linkEle.getBislink())
        del editor.listNodes[editor.currentTab][linkEle.name]

    def seeSubMod(self):
        for lstWind in editor.mdi.subWindowList():
            if (self.name + '.mod') in lstWind.windowTitle():
                editor.mdi.setActiveSubWindow(lstWind)
                return

        editor.addSubWindow(self.name + '.mod')
        path_submod = os.path.dirname(os.path.realpath(__file__))
        file = os.path.join(path_submod, '..', 'submodules', editor.libSubMod[self.name][4], self.name + '.mod')
        editor.pathDiagram[editor.currentTab] = file
        editor.infopathDgr.setText(file)
        f = open(file, 'r', encoding='utf8')
        txt = f.readlines()
        f.close()
        try:
            LoadDiagram(txt)
            editor.diagramView[editor.currentTab].fitInView(editor.diagramScene[editor.currentTab].sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        except Exception as e:
            editor.editText('Error with some modules/submodules, see in {}'.format(file),
                            10, 600, 'ff0000', False, True)
            
    # def paint(self, painter: QPainter, option, widget=None):
    # #     gradient = QLinearGradient(QPointF(0, 0), QPointF(0, 50))
    # #     gradient.setColorAt(0, self.colorGradient1)
    # #     gradient.setColorAt(1, self.colorGradient2)
    # #
    # #     self.setPen(QPen(self.colorPen, 4))
    # #     self.setBrush(QBrush(gradient))
    # #     # brush = QBrush(QColor("#3498db"))
    # #     # painter.setBrush(brush)
    # #     # painter.setPen(self.pen())
    # #     # Dessine un rectangle avec coins arrondis (rx=10, ry=10)
    #     painter.drawRoundedRect(self.rect(), 10, 10)


class BlocksProjects(QTextEdit):

    def __init__(self, diagram, parent=None):
        super(BlocksProjects, self).__init__(parent)

        self_dir_path = os.path.dirname(os.path.realpath(__file__))
        self_dir_path = os.path.dirname(self_dir_path)
        txt = diagram.splitlines()
        for line in txt:
            if line[0:5] == 'block':
                catg = line[line.index("category")+10:line.index("] class")]
                cls = line[line.index("class")+7:line.index("] valInputs")]
                module = importlib.import_module('NodeEditor.modules.' + catg)
                try:
                    cl = getattr(module, cls)
                    self.append(inspect.getsource(cl))
                except Exception as err:
                    pass
        for line in txt:
            if line[0:6] == 'submod':
                catg = line[line.index("nameMod")+10:line.index("] valInputs")]


class Checkbox(QGraphicsRectItem):

    def __init__(self, unit='', listItm=[], label='', isMod=True, parent=None):
        super(Checkbox, self).__init__(parent)

        self.setCursor(QCursor(ItemMouse.HANDLETOPITEM.value))

        self.isMod = isMod
        self.form = 'list_str'
        self.format = self.form

        self.setZValue(2)
        if self.isMod:
            self.setFlags(self.GraphicsItemFlag.ItemIsSelectable | self.GraphicsItemFlag.ItemIsMovable | self.GraphicsItemFlag.ItemSendsGeometryChanges)
            self.setFlag(self.GraphicsItemFlag.ItemIsFocusable, True)
            self.setAcceptHoverEvents(True)

        if unit == 'newCheckbox':
            ConstantExist = True
            inc = 0
            while ConstantExist:
                if 'A' + str(inc) in editor.listConstants[editor.currentTab]:
                    inc += 1
                else:
                    ConstantExist = False
            self.unit = 'A' + str(inc)
        else:
            self.unit = unit

        self.label = label if label else 'checkbox'

        self.listCheckBox = []
        self.listItemsBox = listItm
        self.grid = QGridLayout()
        self.elemProxy = QWidget()

        for i, v in enumerate(listItm):
            if '*' in v:
                self.listCheckBox.append(QCheckBox(v[0:-1]))
                self.listCheckBox[-1].setChecked(True)
            else:
                self.listCheckBox.append(QCheckBox(v))
            self.listCheckBox[-1].clicked.connect(self.checkboxChanged)
            self.grid.addWidget(self.listCheckBox[-1], i, 0)

        self.elemProxy.setLayout(self.grid)

        self.proxyWidget = QGraphicsProxyWidget(self, Qt.WindowType.Widget)
        self.proxyWidget.setWidget(self.elemProxy)
        self.proxyWidget.setPos(3, 3)
        self.proxyWidget.setZValue(3)

        self.w = self.proxyWidget.boundingRect().size().width() + 15
        self.h = self.proxyWidget.boundingRect().size().height() + 6

        # gridSize = ItemGrid.SPACEGRID.value
        # self.w, self.h = round(self.w / gridSize) * gridSize, round(self.h / gridSize) * gridSize

        self.lab = QGraphicsTextItem(self.label, self)
        self.lab.setDefaultTextColor(ItemColor.DEFAULTTEXTCOLOR.value)
        self.lab.setFont(QFont("Times", 12, QFont.Weight.Bold))
        self.lab.setPos(0, -30)
        self.lab.setVisible(True)

        self.setPen(QPen(ItemColor.FRAME_CONSTANTS.value, 3))
        color = TypeColor.str.value
        self.setBrush(QBrush(color))
        self.setRect(0.0, 0.0, self.w, self.h)

        self.inputs, self.outputs = [], []
        self.outputs.append(Port('', 'out', 'list_str', self.unit, True, self.isMod, 80, -12, self))
        self.outputs[0].setPos(self.w + 2, self.h / 2)
        if self.isMod:
            self.updateListItems()

    def checkboxChanged(self):
        self.listItemsBox = []
        for lstCh in self.listCheckBox:
            tmp = lstCh.text().replace('*', '')
            if lstCh.checkState():
                self.listItemsBox.append(tmp + '*')
            else:
                self.listItemsBox.append(tmp)
        if self.isMod:
            self.updateListItems()

    def updateListItems(self):
        editor.listConstants[editor.currentTab][self.unit] = (self.form, self.listItemsBox, self.label)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            self.setPos(self.x(), self.y() - 1)
        if event.key() == Qt.Key.Key_Down:
            self.setPos(self.x(), self.y() + 1)
        if event.key() == Qt.Key.Key_Left:
            self.setPos(self.x() - 1, self.y())
        if event.key() == Qt.Key.Key_Right:
            self.setPos(self.x() + 1, self.y())
#         return QGraphicsRectItem.keyPressEvent(self, *args, **kwargs)

    def mouseDoubleClickEvent(self, event):
        if self.isMod:
            self.editCheckBox()

    def editCheckBox(self):
        tmp = []
        for el in self.listItemsBox:
            tmp.append(el.replace('*', ''))
        p = editCombobox(tmp)
        p.exec()
        if p.getAnswer() == 'ok':
            newList = p.getNewList()
            del self.listCheckBox
            self.listCheckBox = []
            self.listItemsBox = []
            self.elemProxy.deleteLater()
            self.proxyWidget.deleteLater()
            self.grid.deleteLater()
            self.grid = QGridLayout()
            for i, v in enumerate(newList):
                if v:
                    self.listItemsBox.append(v)
                    self.listCheckBox.append(QCheckBox(v))
                    self.listCheckBox[-1].clicked.connect(self.checkboxChanged)
                    self.grid.addWidget(self.listCheckBox[-1], i, 0)
            self.elemProxy = QWidget()
            self.elemProxy.setLayout(self.grid)
            self.proxyWidget = QGraphicsProxyWidget(self, Qt.WindowType.Widget)
            self.proxyWidget.setWidget(self.elemProxy)
            self.proxyWidget.setPos(3, 3)
            self.proxyWidget.setZValue(3)
            w = self.proxyWidget.boundingRect().size().width() + 15
            h = self.proxyWidget.boundingRect().size().height() + 6
            self.setRect(0.0, 0.0, w, h)
            self.outputs[0].setPos(w + 2, h / 2)
            self.updateListItems()

    def contextMenuEvent(self, event):
        if self.isMod:
            menu = QMenu()
            de = menu.addAction('Delete')
            de.triggered.connect(self.deleteItem)
            ca = menu.addAction('Check on all items')
            ca.triggered.connect(self.checkOn)
            fa = menu.addAction('Check off all items')
            fa.triggered.connect(self.checkOff)
            pa = menu.addAction('Change label')
            pa.triggered.connect(self.changeLabel)
            ed = menu.addAction('Edit (double click)')
            ed.triggered.connect(self.editCheckBox)
            menu.exec(event.screenPos())

    def deleteItem(self):
        for elem in editor.diagramView[editor.currentTab].items():
            if type(elem) is LinkItem:
                if editor.listNodes[editor.currentTab][elem.name].find(self.unit + ':') != -1:
                    BlockCreate.deletelink(self, elem, self.unit)
        editor.diagramScene[editor.currentTab].removeItem(self)
        del editor.listConstants[editor.currentTab][self.unit]
        del editor.listItems[editor.currentTab][self.unit]
        editor.deleteItemsLoop(self)
#         UpdateUndoRedo()

    def itemChange(self, *args, **kwargs):
        gridSize = ItemGrid.SPACEGRID.value
        if args[0] == self.GraphicsItemChange.ItemPositionHasChanged:
            xV = round(args[1].x() / gridSize) * gridSize
            yV = round(args[1].y() / gridSize) * gridSize
            self.setPos(QPointF(xV, yV))
        return QGraphicsRectItem.itemChange(self, *args, **kwargs)

    def checkOn(self):
        self.listItemsBox = []
        for lstCh in self.listCheckBox:
            if not lstCh.checkState():
                lstCh.setChecked(True)
            self.listItemsBox.append(lstCh.text()+'*')
        if self.isMod:
            self.updateListItems()

    def checkOff(self):
        self.listItemsBox = []
        for lstCh in self.listCheckBox:
            if lstCh.checkState():
                lstCh.setChecked(False)
            self.listItemsBox.append(lstCh.text())
        if self.isMod:
            self.updateListItems()

    def changeLabel(self):
        listLabCts = []
        for x, y in editor.listConstants[editor.currentTab].items():
            listLabCts.append(y[2])
        listVal = editor.listConstants[editor.currentTab][self.unit]
        oldVal = listVal[2]
        c = changeLabel('Const', self.unit, oldVal)
        c.exec()
        try:
            self.label = c.getNewLabel()
            if self.label in listLabCts:
                self.label += '-b'
            self.lab.setPlainText(self.label)
            del editor.listConstants[editor.currentTab][self.unit]
            editor.listConstants[editor.currentTab][self.unit] = (listVal[0], listVal[1], self.label)
            UpdateUndoRedo()
        except OSError as err:
            print("OS error: {0}".format(err))
        if self.isMod:
            self.updateListItems()


class Clusters(QGraphicsRectItem):
    def __init__(self, unit='', w=80, h=30, val='', form='', label='', isMod=True, parent=None):
        super(Clusters, self).__init__(parent)

        self.isMod = isMod
        self.setCursor(QCursor(ItemMouse.HANDLETOPITEM.value))
        self.caseFinal = False
        self.currentLoop = None
        self.moved = False
        self.val = val
        self.form = form
        self.setZValue(2)
        self.preview = False

        if self.isMod:
            self.setFlags(self.GraphicsItemFlag.ItemIsSelectable | self.GraphicsItemFlag.ItemIsMovable | self.GraphicsItemFlag.ItemSendsGeometryChanges)
            self.setFlag(self.GraphicsItemFlag.ItemIsFocusable, True)
            self.setAcceptHoverEvents(True)

        if unit == 'newCluster':
            ConstantExist = True
            inc = 0
            while ConstantExist:
                if 'A' + str(inc) in editor.listConstants[editor.currentTab]:
                    inc += 1
                else:
                    ConstantExist = False
            self.unit = 'A' + str(inc)
        else:
            self.unit = unit

        self.label = label if label else 'cluster'

        self.format = form

        if 'int' in form:
            self.color = TypeColor.int.value
            self.tp = QSpinBox()
        elif 'float' in form:
            self.color = TypeColor.float.value
            self.tp = QDoubleSpinBox()
        elif 'str' in form:
            self.color = TypeColor.str.value
            self.tp = QTextEdit()
        elif 'bool' in form:
            self.color = TypeColor.bool.value
            self.tp = QComboBox()
            self.tp.addItems(['True', 'False'])

        # self.w = 100 + 15
        # self.h = 28 + 5

        self.proxyWidget = []
        self.w, self.h = w, h

        self.lab = QGraphicsTextItem(self.label, self)
        self.lab.setDefaultTextColor(ItemColor.DEFAULTTEXTCOLOR.value)
        self.lab.setFont(QFont("Times", 12, QFont.Weight.Bold))
        self.lab.setPos(0, -30)
        self.lab.setVisible(True)

        self.infoDim = QGraphicsTextItem()
        self.infoDim = QGraphicsTextItem(self.label, self)
        self.infoDim.setDefaultTextColor(ItemColor.DEFAULTTEXTCOLOR.value)
        self.infoDim.setFont(QFont("Times", 12, QFont.Weight.Bold))
        self.infoDim.setVisible(True)

        self.wmin = 115
        self.hmin = 33
        self.setPen(QPen(ItemColor.FRAME_CONSTANTS.value, 3))
        self.setBrush(QBrush(self.color))
        self.setRect(0.0, 0.0, self.w, self. h)
        self.inputs, self.outputs = [], []
        self.outputs.append(Port('', 'out', self.format, self.unit, True, self.isMod, 80, -12, self))
        self.outputs[0].setPos(self.w + 2, self.h / 2)

        if self.isMod:
            editor.listConstants[editor.currentTab][self.unit] = (self.form, self.val, self.label)
        x, y = self.load(val)
        self.val = val

        if self.isMod:
            del editor.listConstants[editor.currentTab][self.unit]
            editor.listConstants[editor.currentTab][self.unit] = (self.form, self.val, self.label)

        # if self.isMod:
            self.resize = Slide(self)
            self.resize.setPos(x + 2, y)
            self.resize.posChangeCallbacks.append(self.newSize)  # Connect the callback
            self.resize.setFlag(self.resize.GraphicsItemFlag.ItemIsSelectable, True)
            self.resize.wmin = self.wmin
            self.resize.hmin = self.hmin

            self.infoDim.setPos(0, h+5)
            self.infoDim.setPlainText("( {} x {} )".format(self.nrow, self.ncol))

    def load(self, val):
        tmp_val = val
        if 'str' not in self.format and 'bool' not in self.format:
            tmp_val = val[1]
            min, max = val[0], val[2]
        ncol, nrow = 1, 1
        if 'list' in self.format:
            nrow = 1
            tmp_col = []
            for i, lstVal in enumerate(tmp_val):
                tmp_it = self.item(i, 0)
                if 'str' not in self.format:
                    tmp_it.widget().setRange(min, max)
                    tmp_it.widget().setValue(lstVal)
                else:
                    tmp_it.widget().setPlainText(lstVal)
                tmp_col.append(tmp_it)
                ncol = i + 1
            self.proxyWidget.append(tmp_col)
        elif 'array' in self.format:
            nrow = 0
            for row in tmp_val:
                tmp_row = []
                for i, lstVal in enumerate(row):
                    tmp_it = self.item(i, nrow)
                    if 'str' not in self.format:
                        tmp_it.widget().setRange(min, max)
                        tmp_it.widget().setValue(lstVal)
                    else:
                        tmp_it.widget().setPlainText(lstVal)
                    tmp_row.append(tmp_it)
                    ncol = i + 1
                nrow += 1
                self.proxyWidget.append(tmp_row)
        else:
            tmp_it = self.item(0, 0)
            if 'str' not in self.format and 'bool' not in self.format:
                tmp_it.widget().setRange(min, max)
                tmp_it.widget().setValue(tmp_val)
            else:
                tmp_it.widget().setPlainText(tmp_val)
            self.proxyWidget.append([tmp_it])
        wprox, hprox = 102, 28
        w, h = ncol * wprox + 15, nrow * hprox + 5
        # gridSize = ItemGrid.SPACEGRID.value
        # h, w = round(h / gridSize) * gridSize, round(w / gridSize) * gridSize

        self.setRect(0.0, 0.0, w, h)
        self.nrow, self.ncol = nrow, ncol
        return w, h

    def newSize(self, w, h):

        if h < self.hmin:
            h = self.hmin
        if w < self.wmin:
            w = self.wmin

        ncol, nrow = round(w / 100), round(h / 25)
        i, j = 1, 1
        if self.proxyWidget:
            i = len(self.proxyWidget)
            if isinstance(self.proxyWidget[0], list):
                j = len(self.proxyWidget[0])
        if ncol > j:
            n = 0
            for row in self.proxyWidget:
                row.append(self.item(j, n))
                n += 1
        if nrow > i:
            n = len(self.proxyWidget[0])
            tmp = []
            for k in range(n):
                tmp.append(self.item(k, i))
            self.proxyWidget.append(tmp)
        if ncol < j:
            for row in self.proxyWidget:
                editor.diagramScene[editor.currentTab].removeItem(row[-1])
                del row[-1]
        if nrow < i:
            for col in self.proxyWidget[-1]:
                editor.diagramScene[editor.currentTab].removeItem(col)
            del self.proxyWidget[-1]

        wprox, hprox = 102, 28
        w, h = ncol * wprox + 15, nrow * hprox + 5
        # gridSize = ItemGrid.SPACEGRID.value
        # h, w = round(h / gridSize) * gridSize, round(w / gridSize) * gridSize
        self.setRect(0.0, 0.0, w, h)

        self.format = self.format[self.format.index('_') + 1:] if '_' in self.format else self.format
        if len(self.proxyWidget) > 1:
            self.format = 'array_' + self.format
        elif len(self.proxyWidget[0]) > 1:
            self.format = 'list_' + self.format
        self.outputs[0].setPos(w + 2, h / 2)
        self.outputs[0].format = self.format
        self.valueChange()
        if 'str' not in self.format:
            min = self.proxyWidget[0][0].widget().minimum()
            max = self.proxyWidget[0][0].widget().maximum()
            self.setLimits(min, max)

        self.infoDim.setPos(0, h+5)
        self.infoDim.setPlainText("( {} x {} )".format(nrow, ncol))
        self.nrow, self.ncol = nrow, ncol
        return w, h

    def item(self, col, row):
        tp = self.tp.__class__()
        if 'str' in self.format:
            tp.textChanged.connect(self.valueChange)
        elif 'bool' in self.format:
            tp.currentTextChanged.connect(self.valueChange)
        else:
            tp.valueChanged.connect(self.valueChange)
        tp.setStyleSheet("background-color: rgb" + str(self.color.getRgb()[0:3]))
        tp.setGeometry(3 + col * 102, 3 + row * 28, 100, 25)
        tp.setMinimumSize(100, 28)
        tp.setMaximumWidth(100)
        tp.setMaximumHeight(28)
        tp.setEnabled(self.isMod)
        if 'float' in self.format:
            tp.setDecimals(4)

        it = QGraphicsProxyWidget(self, Qt.WindowType.Widget)
        it.setWidget(tp)
        it.setZValue(3)
        return it

    def itemChange(self, *args, **kwargs):
        gridSize = ItemGrid.SPACEGRID.value
        if args[0] == self.GraphicsItemChange.ItemPositionHasChanged:
            xV = round(args[1].x() / gridSize) * gridSize
            yV = round(args[1].y() / gridSize) * gridSize
            self.setPos(QPointF(xV, yV))
        return QGraphicsRectItem.itemChange(self, *args, **kwargs)

    def valueChange(self):
        tmp_val = self.val
        if self.proxyWidget:
            if 'str' in self.format:
                del self.val
                self.val = []
                for elf in self.proxyWidget:
                    self.val.append(list(map(lambda x: x.widget().toPlainText(), elf)))
                if 'list' in self.format:
                    tmp = []
                    for el in self.val[0]:
                        tmp.append(el)
                    self.val = tmp
                elif 'array' in self.format:
                    pass
                else:
                    self.val = self.val[0][0]
            elif 'bool' in self.format:
                del self.val
                self.val = []
            else:
                del self.val
                self.val = []
                for elf in self.proxyWidget:
                    self.val.append(list(map(lambda x: x.widget().value(), elf)))
                if 'list' in self.format:
                    tmp = []
                    for el in self.val[0]:
                        tmp.append(el)
                    self.val = tmp
                elif 'array' in self.format:
                    pass
                else:
                    self.val = self.val[0][0]
                self.val = (tmp_val[0], self.val, tmp_val[2])
            if self.isMod:
                tmp = editor.listConstants[editor.currentTab][self.unit]
                del editor.listConstants[editor.currentTab][self.unit]
                editor.listConstants[editor.currentTab][self.unit] = (self.format, self.val, tmp[2])

    def contextMenuEvent(self, event):
        if self.isMod:
            menu = QMenu()
            de = menu.addAction('Delete')
            de.triggered.connect(self.deleteItem)
            pa = menu.addAction('Change label')
            pa.triggered.connect(self.changeLabel)
            if 'str' not in self.format:
                sl = menu.addAction('Set limits')
                sl.triggered.connect(self.defLimits)
            # ad = menu.addAction('Add dimension')
            # ad.triggered.connect(self.addDimension)
            # rd = menu.addAction('Remove dimension')
            # rd.triggered.connect(self.removeDimension)
            menu.exec(event.screenPos())

    def mouseMoveEvent(self, event):
        event.accept()
        editor.loopMouseMoveEvent(self, event.scenePos())
        return QGraphicsRectItem.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        editor.loopMouseReleaseEvent(self, True)
        return QGraphicsRectItem.mouseReleaseEvent(self, event)

    def defLimits(self):
        tmp = editor.listConstants[editor.currentTab][self.unit]
        if type(tmp[1]).__name__ == 'tuple':
            min = tmp[1][0]
            max = tmp[1][2]
            tmp_value = tmp[1][1]
        else:
            tmp_value = tmp[1]
            if self.form == 'int':
                min, max = -100000, 100000
            else:
                min, max = -100000.0, 100000.0

        c = setLimits(self.form, [min, max])
        c.exec()

        if c.getAnswer() == 'ok':
            min, max = c.getNewValues()[0], c.getNewValues()[1]

        tmp = (tmp[0],
               (min, tmp_value, max),
               tmp[2])
        del editor.listConstants[editor.currentTab][self.unit]
        editor.listConstants[editor.currentTab][self.unit] = tmp
        self.setLimits(min, max)

    def setLimits(self, min, max):
        for r in self.proxyWidget:
            for c in r:
                c.widget().setRange(min, max)
        self.val = (min, self.val[1], max)

    def addDimension(self):
        pass

    def removeDimension(self):
        pass

    def changeLabel(self):
        listVal = editor.listConstants[editor.currentTab][self.unit]
        oldVal = listVal[2]
        c = changeLabel('Cluster', self.unit, oldVal)
        c.exec()
        try:
            self.label = c.getNewLabel()
            self.lab.setPlainText(self.label)
            del editor.listConstants[editor.currentTab][self.unit]
            editor.listConstants[editor.currentTab][self.unit] = (listVal[0], listVal[1], self.label)
            UpdateUndoRedo()
        except OSError as err:
            print("OS error: {0}".format(err))

    def deleteItem(self):
        for elem in editor.diagramView[editor.currentTab].items():
            if type(elem) is LinkItem:
                if editor.listNodes[editor.currentTab][elem.name].find(self.unit + ':') != -1:
                    BlockCreate.deletelink(self, elem, self.unit)
        editor.diagramScene[editor.currentTab].removeItem(self)
        del editor.listConstants[editor.currentTab][self.unit]
        del editor.listItems[editor.currentTab][self.unit]
        editor.deleteItemsLoop(self)


class CommentsItem(QGraphicsRectItem):

    def __init__(self, w, h, text, isMod, parent=None):
        super(CommentsItem, self).__init__(None)
        self.setCursor(QCursor(ItemMouse.HANDLETOPITEM.value))
        self.wmin, self.hmin = 10.0, 10.0
        self.isMod = isMod
        self.inputs, self.outputs = [], []
        self.setPen(QPen(ItemColor.FRAME_COMMENT.value, 10))
        self.setBrush(QBrush(ItemColor.BACKGROUND_COMMENT.value))
        self.setZValue(-2)
        self.setOpacity(0.6)
        self.label = LabelGroup(self)
        self.label.setPlainText(text)
        self.unit = ''
        x, y = self.newSize(w, h)

        if self.isMod:
            self.setFlags(self.GraphicsItemFlag.ItemIsSelectable | self.GraphicsItemFlag.ItemIsMovable | self.GraphicsItemFlag.ItemIsFocusable | self.GraphicsItemFlag.ItemSendsGeometryChanges)
            self.label.setFlags(self.GraphicsItemFlag.ItemIsFocusable | self.GraphicsItemFlag.ItemIsMovable)
            self.resize = Slide(self)
            self.resize.setPos(x, y)
            self.resize.posChangeCallbacks.append(self.newSize)  # Connect the callback
            self.resize.setFlag(self.resize.GraphicsItemFlag.ItemIsSelectable, True)
            self.resize.wmin = self.wmin
            self.resize.hmin = self.hmin

    def deleteItem(self):
        editor.diagramScene[editor.currentTab].removeItem(self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            self.setPos(self.x(), self.y() - 1)
        if event.key() == Qt.Key.Key_Down:
            self.setPos(self.x(), self.y() + 1)
        if event.key() == Qt.Key.Key_Left:
            self.setPos(self.x() - 1, self.y())
        if event.key() == Qt.Key.Key_Right:
            self.setPos(self.x() + 1, self.y())

    def itemChange(self, *args, **kwargs):
        gridSize = ItemGrid.SPACEGRID.value
        if args[0] == self.GraphicsItemChange.ItemPositionHasChanged:
            xV = round(args[1].x() / gridSize) * gridSize
            yV = round(args[1].y() / gridSize) * gridSize
            self.setPos(QPointF(xV, yV))
        return QGraphicsRectItem.itemChange(self, *args, **kwargs)

    def newSize(self, w, h):
        # Limit the block size:
        if h < self.hmin:
            h = self.hmin
            w = self.wmin

        self.setRect(0.0, 0.0, w, h)
        # center label:
        rect = self.label.boundingRect()
        self.label.setPos(0, self.boundingRect().y() - rect.height())

        return w, h


class Connection:

    def __init__(self, name, fromPort, toPort, format):
        self.fromPort = fromPort
        self.pos1 = fromPort
        self.pos2 = fromPort
        if 'array' in format:
            self.a = 12
            self.b = 10
        else:
            self.a = 8
            self.b = 6

        if fromPort:
            self.pos1 = fromPort.scenePos()
            fromPort.posCallbacks.append(self.setBeginPos)
        self.toPort = toPort
        # Create link item:
        self.link = LinkItem(name, format)
        editor.diagramScene[editor.currentTab].addItem(self.link)
        self.link.setPositionTxt(self.pos1)

    def setFromPort(self, fromPort):
        self.fromPort = fromPort
        if self.fromPort:
            self.pos1 = fromPort.scenePos()
            self.fromPort.posCallbacks.append(self.setBeginPos)

    def setToPort(self, toPort):
        self.toPort = toPort
        if self.toPort:
            self.pos2 = toPort.scenePos()
            self.toPort.posCallbacks.append(self.setEndPos)

    def setEndPos(self, endpos):
        self.pos2 = endpos
        if self.fromPort.typeio == 'in':
            self.pos2 = QPointF(self.pos2.x() + 10.0, self.pos2.y())
        self.doLink()

    def setBeginPos(self, pos1):
        self.pos1 = pos1
        self.doLink()

    def doLink(self):
        path = QPainterPath()
        start_x, start_y = self.pos1.x() + 4, self.pos1.y() - 1
        end_x, end_y = self.pos2.x() - 5, self.pos2.y() - 1
        ctrl1_x, ctrl1_y = self.pos1.x() + (self.pos2.x() - self.pos1.x()) * 0.7, self.pos1.y()
        ctrl2_x, ctrl2_y = self.pos2.x() + (self.pos1.x() - self.pos2.x()) * 0.7, self.pos2.y()

        path.moveTo(start_x, start_y)
        path.cubicTo(ctrl1_x, ctrl1_y, ctrl2_x, ctrl2_y, end_x, end_y)

        qp = QPainterPathStroker()
        qp.setCapStyle(Qt.PenCapStyle.SquareCap)
        shape = qp.createStroke(path)

        self.link.setPath(shape)
        self.link.bislink.setPath(shape)
        self.link.setPositionTxt((start_x + end_x) / 2, (start_y + end_y) / 2)

        try:
            theta = atan((ctrl2_y - ctrl1_y) / (ctrl2_x - ctrl1_x))
        except Exception as e:
            theta = 1.5708
        polyhead = QPolygonF([
            QPointF((start_x + end_x) / 2, (start_y + end_y) / 2),
            QPointF(-self.a * cos(theta) + self.b * sin(theta) + (start_x + end_x) / 2,
                    self.b * cos(theta) + self.a * sin(theta) + (start_y + end_y) / 2),
            QPointF(-self.a * cos(theta) - self.b * sin(theta) + (start_x + end_x) / 2,
                    -self.b * cos(theta) + self.a * sin(theta) + (start_y + end_y) / 2)])
        self.link.setPositionShow(polyhead)

    # if link connected nowhere
    def delete(self):
        editor.diagramScene[editor.currentTab].removeItem(self.link)
        editor.diagramScene[editor.currentTab].removeItem(self.link.getlinkTxt())
        editor.diagramScene[editor.currentTab].removeItem(self.link.getlinkShow())
        editor.diagramScene[editor.currentTab].removeItem(self.link.getBislink())


class ConnectorItem(QGraphicsPolygonItem):

    def __init__(self, name, connct='', w=70, h=26, inout='in', format='unkn', Vinput='', isMod=True, parent=None):
        super(ConnectorItem, self).__init__(parent)

        self.name = name
        self.inout = inout
        self.w = 70
        self.h = 26
        self.format = format
        self.moved = False
        self.isMod = isMod
        # self.setAcceptHoverEvents(True)

        if connct == '':
            ConnExist = True
            inc = 0
            while ConnExist:
                if 'C' + str(inc) in editor.listConnects[editor.currentTab]:
                    inc += 1
                else:
                    ConnExist = False
            self.connct = 'C' + str(inc)

        else:
            self.connct = connct

        self.unit = self.connct

        if 'in' in inout:
            if self.isMod:
                editor.listConnects[editor.currentTab][self.connct] = (self.inout, self.name, self.format, Vinput)
            polyhead = QPolygonF([QPointF(0, 0), QPointF(50, 0), QPointF(70, 8),
                                  QPointF(70, 18), QPointF(50, 26), QPointF(0, 26)])
        else:
            if self.isMod:
                editor.listConnects[editor.currentTab][self.connct] = (self.inout, self.name, self.format)
            polyhead = QPolygonF([QPointF(0, 8), QPointF(20, 0), QPointF(70, 0),
                                  QPointF(70, 26), QPointF(20, 26), QPointF(0, 18)])

        self.editConnect()
        self.setPolygon(polyhead)

    def editConnect(self):
        self.setPen(QPen(ItemColor.FRAME_CONNECT.value, 2))
        self.setBrush(QBrush(Qt.GlobalColor.darkGray))
        if self.isMod:
            self.setFlags(self.GraphicsItemFlag.ItemIsSelectable | self.GraphicsItemFlag.ItemIsMovable | self.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setCursor(QCursor(ItemMouse.HANDLETOPITEM.value))
        # Label:
        self.label = QGraphicsTextItem('Conn.', self)
        self.label.setDefaultTextColor(ItemColor.DEFAULTTEXTCOLOR.value)
        rect = self.label.boundingRect()
        lw, lh = rect.width(), rect.height()
        lx1 = lw
        ly1 = (-25)

        self.nameConnect = QGraphicsTextItem(self.connct, self)
        self.nameConnect.setDefaultTextColor(ItemColor.DEFAULTTEXTCOLOR.value)
        rect = self.nameConnect.boundingRect()
        lw, lh = rect.width(), rect.height()
        lx2 = lw
        ly2 = 0

        self.setFlag(self.GraphicsItemFlag.ItemIsFocusable, True)

        # Inputs and outputs of the block:
        if 'in' in self.inout:
            self.inputs = None
            self.outputs = Port(self.name, 'out', self.format, self.connct, True, self.isMod, 80, -12, self)
            self.outputs.setPos(self.w + 2, 1 + self.h / 2)
            lx1 = 2
            lx2 = 4

        else:
            self.outputs = None
            self.inputs = Port(self.name, 'in', self.format, self.connct, True, self.isMod, 80, -12, self)
            self.inputs.setPos(0, 1 + self.h / 2)
            lx1 = self.w - lx1
            lx2 = (self.w - lx2 - 4)

        self.label.setPos(lx1, ly1)
        self.nameConnect.setPos(lx2, ly2)

    def mousePressEvent(self, event):
        # if event.button() == 1 and self.isMod:
        #     if not self.isSelected():
        #         editor.diagramScene[editor.currentTab].clearSelection()
        #         self.setSelected(True)

        if self.isMod:
            if not self.isSelected():
                editor.diagramScene[editor.currentTab].clearSelection()
                self.setSelected(True)

        # QGraphicsPolygonItem.mousePressEvent(self, event)

    def mouseDoubleClickEvent(self, event):
        if self.inout in 'in':
            if self.outputs.label.toPlainText() not in 'unkn':
                self.changelabel()
        if self.inout in 'out':
            if self.inputs.label.toPlainText() not in 'unkn':
                self.changelabel()
        return QGraphicsPolygonItem.mouseDoubleClickEvent(self, event)

    def mouseMoveEvent(self, event):
        self.moved = True
        event.accept()
        return QGraphicsPolygonItem.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        if self.moved:
            UpdateUndoRedo()
            self.moved = False
        return QGraphicsPolygonItem.mouseReleaseEvent(self, event)

    def itemChange(self, *args, **kwargs):
        gridSize = ItemGrid.SPACEGRID.value
        if args[0] == self.GraphicsItemChange.ItemPositionHasChanged:
            xV = round(args[1].x() / gridSize) * gridSize
            yV = round(args[1].y() / gridSize) * gridSize
            self.setPos(QPointF(xV, yV))
        return QGraphicsRectItem.itemChange(self, *args, **kwargs)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            self.setPos(self.x(), self.y() - 1)
        if event.key() == Qt.Key.Key_Down:
            self.setPos(self.x(), self.y() + 1)
        if event.key() == Qt.Key.Key_Left:
            self.setPos(self.x() - 1, self.y())
        if event.key() == Qt.Key.Key_Right:
            self.setPos(self.x() + 1, self.y())

    def contextMenuEvent(self, event):
        if not self.isSelected():
            return
        menu = QMenu()
        de = menu.addAction('Delete')
        de.triggered.connect(self.deleteItem)
        pa = menu.addAction('Change label')
        if self.inout in 'in':
            if self.outputs.label.toPlainText() == 'unkn':
                pa.setEnabled(False)
        if self.inout in 'out':
            if self.inputs.label.toPlainText() == 'unkn':
                pa.setEnabled(False)
        pa.triggered.connect(self.changelabel)
        menu.exec(event.screenPos())

    def changelabel(self):
        oldVal = editor.listConnects[editor.currentTab][self.connct][1]
        c = changeLabel('Conn', self.connct, oldVal)
        c.exec()
        listVal = editor.listConnects[editor.currentTab][self.connct]
        try:
            del editor.listConnects[editor.currentTab][self.connct]
            if self.inout in 'in':
                editor.listConnects[editor.currentTab][self.connct] = (listVal[0], c.getNewLabel(), listVal[2], listVal[3])
                self.outputs.label.setPlainText(c.getNewLabel())
                self.outputs.label.setPos(-self.outputs.label.boundingRect().size().width() - 80, -12)
                tmplistNodes = editor.listNodes[editor.currentTab].copy()
                for ln in tmplistNodes:
                    tmp = tmplistNodes[ln]
                    tmp2 = tmp[0:tmp.index(':')]
                    if self.connct == tmp2:
                        tmp = (self.connct + ':' + c.getNewLabel()) + tmp[tmp.index("#Node#"):]
                        del editor.listNodes[editor.currentTab][ln]
                        editor.listNodes[editor.currentTab][ln] = tmp
#                         break
            else:
                editor.listConnects[editor.currentTab][self.connct] = (listVal[0], c.getNewLabel(), listVal[2])
                self.inputs.label.setPlainText(c.getNewLabel())
                tmplistNodes = editor.listNodes[editor.currentTab].copy()
                for ln in tmplistNodes:
                    tmp = tmplistNodes[ln]
                    tmp2 = tmp[tmp.index('#Node#') + 6:]
                    tmp2 = tmp2[0:tmp2.index(':')]
                    if self.connct == tmp2:
                        tmp = tmp[0:tmp.index('#Node#') + 6] + (self.connct + ':' + c.getNewLabel())
                        del editor.listNodes[editor.currentTab][ln]
                        editor.listNodes[editor.currentTab][ln] = tmp
        except OSError as err:
            print('error change label : ', str(err))
            editor.listConnects[editor.currentTab][self.connct] = listVal

    def deleteItem(self):
        for elem in editor.diagramView[editor.currentTab].items():
            if type(elem) is LinkItem:
                if editor.listNodes[editor.currentTab][elem.name].find(self.connct + ':') != -1:
                    BlockCreate.deletelink(self, elem, self.connct)
        editor.diagramScene[editor.currentTab].removeItem(self)
        del editor.listConnects[editor.currentTab][self.connct]
        del editor.listItems[editor.currentTab][self.connct]


class Constants(QGraphicsRectItem):

    def __init__(self, unit='', w=80, h=30, val='', form='', label='', isMod=True, parent=None):
        super(Constants, self).__init__(parent)

        if 'tuple' in form and 'enumerate' not in form:
            form = 'tuple'

        self.isMod = isMod

        self.setCursor(QCursor(ItemMouse.HANDLETOPITEM.value))

        self.caseFinal = False
        self.currentLoop = None

        self.moved = False
        self.form = form
        self.val = val
        self.setZValue(2)
        self.preview = False

        if self.isMod:
            self.setFlags(self.GraphicsItemFlag.ItemIsSelectable | self.GraphicsItemFlag.ItemIsMovable | self.GraphicsItemFlag.ItemSendsGeometryChanges)
            self.setFlag(self.GraphicsItemFlag.ItemIsFocusable, True)
            self.setAcceptHoverEvents(True)

        if unit == 'newConstant':
            ConstantExist = True
            inc = 0
            while ConstantExist:
                if 'A' + str(inc) in editor.listConstants[editor.currentTab]:
                    inc += 1
                else:
                    ConstantExist = False
            self.unit = 'A' + str(inc)
        else:
            self.unit = unit

        self.label = label if label else 'const'

        self.format = form

        if 'path' == form:
            self.elemProxy = Constants_text(self.unit, val, self.label, False, False)
            self.elemProxy.setStyleSheet("background-color: rgb" + str(TypeColor.path.value.getRgb()[0:3]))
            self.elemProxy.textChanged.connect(self.changeText)
            color = TypeColor.path.value
            if isMod:
                self.warningPath()
                if os.path.exists(val) and val != 'path':
                    self.proxyWarning.setVisible(False)
                else:
                    self.proxyWarning.setVisible(True)
        elif 'list_path' == form:
            tmpval = '\n'.join(val)
            self.elemProxy = Constants_text(self.unit, tmpval, self.label, True, True)
            self.elemProxy.setStyleSheet("background-color: rgb" + str(TypeColor.path.value.getRgb()[0:3]))
            self.elemProxy.textChanged.connect(self.changeText)
            color = TypeColor.path.value
            self.label = label if label else 'pathbox'
            if isMod:
                self.warningPath()
                self.proxyWarning.setVisible(False)
                for lst in val:
                    if not os.path.exists(lst):
                        self.proxyWarning.setVisible(True)
                        break
        elif 'enumerate' in form:
            self.elemProxy = Constants_Combo(self.unit, form, val, self.label, self)
            self.elemProxy.setStyleSheet("QComboBox{selection-background-color: blue; background-color: rgb" + str(TypeColor.str.value.getRgb()[0:3]) +
                                         "}QListView{border : 4px black; background-color: white;}")
            self.format = 'str'
            color = TypeColor.str.value
        elif 'str' == form:
            self.elemProxy = Constants_text(self.unit, val, self.label, True, False)
            self.elemProxy.setStyleSheet("background-color: rgb" + str(TypeColor.str.value.getRgb()[0:3]))
            self.elemProxy.textChanged.connect(self.changeText)
            color = TypeColor.str.value
        elif 'float' == form:
            self.elemProxy = Constants_float(self.unit, val, self.label)
            self.elemProxy.setStyleSheet("background-color: rgb" + str(TypeColor.float.value.getRgb()[0:3]))
            color = TypeColor.float.value
        elif 'int' == form:
            self.elemProxy = Constants_int(self.unit, val, self.label)
            self.elemProxy.setStyleSheet("background-color: rgb" + str(TypeColor.int.value.getRgb()[0:3]))
            color = TypeColor.int.value
        elif 'bool' == form:
            self.elemProxy = Constants_Combo(self.unit, "bool", str(val), self.label, self)
            self.elemProxy.setStyleSheet("selection-background-color: blue; background-color: rgb" + str(TypeColor.bool.value.getRgb()[0:3]))
            color = TypeColor.bool.value
        elif 'tuple' == form:
            self.elemProxy = Constants_tuple(self.unit, val, self.label)
            self.elemProxy.setStyleSheet("selection-background-color: blue; background-color: rgb" + str(TypeColor.tuple.value.getRgb()[0:3]))
            self.elemProxy.textChanged.connect(self.changeText)
            color = TypeColor.tuple.value

        self.proxyWidget = [[QGraphicsProxyWidget(self, Qt.WindowType.Widget)]]
#         self.proxyWidget = QGraphicsProxyWidget(self, Qt.WindowType.Widget)
        self.proxyWidget[0][0].setWidget(self.elemProxy)
        self.proxyWidget[0][0].setPos(3, 3)
        self.proxyWidget[0][0].setZValue(3)

        self.wprox = self.proxyWidget[0][0].boundingRect().size().width()
        self.hprox = self.proxyWidget[0][0].boundingRect().size().height()

        self.w = self.wprox + 15
        self.h = self.hprox + 6

        self.lab = QGraphicsTextItem(self.label, self)
        self.lab.setDefaultTextColor(ItemColor.DEFAULTTEXTCOLOR.value)
        self.lab.setFont(QFont("Times", 12, QFont.Weight.Bold))
        self.lab.setPos(0, -30)
        self.lab.setVisible(True)

        # self.wmin = self.w
        # self.hmin = self.h
        self.setPen(QPen(ItemColor.FRAME_CONSTANTS.value, 2))
        self.setBrush(QBrush(color))
        self.setRect(0.0, 0.0, self.w, self. h)
        self.inputs, self.outputs = [], []
        self.outputs.append(Port('', 'out', self.format, self.unit, True, self.isMod, 80, -12, self))
        self.outputs[0].setPos(self.w + 2, self.h / 2)
        if self.isMod:
            editor.listConstants[editor.currentTab][self.unit] = (self.form, val, self.label)
        else:
            self.elemProxy.setEnabled(False)
        if form in ['str', 'path', 'list_path', 'tuple']:
            self.changeText()

    # def hoverEnterEvent(self, event):
    #     self.tmpzvalue = self.zValue()
    #     self.setZValue(100)
    #     print('{} hover enter'.format(self.unit))
    #     # return QGraphicsRectItem.hoverEnterEvent(self, *args, **kwargs)
    #
    # def hoverLeaveEvent(self, event):
    #     self.setZValue(self.tmpzvalue)
    #     print('{} hover leave'.format(self.unit))
    #     print(type(self.elemProxy))
    #     return QGraphicsRectItem.hoverLeaveEvent(self, event)

    def changeText(self):
        self.elemProxy.setCursorWidth(1)
        textEdition = self.elemProxy
        font = textEdition.document().defaultFont()
        fontMetrics = QFontMetrics(font)
        textSize = fontMetrics.size(0, textEdition.toPlainText())
        w = int(textSize.width()) + 10
        h = int(textSize.height()) + 10
        self.elemProxy.setMinimumSize(w, h)
        self.elemProxy.setMaximumSize(w, h)
        self.elemProxy.resize(w, h)
        self.setRect(0.0, 0.0, w + 15, h + 8)
        self.outputs[0].setPos(w + 15 + 2, (h + 8) / 2)
        if self.isMod:
            if self.form == 'path':
                tmpPath = textEdition.toPlainText()
                tmpPath = tmpPath.replace('\n', '')
                if os.path.exists(tmpPath) and tmpPath != 'path':
                    self.proxyWarning.setVisible(False)
                else:
                    self.proxyWarning.setVisible(True)
            elif self.form == 'list_path':
                tmpPath = textEdition.toPlainText()
                tmpPath = tmpPath.split('\n')
                self.proxyWarning.setVisible(False)
                for lst in tmpPath:
                    if not os.path.exists(lst):
                        self.proxyWarning.setVisible(True)
                        break
#         self.setPos(-(w+15+10), self.pos().y())

    def changeCombo(self):
        w = self.elemProxy.size().width()
        h = self.elemProxy.size().height()
#         self.elemProxy.resize(w, h)
        self.setRect(0.0, 0.0, w + 20, h + 6)
        self.outputs[0].setPos(w + 20 + 2, (h + 6) / 2)

    def itemChange(self, *args, **kwargs):
        gridSize = ItemGrid.SPACEGRID.value
        if args[0] == self.GraphicsItemChange.ItemPositionHasChanged:
            xV = round(args[1].x() / gridSize) * gridSize
            yV = round(args[1].y() / gridSize) * gridSize
            self.setPos(QPointF(xV, yV))
        return QGraphicsRectItem.itemChange(self, *args, **kwargs)

    def foncedBlock(self, fcd):
        if fcd:
            self.setOpacity(0.4)
        else:
            self.setOpacity(1.0)

    def changeLabel(self):
        listVal = editor.listConstants[editor.currentTab][self.unit]
        oldVal = listVal[2]
        c = changeLabel('Const', self.unit, oldVal)
        c.exec()
        try:
            self.label = c.getNewLabel()
            self.lab.setPlainText(self.label)
            del editor.listConstants[editor.currentTab][self.unit]
            editor.listConstants[editor.currentTab][self.unit] = (listVal[0], listVal[1], self.label)
            UpdateUndoRedo()
        except OSError as err:
            print("OS error: {0}".format(err))

    def contextMenuEvent(self, event):
        if self.isMod:
            menu = QMenu()
            de = menu.addAction('Delete')
            de.triggered.connect(self.deleteItem)
            pa = menu.addAction('Change label')
            pa.triggered.connect(self.changeLabel)
            if self.format == 'path':
                fp = menu.addAction('load file path (double click)')
                fp.triggered.connect(lambda: self.loadPath(True))
                dp = menu.addAction('load directory path')
                dp.triggered.connect(lambda: self.loadPath(False))
            elif self.format == 'list_path':
                fps = menu.addAction('load files path')
                fps.triggered.connect(lambda: self.loadPaths(True))
            elif self.format == 'int' or self.format == 'float':
                sl = menu.addAction('Set limits')
                sl.triggered.connect(self.setLimits)
            if type(self.elemProxy) is Constants_Combo and self.format != 'bool':
                ed = menu.addAction('Edit (double click)')
                ed.triggered.connect(self.editComb)
            menu.exec(event.screenPos())

    def editComb(self):
        AllItems = [self.elemProxy.itemText(i) for i in range(self.elemProxy.count())]
        p = editCombobox(AllItems)
        p.exec()
        if p.getAnswer() == 'ok':
            newList = p.getNewList()
            self.elemProxy.clear()
            self.elemProxy.addItems(newList)
            self.elemProxy.txt = "enumerate(" + str(tuple(newList)) + ")"
            self.elemProxy.value = str(newList[0])
            self.elemProxy.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
            self.elemProxy.adjustSize()
            self.form = "enumerate(" + str(tuple(newList)) + ")"
            self.changeCombo()
            del editor.listConstants[editor.currentTab][self.unit]
            editor.listConstants[editor.currentTab][self.unit] = (self.elemProxy.txt, self.elemProxy.value, self.label)
            UpdateUndoRedo()

    def mouseMoveEvent(self, event):
        event.accept()
        editor.loopMouseMoveEvent(self, event.scenePos())
        return QGraphicsRectItem.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        editor.loopMouseReleaseEvent(self, True)
        return QGraphicsRectItem.mouseReleaseEvent(self, event)

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.RightButton:
            self.setSelected(True)

        if event.button() == Qt.MouseButton.LeftButton and self.isMod:
            if not self.isSelected():
                editor.diagramScene[editor.currentTab].clearSelection()
                self.setSelected(True)

        if type(self.elemProxy) is Constants_Combo:
            self.elemProxy.setInsertPolicy(QComboBox.InsertPolicy.InsertAtTop)

#         if event.button() == 1 and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
#             editor.blockSelection(self)

    def mouseDoubleClickEvent(self, event):
        if self.isMod:
            if type(self.elemProxy) is Constants_Combo and self.form != 'bool':
                self.editComb()
                # AllItems = [self.elemProxy.itemText(i) for i in range(self.elemProxy.count())]
                # p = editCombobox(AllItems)
                # p.exec()
                # if p.getAnswer() == 'ok':
                #     newList = p.getNewList()
                #     self.elemProxy.clear()
                #     self.elemProxy.addItems(newList)
                #     self.elemProxy.txt = "enumerate(" + str(tuple(newList)) + ")"
                #     self.elemProxy.value = str(newList[0])
                #     self.elemProxy.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
                #     self.elemProxy.adjustSize()
                #     self.form = "enumerate(" + str(tuple(newList)) + ")"
                #     self.changeCombo()
                #     del editor.listConstants[editor.currentTab][self.unit]
                #     editor.listConstants[editor.currentTab][self.unit] = (self.elemProxy.txt, self.elemProxy.value, self.label)
                #     UpdateUndoRedo()
            elif type(self.elemProxy) is Constants_text:
                if self.form == 'path':
                    self.loadPath(True)
                elif self.form == 'list_path':
                    self.loadPaths(True)
#         return QGraphicsRectItem.mouseDoubleClickEvent(self,event)

    def setLimits(self):
        tmp = editor.listConstants[editor.currentTab][self.unit]
        if type(tmp[1]).__name__ == 'tuple':
            min = tmp[1][0]
            max = tmp[1][2]
            tmp_value = tmp[1][1]
        else:
            tmp_value = tmp[1]
            if self.form == 'int':
                min, max = -100000, 100000
            else:
                min, max = -100000.0, 100000.0

        c = setLimits(self.form, [min, max])
        c.exec()

        if c.getAnswer() == 'ok':
            min, max = c.getNewValues()[0], c.getNewValues()[1]

        tmp = (tmp[0],
               (min, tmp_value, max),
               tmp[2])
        del editor.listConstants[editor.currentTab][self.unit]
        editor.listConstants[editor.currentTab][self.unit] = tmp
        self.elemProxy.setRange(min, max)

    def warningPath(self):
        path_relatif = os.path.dirname(os.path.dirname(
                                        os.path.dirname(
                                            os.path.abspath(__file__))))
        pathWar = os.path.join(path_relatif,
                               'ressources',
                               'alert_path.png')
        self.proxyWarning = QGraphicsProxyWidget(self, Qt.WindowType.Widget)
        pos = self.pos()

        from PIL import Image
        img = Image.open(pathWar)
        sh = img.size

        img = QImage(pathWar)

        pixMap = QPixmap.fromImage(img)

        label_img = QLabel()
        label_img.setPixmap(pixMap)
        label_img.setGeometry(0, 0, 64, 64)
        label_img.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.proxyWarning.setWidget(label_img)
        self.proxyWarning.setPos(pos.x()-70, pos.y() - 15)
        self.proxyWarning.setZValue(3)
        self.proxyWarning.updateGeometry()
        self.proxyWarning.setVisible(False)

    def loadPath(self, fileOrdir):
        currentpathTmp = self.elemProxy.toPlainText()
        if not os.path.exists(currentpathTmp):
            currentpathTmp = editor.currentpathdata
        tmp = ''
        postmp = self.sceneBoundingRect()

        if fileOrdir:
            fileCh = QFileDialog.getOpenFileName(None,
                                                 "Choose file",
                                                 currentpathTmp,
                                                 'All Files (*)',
                                                 None,
                                                 QFileDialog.Option.DontUseNativeDialog)
            if fileCh[0]:
                tmp = fileCh[0]
        else:
            repCh = QFileDialog.getExistingDirectory(None,
                                                     'Choose repertory',
                                                     currentpathTmp,
                                                     QFileDialog.Option.ShowDirsOnly)
            if repCh:
                tmp = repCh

        if tmp:
            editor.currentpathdata = tmp
            self.elemProxy.setPlainText(tmp)
            del editor.listConstants[editor.currentTab][self.unit]
            editor.listConstants[editor.currentTab][self.unit] = ('path', self.elemProxy.toPlainText(), self.label)
            newpostmp = self.sceneBoundingRect()
            self.setPos(postmp.x() + postmp.width() - newpostmp.width(), postmp.y())
            UpdateUndoRedo()

    def loadPaths(self, fileOrDir):

        postmp = self.sceneBoundingRect()

        list_current_items, currentpathTmp = '', ''
        if self.elemProxy.toPlainText() != 'path':
            list_current_items = self.elemProxy.toPlainText().split('\n')
            currentpathTmp = list_current_items[-1]

        if not os.path.exists(currentpathTmp):
            currentpathTmp = editor.currentpathdata

        if fileOrDir:
            filesCh = QFileDialog.getOpenFileNames(None,
                                                   'Choose files',
                                                   currentpathTmp,
                                                   'All Files (*)',
                                                   None,
                                                   QFileDialog.Option.DontUseNativeDialog)
            if filesCh[0]:
                ch = filesCh[0]
                if list_current_items:
                    list_current_items.extend(ch)
                    ch = list_current_items
                editor.currentpathdata = ch[-1]
                tmp = '\n'.join(ch)
                self.elemProxy.setPlainText(tmp)
                del editor.listConstants[editor.currentTab][self.unit]
                editor.listConstants[editor.currentTab][self.unit] = ('path', ch, self.label)
                newpostmp = self.sceneBoundingRect()
                self.setPos(postmp.x() + postmp.width() - newpostmp.width(), postmp.y())
                UpdateUndoRedo()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            self.setPos(self.x(), self.y() - 1)
        if event.key() == Qt.Key.Key_Down:
            self.setPos(self.x(), self.y() + 1)
        if event.key() == Qt.Key.Key_Left:
            self.setPos(self.x() - 1, self.y())
        if event.key() == Qt.Key.Key_Right:
            self.setPos(self.x() + 1, self.y())
#         if QKeySequence(event.key() + int(event.modifiers())) == QKeySequence("Ctrl+C"):
#             editor.listItemStored.clear()
#             editor.listBlSmStored.clear()
#         return QGraphicsRectItem.keyPressEvent(self, *args, **kwargs)

    def deleteItem(self):
        for elem in editor.diagramView[editor.currentTab].items():
            if type(elem) is LinkItem:
                if editor.listNodes[editor.currentTab][elem.name].find(self.unit + ':') != -1:
                    BlockCreate.deletelink(self, elem, self.unit)
        editor.diagramScene[editor.currentTab].removeItem(self)
        del editor.listConstants[editor.currentTab][self.unit]
        del editor.listItems[editor.currentTab][self.unit]
        editor.deleteItemsLoop(self)


class Constants_int(QSpinBox):

    def __init__(self, unit, val, lab, parent=None):
        super(Constants_int, self).__init__(parent)
#         self.setButtonSymbols(QSpinBox.NoButtons)
        if type(val).__name__ == 'tuple':
            self.setRange(val[0], val[2])
            self.setValue(val[1])

        else:
            self.setRange(-100000, 100000)
            self.setValue(val)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.unit = unit
        self.lab = lab

    def focusOutEvent(self, event):
        self.lineEdit().deselect()
        tmp = editor.listConstants[editor.currentTab][self.unit]
        if (type(tmp[1]).__name__) == 'tuple':
            min, max = tmp[1][0], tmp[1][2]
        else:
            min, max = -100000, 100000
        new_val = (min, self.value(), max)
        del editor.listConstants[editor.currentTab][self.unit]
        editor.listConstants[editor.currentTab][self.unit] = ('int', new_val, self.lab)
        self.updateGeometry()
        self.setReadOnly(True)
        UpdateUndoRedo()

    def focusInEvent(self, event):
        self.setReadOnly(False)


class Constants_float(QDoubleSpinBox):

    def __init__(self, unit, val, lab, parent=None):
        super(Constants_float, self).__init__(parent)
        if type(val).__name__ == 'tuple':
            self.setRange(val[0], val[2])
            val = val[1]
        else:
            self.setRange(-100000.0, 100000.0)
        self.setDecimals(6)
        self.setValue(val)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.unit = unit
        self.lab = lab

    def focusOutEvent(self, event):
        self.lineEdit().deselect()
        tmp = editor.listConstants[editor.currentTab][self.unit]
        if (type(tmp[1]).__name__) == 'tuple':
            min, max = tmp[1][0], tmp[1][2]
        else:
            min, max = -100000.0, 100000.0
        new_val = (min, self.value(), max)
        del editor.listConstants[editor.currentTab][self.unit]
        editor.listConstants[editor.currentTab][self.unit] = ('float', new_val, self.lab)
        self.updateGeometry()
        self.setReadOnly(True)
        UpdateUndoRedo()

    def focusInEvent(self, event):
        self.setReadOnly(False)


class Constants_text(QTextEdit):

    def __init__(self, unit, txt, lab, isMuliLines, isList, parent=None):
        super(Constants_text, self).__init__(parent)
        self.setPlainText(txt)  # !!! intermittent bug
        self.setMinimumSize(110, 25)
        self.setMaximumWidth(110)
        self.setMaximumHeight(25)
        self.setAutoFillBackground(False)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setCursorWidth(1)
        self.unit = unit
        self.lab = lab
        self.isMuliLines = isMuliLines
        self.isList = isList

    def focusInEvent(self, event):
        editor.diagramScene[editor.currentTab].clearSelection()
        self.setCursorWidth(1)
        # editor.listItemStored.clear()
        # editor.listBlSmStored.clear()
        # del editor.listCommentsStored[:]
#         event.accept()

    def focusOutEvent(self, event):
        self.setPlainText(self.toPlainText())
        self.setCursorWidth(0)
        tmpTxt = repr(self.toPlainText())
        if ':' in tmpTxt:
            tmpTxt = tmpTxt.replace(':', '')
            tmpTxt = tmpTxt[1:-1]
            self.setPlainText(tmpTxt)
        if tmpTxt:
            if not self.isMuliLines:
                tmpTxt = tmpTxt.replace('\\n', '')
                if tmpTxt[0] == "\'":
                    tmpTxt = tmpTxt[1:-1]
                self.setPlainText(tmpTxt)
            else:
                if tmpTxt[0] == "\'":
                    tmpTxt = tmpTxt[1:-1]
                if self.isList:
                    tmpTxt = tmpTxt.split('\\n')
        tmpform = editor.listConstants[editor.currentTab][self.unit][0]
        del editor.listConstants[editor.currentTab][self.unit]
        editor.listConstants[editor.currentTab][self.unit] = (tmpform, tmpTxt, self.lab)
        UpdateUndoRedo()


class Constants_Combo(QComboBox):

    def __init__(self, unit, txt, val, lab, parent=None):
        super(Constants_Combo, self).__init__()
        self.parent = parent
        self.tmp_zvvalue = None
        if "enumerate" in txt:
            txt.replace(" ", "")
        self.txt = txt
        if txt == 'bool':
            txt = "enumerate(('True','False'))"
        self.addItems([x[1] for x in list(eval(txt))])
        self.setCurrentText(val)
        self.current_value = val
        # self.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.setStyleSheet('QComboBox {combobox-popup: 0}')

        # self.setView(QtWidgets.QListView())
        self.currentIndexChanged.connect(self.newValue)
        self.view().pressed.connect(self.reputZvalue)
        self.unit = unit
        self.lab = lab

    def mousePressEvent(self, mouseEvent):
        current_id = self.currentIndex()
        if self.txt != 'bool':
            # self.setCurrentIndex(0)
            self.setCurrentIndex(current_id)
        self.tmp_zvvalue = self.parent.zValue()
        self.parent.setZValue(100)
        self.setMaxVisibleItems(0)
        return QComboBox.mousePressEvent(self, mouseEvent)
        super(Constants_Combo, self).__init__()

    def hidePopup(self, *args, **kwargs):
        if self.tmp_zvvalue:
            self.parent.setZValue(self.tmp_zvvalue)
        return QComboBox.hidePopup(self, *args, **kwargs)

    def reputZvalue(self):
        self.parent.setZValue(self.tmp_zvvalue)

    def focusOutEvent(self, *args, **kwargs):
        if not self.view().isVisible():
            if self.tmp_zvvalue:
                self.parent.setZValue(self.tmp_zvvalue)

    def newValue(self):
        if self.currentText() != '':
            del editor.listConstants[editor.currentTab][self.unit]
            if self.txt == 'bool':
                curr_txt = self.currentText()
                if curr_txt == 'True':
                    curr_txt = True
                else:
                    curr_txt = False
            else:
                curr_txt = self.currentText()
            editor.listConstants[editor.currentTab][self.unit] = (self.txt, curr_txt, self.lab)
            if self.tmp_zvvalue:
                self.parent.setZValue(self.tmp_zvvalue)
            self.current_value = curr_txt
            UpdateUndoRedo()
        else:
            self.setCurrentText(self.current_value)


class Constants_tuple(QTextEdit):
    def __init__(self, unit, val, lab, parent=None):
        super(Constants_tuple, self).__init__(parent)
        self.setPlainText(str(val))
        self.setMinimumSize(110, 25)
        self.setMaximumWidth(110)
        self.setMaximumHeight(25)
        self.setAutoFillBackground(False)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setCursorWidth(1)
        self.unit = unit
        self.lab = lab

    def focusInEvent(self, event):
        editor.diagramScene[editor.currentTab].clearSelection()
        self.setCursorWidth(1)
        # editor.listItemStored.clear()
        # editor.listBlSmStored.clear()
        # del editor.listCommentsStored[:]
#         event.accept()

    def focusOutEvent(self, event):
        self.setPlainText(self.toPlainText())
        self.setCursorWidth(0)
        try:
            tmpTxt = eval(self.toPlainText()[1:-1])
            # tmpform = editor.listConstants[editor.currentTab][self.unit][0]
            # del editor.listConstants[editor.currentTab][self.unit]
            # editor.listConstants[editor.currentTab][self.unit] = (tmpform, tmpTxt, self.lab)
        except Exception as err:
            tmpTxt = self.correctTuple(self.toPlainText()[1:-1])
            self.setPlainText(str(tmpTxt))
        tmpform = editor.listConstants[editor.currentTab][self.unit][0]
        del editor.listConstants[editor.currentTab][self.unit]
        editor.listConstants[editor.currentTab][self.unit] = (tmpform, tmpTxt, self.lab)
        UpdateUndoRedo()

    def correctTuple(self, tmpTxt):
        newList = []
        for ele in tmpTxt.split(','):
            try:
                if type(ele).__name__:
                    newList.append(eval(ele))
            except Exception as err:
                tmp = ele.replace("'", '')
                tmp = tmp.replace('"', '')
                newList.append(tmp.strip())
        return tuple(newList)


class Control_IF(QComboBox):

    def __init__(self, unit, txt, val, parent=None):
        super(Control_IF, self).__init__(parent)
        self.txt = txt
        if txt == 'bool':
            txt = "enumerate(('True','False'))"
        self.addItems([x[1] for x in list(eval(txt))])
        self.setCurrentText(val)
        self.currentTextChanged.connect(self.newValue)
        self.unit = unit

    def newValue(self):
        if self.currentText() == 'True':
            self.trueCase()
            editor.listIfShowedState[editor.currentTab][self.unit] = True
        else:
            self.falseCase()
            editor.listIfShowedState[editor.currentTab][self.unit] = False

#         UpdateUndoRedo()
#         del editor.listConstants[editor.currentTab][self.unit]
#         editor.listConstants[editor.currentTab][self.unit] = (self.txt, self.currentText())

    def trueCase(self):
        for item in editor.diagramView[editor.currentTab].items():
            if type(item) in [BlockCreate, ForLoopItem, ScriptItem, Imagebox, Checkbox,
                              Constants, Clusters, Probes, StopExecution]:
                if item.unit in editor.listTools[editor.currentTab][self.unit][0]:
                    item.setOpacity(1)
                    self.opacityLink(item.unit, 1)
                    if type(item) is ForLoopItem:
                        self.opacity_1_InLoop(item.unit, 1)
                        try:
                            item.elemProxy.newValue()
                        except Exception as e:
                            pass
                if item.unit in editor.listTools[editor.currentTab][self.unit][1]:
                    item.setOpacity(0)
                    self.opacityLink(item.unit, 0)
                    if type(item) is ForLoopItem:
                        self.opacity_0_InLoop(item.unit, 0)

        for lsi in editor.listTools[editor.currentTab][self.unit][0]:
            if 'N' in lsi:
                self.opacityLink2(lsi, 1)
        for lsi in editor.listTools[editor.currentTab][self.unit][1]:
            if 'N' in lsi:
                self.opacityLink2(lsi, 0)

    def falseCase(self):
        for item in editor.diagramView[editor.currentTab].items():
            if type(item) in [BlockCreate, ForLoopItem, ScriptItem, Imagebox, Checkbox,
                              Constants, Clusters, Probes, StopExecution]:
                if item.unit in editor.listTools[editor.currentTab][self.unit][0]:
                    item.setOpacity(0)
                    self.opacityLink(item.unit, 0)
                    if type(item) is ForLoopItem:
                        self.opacity_0_InLoop(item.unit, 0)
                if item.unit in editor.listTools[editor.currentTab][self.unit][1]:
                    item.setOpacity(1)
                    self.opacityLink(item.unit, 1)
                    if type(item) is ForLoopItem:
                        self.opacity_1_InLoop(item.unit, 1)
                        try:
                            item.elemProxy.newValue()
                        except Exception as e:
                            pass
        for lsi in editor.listTools[editor.currentTab][self.unit][0]:
            if 'N' in lsi:
                self.opacityLink2(lsi, 0)
        for lsi in editor.listTools[editor.currentTab][self.unit][1]:
            if 'N' in lsi:
                self.opacityLink2(lsi, 1)

    def opacity_0_InLoop(self, unit, state):
        listToOpacit = []
        if 'I' in unit:
            listToOpacit.extend(editor.listTools[editor.currentTab][unit][0])
            listToOpacit.extend(editor.listTools[editor.currentTab][unit][1])
        else:
            listToOpacit.extend(editor.listTools[editor.currentTab][unit])

        for elemts in editor.diagramView[editor.currentTab].items():
            if (type(elemts) in [BlockCreate, ForLoopItem, ScriptItem, Imagebox, Checkbox,
                                 Constants, Clusters, Probes]) and elemts.unit in listToOpacit:
                elemts.setOpacity(state)
                self.opacityLink(elemts.unit, state)
                if type(elemts) is ForLoopItem and elemts.unit != unit:
                    self.opacity_0_InLoop(elemts.unit, state)

    def opacity_1_InLoop(self, unit, state):
        listToOpacit = []
        if 'I' in unit:
            listToOpacit.extend(editor.listTools[editor.currentTab][unit][0])
            listToOpacit.extend(editor.listTools[editor.currentTab][unit][1])
        else:
            listToOpacit.extend(editor.listTools[editor.currentTab][unit])

        for elemts in editor.diagramView[editor.currentTab].items():
            if (type(elemts) in [BlockCreate, ForLoopItem, ScriptItem, Imagebox, Checkbox,
                                 Constants, Clusters, Probes]) and \
                                 elemts.unit in listToOpacit:
                elemts.setOpacity(state)
                self.opacityLink(elemts.unit, state)
#                 if state == 1 and ('I' in unit or 'I' in elemts.unit):
#                     elemts.elemProxy.newValue()
                if state == 1:
                    try:
                        elemts.elemProxy.newValue()
                    except Exception as e:
                        pass

                if type(elemts) is ForLoopItem and elemts.unit != unit:
                    self.opacity_1_InLoop(elemts.unit, state)

    def opacityLink(self, unit, state):
        listNode_to_opacity = []
        for key_link, val_link in editor.listNodes[editor.currentTab].items():
            tmp_in = val_link[val_link.index("#Node#") + 6:]
            tmp_in = tmp_in[0:tmp_in.index(':')]
            tmp_out = val_link[0:val_link.index(":")]
            if tmp_in == unit or tmp_out == unit:
                listNode_to_opacity.append(key_link)
        for itLink in editor.diagramView[editor.currentTab].items():
            if type(itLink) is LinkItem:
                if itLink.name in listNode_to_opacity:
                    itLink.setOpacity(state)
                    itLink.bislink.setOpacity(state)
                    itLink.linkTxt.setOpacity(state)
                    itLink.linkShow.setOpacity(state)

    def opacityLink2(self, name, state):
        for itLink in editor.diagramView[editor.currentTab].items():
            if type(itLink) is LinkItem:
                if itLink.name == name:
                    itLink.setOpacity(state)
                    itLink.bislink.setOpacity(state)
                    itLink.linkTxt.setOpacity(state)
                    itLink.linkShow.setOpacity(state)


class Diagram_excution():

    def __init__(self, title_dgr, mode_th, parent=None):
        self.title_dgr = title_dgr
        editor.console.clear()

        self.execute_Diagram(title_dgr, mode_th)

    def execute_Diagram(self, title_dgr, mode_th):
        # self.window_progressBar()

        gc.collect()
        editor.parent().setFocus()
        txt_raw = SaveDiagram().toPlainText()
        txt_code = ''
        for keyS, valS in editor.listTools[editor.currentTab].items():
            if 'S' in keyS or 'J' in keyS:
                tmpS = 'source ' + keyS + ']'
                txt_code += txt_raw[txt_raw.index('[' +
                                    tmpS):txt_raw.index('[/' +
                                    tmpS) + len(tmpS) + 2] + '\n'
        editor.editText('-' * 40, 10, 600, '000000', False, True)
        editor.editText("{}".format(title_dgr), 14, 600, 'ff6f00', False, False)
        if mode_th:
            txt = analyze2(txt_raw, [False, True]).get_analyze(editor.textEdit)
            mode = 'Multi-threading'
        else:
            txt = analyze2(txt_raw, [False, False]).get_analyze(editor.textEdit)
            mode = 'Sequential'

        if txt_code:
            txt += txt_code
        if self.check_script_code(txt):
            editor.editText("Warning: some scripts contain the terms 'QApplication' or 'syst.exit', remove them !",
                            10, 600, 'ff0000', False, True)
            return

        editor.editText(" {} execution: ".format(mode), 10, 600, '0000CC', False, False)
        editor.editText("     > started", 10, 600, '0000CC', False, False)
        editor.editText("     > in progress ...", 10, 600, '0000CC', False, False)

        args = (txt, {}, editor.textEdit, True, '', editor.console)

        # current_dir_path = os.path.dirname(os.path.realpath(__file__))
        # source_disp = os.path.join(current_dir_path, 'tasks_progress.py')
        # subprocess.Popen([sys.executable, source_disp, 'start diagram'])
        self.runner = ThreadDiagram(title_dgr, args, editor)
        try:
            col = '\x1b[38;2;255;100;0m'
            print("\n{} Execution {} (local) in progress ... \033[0m".format(col, title_dgr))
            sr = self.runner.run()
        except Exception as err:
            editor.editText("This diagram contains errors : {}".format(str(err)),
                            10, 600, 'ff0000', False, True)
        self.runner.winBar.close()
        SharedMemoryManager(False)
        # self.runner.sysctrl.kill()
        # for proc in psutil.process_iter():
        #     print("pid:", proc.name())

        # self.runner = Window_progressbar(title_dgr, args, editor)
        # self.runner.close()

    def check_script_code(self, txt):
        if 'QApplication(' in txt:
            return True
        return False


class DiagramScene(QGraphicsScene):

    def __init__(self, parent=None):
        super(DiagramScene, self).__init__(parent)
        self.prevItem = []
        # self.lines = []
        # self.draw_grid()
        self.currentCursor = QPointF(0.0, 0.0)
        self.topCorner = [0, 0]
        self._selectedItemVec = deque()
        self.screen_state = "Full screen"
        self.fullScr = False

        self.addCenterLines()
    # def draw_grid(self):
    #     width = Settings.NUM_BLOCKS_X * Settings.WIDTH
    #     height = Settings.NUM_BLOCKS_Y * Settings.HEIGHT

    def addCenterLines(self):
        pen = QPen(ItemColor.CROSS_SCENE.value, 2)
        crss = QLineF(-10, 0, 10, 0)
        self.addLine(crss, pen)
        crss = QLineF(0, -10, 0, 10)
        self.addLine(crss, pen)

    def deleteItems(self):
        # UpdateUndoRedo()
        for el in self.selectedItems():
            if type(el) is not LinkItem and type(el) is not Slide:
                el.deleteItem()
        UpdateUndoRedo()

    def mouseMoveEvent(self, mouseEvent):
        editor.sceneMouseMoveEvent(mouseEvent)
        super(DiagramScene, self).mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        if mouseEvent.button() == Qt.MouseButton.RightButton:  # Right mouse click
            # Set previous selections selected
            for item in self.prevItem:
                item.setSelected(1)

            item = self.itemAt(mouseEvent.scenePos().x(),
                               mouseEvent.scenePos().y(),
                               QTransform(0, 0, 0, 0, 0, 0))
            if item:
                item.setSelected(1)

        if mouseEvent.button() == Qt.MouseButton.LeftButton:  # Left mouse click
            # Get selected item
            items = editor.diagramScene[editor.currentTab].selectedItems()
            # Shift click
            if mouseEvent.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                # Set previous items selected
                for item in self.prevItem:
                    item.setSelected(1)

                for item in items:
                    self.prevItem.append(item)

                item = self.itemAt(mouseEvent.scenePos().x(),
                                   mouseEvent.scenePos().y(),
                                   QTransform(0, 0, 0, 0, 0, 0))
                if item is None:
                    self.clearSelection()
            else:
                self.prevItem = []
                for item in items:
                    try:
                        if 'I' in item.unit or 'F' in item.unit:
                            item.selectItemsInside(item.unit, True)
                    except Exception as err:
                        pass
                    self.prevItem.append(item)
            # selectionArea()
        editor.sceneMouseReleaseEvent(mouseEvent)
        super(DiagramScene, self).mouseReleaseEvent(mouseEvent)
#         UpdateUndoRedo()

    def mousePressEvent(self, mouseEvent):
        self.currentCursor = mouseEvent.scenePos()
        # self.clearSelection()
        item = self.itemAt(mouseEvent.scenePos().x(),
                           mouseEvent.scenePos().y(),
                           QTransform(0, 0, 0, 0, 0, 0))

        if (not item and
                len(editor.diagramScene[editor.currentTab].selectedItems()) == 0):

            if (mouseEvent.button() == Qt.MouseButton.LeftButton and
                    mouseEvent.modifiers() == Qt.KeyboardModifier.ShiftModifier):
                item = self.itemAt(mouseEvent.scenePos().x(),
                                   mouseEvent.scenePos().y(),
                                   QTransform(0, 0, 0, 0, 0, 0))
                if item:
                    item.setSelected(1)
                    self._selectedItemVec.append(item)
                else:
                    return QGraphicsScene.mousePressEvent(self, mouseEvent)

        return QGraphicsScene.mousePressEvent(self, mouseEvent)

    def fitwindow(self, factor):
        if len(editor.diagramScene[editor.currentTab].items()) > 2:
            self.setSceneRect(self.itemsBoundingRect())
            scene = editor.diagramView[editor.currentTab].scene()
            r = scene.sceneRect()
            # editor.diagramView[editor.currentTab].centerOn(0, 0)
            editor.diagramView[editor.currentTab]\
                .fitInView(r, Qt.AspectRatioMode.KeepAspectRatio)
            # editor.diagramView[editor.currentTab]\
            #     .fitInView(QRectF(0, 0, self.sceneRect().width(), self.sceneRect().height()), Qt.AspectRatioMode.KeepAspectRatio)
            editor.diagramView[editor.currentTab].scale(factor, factor)

    def mouseDoubleClickEvent(self, mouseEvent):
        pos = mouseEvent.scenePos()
        itms = editor.diagramScene[editor.currentTab].items(pos)
        if len(itms) != 0:
            QGraphicsScene.mouseDoubleClickEvent(self, mouseEvent)
        else:
            if not self.fullScr:
                self.fullScr = True
                self.fullScreen()

        # QGraphicsScene.mouseDoubleClickEvent(self, mouseEvent)

    def fullScreen(self):
        currentTitle = editor.getSubWindowCurrentTitle()
        sub_window = SubWindow(self, editor, currentTitle)
        sub_window.exec()
        self.fullScr = False

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_C:
            self.copy_items()
        elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_D:
            self.past_items()
        elif event.key() == Qt.Key.Key_Delete:
            self.deleteItems()
        return QGraphicsScene.keyPressEvent(self, event)

    def copy_items(self):
        editor.listItemStored.clear()
        editor.listBlSmStored.clear()
        editor.listLoopStored.clear()
        del editor.listCommentsStored[:]
        self.topCorner = [0, 0]
        items = self.selectedItems()
        for item in items:
            if type(item) is ForLoopItem:

                editor.listBlSmStored[item.unit] = (editor.libTools
                                                    [editor.currentTab]
                                                    [item.unit])
                editor.listLoopStored[item.unit] = (editor.listTools
                                                    [editor.currentTab]
                                                    [item.unit])
                if 'I' in item.unit:
                    lst = editor.listTools[editor.currentTab][item.unit]
                    flat_list = [item for sublist in lst for item in sublist]
                    for list_bl in flat_list:
                        try:
                            editor.listItems[editor.currentTab][list_bl].setSelected(True)
                        except Exception as err:
                            pass
        for el in self.selectedItems():
            if type(el) is not CommentsItem:
                if type(el) in [BlockCreate, Constants, Clusters,
                                ScriptItem, Probes, ForLoopItem,
                                Checkbox, Imagebox, ConnectorItem, StopExecution]:
                    self.topCorner[0] = min(el.scenePos().x(), self.topCorner[0])
                    self.topCorner[1] = min(el.scenePos().y(), self.topCorner[1])

                    editor.listItemStored[el.unit] = el
                    if 'U' in el.unit:
                        editor.listBlSmStored[el.unit] = (editor.listBlocks
                                                          [editor.currentTab]
                                                          [el.unit])
                    elif 'M' in el.unit:
                        editor.listBlSmStored[el.unit] = (editor.listSubMod
                                                          [editor.currentTab]
                                                          [el.unit])
                    elif 'A' in el.unit:
                        editor.listBlSmStored[el.unit] = (editor.listConstants
                                                          [editor.currentTab]
                                                          [el.unit])
                    elif 'S' in el.unit or 'J' in el.unit:
                        editor.listBlSmStored[el.unit] = el.elemProxy.toPlainText()
                    elif 'C' in el.unit:
                        editor.listBlSmStored[el.unit] = (editor.listConnects
                                                          [editor.currentTab]
                                                          [el.unit])
                    elif 'E' in el.unit:
                        editor.listBlSmStored[el.unit] = (editor.listStopExec
                                                          [editor.currentTab]
                                                          [el.unit])

            else:
                editor.listCommentsStored.append(el)

        for elnd, nod in editor.listNodes[editor.currentTab].items():
            a, b, c, d = nod.replace('#Node#', ':').split(':')
            if a in editor.listItemStored.keys() and c in editor.listItemStored.keys():
                editor.listItemStored[elnd] = nod

    def past_items(self):
        if editor.listItemStored or editor.listCommentsStored:
            self.clearSelection()
            try:
                self.pastItems(editor.listItemStored,
                               editor.listBlSmStored,
                               editor.listLoopStored,
                               editor.listCommentsStored)
            except Exception as err:
                pass
                # print("error:" + str(err))

    def pastItems(self, list_It, list_Bl_Sm, list_Lf_St, list_Comm):
        edit = editor.diagramView[editor.currentTab]

        listUnitOld = list_It.keys()
        listUnitNew = []
        changeUnit = {}
        listItemsTmp = list(editor.listItems[editor.currentTab].keys())
        listNodesTmp = list(editor.listNodes[editor.currentTab].keys())

        for k_un in listUnitOld:
            lst = listItemsTmp + listNodesTmp + listUnitNew
            k_un_tmp = re.sub('[0-9]', '', k_un)
            new_unit = self.searchUnit(lst, k_un_tmp[0], k_un_tmp.replace(k_un_tmp[0], ''))
            listUnitNew.append(new_unit)
            changeUnit[k_un] = new_unit
        x_cursor, y_cursor = self.currentCursor.x(), self.currentCursor.y()
        delta_x, delta_y = x_cursor - self.topCorner[0], y_cursor - self.topCorner[1]

        for nameUnit, ins in list_It.items():
            if 'N' not in nameUnit:
                try:
                    posRe = (ins.scenePos().x() + delta_x, ins.scenePos().y() + delta_y,
                             ins.boundingRect().width() - 2, ins.boundingRect().height() - 2)
                except Exception as e:
                    posRe = (0, 0, 100, 100)

            if 'U' in nameUnit:
                tmpVal = list_Bl_Sm[nameUnit][2]
                newVal = []
                for lst in range(len(tmpVal[0])):
                    newV = tmpVal[1][lst]
                    try:
                        if 'Node' in newV:
                            unitNode = newV[newV.index('(')+1:newV.index(')')]
                            if unitNode in listUnitOld:
                                newV = newV.replace(unitNode,
                                                    changeUnit[unitNode])
                            else:
                                newV = searchInitialValueBlock(ins.name, tmpVal[0][lst]).getValue()
                    except Exception as er:
                        pass
                    newVal.append(newV)
                new_inout = ((ins.inout[0][0],
                              newVal,
                              ins.inout[0][2],
                              ins.inout[0][3]),)
                edit.loadBlock(changeUnit[nameUnit],
                               ins.name,
                               ins.category,
                               posRe,
                               *new_inout)
            elif 'M' in nameUnit:
                tmpVal = list_Bl_Sm[nameUnit][1]
                newVal = []
                for lst in range(len(tmpVal[0])):
                    newV = tmpVal[1][lst]
                    try:
                        if 'Node' in newV:
                            unitNode = newV[newV.index('(')+1:newV.index(')')]
                            if unitNode in listUnitOld:
                                newV = newV.replace(unitNode,
                                                    changeUnit[unitNode])
                            else:
                                newV = searchInitialValueSubMod(ins.name, tmpVal[0][lst]).getValue()
                    except Exception as er:
                        pass
                    newVal.append(newV)
                new_inout = ((ins.inout[0][0],
                              newVal,
                              ins.inout[0][2],
                              ins.inout[0][3]),)
                edit.loadMod(changeUnit[nameUnit],
                             ins.name, posRe, *new_inout)
            elif 'A' in nameUnit:
                if type(ins) in [Constants, Imagebox, Checkbox]:
                    values = list_Bl_Sm[nameUnit]
                    if ins.format == 'list_str':
                        form = 'list_str'
                        val = values[1]
                    elif ins.format == 'path_box':
                        form = 'path_box'
                        val = values[1]
                    elif ins.format == 'path':
                        form = 'path'
                        if "'" in values[1]:
                            val = values[1][1:-1]  # to remove guillemets
                        else:
                            val = values[1]
                    elif ins.format == 'list_path':
                        form = 'list_path'
                        val = values[1]
                    elif ins.format == 'str':
                        form = values[0]
                        if "'" in values[1]:
                            val = values[1][1:-1]  # to remove guillemets
                        else:
                            val = values[1]
                    else:
                        form = values[0]
                        val = values[1]
                    edit.loadConstant(changeUnit[nameUnit],
                                      posRe, val, form, ins.label)
                else:
                    values = list_Bl_Sm[nameUnit]
                    form = values[0]
                    if ins.format == 'str':
                        if "'" in values[1]:
                            val = values[1][1:-1]  # to remove guillemets
                        else:
                            val = values[1]
                    else:
                        val = values[1]
                    edit.loadCluster(changeUnit[nameUnit],
                                     posRe, val, form, ins.label)
            elif 'S' in nameUnit or 'J' in nameUnit:
                edit.loadScriptItem(changeUnit[nameUnit], ins.name, posRe,
                                    ins.inout[0], ins.inout[1])
                ball = edit.returnBlockSystem()
                ball.elemProxy.setText(list_Bl_Sm[nameUnit])
            elif 'P' in nameUnit:
                edit.loadProbe(changeUnit[nameUnit],
                               ins.label, ins.format, posRe)
            elif 'C' in nameUnit:
                edit.loadConn(changeUnit[nameUnit],
                              'unkn', posRe, ins.inout, 'unkn', '')
            elif 'F' in nameUnit:
                edit.loadLoopFor(changeUnit[nameUnit], posRe,
                                 list_Bl_Sm[nameUnit][0],
                                 list_Bl_Sm[nameUnit][1])
                for lst_it in list_Lf_St[nameUnit]:
                    editor.listTools[editor.currentTab][changeUnit[nameUnit]].append(changeUnit[lst_it])
            elif 'I' in nameUnit:
                edit.loadLoopFor(changeUnit[nameUnit], posRe,
                                 list_Bl_Sm[nameUnit][0],
                                 list_Bl_Sm[nameUnit][1])
                tmp = [[], []]
                for lst_it in list_Lf_St[nameUnit][0]:
                    tmp[0].append(changeUnit[lst_it])
                for lst_it in list_Lf_St[nameUnit][1]:
                    tmp[1].append(changeUnit[lst_it])
                editor.listTools[editor.currentTab][changeUnit[nameUnit]] = tmp
            elif 'E' in nameUnit:
                edit.loadStopExec(changeUnit[nameUnit], posRe)
                editor.listStopExec[editor.currentTab][changeUnit[nameUnit]] = ()
            # else:
            #     edit.loadComments(posRe, ins.label.toPlainText())

            edit.returnBlockSystem().setSelected(1)

        for nameUnit, ins in list_It.items():
            if 'N' in nameUnit:
                a, b, c, d = ins.replace('#Node#', ':').split(':')
                a = changeUnit[a]
                c = changeUnit[c]
                newNode = changeUnit[nameUnit]
                editor.listNodes[editor.currentTab][newNode] = (a + ':' + b +
                                                                '#Node#' +
                                                                c + ':' + d)
                tmp = editor.listItems[editor.currentTab][a]
#                 tmp.setSelected(1)
                if 'A' in a:
                    fromPort = tmp.outputs[0]
                else:
                    for lin in tmp.outputs:
                        if type(lin) is Port and lin.name == b:
                            fromPort = lin
                            break
                tmp = editor.listItems[editor.currentTab][c]
#                 tmp.setSelected(1)
                for lin in tmp.inputs:
                    if type(lin) is Port and lin.name == d:
                        toPort = lin
                        break
                startConnection = Connection(newNode,
                                             fromPort, toPort,
                                             fromPort.format)
                startConnection.setEndPos(toPort.scenePos())
                startConnection.setToPort(toPort)

        for ins in list_Comm:
            try:
                posRe = (ins.scenePos().x() + delta_x,
                         ins.scenePos().y() + delta_y,
                         ins.boundingRect().width() - 2,
                         ins.boundingRect().height() - 2)
                # self.currentCursor = QPointF(0.0, 0.0)
            except Exception as e:
                posRe = (0, 0, 100, 100)
            edit.loadComments(posRe, ins.label.toPlainText())

        ValueZ2()

        self.fitwindow(0.8)
        UpdateUndoRedo()
        Menu().btnPressed(QAction('Refresh Diagram'))
        for lst_it in changeUnit.values():
            editor.listItems[editor.currentTab][lst_it].setSelected(True)

    def searchUnit(self, list, char_unit, ext):
        NodeExist = True
        inc = 0
        while NodeExist:
            newChar = char_unit + str(inc)
            if newChar in list or newChar+"m" in list or newChar+"t" in list or newChar+"m*" in list or newChar+"t*" in list:
                inc += 1
            else:
                NodeExist = False
        return char_unit + str(inc) + ext


class DiagramView(QGraphicsView):

    def __init__(self, scene, parent=None):
        QGraphicsView.__init__(self, scene, parent)
        self.setRenderHints(QPainter.RenderHint.Antialiasing |
                            QPainter.RenderHint.SmoothPixmapTransform)
        # self.setMouseTracking(True)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.scalefactor = 1
        self.setBackgroundBrush(ItemColor.BACKGROUND.value)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setRubberBandSelectionMode(Qt.ItemSelectionMode.IntersectsItemShape)
        # self.gridVisible = True
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.horizontalScrollBar().setStyleSheet('background: grey')
        # self.verticalScrollBar().setStyleSheet('background: grey')
        # self.verticalScrollBar().installEventFilter(self);
        # self.horizontalScrollBar().installEventFilter(self);
        self.setContentsMargins(0, 0, 0, 0)
        self.setMouseTracking(True)
        self.setAcceptDrops(True)

        self.caseFinal = False
        self.currentLoop = None
        self.scriptFinal = False
        self.currentScript = None
        self.m_originX, self.m_originY = 0, 0

#         self.startPos = None

    def dragEnterEvent(self, event):
        event.accept()
        event.acceptProposedAction()
        if event.mimeData().hasFormat('mod_SubMod')\
                or event.mimeData().hasFormat('blocks_subModules')\
                or event.mimeData().hasFormat('structures_tools'):
            event.accept()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('mod_SubMod')\
                or event.mimeData().hasFormat('blocks_subModules')\
                or event.mimeData().hasFormat('structures_tools'):
            view_pos = event.position()
            pos = self.mapToScene(int(view_pos.x()), int(view_pos.y()))
            itm = self.scene().itemAt(pos, QTransform(0, 0, 0, 0, 0, 0))

            if type(itm) is ForLoopItem:
                itm.activeState()
                self.caseFinal = True
#                 self.currentLoop = itm.unit
                if self.currentLoop:
                    if self.currentLoop.unit != itm.unit:
                        self.currentLoop.normalState()
                self.currentLoop = itm
            else:
                for elem in self.items():
                    if type(elem) is ForLoopItem:
                        elem.normalState()
                        self.caseFinal = False

            if event.mimeData().hasFormat('mod_SubMod'):
                if type(itm) is QGraphicsProxyWidget:
                    if type(itm.parentItem()) == ScriptItem:
                        itm.parentItem().activeState()
                        self.scriptFinal = True
                        self.currentScript = itm
                else:
                    for elem in self.items():
                        if type(elem) is QGraphicsProxyWidget:
                            if type(elem.parentItem()) == ScriptItem:
                                elem.parentItem().normalState()
                                self.scriptFinal = False

            event.accept()

    # def drawBackground(self, painter, rect):
    #     gridSize = ItemGrid.SPACEGRID.value
    #     pen = QPen(QColor(100, 100, 230))
    #     pen.setWidth(2)
    #     painter.setPen(pen)
    #     left = int(rect.left()) - (int(rect.left()) % gridSize)
    #     top = int(rect.top()) - (int(rect.top()) % gridSize)
    #     for x in range(left, int(rect.right()), gridSize):
    #         for y in range(top, int(rect.bottom()), gridSize):
    #             painter.drawPoints(QPointF(x,y))

    # def showGrid(self, stat):
    #     if stat:
    #         self.gridVisible = True
    #     else:
    #         self.gridVisible = False
    #     self.update()

    def dropEvent(self, event):
        cur_dw = editor.diagramView.index(self)
        for lstWind in editor.mdi.subWindowList():
            if lstWind.windowNumber == cur_dw:
                editor.mdi.setActiveSubWindow(lstWind)
                break

        editor.diagramScene[editor.currentTab].clearSelection()

        if event.mimeData().hasUrls():
            dialog = QProgressDialog('Loading ...', None, 0, 0, None)
            bar = QProgressBar(dialog)
            bar.setTextVisible(True)
            bar.setMinimum(0)
            bar.setMaximum(100)
            dialog.setBar(bar)
            dialog.show()
            view_pos = event.position()
            pos_cur = self.mapToScene(int(view_pos.x()), int(view_pos.y()))
            i, len_item = 0, len(event.mimeData().urls())
            dialog.setValue(i)
            for lstUrl in event.mimeData().urls():
                current_obj = lstUrl.toLocalFile()
                QApplication.processEvents()
                dialog.setValue(int(100*i/len_item))
                i += 1
                if os.path.isdir(current_obj):
                    self.a1 = Constants('newConstant', 80, 30, current_obj,
                                        'path', '', True)
                    self.a1.setPos(pos_cur)
                    self.scene().addItem(self.a1)
                    self.addItemLoop(self.a1.unit)
                else:
                    filename, file_extension = os.path.splitext(current_obj)
                    if file_extension in ['.nii', '.nii.gz', '.jpg', '.png']:
                        self.a1 = Imagebox('newImagebox', current_obj, '',
                                           True)
                        self.a1.setPos(pos_cur)
                        self.scene().addItem(self.a1)
                    elif file_extension in ['.dgr']:
                        return
                    else:
                        self.a1 = Constants('newConstant', 80, 30,
                                            current_obj, 'path', '', True)
                        self.a1.setPos(pos_cur)
                        self.scene().addItem(self.a1)
                        self.addItemLoop(self.a1.unit)
                editor.listItems[editor.currentTab][self.a1.unit] = self.a1
                pos_cur = QPointF(pos_cur.x() + 50, pos_cur.y() + 50)
            dialog.close()
            UpdateUndoRedo()

        elif event.mimeData().hasFormat('mod_SubMod'):
            if self.scriptFinal:
                name = str(event.mimeData().data('mod_SubMod'))
                name = name[2:len(name) - 1]
                self.addItemScript(self.currentScript, name)
                self.scriptFinal = False
            else:
                name = str(event.mimeData().data('mod_SubMod'))
                name = name[2:len(name) - 1]
                self.b1 = ProcessItem('newBlock',
                                      name,
                                      editor.getlib()[name][0],
                                      150, 80,
                                      editor.getlib()[name][1]).getBlocks()
                view_pos = event.position()
                self.b1.setPos(self.mapToScene(int(view_pos.x()), int(view_pos.y())))

                # self.b1.setPos(self.mapToScene(event.pos()))
                self.scene().addItem(self.b1)
                editor.listItems[editor.currentTab][self.b1.unit] = self.b1
                self.addItemLoop(self.b1.unit)

        elif event.mimeData().hasFormat('blocks_subModules'):
            name = str(event.mimeData().data('blocks_subModules'))
            name = name[2:len(name) - 1]
            self.bm = SubProcessItem('newSubMod',
                                     name, 150, 80, None).getSubblocks()
            view_pos = event.position()
            self.bm.setPos(self.mapToScene(int(view_pos.x()), int(view_pos.y())))
            # self.bm.setPos(self.mapToScene(event.pos()))
            self.scene().addItem(self.bm)
            editor.listItems[editor.currentTab][self.bm.unit] = self.bm
            self.addItemLoop(self.bm.unit)

        elif event.mimeData().hasFormat('structures_tools'):
            name = str(event.mimeData().data('structures_tools'))
            name = name[2:len(name) - 1]
            if "For" in name:
                self.a1 = ForLoopItem('newForLoop', name, 400.0, 400.0, True, [], [])
            elif "If" in name:
                self.a1 = ForLoopItem('newIf', name, 400.0, 400.0, True, [], [])
            elif "Comments" in name:
                self.a1 = CommentsItem(200, 150, 'Comments', True)
            elif "Constant_" in name:
                if 'string' in name:
                    val = 'your text'
                    form = 'str'
                elif 'integer' in name:
                    val = 0
                    form = 'int'
                elif 'float' in name:
                    val = 0.0
                    form = 'float'
                elif 'combobox' in name:
                    form = "enumerate(('item1','item2','item3'))"
                    val = 'item1'
                elif 'boolean' in name:
                    val = True
                    form = 'bool'
                elif 'path' in name:
                    val = 'path'
                    form = 'path'
                elif 'tuple' in name:
                    val = (0,)
                    form = 'tuple'
                self.a1 = Constants('newConstant', 80, 30, val, form, '', True)
            elif "Cluster_" in name:
                if 'integer' in name:
                    val = (-10000, 0, 10000)
                    form = 'int'
                elif 'float' in name:
                    val = (-10000.0, 0.0, 10000.0)
                    form = 'float'
                elif 'string' in name:
                    val = ''
                    form = 'str'
                elif 'boolean' in name:
                    val = True
                    form = 'bool'
                self.a1 = Clusters('newCluster', 115, 33, val, form, '', True)
            elif "Script_python" in name:
                self.a1 = ScriptItem('newScript', name, 400.0, 400.0, True, True)
            elif "Macro_ImageJ" in name:
                self.a1 = ScriptItem('newMacro', name, 400.0, 400.0, True, True, [], [['macro_out', 'out', 'str']])
            elif name in ["Value", "Type", "Length"]:
                self.a1 = Probes('new', 'unkn', name, True)
            elif "Checkbox" in name:
                self.a1 = Checkbox('newCheckbox', ['Item1', 'Item2'], '', True)
            elif "Imagebox" in name:
                self.a1 = Imagebox('newImagebox', 'path', '', True)
            elif "Pathbox" in name:
                self.a1 = Constants('newConstant', 80, 30, ['path'], 'list_path', '', True)
            elif "Connector" in name:
                if "_input" in name:
                    self.a1 = ConnectorItem('unkn', '', 70, 26, 'in', 'unkn', '', True)
                else:
                    self.a1 = ConnectorItem('unkn', '', 70, 26, 'out', 'unkn', '', True)
            elif "Stop_execution" in name:
                self.a1 = StopExecution('newStopExec', True)
            view_pos = event.position()
            self.a1.setPos(self.mapToScene(int(view_pos.x()), int(view_pos.y())))
            self.scene().addItem(self.a1)

            try:
                editor.listItems[editor.currentTab][self.a1.unit] = self.a1
                self.addItemLoop(self.a1.unit)
            except Exception as e:
                pass
        UpdateUndoRedo()
        return QGraphicsView.dropEvent(self, event)

    def addItemLoop(self, unitItem):
        if self.currentLoop:
            ind = 0
            if self.currentLoop.loopIf:
                if self.currentLoop.elemProxy.currentText() == 'False':
                    ind = 1
            for elem in editor.diagramScene[editor.currentTab].items():
                if type(elem) is ForLoopItem and elem.unit == self.currentLoop.unit:
                    elem.normalState()
                    elem.IteminLoop(unitItem, self.caseFinal, ind)
                    elem.resize_frame(ind)
                    self.currentLoop = None
                    self.caseFinal = False
                    break

    def addItemScript(self, item, name):
        item.parentItem().normalState()
        txt = item.widget().toPlainText()
        txt_import = 'from NodeEditor.modules.{} import {}'.format(editor.getlib()[name][0], name) + '\n'
        txt_import += txt
        item.widget().setPlainText(txt_import)

    def loadBlock(self, unit, name, cat, pos, *inout):
        b2 = ProcessItem(unit, name, cat, pos[2], pos[3], *inout).getBlocks()
        b2.setPos(pos[0], pos[1])
        self.scene().addItem(b2)
        editor.listItems[editor.currentTab][b2.unit] = b2
        self.ball = b2

    def loadMod(self, unit, name, pos, *inout):
        b3 = SubProcessItem(unit, name, pos[2], pos[3], *inout).getSubblocks()
        b3.setPos(pos[0], pos[1])
        self.scene().addItem(b3)
        editor.listItems[editor.currentTab][b3.unit] = b3
        self.ball = b3

    def loadConn(self, unit, name, pos, inout, format, Vinput):
        b4 = ConnectorItem(name, unit, pos[2], pos[3], str(inout), format, Vinput, True)
        b4.setPos(pos[0], pos[1])
        self.scene().addItem(b4)
        editor.listItems[editor.currentTab][b4.unit] = b4
        self.ball = b4

    def loadComments(self, pos, text):
        b5 = CommentsItem(pos[2], pos[3], text, True)
        b5.setPos(pos[0], pos[1])
        self.scene().addItem(b5)
        self.ball = b5

    def loadLoopFor(self, unit, pos, inp, outp):
        if 'I' in unit:
            name = 'If'
        else:
            name = 'For_sequential'
            if 'm' in unit:
                name = 'For_multiprocessing'
            if 't' in unit:
                name = 'For_multithreading'
        b6 = ForLoopItem(unit, name, pos[2], pos[3], True, inp, outp)
        b6.setPos(pos[0], pos[1])
        self.scene().addItem(b6)
        editor.listItems[editor.currentTab][b6.unit] = b6
        self.ball = b6

    def loadConstant(self, unit, pos, vout, format, label):
        if format == 'list_str':
            b7 = Checkbox(unit, vout, label, True)
        elif format == 'path_box':
            b7 = Imagebox(unit, vout, label, True)
        else:
            b7 = Constants(unit, pos[2], pos[3], vout, format, label, True)
        b7.setPos(pos[0], pos[1])
        self.scene().addItem(b7)
        editor.listItems[editor.currentTab][b7.unit] = b7
        self.ball = b7

    def loadCluster(self, unit, pos, vout, format, label):
        b8 = Clusters(unit, pos[2], pos[3], vout, format, label, True)
        b8.setPos(pos[0], pos[1])
        self.scene().addItem(b8)
        editor.listItems[editor.currentTab][b8.unit] = b8
        self.ball = b8

    def loadScriptItem(self, unit, title, pos, inp, outp):
        b9 = ScriptItem(unit, title, pos[2], pos[3], True, True, inp, outp)
        b9.setPos(pos[0], pos[1])
        self.scene().addItem(b9)
        editor.listItems[editor.currentTab][b9.unit] = b9
        self.ball = b9

    def loadProbe(self, unit, label, format, pos):
        b10 = Probes(unit, format, label, True)
        b10.setPos(pos[0], pos[1])
        self.scene().addItem(b10)
        editor.listItems[editor.currentTab][b10.unit] = b10
        self.ball = b10

    def loadStopExec(self, unit, pos):
        b11 = StopExecution(unit, True)
        b11.setPos(pos[0], pos[1])
        self.scene().addItem(b11)
        editor.listItems[editor.currentTab][b11.unit] = b11
        self.ball = b11

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.__prevMousePos = event.pos()
        elif event.button() == Qt.MouseButton.LeftButton:
            # self.m_originX, self.m_originY = event.pos().x(), event.pos().y()
            self.m_originX, self.m_originY = self.mapToScene(event.pos()).x(), self.mapToScene(event.pos()).y()
            return QGraphicsView.mousePressEvent(self, event)
        else:
            super(DiagramView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.MiddleButton:
            offset = self.__prevMousePos - event.pos()
            self.__prevMousePos = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + offset.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() + offset.y())
        else:
            super(DiagramView, self).mouseMoveEvent(event)

    # def eventFilter(self, object, event):
    #     if object == self.verticalScrollBar() and event.type() == event.Wheel:
    #         return True
    #     if object == self.horizontalScrollBar() and event.type() == event.Wheel:
    #         return True
    #     return False
        # return QGraphicsView.eventFilter(self, object, event)

    def wheelEvent(self, event):
        adj = 0.1777
        if event.angleDelta().y() < 0:
            adj = -adj
        self.scalefactor += adj
        self.scale(1 + adj, 1 + adj)
        rectBounds = self.scene().itemsBoundingRect()
        self.scene().setSceneRect(rectBounds.x() - 200, rectBounds.y() - 200, rectBounds.width() + 400, rectBounds.height() + 400)

    def returnBlockSystem(self):
        return self.ball


class DimLink(Enum):
    simple = 2
    list = 6
    array = 8
    bis = 3


class ForLoopItem(QGraphicsRectItem):

    def __init__(self, unit, name, w, h, isMod, *inout, parent=None):
        super(ForLoopItem, self).__init__(None)
        self.normalState()
        self.setBrush(ItemColor.BACKGROUND_LOOP.value)
        self.setZValue(-1)
        self.unit = unit
        self.w = w
        self.h = h
        self.wmin = 100.0
        self.hmin = 100.0
        self.nbin, self.nbout = 0, 0
        self.moved = False
        self.isMod = isMod
        self.preview = False
        self.loopIf = False
        self.name = name
        if 'F' in unit or unit == 'newForLoop' or not unit:
            self.loopSizeMini = [[w, h], [0.0, 0.0]]
        elif 'I' in unit or unit == 'newIf':
            self.loopSizeMini = [[w, h], [w, h]]

        self.setCursor(QCursor(ItemMouse.HANDLETOPITEM.value))

        self.caseFinal = False
        self.currentLoop = None

        if unit == 'newForLoop':
            ForLoopExist = True
            inc = 0
            while ForLoopExist:
                if 'F' + str(inc) in editor.listTools[editor.currentTab] or \
                   'F' + str(inc) + "m" in editor.listTools[editor.currentTab] or \
                   'F' + str(inc) + "m*" in editor.listTools[editor.currentTab] or \
                   'F' + str(inc) + "t" in editor.listTools[editor.currentTab] or \
                   'F' + str(inc) + "t*" in editor.listTools[editor.currentTab]:
                    inc += 1
                else:
                    ForLoopExist = False
            self.unit = 'F' + str(inc)
            if name == 'For_multiprocessing':
                self.unit += 'm*'
            elif name == 'For_multithreading':
                self.unit += 't*'
        elif unit == 'newIf':
            self.loopIf = True
            IfConditionExist = True
            inc = 0
            while IfConditionExist:
                if 'I' + str(inc) in editor.listTools[editor.currentTab]:
                    inc += 1
                else:
                    IfConditionExist = False
            self.unit = 'I' + str(inc)
        else:
            if 'I' in unit:
                self.loopIf = True
            self.unit = unit

        self.inputs, self.outputs = [], []

        if self.isMod:
            if self.loopIf:
                editor.listTools[editor.currentTab][self.unit] = [[], []]
            else:
                editor.listTools[editor.currentTab][self.unit] = []
            editor.libTools[editor.currentTab][self.unit] = [[], []]

            if inout:
                editor.libTools[editor.currentTab][self.unit] = inout
                if inout[0]:
                    for i in range(0, len(inout[0])):
                        self.updateTunnelInput(inout[0][i])
                if inout[1]:
                    for i in range(0, len(inout[1])):
                        self.updateTunnelOutput(inout[1][i])

        self.label = QGraphicsTextItem(name, self)
        self.label.setFont(QFont("Times", 16, QFont.Weight.Bold))
        self.label.setDefaultTextColor(ItemColor.TEXT_LOOP.value)

        self.nameUnit = QGraphicsTextItem(self.unit, self)
        self.nameUnit.setDefaultTextColor(ItemColor.DEFAULTTEXTCOLOR.value)

        x, y = self.newSize(self.w, self.h)

        if self.isMod:
            self.setFlags(self.GraphicsItemFlag.ItemIsSelectable | self.GraphicsItemFlag.ItemIsMovable | self.GraphicsItemFlag.ItemIsFocusable | self.GraphicsItemFlag.ItemSendsGeometryChanges)
            self.resize = Slide(self)
            self.resize.setPos(x, y)
            self.resize.posChangeCallbacks.append(self.newSize)  # Connect the callback
            self.resize.setFlag(self.resize.GraphicsItemFlag.ItemIsSelectable, True)
            self.resize.wmin = self.wmin
            self.resize.hmin = self.hmin

        if name == 'If':
            if isMod:
                if editor.listIfShowedState:
                    if self.unit in editor.listIfShowedState[editor.currentTab].keys():
                        self.elemProxy = Control_IF(self.unit, "bool", str(editor.listIfShowedState[editor.currentTab][self.unit]))
                    else:
                        self.elemProxy = Control_IF(self.unit, "bool", 'True')
                        editor.listIfShowedState[editor.currentTab][self.unit] = True
                else:
                    editor.listIfShowedState[editor.currentTab][self.unit] = True
                self.elemProxy.setStyleSheet("selection-background-color: blue; background-color: rgb" + str(TypeColor.bool.value.getRgb()[0:3]))
                self.proxyWidget = QGraphicsProxyWidget(self, Qt.WindowType.Widget)
                self.proxyWidget.setWidget(self.elemProxy)
                self.proxyWidget.setPos(3, 3)
                self.proxyWidget.setZValue(3)
                portCondition = Port('val', 'in', 'bool', self.unit, False, True, -18, -25, self)
                self.inputs.append(portCondition)
                portCondition.setPos(0, 15)

    def itemChange(self, *args, **kwargs):
        gridSize = ItemGrid.SPACEGRID.value
        if args[0] == self.GraphicsItemChange.ItemPositionHasChanged:
            xV = round(args[1].x() / gridSize) * gridSize
            yV = round(args[1].y() / gridSize) * gridSize
            self.setPos(QPointF(xV, yV))
        return QGraphicsRectItem.itemChange(self, *args, **kwargs)

    def keyPressEvent(self, keyEvent):
        if keyEvent.key() == Qt.Key.Key_Delete:
            self.deleteItem()
#             UpdateUndoRedo()
        if keyEvent.key() == Qt.Key.Key_Up:
            self.setPos(self.x(), self.y() - 1)
        if keyEvent.key() == Qt.Key.Key_Down:
            self.setPos(self.x(), self.y() + 1)
        if keyEvent.key() == Qt.Key.Key_Left:
            self.setPos(self.x() - 1, self.y())
        if keyEvent.key() == Qt.Key.Key_Right:
            self.setPos(self.x() + 1, self.y())
        return QGraphicsRectItem.keyPressEvent(self, keyEvent)

    def mousePressEvent(self, event):
        if self.isMod:
            if event.button() == Qt.MouseButton.LeftButton:
                # editor.diagramScene[editor.currentTab].clearSelection()
                self.setSelected(True)

            if event.button() == Qt.MouseButton.RightButton:
                self.setSelected(True)

            # if self.isMod:
            self.selectItemsInside(self.unit, True)
#             UpdateUndoRedo()
#         return QGraphicsRectItem.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        pos = event.scenePos()
        if not self.preview and self.isMod:
            listTypeItems = []
            itms = editor.diagramScene[editor.currentTab].items(pos)

            for elem in itms:
                if type(elem) is ForLoopItem:
                    if elem.unit != self.unit:
                        listTypeItems.append(elem)

            if listTypeItems:
                if len(listTypeItems) > 1:
                    postmp = None
                    elemtmp = None
                    try:
                        self.currentLoop.normalState()
                    except Exception as e:
                        pass
                    for lsElem in listTypeItems:
                        if not postmp:
                            postmp = lsElem.pos()
                            elemtmp = lsElem
                        elif postmp.x() < lsElem.pos().x():
                            postmp = lsElem.pos()
                            elemtmp = lsElem

#                     self.currentLoop = elemtmp
#                     self.currentLoop.activeState()
#                     self.caseFinal = True
                else:
                    elemtmp = listTypeItems[0]
                    try:
                        ind = 0
                        if self.currentLoop.loopIf:
                            if self.currentLoop.elemProxy.currentText() == 'False':
                                ind = 1
                        self.currentLoop.normalState()
                        self.currentLoop.IteminLoop(self.unit, False, ind)
                        self.currentLoop = None
                        self.caseFinal = False
                    except Exception as e:
                        pass

                self.currentLoop = elemtmp
                self.currentLoop.activeState()
                self.caseFinal = True
            else:
                if self.currentLoop:
                    ind = 0
                    if self.currentLoop.loopIf:
                        if self.currentLoop.elemProxy.currentText() == 'False':
                            ind = 1
                    self.currentLoop.normalState()
                    self.currentLoop.IteminLoop(self.unit, False, ind)
                    self.currentLoop = None
                    self.caseFinal = False

            event.accept()
            self.moved = True

        return QGraphicsRectItem.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        if self.isMod:
            pos = event.scenePos()
            if self.currentLoop:
                ind = 0
                if self.currentLoop.loopIf:
                    if self.currentLoop.elemProxy.currentText() == 'False':
                        ind = 1
                self.currentLoop.IteminLoop(self.unit, True, ind)
                self.currentLoop.normalState()
                self.currentLoop.resize_frame(ind)
                self.currentLoop = None
                self.caseFinal = False
            if self.moved:
                UpdateUndoRedo()
                self.moved = False

            self.selectItemsInside(self.unit, True)
#             UpdateUndoRedo()

            return QGraphicsRectItem.mouseReleaseEvent(self, event)

    def selectItemsInside(self, unit, state):
        listToMove = []
        if 'I' in unit:
            listToMove.extend(editor.listTools[editor.currentTab][unit][0])
            listToMove.extend(editor.listTools[editor.currentTab][unit][1])

        else:
            listToMove.extend(editor.listTools[editor.currentTab][unit])

        for elemts in self.scene().items():
            if (type(elemts) in [BlockCreate, ForLoopItem, Constants, Clusters, Checkbox,
                                 ScriptItem, Probes, StopExecution, Imagebox] and
                    elemts.unit in listToMove):
                elemts.setSelected(state)
                if type(elemts) is ForLoopItem and elemts.unit != self.unit:
                    self.selectItemsInside(elemts.unit, state)

    def newSize(self, w, h):
        # print(w, h)
        if 'F' in self.unit:
            w, h = max(w, self.loopSizeMini[0][0]), max(h, self.loopSizeMini[0][1])
        else:
            w, h = max(w, self.loopSizeMini[0][0], self.loopSizeMini[1][0]), max(h, self.loopSizeMini[0][1], self.loopSizeMini[1][1])
            # if w < max(self.loopSizeMini[0][0], self.loopSizeMini[1][0]):
            #     w = max(self.loopSizeMini[0][0], self.loopSizeMini[1][0])
            # if h < max(self.loopSizeMini[0][1], self.loopSizeMini[1][1]):
            #     h = max(self.loopSizeMini[0][1], self.loopSizeMini[1][1])

        self.setRect(0.0, 0.0, w, h)
        self.label.setPos(0, -40)
        if self.nbin > 0:
            y = (h) / (self.nbin + 1)
            dy = (h) / (self.nbin + 1)
            for inp in range(len(self.inputs)):
                if 'in' in self.inputs[inp].name:
                    self.inputs[inp].setPos(-9, y)
                    self.outputs[inp].setPos(11, y)
                    y += dy
        if self.nbout > 0:
            y = (h) / (self.nbout + 1)
            dy = (h) / (self.nbout + 1)
            for inp in range(len(self.inputs)):
                if 'out' in self.inputs[inp].name:
                    self.inputs[inp].setPos(w - 9, y)
                    self.outputs[inp].setPos(w + 11, y)
                    y += dy
        rect = self.nameUnit.boundingRect()
        lw, lh = rect.width(), rect.height()
        lx = (w - lw) / 2
        ly = (h)
        self.nameUnit.setPos(lx, ly)
        self.w = w
        self.h = h
        # self.loopBottom = [w, h]
        # print('loopBottom current:', self.loopBottom)
        return w, h

    def updateSize(self):
        factorh = 20
        hmin = factorh * len(self.inputs)
        if self.hmin < hmin:
            self.hmin = hmin
        w, h = self.w, self.h
        if h < hmin:
            h = hmin
        hmin = factorh * len(self.outputs)
        if h < hmin:
            h = hmin
        if w < self.wmin:
            w = self.wmin
        x, y = self.newSize(w, h)
        return x, y

    def contextMenuEvent(self, event):
        if event.isAccepted:
            pass
        if self.isMod:
            menu = QMenu()
            intu = menu.addAction('Add tunnel input')
            intu.triggered.connect(self.addTunnelInputManual)
            outtu = menu.addAction('Add tunnel output')
            outtu.triggered.connect(self.addTunnelOutputManual)
            de = menu.addAction('Delete')
            de.triggered.connect(self.deleteItem)
            pa = menu.addAction('Parameters')
            pa.triggered.connect(self.editParameters)
            cs = menu.addAction('Change to sequencial For')
            cs.triggered.connect(self.changeForMode1)
            ct = menu.addAction('change to multithreading For')
            ct.triggered.connect(self.changeForMode2)
            cm = menu.addAction('Change to multiprocessing For')
            cm.triggered.connect(self.changeForMode3)
            if 'm' in self.unit:
                cm.setEnabled(False)
            elif 't' in self.unit:
                ct.setEnabled(False)
            else:
                cs.setEnabled(False)
                pa.setEnabled(False)

            menu.exec(event.screenPos())
#             return QGraphicsRectItem.contextMenuEvent(self, event)

    # to sequencial mode
    def changeForMode1(self):
        if 'm' in self.unit:
            tmp = self.unit[0:self.unit.index('m')]
        if 't' in self.unit:
            tmp = self.unit[0:self.unit.index('t')]
        self.name = 'For_sequential'
        self.updateListNodeTools(self.unit, tmp)
        self.unit = tmp
        self.nameUnit.setPlainText(tmp)
        self.label.setPlainText(self.name)
        for i in range(len(self.inputs)):
            self.inputs[i].unit = self.unit
        for i in range(len(self.outputs)):
            self.outputs[i].unit = self.unit
        UpdateUndoRedo()

    # to multithreading mode
    def changeForMode2(self):
        tmp = self.unit
        if 'm' in tmp:
            tmp = tmp.replace('m', '')
        if '*' in tmp:
            tmp = tmp.replace('*', '')
        tmp += 't*'
        self.name = 'For_multithreading'
        self.updateListNodeTools(self.unit, tmp)
        self.unit = tmp
        self.nameUnit.setPlainText(tmp)
        self.label.setPlainText(self.name)
        for i in range(len(self.inputs)):
            self.inputs[i].unit = self.unit
        for i in range(len(self.outputs)):
            self.outputs[i].unit = self.unit
        UpdateUndoRedo()

    # to multiprocess mode
    def changeForMode3(self):
        tmp = self.unit
        if 't' in tmp:
            tmp = tmp.replace('t', '')
        if '*' in tmp:
            tmp = tmp.replace('*', '')
        tmp += 'm*'
        self.name = 'For_multiprocessing'
        self.updateListNodeTools(self.unit, tmp)
        self.unit = tmp
        self.nameUnit.setPlainText(tmp)
        self.label.setPlainText(self.name)
        for i in range(len(self.inputs)):
            self.inputs[i].unit = self.unit
        for i in range(len(self.outputs)):
            self.outputs[i].unit = self.unit
        UpdateUndoRedo()

    def addTunnelInputManual(self):
        listNameTunnel = []
        for el in editor.libTools[editor.currentTab][self.unit][0]:
            listNameTunnel.append(el[0][0])

        for inc in range(0, len(listNameTunnel) + 1):
            if 'in' + str(inc) not in listNameTunnel:
                name = 'in' + str(inc)
                break

        c = defineTunnels(name, self.name, 'unknow')
        c.exec()

        if c.getNewValues():
            format = c.getNewValues()[0]
            typein = c.getNewValues()[1] + '_'
            typein = typein.replace('simple_', '')
            typeout = c.getNewValues()[2] + '_'
            typeout = typeout.replace('simple_', '')
            self.addTunnelInput(name, format, typein, typeout)

    def addTunnelInputAuto(self, typein):
        listNameTunnel = []
        for el in editor.libTools[editor.currentTab][self.unit][0]:
            listNameTunnel.append(el[0][0])

        indice = 0

        for inc in range(0, len(listNameTunnel) + 1):
            if 'in' + str(inc) not in listNameTunnel:
                name = 'in' + str(inc)
                indice = inc
                break

        format = typein
        if '_' in typein:
            format = typein[typein.index('_')+1:]
            typein = typein[0:typein.index('_')+1:]
        typeout = typein

        if 'F' in self.unit:
            if "array" in typein:
                typeout = "list_"
            elif "list" in typein:
                typeout = ""

        self.addTunnelInput(name, format, typein, typeout)

        return indice

    def alphaNumOrder(self, string):
        return ''.join([format(int(x), '05d') if x.isdigit()
                       else x for x in re.split(r'(\d+)', string)])

    def addTunnelInput(self, name, format, typein, typeout):
        self.nbin += 1
        portIn = Port(name, 'in', 'unkn', self.unit, False, True, 0, 0, self)
        portOut = Port(name, 'out', 'unkn', self.unit, False, True, 0, 0, self)
        self.inputs.append(portIn)
        self.outputs.append(portOut)

        self.inputs.sort(key=lambda x: self.alphaNumOrder(x.name))
        self.outputs.sort(key=lambda x: self.alphaNumOrder(x.name))

        x, y = self.updateSize()
        self.resize.setPos(x, y)

        portIn.format = typein + format
        portOut.format = typeout + format

        for types in TypeColor:
            if types.name in format:
                color = types.value

        portIn.setBrush(color)
        portOut.setBrush(color)

        listEnter = editor.libTools[editor.currentTab][self.unit][0]
        listOut = editor.libTools[editor.currentTab][self.unit][1]
        if listEnter:
            listEnter.append([[portIn.name, portIn.typeio, portIn.format], [portOut.name, portOut.typeio, portOut.format]])
        else:
            listEnter = [[[portIn.name, portIn.typeio, portIn.format], [portOut.name, portOut.typeio, portOut.format]]]

        editor.libTools[editor.currentTab][self.unit] = [listEnter, listOut]
        UpdateUndoRedo()

    def addTunnelOutputManual(self):
        listNameTunnel = []
        for el in editor.libTools[editor.currentTab][self.unit][1]:
            listNameTunnel.append(el[0][0])

        for inc in range(0, len(listNameTunnel) + 1):
            if 'out' + str(inc) not in listNameTunnel:
                name = 'out' + str(inc)
                break

        c = defineTunnels(name, self.name, 'unknow')
        c.exec()

        if c.getNewValues():
            format = c.getNewValues()[0]
            typein = c.getNewValues()[1] + '_'
            typein = typein.replace('simple_', '')
            typeout = c.getNewValues()[2] + '_'
            typeout = typeout.replace('simple_', '')
            self.addTunnelOutput(name, format, typein, typeout)

    def addTunnelOutputAuto(self, typeout):
        if 'enumerate' in typeout:
            typeout = 'str'
        listNameTunnel = []
        for el in editor.libTools[editor.currentTab][self.unit][1]:
            listNameTunnel.append(el[0][0])

        indice = 0

        for inc in range(0, len(listNameTunnel) + 1):
            if 'out' + str(inc) not in listNameTunnel:
                name = 'out' + str(inc)
                indice = inc
                break

        format = typeout
        if '_' in typeout:
            format = typeout[typeout.index('_')+1:]
            typeout = typeout[0:typeout.index('_')+1]
        else:
            typeout = ""

        typein = typeout

        if 'F' in self.unit:
            if "array" in typeout:
                typein = "list_"
            elif "list" in typeout:
                typein = ""

        self.addTunnelOutput(name, format, typein, typeout)

        return indice

    def addTunnelOutput(self, name, format, typein, typeout):
        self.nbout += 1
        portIn = Port(name, 'in', 'unkn', self.unit, False, True, 0, 0, self)
        portOut = Port(name, 'out', 'unkn', self.unit, False, True, 0, 0, self)

        self.inputs.append(portIn)
        self.outputs.append(portOut)

        self.inputs.sort(key=lambda x: self.alphaNumOrder(x.name))
        self.outputs.sort(key=lambda x: self.alphaNumOrder(x.name))

        x, y = self.updateSize()
        self.resize.setPos(x, y)

        portIn.format = typein + format
        portOut.format = typeout + format

        for types in TypeColor:
            if types.name in format:
                color = types.value

        portIn.setBrush(color)
        portOut.setBrush(color)

        listEnter = editor.libTools[editor.currentTab][self.unit][0]
        listOut = editor.libTools[editor.currentTab][self.unit][1]

        if listOut:
            listOut.append([[portIn.name, portIn.typeio, portIn.format], [portOut.name, portOut.typeio, portOut.format]])
        else:
            listOut = [[[portIn.name, portIn.typeio, portIn.format], [portOut.name, portOut.typeio, portOut.format]]]

        editor.libTools[editor.currentTab][self.unit] = [listEnter, listOut]
        UpdateUndoRedo()

    def updateTunnelInput(self, inp):
        self.nbin += 1
        name = inp[0][0]
        portIn = Port(name, 'in', inp[0][2], self.unit, False, True, 0, 0, self)
        portOut = Port(name, 'out', inp[1][2], self.unit, False, True, 0, 0, self)
#         portIn.label.setPlainText(name)
        self.inputs.append(portIn)
        self.outputs.append(portOut)

        listEnter = []
        listOut = []
        try:
            listEnter = editor.libTools[editor.currentTab][self.unit][0]
        except Exception as e:
            pass

        try:
            listOut = editor.libTools[editor.currentTab][self.unit][1]
        except Exception as e:
            pass

        format = inp[0][2]

        for types in TypeColor:
            if types.name in format:
                color = types.value

        portIn.setBrush(color)
        portOut.setBrush(color)

    def updateTunnelOutput(self, outp):
        self.nbout += 1
        name = outp[0][0]
        portOut = Port(name, 'out', outp[1][2], self.unit, False, True, -24, -25, self)
        portIn = Port(name, 'in', outp[0][2], self.unit, False, True, 4, -12, self)
        self.outputs.append(portOut)
        self.inputs.append(portIn)

        listEnter = []
        listOut = []
        try:
            listEnter = editor.libTools[editor.currentTab][self.unit][0]
        except Exception as e:
            pass

        try:
            listOut = editor.libTools[editor.currentTab][self.unit][1]
        except Exception as e:
            pass

        format = outp[0][2]

        for types in TypeColor:
            if types.name in format:
                color = types.value

        portIn.setBrush(color)
        portOut.setBrush(color)

    def deleteTunnel(self, name):

        if 'in' in name:
            self.nbin -= 1
        elif 'out' in name:
            self.nbout -= 1

        for elem in editor.diagramView[editor.currentTab].items():
            if type(elem) is Port:
                if elem.name == name and elem.unit == self.unit:
                    editor.diagramScene[editor.currentTab].removeItem(elem)
                    if elem.typeio == 'in':
                        self.inputs.remove(elem)
                    else:
                        self.outputs.remove(elem)
            if type(elem) is LinkItem:
                if editor.listNodes[editor.currentTab][elem.name].find(self.unit + ':' + name) != -1:
                    BlockCreate.deletelink(self, elem, self.unit)
        x, y = self.updateSize()
        self.resize.setPos(x, y)

        listEnter = []
        listOut = []
        try:
            listEnter = editor.libTools[editor.currentTab][self.unit][0]
            c = 0
            for le in listEnter:
                if le[0][0] == name:
                    del listEnter[c]
                    break
                c += 1
        except Exception as e:
            pass

        try:
            listOut = editor.libTools[editor.currentTab][self.unit][1]
            c = 0
            for lo in listOut:
                if lo[0][0] == name:
                    del listOut[c]
                    break
                c += 1
        except Exception as e:
            pass

        del editor.libTools[editor.currentTab][self.unit]
        editor.libTools[editor.currentTab][self.unit] = [listEnter, listOut]
        UpdateUndoRedo()

    def normalState(self):
        self.setPen(QPen(ItemColor.FRAME_LOOP_NORMAL.value, 8))

    def activeState(self):
        self.setPen(QPen(ItemColor.FRAME_LOOP_ACTIVED.value, 8))

    def IteminLoop(self, unitItem, casef, ind):
        # print(unitItem, casef, ind)
        ItemToExclude = []
        listItem = editor.listTools[editor.currentTab][self.unit]

        if self.unit not in unitItem:
            if self.loopIf:
                if casef:
                    listItem[ind].append(unitItem)
                else:
                    try:
                        listItem[ind].remove(unitItem)
                    except Exception as e:
                        pass
                listItem[ind] = list(set(listItem[ind]))

            else:
                if casef:
                    listItem.append(unitItem)
                else:
                    try:
                        listItem.remove(unitItem)
                    except Exception as e:
                        pass
                listItem = list(set(listItem))
            editor.listTools[editor.currentTab][self.unit] = listItem
            ValueZ2()

    def resize_frame(self, ind):
        loopTop = [self.scenePos().x(), self.scenePos().y()]
        loopBound = self.boundingRect()
        loopBottom = [loopTop[0] + loopBound.width(), loopTop[1] + loopBound.height()]
        loopBottom2 = loopBottom.copy()
        tmpTop, tmpBottom = loopTop.copy(), loopBottom.copy()
        posBottomMax = [loopTop[0], loopTop[1]]
        listItem = editor.listTools[editor.currentTab][self.unit]
        if self.loopIf:
            listItem = listItem[ind]
        for lstim in listItem:
            if 'N' not in lstim:
                adBottom = [0.0, 0.0]
                currentItem = editor.listItems[editor.currentTab][lstim]
                posTop = [currentItem.scenePos().x(), currentItem.scenePos().y()]
                boud = currentItem.boundingRect()
                posBottom = [posTop[0] + boud.width(), posTop[1] + boud.height()]

                loopTop[0], loopTop[1] = min(loopTop[0], posTop[0]), min(loopTop[1], posTop[1])
                loopBottom[0], loopBottom[1] = max(loopBottom[0], posBottom[0]), max(loopBottom[1], posBottom[1])

                posBottomMax = [max(posBottomMax[0], posBottom[0]), max(posBottomMax[1], posBottom[1])]
                # loopBottom2[0], loopBottom2[1] = min(loopBottom2[0], posBottomMax[0]), min(loopBottom2[1], posBottomMax[1])
                loopBottom2 = posBottomMax

                if loopBottom2[0]*loopTop[0] > 0:
                    adBottom[0] = abs(abs(loopBottom2[0]) - abs(loopTop[0])) + 20
                else:
                    adBottom[0] = abs(abs(loopBottom2[0]) - loopTop[0]) + 20
                if loopBottom2[1]*loopTop[1] > 0:
                    adBottom[1] = abs(abs(loopBottom2[1]) - abs(loopTop[1])) + 20
                else:
                    adBottom[1] = abs(abs(loopBottom2[1]) - loopTop[1]) + 20
                # adBottom = [abs(abs(loopBottom2[0]) - abs(loopTop[0])) + 20, abs(abs(loopBottom2[1]) - abs(loopTop[1])) + 20]
                self.loopSizeMini[ind] = adBottom
                # self.loopBottom = [max(self.loopBottom[0], adBottom[0]), max(self.loopBottom[1], adBottom[1])]

        if (tmpTop != loopTop) or (tmpBottom != loopBottom):
            delt1, delt2 = 0, 0
            if (tmpTop != loopTop):
                delt1 = 50
            if (tmpBottom != loopBottom):
                delt2 = 100
            w, h = loopBottom[0] - loopTop[0], loopBottom[1] - loopTop[1]
            self.setPos(QPointF(loopTop[0] - delt1, loopTop[1] - delt1))
            self.newSize(w + delt2, h + delt2)
            x, y = self.updateSize()
            self.resize.setPos(x, y)
            self.loopSizeMini[ind] = [x, y]

    def editParameters(self):
        c = editParamLoopFor('For Loop', self.nameUnit.toPlainText())
        c.exec()
        tmp = self.unit
        check, cpu_ct, answ = c.getNewValues()
        if answ == 'ok':
            if check:
                if '*' not in self.unit:
                    tmp += '*'
                    self.updateListNodeTools(self.unit, tmp)
                    self.nameUnit.setPlainText(tmp)
                    self.unit = tmp
                    for i in range(len(self.inputs)):
                        self.inputs[i].unit = self.unit
                    for i in range(len(self.outputs)):
                        self.outputs[i].unit = self.unit
                    UpdateUndoRedo()
            else:
                if '*' in self.unit:
                    tmp = self.unit.replace('*', '')
                    self.updateListNodeTools(self.unit, tmp)
                    self.nameUnit.setPlainText(tmp)
                    self.unit = tmp
                    for i in range(len(self.inputs)):
                        self.inputs[i].unit = self.unit
                    for i in range(len(self.outputs)):
                        self.outputs[i].unit = self.unit
                    UpdateUndoRedo()
            if cpu_ct > os.cpu_count():
                cpu_ct = os.cpu_count()

            Config().setCpuCount(cpu_ct)

    def updateListNodeTools(self, oldUnit, newUnit):
        editor.libTools[editor.currentTab][newUnit] = editor.libTools[editor.currentTab][oldUnit]
        del editor.libTools[editor.currentTab][oldUnit]
        editor.listTools[editor.currentTab][newUnit] = editor.listTools[editor.currentTab][oldUnit]
        del editor.listTools[editor.currentTab][oldUnit]
        tmplist = editor.listTools[editor.currentTab].copy()
        for key_lstools, val_listools in tmplist.items():
            if 'F' in key_lstools:
                if oldUnit in val_listools:
                    new_list = val_listools
                    new_list.remove(oldUnit)
                    new_list.append(newUnit)
                    del editor.listTools[editor.currentTab][key_lstools]
                    editor.listTools[editor.currentTab][key_lstools] = new_list
            elif 'I' in key_lstools:
                if oldUnit in val_listools[0]:
                    new_list = val_listools[0]
                    same_list = val_listools[1]
                    new_list.remove(oldUnit)
                    new_list.append(newUnit)
                    del editor.listTools[editor.currentTab][key_lstools]
                    editor.listTools[editor.currentTab][key_lstools] = [new_list, same_list]
                elif oldUnit in val_listools[1]:
                    same_list = val_listools[0]
                    new_list = val_listools[1]
                    new_list.remove(oldUnit)
                    new_list.append(newUnit)
                    del editor.listTools[editor.currentTab][key_lstools]
                    editor.listTools[editor.currentTab][key_lstools] = [same_list, new_list]
        for keyN, valN in editor.listNodes[editor.currentTab].items():
            if oldUnit in valN:
                editor.listNodes[editor.currentTab][keyN] = valN.replace(oldUnit, newUnit)
        editor.listItems[editor.currentTab][newUnit] = editor.listItems[editor.currentTab][oldUnit]
        del editor.listItems[editor.currentTab][oldUnit]

    def deleteItem(self):
        editor.diagramScene[editor.currentTab].removeItem(self)
        ItemsToDelete = []
        if self.loopIf:
            if self.elemProxy.currentText() == 'True':
                ItemsToDelete = editor.listTools[editor.currentTab][self.unit][1]
            else:
                ItemsToDelete = editor.listTools[editor.currentTab][self.unit][0]
            del editor.listIfShowedState[editor.currentTab][self.unit]
        for elem in editor.diagramView[editor.currentTab].items():
            if type(elem) is LinkItem:
                if editor.listNodes[editor.currentTab][elem.name].find(self.unit + ':') != -1:
                    BlockCreate.deletelink(self, elem, self.unit)
            else:
                if ItemsToDelete and type(elem) in [BlockCreate, Constants, Clusters, ForLoopItem, Checkbox,
                                                    ScriptItem, Probes, Checkbox, Imagebox, StopExecution]:
                    if elem.unit in ItemsToDelete:
                        elem.deleteItem()
        del editor.listTools[editor.currentTab][self.unit]
        del editor.libTools[editor.currentTab][self.unit]
        del editor.listItems[editor.currentTab][self.unit]
        editor.deleteItemsLoop(self)


class getPathWork():
    def pathWork(self):
        return editor.currentpathwork


class Imagebox(QGraphicsRectItem):

    def __init__(self, unit='', pathImage='path', label='', isMod=True, parent=None):
        super(Imagebox, self).__init__(parent)

        self.sh = ("")
        self.form = 'path_box'
        self.format = self.form

        self.preview = False
        self.moved = False
        self.currentLoop = None

        self.isMod = isMod
        self.setZValue(2)
        if self.isMod:
            self.setFlags(self.GraphicsItemFlag.ItemIsSelectable | self.GraphicsItemFlag.ItemIsMovable | self.GraphicsItemFlag.ItemIsFocusable)
            self.setFlag(self.GraphicsItemFlag.ItemSendsGeometryChanges)
            self.setAcceptHoverEvents(True)

        if unit == 'newImagebox':
            ConstantExist = True
            inc = 0
            while ConstantExist:
                if 'A' + str(inc) in editor.listConstants[editor.currentTab]:
                    inc += 1
                else:
                    ConstantExist = False
            self.unit = 'A' + str(inc)
        else:
            self.unit = unit

        self.label = label if label else 'imagebox'

        self.elemProxy = QLabel()
        self.elemProxy.setBackgroundRole(QPalette.ColorRole.Base)
        self.elemProxy.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.elemProxy.setScaledContents(True)

        self.proxyWidget = QGraphicsProxyWidget(self, Qt.WindowType.Widget)
        self.proxyWidget.setWidget(self.elemProxy)
        self.proxyWidget.setPos(3, 3)
        self.proxyWidget.setZValue(3)
        self.elemProxy.setCursor(QCursor(ItemMouse.HANDLETOPITEM.value))

        self.w = self.proxyWidget.boundingRect().size().width() + 6
        self.h = self.proxyWidget.boundingRect().size().height() + 6

        self.lab = QGraphicsTextItem(self.label, self)
        self.lab.setDefaultTextColor(ItemColor.DEFAULTTEXTCOLOR.value)
        self.lab.setFont(QFont("Times", 12, QFont.Weight.Bold))
        self.lab.setPos(0, -30)
        self.lab.setVisible(True)

        self.labshape = QGraphicsTextItem('path', self)
        self.labshape.setDefaultTextColor(ItemColor.DEFAULTTEXTCOLOR.value)
        self.labshape.setFont(QFont("Times", 12, QFont.Weight.Bold))
        self.labshape.setPos(- 2 + self.w / 2, self.h + 3)

        self.setPen(QPen(ItemColor.FRAME_CONSTANTS.value, 3))
        color = ItemColor.BACKGROUND.value
        self.setBrush(QBrush(color))
        self.setRect(0.0, 0.0, self.w, self.h)
        self.inputs, self.outputs = [], []
        self.outputs.append(Port('', 'out', 'path', self.unit, True, self.isMod, 80, -12, self))
        self.outputs[0].setPos(self.w + 2, self.h / 2)
#         if self.isMod:
#             editor.listConstants[editor.currentTab][self.unit] = ('path_box', self.pathImage, self.label)
        if os.path.isfile(pathImage) and pathImage != 'path':
            self.loadImage(pathImage)
        else:
            pathbkg = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            pathbkg = os.path.join(pathbkg, 'ressources', 'no_img.png')
            self.pathImage = 'path'
            oImage = QImage(pathbkg)
            self.elemProxy.setPixmap(QPixmap.fromImage(oImage))
#             self.elemProxy.adjustSize()
            self.elemProxy.setGeometry(5, 5, 150, 150)
            self.proxyWidget.setWidget(self.elemProxy)
            self.w = self.proxyWidget.boundingRect().size().width() + 11
            self.h = self.proxyWidget.boundingRect().size().height() + 11
            self.setRect(0.0, 0.0, self.w, self.h)
            self.outputs[0].setPos(self.w + 2, self.h / 2)
            if self.isMod:
                editor.listConstants[editor.currentTab][self.unit] = ('path_box', self.pathImage, self.label)

    def mouseDoubleClickEvent(self, event):
        if self.isMod:
            if self.pathImage == 'path':
                self.pathImage = editor.currentpathdata
            dialog = QProgressDialog('Loading image', None, 0, 0, None)
            bar = QProgressBar(dialog)
            bar.setTextVisible(False)
            bar.setMinimum(0)
            bar.setMaximum(0)
            dialog.setBar(bar)
            dialog.show()
            fileDiagram = QFileDialog.getOpenFileName(
                                None,
                                "Choose Nifti, jpeg file",
                                self.pathImage,
                                'Nifti (*.nii *.nii.gz *.jpg *.png)',
                                None,
                                QFileDialog.Option.DontUseNativeDialog)
            if fileDiagram[0] != '':
                try:
                    del editor.listImgBox[editor.currentTab][self.unit]
                except Exception as err:
                    pass
                self.loadImage(fileDiagram[0])
                editor.currentpathdata = fileDiagram[0]
                UpdateUndoRedo()
            dialog.close()

    def mouseMoveEvent(self, mouseEvent):
        # self.moved = True
        mouseEvent.accept()
        editor.loopMouseMoveEvent(self, mouseEvent.scenePos())
        return QGraphicsRectItem.mouseMoveEvent(self, mouseEvent)

    def mouseReleaseEvent(self, event):
        # if self.moved:
        #     UpdateUndoRedo()
        #     self.moved = False
        editor.loopMouseReleaseEvent(self, True)
        return QGraphicsRectItem.mouseReleaseEvent(self, event)

    def loadImage(self, pathFile):
        from PIL import Image
        self.pathImage = pathFile
        x_scale, y_scale, z_scale = 1.0, 1.0, 1.0
        ratio = 1
        showFov = False
        if self.unit in editor.listImgBox[editor.currentTab]:
            oImage = editor.listImgBox[editor.currentTab][self.unit][0]
            self.sh = editor.listImgBox[editor.currentTab][self.unit][1]
            self.fov = editor.listImgBox[editor.currentTab][self.unit][2]
            x_scale, y_scale = editor.listImgBox[editor.currentTab][self.unit][3]
            ratio = x_scale / y_scale
            del editor.listImgBox[editor.currentTab][self.unit]
        elif self.pathImage.endswith(('.jpg', '.png')):
            img = Image.open(self.pathImage)
            self.sh = img.size
            self.fov = ''
            oImage = QImage(self.pathImage)
        else:
            showFov = True
            import nibabel as nib
            import numpy as np
            from scipy.ndimage import rotate
            img = nib.load(pathFile)
            x_scale, y_scale, z_scale = img.header['pixdim'][1], img.header['pixdim'][2], img.header['pixdim'][3]
            ratio = x_scale / y_scale
            cal_max, cal_min = img.header['cal_max'], img.header['cal_min']
            self.sh = img.shape
            self.fov = ''
            img = img.get_fdata().copy()
            img[np.isnan(img)] = 0.0
            if len(self.sh) == 3:
                img = img[:, :, int(round(self.sh[2]/2))]
            elif len(self.sh) == 4:
                img = img[:, :, int(round(self.sh[2]/2)), int(round(self.sh[3]/2))]
            elif len(self.sh) == 5:
                img = img[:, :, int(round(self.sh[2]/2)), int(round(self.sh[3]/2)), int(round(self.sh[4]/2))]
            img = np.fliplr(rotate(img, -90, reshape=True))
            img = np.uint8(255.0 * (img - img.min())/np.ptp(img))
            totalBytes = img.nbytes
            bytesPerLine = int(totalBytes/self.sh[1])
            oImage = QImage(img, self.sh[0], self.sh[1], bytesPerLine, QImage.Format.Format_Indexed8)
        # factor = max([self.sh[0], self.sh[1]]) / 300.0
        fov_x, fov_y = x_scale * self.sh[0], y_scale * self.sh[1]
        factor = max(fov_x, fov_y) / 400.0
        if not self.fov:
            self.fov = '{:.2f}x{:.2f}x{:.2f} mm3'.format(fov_x, fov_y, z_scale)
        self.elemProxy.setPixmap(QPixmap.fromImage(oImage))
        # self.elemProxy.setGeometry(5, 5, int(self.sh[0] / factor), int(self.sh[1] / factor))
        self.elemProxy.setGeometry(5, 5, int(fov_x / factor), int(fov_y / factor))
        editor.listImgBox[editor.currentTab][self.unit] = (oImage, self.sh, self.fov, (x_scale, y_scale))
        self.proxyWidget.resize(10, 10)
        self.proxyWidget.updateGeometry()
        # self.proxyWidget.resize(self.sh[0] / factor, self.sh[1] / (ratio * factor))
        self.proxyWidget.resize(fov_x / factor, fov_y / (ratio * factor))

        self.proxyWidget.setWidget(self.elemProxy)
        self.proxyWidget.updateGeometry()
        self.w = self.proxyWidget.boundingRect().size().width() + 8
        self.h = self.proxyWidget.boundingRect().size().height() + 8
        self.setRect(0.0, 0.0, self.w, self.h)
        self.outputs[0].setPos(self.w + 2, self.h / 2)
        # if showFov:
        #     self.labshape.setPlainText('{}\r{}'.format(str(self.fov), str(self.sh)))
        # else:
        #     self.labshape.setPlainText(str(self.sh))
        self.labshape.setPlainText('{}\r{}'.format(str(self.fov), str(self.sh)))
        rect = self.labshape.boundingRect()
        self.labshape.setPos((self.w / 2) - rect.size().width() / 2, self.h + 3)
        editor.listConstants[editor.currentTab][self.unit] = ('path_box', pathFile, self.label)

        # UpdateUndoRedo()

    def hoverEnterEvent(self, event):
        # self.setFocus(True)
        txt = "<p style=\"background-color: #fff59d;\">"
        txt += "<br><span style=\" \
               font-size:9pt; \
               font-weight:1000; \
               color:#AA1100; \" >"
        txt += self.pathImage
        txt += "<br></span></p>"
        self.setToolTip(txt)
        event.accept()
#         return QGraphicsRectItem.hoverEnterEvent(self, event)

    # def itemChange(self, *args, **kwargs):
    #     gridSize = ItemGrid.SPACEGRID.value
    #     if args[0] == self.GraphicsItemChange.ItemPositionHasChanged:
    #         xV = round(args[1].x() / gridSize) * gridSize
    #         yV = round(args[1].y() / gridSize) * gridSize
    #         self.setPos(QPointF(xV, yV))
    #     return QGraphicsRectItem.itemChange(self, *args, **kwargs)

    def contextMenuEvent(self, event):
        if self.isMod:
            menu = QMenu()
            de = menu.addAction('Delete')
            de.triggered.connect(self.deleteItem)
            pa = menu.addAction('Change label')
            pa.triggered.connect(self.changeLabel)
            li = menu.addAction('Load image')
            li.triggered.connect(self.mouseDoubleClickEvent)
            # br = menu.addAction('Display range')
            # br.triggered.connect(self.displayRange)
            menu.exec(event.screenPos())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            self.setPos(self.x(), self.y() - 1)
        if event.key() == Qt.Key.Key_Down:
            self.setPos(self.x(), self.y() + 1)
        if event.key() == Qt.Key.Key_Left:
            self.setPos(self.x() - 1, self.y())
        if event.key() == Qt.Key.Key_Right:
            self.setPos(self.x() + 1, self.y())

    def changeLabel(self):
        listLabCts = []
        for x, y in editor.listConstants[editor.currentTab].items():
            listLabCts.append(y[2])
        listVal = editor.listConstants[editor.currentTab][self.unit]
        oldVal = listVal[2]
        c = changeLabel('Const', self.unit, oldVal)
        c.exec()
        try:
            self.label = c.getNewLabel()
            if self.label in listLabCts:
                self.label += '-b'
            self.lab.setPlainText(self.label)
            del editor.listConstants[editor.currentTab][self.unit]
            editor.listConstants[editor.currentTab][self.unit] = (listVal[0], listVal[1], self.label)
            UpdateUndoRedo()
        except OSError as err:
            print("OS error: {0}".format(err))

    def deleteItem(self):
        for elem in editor.diagramView[editor.currentTab].items():
            if type(elem) is LinkItem:
                if editor.listNodes[editor.currentTab][elem.name].find(self.unit + ':') != -1:
                    BlockCreate.deletelink(self, elem, self.unit)
        editor.diagramScene[editor.currentTab].removeItem(self)
        del editor.listConstants[editor.currentTab][self.unit]
        del editor.listItems[editor.currentTab][self.unit]
        try:
            del editor.listImgBox[editor.currentTab][self.unit]
        except Exception as err:
            pass
        editor.deleteItemsLoop(self)

    # def displayRange(self):
    #     pass


class ItemColor(Enum):
    BACKGROUND = QColor(40, 40, 40, 100)
    PROCESS_TOP = QColor(62, 83, 104, 255)
    PROCESS_BOT = QColor(44, 62, 80, 255)
    FRAME_PROCESS = QColor(140, 140, 140, 200)
    SUBPROCESS_TOP = QColor(250, 100, 0, 255)
    SUBPROCESS_BOT = QColor(200, 50, 0, 255)
    BACKGROUND_LOOP = QColor(70, 70, 70, 150)
    TEXT_LOOP = QColor(160, 160, 100, 255)
    FRAME_SUBPROCESS = QColor(250, 100, 0, 255)
    FRAME_LOOP_NORMAL = QColor(190, 190, 190, 255)
    FRAME_LOOP_ACTIVED = QColor(50, 250, 0, 255)
    DEFAULTTEXTCOLOR = QColor(220, 220, 220, 200)
    TEXT_LABEL_PROCESS = QColor(220, 100, 100, 255)
    TEXT_PORT_LABEL_INPUT = QColor(220, 220, 220, 255)
    TEXT_PORT_LABEL_OUTPUT = QColor(220, 220, 220, 255)
    TEXT_PORT_LABEL_INPUT2 = QColor(150, 150, 150, 255)
    TEXT_PORT_LABEL_OUTPUT2 = QColor(150, 150, 150, 255)
    BIS_LINK = BACKGROUND
#     bis_link = QColor(30, 30, 30, 255)
    FOCUS_LINK = QColor(150, 150, 250, 255)
    FRAME_COMMENT = QColor(100, 100, 200, 255)
    BACKGROUND_COMMENT = QColor(60, 140, 255, 100)
    BACKGROUND_TXT_COMMENT = QColor(0, 0, 255, 255)
    TEXT_COMMENT = QColor(120, 150, 250, 255)
    CROSS_SCENE = QColor(250, 100, 0, 255)
    FRAME_SCRIPT = QColor(160, 160, 160, 255)
    FRAME_CONNECT = QColor(0, 250, 100, 255)
    FRAME_CONSTANTS = QColor(140, 140, 140, 255)
    FRAME_PROBE = QColor(160, 160, 160, 255)
    TEXT_TAB = QColor(20, 20, 20, 255)


class ItemMouse(Enum):
    HANDLETOPITEM = Qt.CursorShape.PointingHandCursor
    CROSSCURSOR = Qt.CursorShape.CrossCursor
    HORCURSOR = Qt.CursorShape.SizeHorCursor
    DIAGCURSOR = Qt.CursorShape.SizeFDiagCursor
    ALLCURSOR = Qt.CursorShape.SizeAllCursor
    # VERCURSOR = Qt.CursorShape.SizeVerCursor
    # SPLITVCURSOR = Qt.CursorShape.SplitVCursor
    # SPLITHCURSOR = Qt.CursorShape.SplitHCursor
    # HANDLETOPLEFT = Qt.CursorShape.SizeFDiagCursor
    # HANDLETOPMIDDLE = Qt.CursorShape.SizeVerCursor
    # HANDLETOPRIGHT = Qt.CursorShape.SizeBDiagCursor
    # HANDLEMIDDLELEFT = Qt.CursorShape.SizeHorCursor
    # HANDLEMIDDLERIGHT = Qt.CursorShape.SizeHorCursor
    # HANDLEBOTTOMLEFT = Qt.CursorShape.SizeBDiagCursor
    # HANDLEBOTTOMMIDDLE = Qt.CursorShape.SizeVerCursor
    # HANDLEBOTTOMRIGHT = Qt.CursorShape.SizeFDiagCursor


class ItemGrid(Enum):
    SPACEGRID = 0.01
    # SPACEGRID = 25


class ItemResize(Enum):
    FONT_TEXT = 14

    @classmethod
    def screenSize(cls):
        return QApplication.primaryScreen().size()

    @classmethod
    def newSize(cls):
        return cls.screenSize()


class LabelGroup(QGraphicsTextItem):

    def __init__(self, parent=None):
        super(LabelGroup, self).__init__(parent)

        self.setDefaultTextColor(ItemColor.TEXT_COMMENT.value)
        self.setFont(QFont("Times", 30, QFont.Weight.Bold))
        self.setZValue(0)

    def mouseDoubleClickEvent(self, event):
        self.changeComment()
        UpdateUndoRedo()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            editor.diagramScene[editor.currentTab].clearSelection()
            self.setSelected(True)
            event.accept()
            return QGraphicsTextItem.mousePressEvent(self, event)

    class _CommentEdit(QDialog):

        def __init__(self, parent=None):
            super(LabelGroup._CommentEdit, self).__init__(parent)
            layout = QVBoxLayout(self)
            hlay1 = QHBoxLayout()
            layout.addLayout(hlay1)
            hlay1.addWidget(QLabel('Comment:'))
            self.name_line = QTextEdit()
            hlay1.addWidget(self.name_line)
            hlay2 = QHBoxLayout()
            layout.addLayout(hlay2)
            ok = QPushButton('OK')
            hlay2.addWidget(ok)
            cancel = QPushButton('Cancel')
            hlay2.addWidget(cancel)
            ok.clicked.connect(self.accept)
            cancel.clicked.connect(self.reject)

    def changeComment(self):
        dial = self._CommentEdit()
        dial.name_line.setText(self.toPlainText())
        res = dial.exec()
        if res:
            self.setPlainText(str(dial.name_line.toPlainText()))
            self.setPos(self.boundingRect().x(), self.boundingRect().y() - self.boundingRect().height())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            self.setPos(self.x(), self.y() - 2)
        if event.key() == Qt.Key.Key_Down:
            self.setPos(self.x(), self.y() + 2)
        if event.key() == Qt.Key.Key_Left:
            self.setPos(self.x() - 2, self.y())
        if event.key() == Qt.Key.Key_Right:
            self.setPos(self.x() + 2, self.y())


class LibMod(QStandardItemModel):

    def __init__(self, nameItem, parent=None):
        QStandardItemModel.__init__(self, parent)
        self.name = nameItem

    def mimeTypes(self):
        return [self.name]

    def mimeData(self, items):
        mimedata = QMimeData()
        for item in items:
            if item.isValid():
                try:
                    txt = self.data(item, Qt.ItemDataRole.DisplayRole)
                    if txt not in editor.listCategorySubMod:
                        mimedata.setData(self.name, QByteArray(txt.encode()))
                except Exception as e:
                    pass
        return mimedata


class LinkItem(QGraphicsPathItem):

    def __init__(self, name, typeColor):
        super(LinkItem, self).__init__(None)

        # self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        # self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemScenePositionHasChanged, True)

        self.bislink = QGraphicsPathItem()
        self.bislink.setZValue(3)

        self.setCursor(QCursor(ItemMouse.HANDLETOPITEM.value))

        for types in TypeColor:
            if types.name in typeColor:
                self.color = types.value

        if 'list' in str(typeColor):
            self.weight = DimLink.list.value
            self.bislink.setPen(QPen(Qt.PenStyle.NoPen))

        elif 'array' in str(typeColor):
            self.weight = DimLink.array.value
            self.bislink.setPen(QPen(ItemColor.BIS_LINK.value, DimLink.bis.value, Qt.PenStyle.SolidLine))

        else:
            self.weight = DimLink.simple.value
            self.bislink.setPen(QPen(Qt.PenStyle.NoPen))

        self.setPen(QPen(self.color, self.weight))
        # self.setBrush(QBrush(Qt.BrushStyle.NoBrush))
        # self.setScale(1)
        self.setZValue(2)

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable, True)
        # self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
#         self.setAcceptHoverEvents(True)

        self.name = ''

        if name == '':
            NodeExist = True
            inc = 0
            while NodeExist:
                if 'N' + str(inc) in editor.listNodes[editor.currentTab]:
                    inc += 1
                else:
                    NodeExist = False
            self.name = 'N' + str(inc)
        else:
            self.name = name

        self.linkTxt = LinkText(self.name, self.color)
        self.linkTxt.setVisible(True)
        self.linkShow = LinkArrow(self.color)
        self.linkShow.setVisible(True)

        editor.diagramScene[editor.currentTab].addItem(self.linkTxt)
        editor.diagramScene[editor.currentTab].addItem(self.linkShow)
        editor.diagramScene[editor.currentTab].addItem(self.bislink)

    def foncedBlock(self, fcd):
        if fcd:
            self.setOpacity(0.4)
        else:
            self.setOpacity(1.0)

    # def focusInEvent(self, event):
    #     style_sh = ItemColor.FOCUS_LINK.value
    #     self.setPen(QPen(style_sh, 2, Qt.PenStyle.SolidLine))
    #     self.linkTxt.setDefaultTextColor(style_sh)
    #     self.linkShow.setPen(QPen(style_sh, 2))
    #     self.bislink.setPen(QPen(Qt.PenStyle.NoPen))
    #     return QGraphicsPathItem.focusInEvent(self, event)

    def focusOutEvent(self, event):
        self.setPen(QPen(self.color, self.weight))
        self.linkTxt.setDefaultTextColor(self.color)
        self.linkShow.setPen(QPen(self.color, 2))
        if self.weight == 8:
            self.bislink.setPen(QPen(ItemColor.BIS_LINK.value, DimLink.bis.value, Qt.PenStyle.SolidLine))
        return QGraphicsPathItem.focusOutEvent(self, event)

    def mousePressEvent(self, event):
        editor.diagramScene[editor.currentTab].clearSelection()
        # self.setSelected(True)
        if event.button() == Qt.MouseButton.RightButton:
            pos = event.scenePos()
            items = editor.diagramScene[editor.currentTab].items(pos)
            listItems = [type(it) for it in items]
            if Port not in listItems:
                menu = QMenu()
                de = menu.addAction('Delete this link')
                de.triggered.connect(self.deletelink)
                menu.exec(event.screenPos())
        elif event.button() == Qt.MouseButton.LeftButton:
            style_sh = ItemColor.FOCUS_LINK.value
            self.setPen(QPen(style_sh, 2, Qt.PenStyle.SolidLine))
            self.linkTxt.setDefaultTextColor(style_sh)
            self.linkShow.setPen(QPen(style_sh, 2))
            self.bislink.setPen(QPen(Qt.PenStyle.NoPen))
            # return QGraphicsPathItem.focusInEvent(self, event)
        # return QGraphicsPathItem.mousePressEvent(self, event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            try:
                self.deletelink()
            except Exception as err:
                Menu().btnPressed(QAction('Refresh Diagram'))

    def setPath(self, event):
        return QGraphicsPathItem.setPath(self, event)

    def deletelink(self):
        nameItem = editor.listNodes[editor.currentTab][self.name]
        nameItemTmp0 = nameItem[0:nameItem.index('#Node#')]
        unit = nameItemTmp0[0:nameItemTmp0.index(':')]
        BlockCreate.deletelink(self, self, unit)
        # UpdateUndoRedo()

    def setPositionTxt(self, *pos):
        self.linkTxt.setPos(*pos)

    def setPositionShow(self, posPolygon):
        self.linkShow.setPolygon(posPolygon)

    def getlinkTxt(self):
        return self.linkTxt

    def getlinkShow(self):
        return self.linkShow

    def getBislink(self):
        return self.bislink


class LinkArrow(QGraphicsPolygonItem):

    def __init__(self, color, parent=None):
        super(LinkArrow, self).__init__(parent)
        self.setPen(QPen(color, 2))
        self.setBrush(color)
        self.setZValue(3)


class LinkText(QGraphicsTextItem):

    def __init__(self, textNode, color, parent=None):
        super(LinkText, self).__init__(parent)
        self.setPlainText(textNode)
        self.setFont(QFont("Times", 10, QFont.Weight.Normal))
        self.setDefaultTextColor(color)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)

    def mousePressEvent(self, event):
        editor.diagramScene[editor.currentTab].clearSelection()
        return QGraphicsTextItem.mousePressEvent(self, event)


class LoadCodeScript:

    def __init__(self):
        self.listCodeScript = ''
        for keyS, valS in editor.listItems[editor.currentTab].items():
            if 'S' in keyS or 'J' in keyS:
                if type(valS) is ScriptItem:
                    txt = '[source ' + valS.unit + ']\n'
                    txt += repr(self.getInputsScript(keyS)) + '\n'
                    txt += valS.elemProxy.toPlainText() + '\n'
                    txt += str([keyS +
                                ':' +
                                item.name for item in valS.outputs]) + '\n'
                    txt += '[/source ' + valS.unit + ']\n'
                    self.listCodeScript += txt

    def writeListScript(self):
        return self.listCodeScript

    def getInputsScript(self, unitScript):
        listInputVal = []
        for key, val in editor.listNodes[editor.currentTab].items():
            tmpout = val[val.index("#Node") + 6:]
            if unitScript + ':' in tmpout:
                tmpIn = tmpout[tmpout.index(':') + 1:]
                tmpVal = val[0:val.index('#Node#')]
                if 'A' in tmpVal[0:1]:
                    tmpConstName = tmpVal[0:-1]
                    tmpIt = editor.listItems[editor.currentTab][tmpConstName]
                    tmpVal = editor.listConstants[editor.currentTab][tmpConstName][1]
                    if editor.listConstants[editor.currentTab][tmpConstName][0] in ['int',
                                                                                    'float',
                                                                                    'list_int',
                                                                                    'list_float',
                                                                                    'array_int',
                                                                                    'array_float']:
                        try:
                            tmpVal = tmpVal[1]
                        except Exception as err:
                            pass
                    if type(tmpIt).__name__ == 'Checkbox':
                        tmpVal = [i[0:-1] for i in tmpVal if '*' in i]
                    tmpVal = repr(tmpVal)
                listInputVal.append(tmpIn + '=' + tmpVal)
        return listInputVal


class LoadDiagram:

    def __init__(self, txt):

        editor.diagramScene[editor.currentTab].addCenterLines()
        edit = DiagramView(editor.diagramScene[editor.currentTab])
        listNd = {}
        listCn, listBl, listFo, listIf = {}, {}, {}, {}
        listSm, listCt, listSc, listPr = {}, {}, {}, {}
        listCode = {}
        insource = False
        tmpKeyScript = ''
        tmpValScript = ''

        for line in txt:

            if line[0:4] == 'link' and 'node' in line:
                args = ["link", "node"]
                nameNode, line = GetValueInBrackets(line, args).getValues()
                editor.listNodes[editor.currentTab][nameNode] = line
                listNd[nameNode] = line.replace('#Node#', ':').split(':')

            elif line[0:5] == 'block' and 'RectF' in line:
                args = ["block", "category", "class", "valInputs", "RectF"]
                unit, cat, classs, Vinput, pos = GetValueInBrackets(line, args).getValues()
                pos = eval(pos)
                edit.loadBlock(unit, classs, cat, pos, eval(Vinput))
                listBl[unit] = edit.returnBlockSystem()

            elif line[0:5] == 'probe' and 'RectF' in line:
                args = ["probe", "label", "format", "RectF"]
                unit, label, form, pos = GetValueInBrackets(line, args).getValues()
                pos = eval(pos)
                edit.loadProbe(unit, label, form, pos)
                listPr[unit] = edit.returnBlockSystem()

            elif line[0:8] == 'comments' and 'RectF' in line:
                args = ["comments", "RectF", "text"]
                unit, pos, cmt = GetValueInBrackets(line, args).getValues()
                pos = eval(pos)
                cmt = cmt.replace("\\n", '\n')
                cmt = cmt.replace("'", '')
                cmt = cmt.replace('"', '')
                edit.loadComments(pos, cmt)

            elif line[0:7] == 'loopFor' and 'RectF' in line:
                args = ["loopFor", "inputs", "outputs", "listItems", "RectF"]
                unit, inp, outp, listIt, pos = GetValueInBrackets(line, args).getValues()
                pos = eval(pos)
                edit.loadLoopFor(unit, pos, eval(inp), eval(outp))
                listFo[unit] = edit.returnBlockSystem()
                editor.listTools[editor.currentTab][unit] = eval(listIt)

            elif line[0:6] == 'loopIf' and 'RectF' in line:
                args = ["loopIf", "inputs", "outputs", "listItems", "RectF"]
                unit, inp, outp, listIt, pos = GetValueInBrackets(line, args).getValues()
                pos = eval(pos)
                edit.loadLoopFor(unit, pos, eval(inp), eval(outp))
                listIf[unit] = edit.returnBlockSystem()
                editor.listTools[editor.currentTab][unit] = eval(listIt)

            elif line[0:6] == 'submod' and 'RectF' in line:
                args = ["submod", "nameMod", "catMod", "valInputs", "RectF"]
                unit, nameMod, catMod, Vinput, pos = GetValueInBrackets(line, args).getValues()
                pos = eval(pos)
                edit.loadMod(unit, nameMod, pos, eval(Vinput))
                listSm[unit] = edit.returnBlockSystem()

            elif line[0:8] == 'constant' and 'RectF' in line:
                args = ["constant", "value", "format", "label", "RectF"]
                unit, vout, fort, lab, pos = GetValueInBrackets(line, args).getValues()
                if fort == 'bool':
                    vout = eval(vout)
                pos = eval(pos)
                try:
                    edit.loadConstant(unit, pos, eval(vout), fort, lab)
                except Exception as err:
                    edit.loadConstant(unit, pos, vout, fort, lab)

                listCt[unit] = edit.returnBlockSystem()

            elif line[0:7] == 'cluster' and 'RectF' in line:
                args = ["cluster", "value", "format", "label", "RectF"]
                unit, vout, fort, lab, pos = GetValueInBrackets(line, args).getValues()
                pos = eval(pos)
                edit.loadCluster(unit, pos, eval(vout), fort, lab)
                listCt[unit] = edit.returnBlockSystem()

            elif line[0:6] == 'script' and 'RectF' in line:
                args = ["script", "title", "inputs", "outputs", "code", "RectF"]
                unit, tit, inp, outp, code, pos = GetValueInBrackets(line, args).getValues()
                pos = eval(pos)
                inp = "["+inp+"]"
                outp = "["+outp+"]"
                edit.loadScriptItem(unit, tit, pos, eval(inp), eval(outp))
                listSc[unit] = edit.returnBlockSystem()
                editor.listTools[editor.currentTab][unit] = code

            elif line[0:8] == '[source ':
                insource = True
                tmpKeyScript = line[line.index('[source ') + 8:]
                tmpKeyScript = tmpKeyScript[0:tmpKeyScript.index(']')]
            elif line[0:9] == '[/source ':
                tmpValScript = '\n'.join(tmpValScript.splitlines()[1:-1])
                listCode[tmpKeyScript] = tmpValScript
                insource = False
                tmpValScript = ''
            elif insource:
                if '\n' not in line:
                    line += '\n'
                tmpValScript += line

            elif line[0:5] == 'connt' and 'RectF' in line:
                args = ["connt", "name", "type", "format", "valOut", "RectF"]
                unit, name, typ, form, Vinput, pos = GetValueInBrackets(line, args).getValues()
                try:
                    pos = edit.mapToScene(eval(pos))
                except Exception as e:
                    pos = eval(pos)
                edit.loadConn(unit, name, pos, str(typ), form, Vinput)
                listCn[unit] = edit.returnBlockSystem()

            elif line[0:8] == 'stopexec' and 'RectF' in line:
                args = ["stopexec", "RectF"]
                unit, pos = GetValueInBrackets(line, args).getValues()
                pos = eval(pos)
                edit.loadStopExec(unit, pos)

        for lk, lv in listNd.items():
            unitStart = lv[0]
            namePortStart = lv[1]
            unitEnd = lv[2]
            namePortEnd = lv[3]

            fromPort = None
            toPort = None

            if 'U' in unitStart:
                for lin in listBl[unitStart].outputs:
                    if type(lin) is Port and lin.name == namePortStart:
                        fromPort = lin
                        break
            elif 'M' in unitStart:
                for lin in listSm[unitStart].outputs:
                    if type(lin) is Port and lin.name == namePortStart:
                        fromPort = lin
                        break
            elif 'C' in unitStart:
                fromPort = listCn[unitStart].outputs
            elif 'F' in unitStart:
                for lin in listFo[unitStart].outputs:
                    if type(lin) is Port and lin.name == namePortStart:
                        fromPort = lin
                        break
            elif 'I' in unitStart:
                for lin in listIf[unitStart].outputs:
                    if type(lin) is Port and lin.name == namePortStart:
                        fromPort = lin
                        break
            elif 'S' in unitStart or 'J' in unitStart:
                for lin in listSc[unitStart].outputs:
                    if type(lin) is Port and lin.name == namePortStart:
                        fromPort = lin
                        break
            elif 'A' in unitStart:
                fromPort = listCt[unitStart].outputs[0]

            if 'U' in unitEnd:
                for lout in listBl[unitEnd].inputs:
                    if type(lout) is Port and lout.name == namePortEnd:
                        toPort = lout
                        break
            elif 'M' in unitEnd:
                for lout in listSm[unitEnd].inputs:
                    if type(lout) is Port and lout.name == namePortEnd:
                        toPort = lout
                        break
            elif 'C' in unitEnd:
                toPort = listCn[unitEnd].inputs
            elif 'P' in unitEnd:
                toPort = listPr[unitEnd].inputs[0]
            elif 'F' in unitEnd:
                for lout in listFo[unitEnd].inputs:
                    if type(lout) is Port and lout.name == namePortEnd:
                        toPort = lout
                        break
            elif 'I' in unitEnd:
                for lout in listIf[unitEnd].inputs:
                    if type(lout) is Port and lout.name == namePortEnd:
                        toPort = lout
                        break
            elif 'S' in unitEnd or 'J' in unitEnd:
                for lout in listSc[unitEnd].inputs:
                    if type(lout) is Port and lout.name == namePortEnd:
                        toPort = lout
                        break
            try:
                startConnection = Connection(lk,
                                             fromPort, toPort,
                                             fromPort.format)
                startConnection.setEndPos(toPort.scenePos())
                startConnection.setToPort(toPort)
            except Exception as e:
                editor.editText('This diagram contains errors :{}'.format(lk),
                                10, 600, 'ff0000', False, True)

        if listSc:
            for elem in editor.diagramView[editor.currentTab].items():
                if type(elem) is ScriptItem:
                    elem.elemProxy.setPlainText(listCode[elem.unit])

        ValueZ2()


class Menu(QMenuBar):

    def __init__(self, parent=None):
        QMenuBar.__init__(self, parent)
        self.setFixedHeight(30)
        # self.setFixedWidth(500)
        self.adjustSize()
        hist = Config().getPathHistories()
        start_run = Config().getRunStart()
        self.Dictexamples = {}

        self.menuDgr = self.addMenu('Files')
        newdgr = self.menuDgr.addAction('New Diagram')
        newdgr.setShortcut('Ctrl+n')
        opendgr = self.menuDgr.addAction('Open Diagram')
        opendgr.setShortcut('Ctrl+o')
        saveDgr = self.menuDgr.addAction('Save Diagram')
        saveDgr.setShortcut('Ctrl+s')
        self.menuDgr.addAction('Save Diagram As...')
        closeDgr = self.menuDgr.addAction('Close Diagram\tCtrl+W')
        claseAll = self.menuDgr.addAction('Close All Diagram')
        self.menuDgr.addSeparator()
        self.openRecent = self.menuDgr.addMenu('Open Recent')
        if hist:
            for h in hist:
                self.openRecent.addAction(h.strip())
        self.menuDgr.addSeparator()
        exitMrw = self.menuDgr.addAction('Exit')
        exitMrw.setShortcut('Ctrl+q')
        self.menuDgr.triggered[QAction].connect(self.btnPressed)

        self.menuEdit = self.addMenu('Edit')
        fit = self.menuEdit.addAction('Fit to window')
        fit.setShortcut('F')
        cop = self.menuEdit.addAction('Copy')
        cop.setShortcut('Ctrl+C')
        past = self.menuEdit.addAction('Paste')
        past.setShortcut('Ctrl+D')
        undo = self.menuEdit.addAction('Undo')
        undo.setShortcut('Ctrl+Z')
        redo = self.menuEdit.addAction('Redo')
        redo.setShortcut('Ctrl+Y')
        casd = self.menuEdit.addAction('Cascade')
        casd.setShortcut('Ctrl+F')
        til = self.menuEdit.addAction('Tiled')
        til.setShortcut('Ctrl+G')
        maxd = self.menuEdit.addAction('Maximized')
        maxd.setShortcut('Ctrl+H')
        self.menuEdit.triggered[QAction].connect(self.btnPressed)
        self.menuPipe = self.addMenu('Diagram')
        anaPipe = self.menuPipe.addAction('Analyze this Diagram')
        anaPipe.setShortcut('Ctrl+A')
        self.menuPipe.addSeparator()
        runpipe = self.menuPipe.addAction('Run this Diagram')
        runpipe.setShortcut(QKeySequence('Ctrl+R'))
        runpipethread = self.menuPipe.addAction('Run this Diagram ' +
                                                'in Threading mode')
        runpipethread.setShortcut('Ctrl+T')
        runmultipipe = self.menuPipe.addAction('Run multiple Diagrams')
        runmultipipe.setShortcut('Ctrl+M')
        self.menuPipe.addSeparator()
        runpipessh = self.menuPipe.addAction('Run this Diagram on cluster HPC')
        runpipethreadssh = self.menuPipe.addAction('Run this Diagram ' +
                                                   'in Threading mode on cluster HPC')
        runmultipipessh = self.menuPipe.addAction('Run multiple Diagrams on cluster HPC')
        self.menuPipe.addSeparator()
        runmultipipealt = self.menuPipe.addAction('Run multiple Diagrams alternately')
        self.menuPipe.addSeparator()
        listItm = self.menuPipe.addAction('See List Items')
        listItm.setShortcut('Ctrl+I')
        listLib = self.menuPipe.addAction('See List Libraries')
        listLib.setShortcut('Ctrl+L')
        rawFile = self.menuPipe.addAction('See Raw file')
        rawFile.setShortcut(('Ctrl+B'))
        self.menuPipe.addSeparator()
        empShm = self.menuPipe.addAction('Clear Shared Memory')
        # self.menuPipe.addSeparator()
        # # show_grid = Config().getShowGrid()
        # self.show_grid_action = self.menuPipe.addAction('Show grid')
        # self.show_grid_action.setCheckable(True)
        # # self.show_grid_action.setChecked(show_grid)

        self.menuPipe.triggered[QAction].connect(self.btnPressed)

        self.menuSub = self.addMenu('Submodul')
        self.menuSub.addAction('Create Submodul')
        self.menuSub.addAction('Save Submodul        Ctrl+S')
        self.menuSub.triggered[QAction].connect(self.btnPressed)

        self.menuPack = self.addMenu('Configuration')
        self.menuPack.addAction('Packages manager')
        self.menuPack.addAction('Reload environment variables')
        self.menuPack.addAction('Clusters configuration')
        self.menuPack.triggered[QAction].connect(self.btnPressed)

        # self.menuProj = self.addMenu('Projects')
        # self.menuProj.addAction('Open project')
        # self.menuProj.addAction('Save project')

        self.menuPlug = self.addMenu('Plugins')
        for key_pl, val_pl in editor.listPlugins.items():
            self.menuPlug.addAction(key_pl)
        self.menuPlug.triggered[QAction].connect(self.btnPressed)

        self.menuHelp = self.addMenu('Help')
        self.menuHelp.addAction('About skrypy')
        self.menuHelp.addAction('HTML documentation')
        self.menuHelp.addAction('Update Skrypy')
        # self.menuHelp.addAction('Preferences')
        self.menuHelp.addSeparator()
        self.examples = self.menuHelp.addMenu('Examples')
        expl = self.load_dir_examples()
        if expl:
            pathExamples = os.path.dirname(os.path.realpath(__file__))
            pathExamples = os.path.dirname(pathExamples)
            pathExamples = os.path.join(pathExamples, 'examples')
            expl = sorted(expl)
            for lstD in expl:
                self.exs = self.examples.addMenu(lstD)
                expl_files = self.load_file_examples(
                    os.path.join(pathExamples,
                                 lstD))
                for lstF in expl_files:
                    self.Dictexamples[lstF] = os.path.join(pathExamples,
                                                           lstD)
                    self.exs.addAction(lstF)

        self.menuHelp.triggered[QAction].connect(self.btnPressed)

    def load_dir_examples(self):
        pathExamples = os.path.dirname(os.path.realpath(__file__))
        pathExamples = os.path.dirname(pathExamples)
        pathExamples = os.path.join(pathExamples, 'examples')
        if os.path.isdir(pathExamples):
            listDir = [dI for dI in os.listdir(pathExamples)
                       if os.path.isdir(os.path.join(pathExamples, dI))]
            return listDir
        else:
            return None

    def load_file_examples(self, pathExemp):
        onlyfiles = [f for f in os.listdir(pathExemp)
                     if os.path.isfile(os.path.join(pathExemp, f))]
        onlyfiles = sorted(onlyfiles)
        return onlyfiles

    def saveHistories(self, path):
        hist = Config().getPathHistories()
        if hist:
            if path not in hist:
                if len(hist) > 9:
                    hist.pop(0)
                    firstAction = self.openRecent.actions()[0]
                    self.openRecent.removeAction(firstAction)
                hist.append(path)
                Config().setPathHistories(hist)
                self.openRecent.addAction(path)
        else:
            hist = [path]
            Config().setPathHistories(hist)
            self.openRecent.addAction(path)

    def saveDiagramsConfig(self, file):
        list_dgr = Config().getPathDiagrams()
        if list_dgr:
            if file not in list_dgr:
                list_dgr.append(file)
                Config().setPathDiagrams(list_dgr)
        else:
            list_dgr = [file]
            Config().setPathDiagrams(list_dgr)

    def pack_manager(self):
        c = manage_pck()
        c.exec()

    def load_previous_diagram(self):
        last_exist_file = ''
        lst_dgr = Config().getPathDiagrams()
        if lst_dgr:
            lst_dgr.sort()
            for i, elem in enumerate(lst_dgr):
                if os.path.exists(elem):
                    f = open(elem, 'r', encoding='utf8')
                    txt = f.readlines()
                    f.close()
                    try:
                        editor.currentpathwork = elem
                        editor.addSubWindow(os.path.basename(elem))
                        last_exist_file = elem
                        LoadDiagram(txt)
                        editor.diagramScene[editor.currentTab].fitwindow(1.0)
                        editor.pathDiagram[editor.currentTab] = elem
                        editor.diagramView[editor.currentTab].scene().clearSelection()
                        editor.infopathDgr.setText(elem)
                        # editor.textEdit.clear()
                        UpdateUndoRedo()
                    except Exception as e:
                        editor.editText("This diagram contains errors : {}".format(str(e)),
                                        10, 600, 'ff0000', False, True)

            editor.infopathDgr.setText(last_exist_file)
            editor.currentpathwork = last_exist_file
            if not last_exist_file:
                editor.infopathDgr.setText('')
        else:
            editor.addSubWindow('')
            self.btnPressed(QAction('Tiled'))
            editor.infopathDgr.setText('')

    def save_project(self):
        pass

    def btnPressed(self, act):
        tmpActText = act.text()
        if tmpActText in editor.listPlugins.keys():
            try:
                pathModules = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
                pathModules = os.path.join(pathModules, 'modules')
                module = importlib.import_module(editor.listPlugins[tmpActText])
                plug = getattr(module, tmpActText)
                plug(SaveDiagram().toPlainText(), pathModules)
                editor.editText(" > Diagram executed with the plugin {}".format(tmpActText),
                                12, 600, 'ff6f00', False, True)
            except Exception as er:
                editor.editText(" > {} runtime error: {}".format(tmpActText, str(er)),
                                12, 600, 'cc0000', False, True)

        elif tmpActText == 'Show/hide Tools':
            editor.splitter1.setVisible(not editor.splitter1.isVisible())
        elif tmpActText == 'Show/hide Console':
            editor.splitterp.setVisible(not editor.splitterp.isVisible())
        elif tmpActText == 'Show/hide Progress':
            editor.splitter3.setVisible(not editor.splitter3.isVisible())
        elif tmpActText == 'Refresh Diagram':
            if len(editor.mdi.subWindowList()) >= 1:
                editor.diagramView[editor.currentTab].scene().clearFocus()
                ct = editor.currentTab
                listIf = {}
                if editor.pointTyping[ct] > 0:
                    for elm in editor.diagramView[ct].items():
                        try:
                            if 'I' in elm.unit:
                                listIf[elm.unit] = elm.elemProxy.currentText()
                        except Exception as err:
                            pass
                        editor.diagramScene[ct].removeItem(elm)
                    newDiagram = editor.undoredoTyping[ct][editor.pointTyping[ct]]
                    LoadDiagram(newDiagram.splitlines())
                    UpdateList(newDiagram)

                    for elm in editor.diagramView[ct].items():
                        try:
                            if 'I' in elm.unit:
                                elm.elemProxy.setCurrentText(listIf[elm.unit])
                                elm.elemProxy.newValue()
                        except Exception as err:
                            pass

        elif tmpActText == 'Exit':
            QApplication.instance().quit()

        elif tmpActText == 'load_previous_diagram':
            self.load_previous_diagram()

        elif tmpActText == 'New Diagram':
            editor.addSubWindow('')
            editor.infopathDgr.setText('')

        elif (tmpActText == 'Save Diagram' or
                tmpActText == 'Save Diagram As...'):
            if len(editor.mdi.subWindowList()) == 0:
                return
            file = editor.pathDiagram[editor.currentTab]
            extension = os.path.splitext(file)[1]
            fileNameonly = os.path.basename(file)

            connectorPresent = False
            for item in editor.diagramView[editor.currentTab].items():
                if type(item) is ConnectorItem:
                    connectorPresent = True
                    break

            if not connectorPresent:
                self.btnPressed(QAction('Refresh Diagram'))
                txt = SaveDiagram()
#                 blk = BlocksProjects(txt.toPlainText())
                if ('.dgr' not in extension or
                        tmpActText == 'Save Diagram As...'):
                    file = QFileDialog\
                                .getSaveFileName(
                                    self,
                                    "save diagram " + str(editor.currentTab),
                                    editor.currentpathwork, "Diagrams (*.dgr)",
                                    None,
                                    QFileDialog.Option.DontUseNativeDialog)
                    file = file[0]
                    editor.currentpathwork = file
                    if file:
                        if '.dgr' not in file:
                            file += '.dgr'
                        fileNameonly = os.path.basename(file)

                try:
                    if file:
                        f = open(file, 'w', encoding='utf8')
                        f.write(txt.toPlainText())
                        f.write('\n[execution]\n')
                        f.write(analyze2(txt.toPlainText(), [False, True]).get_analyze(editor.textEdit))
                        f.close()
#                         base = os.path.splitext(file)[0] + '.blk'
#                         f = open(base, 'w', encoding='utf8')
#                         f.write(blk.toPlainText())
#                         f.close()
                        editor.pathDiagram[editor.currentTab] = file
                        editor.setSubWindowCurrentTitle(fileNameonly)
                        editor.infopathDgr.setText(file)
                        self.saveDiagramsConfig(file)
                        return 'yes'
                        if 'NodeEditor/examples' not in file:
                            self.saveHistories(file)
                    else:
                        return 'cancel'
                except OSError as err:
                    print("OS error: {0}".format(err))

            else:
                if '.mod' not in extension:
                    tmpActText = 'Create Submodul'
                else:
                    tmpActText = 'Save Submodul        Ctrl+S'

        elif tmpActText == 'Open Diagram':

            dialog = QProgressDialog('Progress', None, 0, 0, self)
            bar = QProgressBar(dialog)
            bar.setTextVisible(False)
            bar.setMinimum(0)
            bar.setMaximum(100)
            dialog.setBar(bar)
            dialog.show()

            filesCh = QFileDialog.getOpenFileNames(
                                                self,
                                                "Open diagram",
                                                editor.currentpathwork,
                                                'Diagrams (*.dgr)',
                                                None,
                                                QFileDialog.Option.DontUseNativeDialog)
            if filesCh[0]:
                editor.currentpathwork = os.path.dirname(filesCh[0][0])
                i, len_item = 0, len(filesCh[0])

                for fileDiagram in filesCh[0]:
                    dialog.setValue(int(100*i/len_item))
                    i += 1
                    if fileDiagram in editor.pathDiagram:
                        editor.editText("{} is already open".format(fileDiagram),
                                        10, 600, 'cc0000', False, True)
                    else:
                        editor.addSubWindow(os.path.basename(fileDiagram))
                        editor.pathDiagram[editor.currentTab] = fileDiagram
                        fileNameonly = os.path.basename(fileDiagram)
                        editor.infopathDgr.setText(fileDiagram)
                        f = open(fileDiagram, 'r', encoding='utf8')
                        txt = f.readlines()
                        f.close()
                        try:
                            LoadDiagram(txt)
                            self.btnPressed(QAction("Fit to window"))
                            editor.diagramView[editor.currentTab].scene().clearSelection()
                            file = editor.pathDiagram[editor.currentTab]
                            # fileNameonly = os.path.basename(file)
                            editor.mdi.currentSubWindow().setWindowTitle(fileNameonly)
                            editor.currentpathwork = file
                            editor.infopathDgr.setText(file)
                            self.saveHistories(fileDiagram)
                            self.saveDiagramsConfig(fileDiagram)
                            UpdateUndoRedo()
                        except Exception as err:
                            editor.editText(fileNameonly, 14, 600, 'ff6f00', False, False)
                            editor.editText("This diagram contains errors : {} missed".format(str(err)),
                                            10, 600, 'ff0000', False, True)
                self.btnPressed(QAction('Tiled'))
            dialog.close()

        elif tmpActText == 'Close Diagram\tCtrl+W':
            title_current = editor.getSubWindowCurrentTitle()
            for j in editor.mdi.subWindowList():
                if j.windowTitle() == title_current:
                    j.close()

        elif tmpActText == 'Close All Diagram':
            editor.mdi.closeAllSubWindows()

        elif tmpActText == 'Run this Diagram':
            # editor.textEdit.clear()
            if len(editor.mdi.subWindowList()) >= 1:
                if not editor.listConnects[editor.currentTab]:
                    currentTitle = editor.getSubWindowCurrentTitle()
                    Diagram_excution(currentTitle, False)
                else:
                    editor.editText(" > You can't run Diagram with connectors",
                                    10, 600, 'cc0000', False, True)

        elif tmpActText == 'Run this Diagram in Threading mode':
            # editor.textEdit.clear()
            if len(editor.mdi.subWindowList()) >= 1:
                if not editor.listConnects[editor.currentTab]:
                    currentTitle = editor.getSubWindowCurrentTitle()
                    Diagram_excution(currentTitle, True)
                else:
                    editor.editText(" > You can't run Diagram with connectors",
                                    10, 600, 'cc0000', False, True)

        elif tmpActText == 'Run multiple Diagrams':
            # editor.textEdit.clear()
            list_dgr = []
            list_dgr_tit = {}
            for lstWind in editor.mdi.subWindowList():
                titleTab = lstWind.windowTitle()
                if not titleTab.endswith('.mod'):
                    list_dgr.append(titleTab)
                    list_dgr_tit[titleTab] = lstWind
            c = multiple_execution(list_dgr, 'local')
            c.exec()
            order_dgr = []
            mdi_count = len(editor.mdi.subWindowList())
            for lstdg in c.getNewValues()[0:-2]:
                if lstdg[0] != 'None':
                    editor.mdi.setActiveSubWindow(list_dgr_tit[lstdg[0]])
                    if not editor.listConnects[editor.currentTab]:
                        Diagram_excution(lstdg[0], lstdg[1])
                    else:
                        editor.editText("{} :<br>You can't run Diagram with connectors".format(title_dgr),
                                        10, 600, 'cc0000', False, True)

        elif tmpActText == 'Run this Diagram on cluster HPC':
            if len(editor.mdi.subWindowList()) >= 1:
                if not editor.listConnects[editor.currentTab]:
                    currentTitle = editor.getSubWindowCurrentTitle()
                    if '*' in currentTitle:
                        self.showdialog("the diagram is not saved.\nSave and relaunch.")
                        return
                    print("run", currentTitle)
                    ssh_diagram_execution([editor.infopathDgr.text()], 'Sequential', None)
                else:
                    editor.editText(" > You can't run Diagram with connectors",
                                    10, 600, 'cc0000', False, True)

        elif tmpActText == 'Run this Diagram in Threading mode on cluster HPC':
            # editor.textEdit.clear()
            if len(editor.mdi.subWindowList()) >= 1:
                if not editor.listConnects[editor.currentTab]:
                    currentTitle = editor.getSubWindowCurrentTitle()
                    if '*' in currentTitle:
                        self.showdialog("the diagram is not saved.\nSave and relaunch.")
                        return
                    print("threading", currentTitle)
                    ssh_diagram_execution([editor.infopathDgr.text()], 'Multi-threading', None)
                else:
                    editor.editText(" > You can't run Diagram with connectors",
                                    10, 600, 'cc0000', False, True)

        elif tmpActText == 'Run multiple Diagrams on cluster HPC':
            # editor.textEdit.clear()
            if not all(os.path.exists(s) for s in editor.pathDiagram):
                self.showdialog("Some diagrams are not saved.\nSave and relaunch.")
                return
            list_dgr = []
            list_dgr_tit = {}
            for lstWind in editor.mdi.subWindowList():
                titleTab = lstWind.windowTitle()
                if not titleTab.endswith('.mod'):
                    list_dgr.append(titleTab)
                    list_dgr_tit[titleTab] = lstWind
            c = multiple_execution(list_dgr, 'cluster')
            c.exec()
            order_dgr = []
            source_dgr = []
            if c.getNewValues():
                for lstdg in c.getNewValues()[0:-2]:
                    if lstdg[0] != 'None':
                        if '*' in lstdg[0]:
                            self.showdialog("Some diagram(s) have been modified.\nSave and relaunch.")
                            return
                        editor.mdi.setActiveSubWindow(list_dgr_tit[lstdg[0]])
                        if not editor.listConnects[editor.currentTab]:
                            # Diagram_excution(lstdg[0], lstdg[1])
                            source_dgr.append([s for s in editor.pathDiagram if lstdg[0] == os.path.basename(s)][0])
                        else:
                            editor.editText("{} :<br>You can't run Diagram with connectors".format(title_dgr),
                                            10, 600, 'cc0000', False, True)
                            return

                ssh_diagram_execution(source_dgr, 'Multi-threading', None)

        elif tmpActText == 'Run multiple Diagrams alternately':
            if not all(os.path.exists(s) for s in editor.pathDiagram):
                self.showdialog("Some diagrams are not saved.\nSave and relaunch.")
                return
            list_dgr = []
            list_dgr_tit = {}
            for lstWind in editor.mdi.subWindowList():
                titleTab = lstWind.windowTitle()
                if not titleTab.endswith('.mod'):
                    list_dgr.append(titleTab)
                    list_dgr_tit[titleTab] = lstWind
            c = multiple_execution_altern(list_dgr)
            c.exec()
            order_dgr = []
            source_dgr = []
            if c.getNewValues():
                for lstdg in c.getNewValues()[0:-2]:
                    if lstdg[0] != 'None':
                        if '*' in lstdg[0]:
                            self.showdialog("Some diagram(s) have been modified.\nSave and relaunch.")
                            return
                        editor.mdi.setActiveSubWindow(list_dgr_tit[lstdg[0]])
                        if not editor.listConnects[editor.currentTab]:
                            # Diagram_excution(lstdg[0], lstdg[1])
                            source_dgr.append(([s for s in editor.pathDiagram if lstdg[0] == os.path.basename(s)][0], lstdg[1], lstdg[2]))
                        else:
                            editor.editText("{} :<br>You can't run Diagram with connectors".format(title_dgr),
                                            10, 600, 'cc0000', False, True)
                            return
                col = '\x1b[38;2;0;255;0m'
                for src in source_dgr:
                    diagr = os.path.basename(src[0])
                    if src[2] == 'local':
                        editor.mdi.setActiveSubWindow(list_dgr_tit[diagr])
                        Diagram_excution(diagr, src[1])
                    else:
                        ssh_diagram_execution([src[0]], 'Multi-threading', src[2])
        # elif tmpActText == 'Show grid':
        #     showGrid = self.show_grid_action.isChecked()
        #     editor.diagramView[editor.currentTab].update()

        elif tmpActText == 'Analyze this Diagram':
            if len(editor.mdi.subWindowList()) >= 1:
                txt = SaveDiagram()
                analyze2(txt.toPlainText(), [False, True]).get_analyze(editor.textEdit)

        if tmpActText == 'Create Submodul':
            if len(editor.mdi.subWindowList()) == 0:
                return
            connectPresent = False
            for item in editor.diagramView[editor.currentTab].items():
                if type(item) is ConnectorItem:
                    connectPresent = True
                    break

            if connectPresent:
                pat_submod = os.path.dirname(os.path.realpath(__file__))
                pat_submod = os.path.dirname(pat_submod)
                txt = SaveDiagram()
                file = QFileDialog.getSaveFileName(self,
                                                   "save submodul " +
                                                   str(editor.currentTab),
                                                   str(os.path.join(
                                                       pat_submod,
                                                       'submodules')),
                                                   "SubModul (*.mod)",
                                                   None,
                                                   QFileDialog.
                                                   DontUseNativeDialog)
                file = file[0]
                try:
                    if '.mod' not in file and file:
                        file += '.mod'
                    f = open(file, 'w', encoding='utf8')
                    f.write(txt.toPlainText())
                    f.write('\n[execution]\n')
                    f.write(analyze2(txt.toPlainText(), [False, True]).get_analyze(editor.textEdit))
                    f.close()
                    editor.pathDiagram[editor.currentTab] = file
                    fileNameonly = os.path.basename(file)
                    current_dir = os.path.basename(os.path.dirname(file))
                    editor.mdi.currentSubWindow().setWindowTitle(fileNameonly)
                    editor.refreshSubModLib(fileNameonly[0:-4], current_dir)
                except Exception as e:
                    pass
            else:
                if not connectPresent:
                    editor.editText(" > You can't create modul without connectors",
                                    10, 600, 'cc0000', False, True)

        if tmpActText == 'Save Submodul        Ctrl+S':
            if len(editor.mdi.subWindowList()) == 0:
                return
            file = editor.pathDiagram[editor.currentTab]
            fileNameonly = os.path.basename(file)
            current_dir = os.path.basename(os.path.dirname(file))
            connectPresent = False
            for item in editor.diagramView[editor.currentTab].items():
                if type(item) is ConnectorItem:
                    connectPresent = True
                    break

            if connectPresent:
                txt = SaveDiagram()
                try:
                    f = open(file, 'w', encoding='utf8')
                    f.write(txt.toPlainText())
                    f.write('\n[execution]\n')
                    f.write(analyze2(txt.toPlainText(), [False, True]).get_analyze(editor.textEdit))
                    f.close()
                    editor.pathDiagram[editor.currentTab] = file
                    editor.mdi.currentSubWindow().setWindowTitle(fileNameonly)
                    editor.refreshSubModLib(fileNameonly[0:-4], current_dir)
                except Exception as e:
                    pass
            else:
                if not connectPresent:
                    editor.editText(" > You can't create modul without connectors",
                                    10, 600, 'cc0000', False, True)

        elif tmpActText == 'See List Items':
            if len(editor.mdi.subWindowList()) == 0:
                return
            currentTitle = editor.getSubWindowCurrentTitle()
            text = ("listNodes :\n{}\n\nlistBlocks :\n{}\n\nlistSubMod :\n{}\n\n"
                    "listConstants :\n{}\n\nlistTools :\n{}\n\nlibTools :\n{}\n\n"
                    "listImgBox :\n{}\n\nlistProbes :\n{}\n\nlistConnects :\n{}\n\n"
                    "listStopExec : \n{}\n\nlistIfShowState :\n{}\n\n"
                    "listItems :\n{}\n\n"
                    .format('\n'.join(f'{key} : {value}' for key, value in editor.listNodes[editor.currentTab].items()),
                            '\n'.join(f'{key} : {value}' for key, value in editor.listBlocks[editor.currentTab].items()),
                            '\n'.join(f'{key} : {value}' for key, value in editor.listSubMod[editor.currentTab].items()),
                            '\n'.join(f'{key} : {value}' for key, value in editor.listConstants[editor.currentTab].items()),
                            '\n'.join(f'{key} : {value}' for key, value in editor.listTools[editor.currentTab].items()),
                            '\n'.join(f'{key} : {value}' for key, value in editor.libTools[editor.currentTab].items()),
                            '\n'.join(f'{key} : {value}' for key, value in editor.listImgBox[editor.currentTab].items()),
                            '\n'.join(f'{key} : {value}' for key, value in editor.listProbes[editor.currentTab].items()),
                            '\n'.join(f'{key} : {value}' for key, value in editor.listConnects[editor.currentTab].items()),
                            '\n'.join(f'{key} : {value}' for key, value in editor.listStopExec[editor.currentTab].items()),
                            '\n'.join(f'{key} : {value}' for key, value in editor.listIfShowedState[editor.currentTab].items()),
                            '\n'.join(f'{key} : {value}' for key, value in editor.listItems[editor.currentTab].items())
                            ))

            # diagramInfo(text).exec()
            current_dir_path = os.path.dirname(os.path.realpath(__file__))
            source_disp = os.path.join(current_dir_path, 'systemInfo.py')
            result = subprocess.Popen([sys.executable, source_disp, text, currentTitle])

        elif tmpActText == 'See List Libraries':
            text = ("libBlocks :\n{}\n\nlibSubMod :\n{}\n\n"
                    .format('\n'.join(f'{key} : {value}' for key, value in editor.libBlocks.items()),
                            '\n'.join(f'{key} : {value}' for key, value in editor.libSubMod.items())))
            # diagramInfo(text).exec()
            current_dir_path = os.path.dirname(os.path.realpath(__file__))
            source_disp = os.path.join(current_dir_path, 'systemInfo.py')
            result = subprocess.Popen([sys.executable, source_disp, text, "List Libraries"])

        elif tmpActText == 'See Raw file':
            if len(editor.mdi.subWindowList()) == 0:
                return
            currentTitle = editor.getSubWindowCurrentTitle()
            if editor.pathDiagram[editor.currentTab]:
                f = open(editor.pathDiagram[editor.currentTab], 'r', encoding='utf8')
                # diagramInfo(f.read()).exec()
                current_dir_path = os.path.dirname(os.path.realpath(__file__))
                source_disp = os.path.join(current_dir_path, 'systemInfo.py')
                result = subprocess.Popen([sys.executable, source_disp, f.read(), currentTitle])
                f.close()

        elif tmpActText == 'Clear Shared Memory':
            SharedMemoryManager(True)

        elif tmpActText == 'HTML documentation':
            path_html = os.path.dirname(os.path.realpath(__file__))
            tmp = str(os.path.join(path_html, '../../../docs', 'index.html'))
            webbrowser.open(tmp)

        elif tmpActText == 'Update Skrypy':
            c = skrypy_update(self)
            c.exec()
            if c.getAnswer() == 'YES':
                msg = QMessageBox()
                msg.setWindowTitle("Update done...")
                msg.setText("Please close and restart Skrypy")
                msg.setIcon(QMessageBox.Icon.Question)
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()

        elif tmpActText == 'Preferences':
            c = setPreferences([True, False, True])
            c.exec()
            p1, p2, p3 = c.getNewValues()[0]
            if c.getNewValues()[1] == 'ok':
                for dg in editor.diagramScene:
                    for elem in dg.items():
                        if type(elem) is LinkItem:
                            elem.linkTxt.setVisible(p2)
                            elem.linkShow.setVisible(p3)
                        else:
                            try:
                                elem.nameUnit.setVisible(p1)
                            except Exception as err:
                                pass

        elif tmpActText == 'Setting Standalone Paths':
            c = windowConfig()
            c.exec()
            ConfigModuls().saveConfig()

        elif tmpActText == 'Copy':
            if len(editor.mdi.subWindowList()) >= 1:
                editor.diagramScene[editor.currentTab].copy_items()

        elif tmpActText == 'Paste':
            if len(editor.mdi.subWindowList()) >= 1:
                editor.diagramScene[editor.currentTab].past_items()

        elif tmpActText == 'Cascade':
            editor.mdi.cascadeSubWindows()
            for lstWid in editor.mdi.subWindowList():
                if not lstWid.isMinimized():
                    lstWid.resize(400, 400)
                editor.mdi.setActiveSubWindow(lstWid)
                self.btnPressed(QAction("Fit to window"))

        elif tmpActText == 'Tiled':
            editor.mdi.tileSubWindows()
            for lstWid in editor.mdi.subWindowList():
                editor.mdi.setActiveSubWindow(lstWid)
                self.btnPressed(QAction("Fit to window"))
            editor.mdi.WindowOrder(3)

        elif tmpActText == 'Maximized':
            for lstWid in editor.mdi.subWindowList():
                lstWid.showMaximized()

        elif tmpActText == 'Undo':
            if len(editor.mdi.subWindowList()) >= 1:
                ct = editor.currentTab
                if editor.pointTyping[ct] > 0:
                    editor.pointTyping[ct] -= 1
                    for elm in editor.diagramView[ct].items():
                        editor.diagramScene[ct].removeItem(elm)
                    newDiagram = editor.undoredoTyping[ct][editor.pointTyping[ct]]
                    LoadDiagram(newDiagram.splitlines())
                    UpdateList(newDiagram)
                    if editor.pointTyping[ct] == 0:
                        currentTitle = editor.getSubWindowCurrentTitle()
                        currentTitle = currentTitle.replace('*', '')
                        editor.setSubWindowCurrentTitle(currentTitle)

        elif tmpActText == 'Redo':
            if len(editor.mdi.subWindowList()) >= 1:
                ct = editor.currentTab
                if editor.pointTyping[ct] < len(editor.undoredoTyping[ct]) - 1:
                    editor.pointTyping[ct] += 1
                    for elm in editor.diagramView[ct].items():
                        editor.diagramScene[ct].removeItem(elm)
                    newDiagram = editor.undoredoTyping[ct][editor.pointTyping[ct]]
                    LoadDiagram(newDiagram.splitlines())
                    UpdateList(newDiagram)
                    if editor.pointTyping[ct] == 1:
                        currentTitle = editor.getSubWindowCurrentTitle()
                        currentTitle = '{}{}'.format(currentTitle, '*')
                        editor.setSubWindowCurrentTitle(currentTitle)

        elif tmpActText == 'Fit to window':
            if len(editor.mdi.subWindowList()) >= 1:
                editor.diagramScene[editor.currentTab].fitwindow(0.8)

        # elif tmpActText == 'Diagram report':
        #     global report_diagram
        #     report_diagram = self.list_report_action.isChecked()
        #     Config().setDiagramReport(report_diagram)

        # elif tmpActText == 'Show grid':
        #    show_grid = self.show_grid_action.isChecked()
        #    Config().setShowGrid(show_grid)
        #    editor.diagramView[editor.currentTab].drawBackground()

        elif tmpActText == 'Packages manager':
            self.pack_manager()

        elif tmpActText == 'Save project':
            self.save_project()

        elif tmpActText == 'Reload environment variables':
            Start_environment(True)

        elif tmpActText == 'Clusters configuration':
            c = servers_window('config', None)
            c.exec()

        elif os.path.splitext(tmpActText)[1] == '.dgr':
            if not os.path.exists(tmpActText):
                try:
                    tmpActText = os.path.join(self.Dictexamples[tmpActText], tmpActText)
                except Exception as err:
                    return

            if tmpActText in editor.pathDiagram:
                editor.editText("{} is already open".format(tmpActText),
                                10, 600, 'cc0000', False, True)
                return

            editor.addSubWindow(os.path.basename(tmpActText))
            editor.currentpathwork = tmpActText
            editor.pathDiagram[editor.currentTab] = tmpActText
            editor.infopathDgr.setText(tmpActText)

            f = open(tmpActText, 'r', encoding='utf8')
            txt = f.readlines()
            f.close()
            try:
                LoadDiagram(txt)
                editor.diagramView[editor.currentTab].fitInView(
                                    editor.diagramScene[editor.currentTab].
                                    sceneRect(),
                                    Qt.AspectRatioMode.KeepAspectRatio)
                editor.diagramView[editor.currentTab].scale(0.8, 0.8)
                # editor.textEdit.clear()
                self.saveDiagramsConfig(tmpActText)
                UpdateUndoRedo()
            except Exception as e:
                editor.editText("This diagram contains errors : {}".format(str(e)),
                                10, 600, 'ff0000', False, True)

        elif tmpActText == 'About skrypy':
            AboutSoft(self)

    def showdialog(self, msg):
        dlg = QMessageBox(editor)
        dlg.setWindowTitle("warning")
        dlg.setWindowModality(Qt.WindowModality.ApplicationModal)
        dlg.setText(msg)
        button = dlg.exec()

        # if button == QMessageBox.StandardButton.Ok:
        #     print("OK!")


class NodeEdit(QWidget):

    def __init__(self, textInfo):
        super(NodeEdit, self).__init__()
        global editor
        editor = self

        self.infopathDgr = textInfo
        self.currentTab = 0
        self.listItems, self.listBlocks, self.listNodes, self.listSubMod = [], [], [], []
        self.listImgBox, self.listProbes, self.listCategorySubMod = [], [], []
        self.listConnects, self.listTools, self.listConstants, self.libTools = [], [], [], []
        self.listStopExec, self.listIfShowedState = [], []
        self.libSubMod, libBlocks, self.listCategory = {}, {}, []
        self.undoredoTyping, self.pointTyping = [], []
        self.diagramScene, self.diagramView, self.pathDiagram = [], [], []
        self.list_tools, self.list_tree = {}, {}
        self.listItemStored, self.listBlSmStored, self.listLoopStored = {}, {}, {}
        self.listCommentsStored = []
        self.autofit = True

        self.currentpathwork = os.path.dirname(os.path.realpath(__file__))
        self.currentpathwork = str(os.path.join(self.currentpathwork, '../examples'))
        self.currentpathdata = os.path.expanduser('~')

        self.listPlugins = Plugin().plugins_load()

        QWidget.__init__(self)
        self.setWindowTitle("Diagram editor")

# create libraries processes
        reps = os.path.dirname(__file__)
        reps, last = os.path.split(reps)
        rep = os.path.join(reps, 'modules')
        lstmod = os.listdir(rep)
        lstmod.sort()

# add structures
        self.listCategoryTools = {'Box': ('Checkbox', 'Imagebox', 'Pathbox'),
                                  'Clusters': ('Cluster_integer', 'Cluster_float', 'Cluster_string'),
                                  'Condition': ('If',),
                                  'Connector': ('Connector_input', 'Connector_output'),
                                  'Constants': ('Constant_integer', 'Constant_float', 'Constant_string',
                                                'Constant_combobox', 'Constant_boolean', 'Constant_path',
                                                'Constant_tuple'),
                                  'Control': ('Stop_execution',),
                                  'Loop': ('For_sequential', 'For_multiprocessing', 'For_multithreading'),
                                  'Probes': ('Value', 'Type', 'Length'),
                                  'Script': ('Script_python', 'Macro_ImageJ'),
                                  'Tools': ('Comments',)}
        self.icon1 = os.path.join(reps, '..', 'ressources', 'struct.png')
        self.list_tools['Structures'] = self.icon1
        self.icon2 = os.path.join(reps, '..', 'ressources', 'tools.png')
        self.list_tools['Tools'] = self.icon2
        self.icon3 = os.path.join(reps, '..', 'ressources', 'submod.png')
        self.list_tools['SubModules'] = self.icon3
        # self.list_tools[''] = None

        self.get_sub_tree()

# processes blocks
        for name in lstmod:
            tmp = (os.path.join(rep, name))
            if (os.path.isdir(tmp) and
                    '__pycache__' not in tmp and
                    'sources' not in tmp):
                # library of processes
                mod_instance = getlistModules(name)
                infoModules = mod_instance.listInspect()
                list_cat = sorted(infoModules.keys())
                self.list_tools[name] = mod_instance.getIconPath()
                # for category, cl in infoModules.items():
                list_by_cat = {}
                for category in list_cat:
                    self.listCategory.append(category)
                    list_module = []
                    for clas in infoModules[category]:
                        libBlocks[clas[0]] = (name + '.' + category, clas[1:5])
                        list_module.append(clas[0])
                    list_by_cat[category] = list_module
            self.list_tree[name] = list_by_cat

        self.setlib(libBlocks)
        self.library_tools = buildLibrary(self.list_tools)
        self.library_tools.menu_choosen.connect(self.menu_choosen)
        self.scrollTools = scrollTools(self.library_tools)
        width_lib = self.library_tools.frameGeometry().width()

# add submodules

        style_bkg = str(ItemColor.BACKGROUND.value.getRgb()[0:3])

        #######################################################################
        # self.textSharedMemory = TextInfo(self)
        # self.textSharedMemory.setStyleSheet("background-color : gray; ")

        #######################################################################
        self.textEdit = TextInfo(self)
        self.textEdit.setStyleSheet("background-color : lightgray")

        #######################################################################
        self.console = TextInfo(self)
        self.console.setStyleSheet("background-color : rgb{}; color:#999999;".format(style_bkg))
        # self._process = QProcess(self)
        # self._process.setProcessChannelMode(QtCore.QProcess.ProcessChannelMode.MergedChannels)
        # self._process.readyRead.connect(self.on_readReady)

        #######################################################################
        self.shm = TextInfo(self)
        self.shm.setStyleSheet("background-color : rgb{}; color:#999999;".format(style_bkg))

        #######################################################################
        tabW = QTabWidget()
        tabW.addTab(self.console, "Probes")
        tabW.addTab(self.shm, "Shared Memory")

        #######################################################################
        previewBlock = QWidget(self)
        self.previewScene = QGraphicsScene()
        self.previewScene.setSceneRect(QRectF())
        self.previewDiagram = PreviewBlock()
        self.previewDiagram.setScene(self.previewScene)
        layoutDiagram = QVBoxLayout()
        layoutDiagram.addWidget(self.previewDiagram)
        layoutDiagram.setContentsMargins(0, 0, 0, 0)
        previewBlock.setStyleSheet("background-color:rgb" + style_bkg)

        previewBlock.setLayout(layoutDiagram)

        legend = QWidget(self)
        self.legendScene = QGraphicsScene()
        self.legendScene.setSceneRect(QRectF())
        self.legendDiagram = PreviewBlock()
        self.legendDiagram.setScene(self.legendScene)
        self.legendDiagram.scale(0.8, 0.8)
        layoutDiagram = QVBoxLayout()
        layoutDiagram.addWidget(self.legendDiagram)
        layoutDiagram.setContentsMargins(0, 0, 0, 0)
        legend.setStyleSheet("background-color:rgb" + style_bkg)
        legend.setLayout(layoutDiagram)
        ShowLegend()

        self.mdi = QMdiArea()
        self.mdi.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.mdi.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.mdi.setViewMode(QMdiArea.ViewMode.TabbedView)
        self.mdi.setTabsClosable(True)
        # self.mdi.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.mdi.subWindowActivated.connect(self.windActivation)

        self.completer = QCompleter()
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        searchEngine = QWidget(self)
        searchEngine.setFixedHeight(50)
        hbox = QHBoxLayout(searchEngine)
        self.labelField = QLabel("Search : ")
        hbox.addWidget(self.labelField)
        self.searchField = QLineEdit(searchEngine)
        self.searchField.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.searchField.setCompleter(self.completer)
        self.searchField.textChanged.connect(self.searchCurrent)
        self.completer.activated.connect(self.searchResult)
#         self.searchField.returnPressed.connect(self.searchResult)
        hbox.addWidget(self.searchField)

        path_relatif = os.path.dirname(reps)
        pathColl = os.path.join(path_relatif, 'ressources', 'collapse.png')
        pathExp = os.path.join(path_relatif, 'ressources', 'expand.png')

        self.button_mainMenu = QPushButton('main menu')
        self.button_mainMenu.clicked.connect(self.return_menu)

        self.coll_lib = QPushButton()
        self.coll_lib.setIcon(QIcon(pathColl))
        self.coll_lib.setToolTip('Collapse all')
        self.coll_lib.setMaximumWidth(30)
        self.coll_lib.setEnabled(False)
        self.coll_lib.clicked.connect(self.collapse)

        self.exp_lib = QPushButton()
        self.exp_lib.setIcon(QIcon(pathExp))
        self.exp_lib.setToolTip('Expand all')
        self.exp_lib.setMaximumWidth(30)
        self.exp_lib.setEnabled(False)
        self.exp_lib.clicked.connect(self.expand)

        menu_lib = QHBoxLayout(self)
        menu_lib.addWidget(self.button_mainMenu)
        menu_lib.addWidget(self.coll_lib)
        menu_lib.addWidget(self.exp_lib)
        menu_lib_wid = QWidget()
        menu_lib_wid.setLayout(menu_lib)

        self.menub = Menu(self)
        self.menut = ToolBar(self.mdi)

        self.splitter1 = QSplitter(Qt.Orientation.Vertical)
        self.splitter1.addWidget(searchEngine)
        self.splitter1.addWidget(menu_lib_wid)
        self.splitter1.addWidget(self.scrollTools)
        self.splitter1.addWidget(previewBlock)
        self.splitter1.setSizes([20, 20, 500, 120])

        self.splitterp = QSplitter(Qt.Orientation.Horizontal)
        self.splitterp.addWidget(tabW)
        self.splitterp.addWidget(legend)
        self.splitterp.setSizes([400, 150])

        self.splitter2 = QSplitter(Qt.Orientation.Vertical)
        self.splitter2.addWidget(self.menut)
        self.splitter2.addWidget(self.mdi)
        self.splitter2.addWidget(self.splitterp)
        self.splitter2.setSizes([10, 400, 100])

        self.splitter3 = QSplitter(Qt.Orientation.Vertical)
        self.splitter3.addWidget(self.textEdit)

        self.splitter4 = QSplitter(Qt.Orientation.Horizontal)
        self.splitter4.addWidget(self.splitter1)
        self.splitter4.addWidget(self.splitter2)
        self.splitter4.addWidget(self.splitter3)
        self.splitter4.setSizes([100, 800, 100])

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addWidget(self.menub)
        self.verticalLayout.addWidget(self.splitter4)

        self.startConnection = None
        self.startSelection = None

        self.menub.btnPressed(QAction('load_previous_diagram'))
        Start_environment(False)
        SharedMemoryManager(False)

    def addSubWindow(self, title):
        i = len(self.mdi.subWindowList())
        self.listItems.append({})
        self.listBlocks.append({})
        self.listNodes.append({})
        self.listConnects.append({})
        self.listSubMod.append({})
        self.listTools.append({})
        self.listIfShowedState.append({})
        self.listConstants.append({})
        self.libTools.append({})
        self.listProbes.append({})
        self.listImgBox.append({})
        self.listStopExec.append({})
        self.pointTyping.append(-1)
        self.undoredoTyping.append({})
        self.pathDiagram.append('')
        self.diagramScene.append(DiagramScene(self))
        self.diagramView.append(DiagramView(self.diagramScene[i], self))
        # self.diagramView[-1].gridVisible = showGrid
        layoutDiagram = QVBoxLayout()
        layoutDiagram.addWidget(self.diagramView[i])
        layoutDiagram.setContentsMargins(0, 0, 0, 0)
        wid = QWidget()
        # wid.setStyleSheet("background-color:rgb(30,30,30)")
        style_bkg = str(ItemColor.BACKGROUND.value.getRgb()[0:3])
        wid.setStyleSheet("background-color:rgb" + style_bkg)
        wid.setLayout(layoutDiagram)
        if title == '':
            title = self.searchFreeNameWindow()
        sub = SubWindowManager()
        sub.setWidget(wid)
        sub.setWindowTitle(title)
        sub.showFullScreen()
        sub.windowNumber = i
        self.mdi.addSubWindow(sub, Qt.WindowType.WindowShadeButtonHint)
        self.mdi.setActiveSubWindow(sub)
        sub.signal1.connect(self.closeSubWindow)
        sub.signal2.connect(self.windSelection)
        sub.show()

    def searchFreeNameWindow(self):
        listTitle = [nm.windowTitle() for nm in self.mdi.subWindowList()]
        count = 0
        found = False
        while not found:
            newName = "Diagram{}*".format(str(count))
            if newName not in listTitle and (newName + "*") not in listTitle:
                found = True
            else:
                count += 1
        return newName

    # def windClosed(self, obj):
    #     num = obj.windowNumber
    #     self.mdi.removeSubWindow(obj)
    #     self.closeSubWindow(num)

    def windActivation(self):
        try:
            currentsubWind = self.mdi.activeSubWindow()
            self.currentTab = currentsubWind.windowNumber
            if self.autofit:
                editor.diagramScene[editor.currentTab].fitwindow(0.8)
            try:
                self.infopathDgr.setText(self.pathDiagram[self.currentTab])
                self.currentpathwork = self.pathDiagram[self.currentTab]
            except Exception as er:
                pass
        except Exception as err:
            pass

    def windSelection(self, title, num):
        self.currentTab = num
        try:
            self.infopathDgr.setText(self.pathDiagram[self.currentTab])
            self.currentpathwork = self.pathDiagram[self.currentTab]
        except Exception as er:
            pass

    @pyqtSlot(str)
    def menu_choosen(self, name):
        if name == 'Structures':
            tmp = self.get_str_tree()
        elif name == 'SubModules':
            tmp = self.get_sub_tree()
        else:
            tmp = self.get_lib_tree(name)
        self.scrollTools.setWidget(tmp)
        self.coll_lib.setEnabled(True)
        self.exp_lib.setEnabled(True)

    def return_menu(self):
        self.library_tools = buildLibrary(self.list_tools)
        self.library_tools.menu_choosen.connect(self.menu_choosen)
        self.scrollTools.setWidget(self.library_tools)
        self.coll_lib.setEnabled(False)
        self.exp_lib.setEnabled(False)

    def collapse(self):
        tabCurrent = self.scrollTools.widget()
        try:
            tabCurrent.collapseAll()
        except Exception as err:
            pass

    def expand(self):
        tabCurrent = self.scrollTools.widget()
        try:
            tabCurrent.expandAll()
        except Exception as err:
            pass

    def get_str_tree(self):
        libMod1 = LibMod('structures_tools')
        libMod1.setColumnCount(1)
        libBrowser = TreeLibrary()
        model1 = LibMod('structures_tools')
        model1.setColumnCount(1)
        model1.setHeaderData(0, Qt.Orientation.Horizontal, 'Structures')
        rootNode1 = model1.invisibleRootItem()

        for k_cat, v_cat in self.listCategoryTools.items():
            branch1 = QStandardItem(k_cat)
            branch1.setEditable(False)
            for cst in v_cat:
                stdItem1 = QStandardItem(QIcon(self.icon1), cst)
                stdItem1.setEditable(False)
                libMod1.appendRow(stdItem1)
                branch1.appendRow([QStandardItem(stdItem1), None])
            rootNode1.appendRow([branch1, None])

        libBrowser.setModel(model1)
        libBrowser.hideColumn(1)
        libBrowser.setAlternatingRowColors(True)
        libBrowser.expandAll()
        libBrowser.setDragDropMode(libBrowser.DragDropMode.DragOnly)

        return libBrowser

    def get_sub_tree(self):
        libMod3 = LibMod('blocks_subModules')
        libMod3.setColumnCount(1)
        listSubMod = getlistSubModules()
        category_submod = listSubMod.listDir()
        list_cat = sorted(category_submod.keys())
        self.libSubMod = listSubMod.listSubModules()
        list_submod = sorted(self.libSubMod.keys())

        libBrowser = TreeLibrary()
        model3 = LibMod('blocks_subModules')
        model3.setColumnCount(1)
        model3.setHeaderData(0, Qt.Orientation.Horizontal, 'SubModules')
        rootNode3 = model3.invisibleRootItem()

        self.listCategorySubMod.append('SubModules')

        for listcat in list_cat:
            branch1 = QStandardItem(listcat)
            branch1.setEditable(False)
            branch1.setSelectable(False)
            for submod in sorted(category_submod[listcat]):
                stdItem3 = QStandardItem(QIcon(self.icon3), submod)
                stdItem3.setEditable(False)
                libMod3.appendRow(stdItem3)
                branch1.appendRow([QStandardItem(stdItem3), None])
            rootNode3.appendRow([branch1, None])

            libBrowser.setModel(model3)
            # libBrowser.setColumnWidth(0, 200)
            libBrowser.hideColumn(1)
            libBrowser.setAlternatingRowColors(True)
            libBrowser.expandAll()
            libBrowser.setDragDropMode(libBrowser.DragDropMode.DragOnly)

        return libBrowser

    def get_lib_tree(self, name):
        name = name.replace('\n', '_')
        icon = self.list_tools[name]
        libBrowser = TreeLibrary()
        model2 = LibMod('mod_SubMod')
        model2.setColumnCount(1)
        model2.setHeaderData(0, Qt.Orientation.Horizontal, name)
        rootNode2 = model2.invisibleRootItem()

        rootLib = self.list_tree[name]

        stdItem2 = []
        for category, modules in rootLib.items():
            stdItem2.clear()
            branch1 = QStandardItem(category)
            branch1.setEditable(False)
            branch1.setSelectable(False)
            for clas in modules:
                stdItem2.append(QStandardItem(QIcon(icon), clas))
            for i in stdItem2:
                i.setEditable(False)
                branch1.appendRow([QStandardItem(i), None])
            rootNode2.appendRow([branch1, None])

        libBrowser.setModel(model2)
        libBrowser.setColumnWidth(0, 200)
        libBrowser.hideColumn(1)
        libBrowser.setAlternatingRowColors(True)
        libBrowser.expandAll()
        libBrowser.setDragDropMode(libBrowser.DragDropMode.DragOnly)

        return libBrowser

    def getlib(self):
        return self.libBlocks

    def getSubWindowCurrentTitle(self):
        if len(self.mdi.subWindowList()) == 1:
            currentTitle = self.mdi.subWindowList()[0].windowTitle()
        else:
            currentTitle = self.mdi.currentSubWindow().windowTitle()
        return currentTitle

    def setSubWindowCurrentTitle(self, title):
        if len(self.mdi.subWindowList()) > 1:
            self.mdi.currentSubWindow().setWindowTitle(title)
        else:
            self.mdi.subWindowList()[0].setWindowTitle(title)

    def setlib(self, lib):
        self.libBlocks = lib.copy()

    def closeSubWindow(self, obj):
        currentIndex = 0
        isMax = obj.isMaximized()
        try:
            currentIndex = obj.windowNumber
        except Exception as err:
            pass
        if not self.diagramScene[currentIndex].fullScr:
            currentTitle = obj.windowTitle()
            self.mdi.removeSubWindow(obj)
            obj.close()
            obj.deleteLater()
            del self.listItems[currentIndex]
            del self.listBlocks[currentIndex]
            del self.listNodes[currentIndex]
            del self.listSubMod[currentIndex]
            del self.listConnects[currentIndex]
            del self.listConstants[currentIndex]
            del self.listTools[currentIndex]
            del self.libTools[currentIndex]
            del self.listProbes[currentIndex]
            del self.listImgBox[currentIndex]
            del self.listStopExec[currentIndex]
            del self.undoredoTyping[currentIndex]
            del self.pointTyping[currentIndex]
            del self.diagramView[currentIndex]
            del self.diagramScene[currentIndex]
            del self.pathDiagram[currentIndex]
            del self.listIfShowedState[currentIndex]

            try:
                self.infopathDgr.setText(self.pathDiagram[self.currentTab])
            except Exception as err:
                pass

            for lstWid in self.mdi.subWindowList():
                if lstWid.windowNumber > currentIndex:
                    lstWid.windowNumber -= 1
                    self.currentTab = lstWid.windowNumber
                    self.mdi.setActiveSubWindow(lstWid)
                if isMax:
                    lstWid.showMaximized()

            # for lstWid in self.mdi.subWindowList():
            #     print(lstWid.windowNumber, lstWid.windowTitle(), self.pathDiagram[lstWid.windowNumber])

            list_dgr = Config().getPathDiagrams()
            if list_dgr:
                for elem in list_dgr:
                    if currentTitle in elem:
                        list_dgr.remove(elem)
            Config().setPathDiagrams(list_dgr)

    # def blockSelection(self, blockSelected):
    #     for dd in self.diagramScene[self.currentTab].items():
    #         if type(dd) is LinkItem:
    #             tmp = self.listNodes[self.currentTab][dd.name]
    #             if blockSelected.unit + ':' in tmp:
    #                 dd.foncedBlock(False)
    #             else:
    #                 dd.foncedBlock(True)
    #         if type(dd) is BlockCreate or type(dd) is Constants:
    #             if dd == blockSelected:
    #                 dd.foncedBlock(False)
    #             else:
    #                 dd.foncedBlock(True)

    def refreshSubModLib(self, itemblock, filpy):
        self.menu_choosen('SubModules')
        tabCurrent = self.scrollTools.widget()

        if tabCurrent:
            model = tabCurrent.model()
            root = model.invisibleRootItem()
            category_idx, child_idx = self.indexItems(root, filpy, itemblock)
            tabCurrent.selectionModel().clear()
            idx = model.indexFromItem(model.item(category_idx).child(child_idx))
            tabCurrent.setCurrentIndex(idx)

    def searchCurrent(self):
        self.lstSearch = {}
        for el, vl in self.getlib().items():
            self.lstSearch[el] = vl[0]
        for eg, vg in self.libSubMod.items():
            self.lstSearch[eg] = vg[-1]
        self.completer.setModel(QStringListModel(sorted(self.lstSearch.keys())))
        self.searchField.setCompleter(self.completer)
        self.searchField.disconnect()
        self.searchField.returnPressed.connect(self.searchResult2)

    def searchResult(self):
        itemblock = self.searchField.text()
        if not itemblock:
            return
        tmp2 = self.lstSearch[itemblock]
        if '.' in tmp2:
            cat = tmp2.split('.')[0]
            filpy = tmp2.split('.')[1]
            tabCurrent = None
            self.menu_choosen(cat)
            tabCurrent = self.scrollTools.widget()
        else:
            filpy = tmp2
            tabCurrent = None
            self.menu_choosen('SubModules')
            tabCurrent = self.scrollTools.widget()

        if tabCurrent:
            model = tabCurrent.model()
            root = model.invisibleRootItem()
            category_idx, child_idx = self.indexItems(root, filpy, itemblock)
            tabCurrent.selectionModel().clear()
            idx = model.indexFromItem(model.item(category_idx).child(child_idx))
            tabCurrent.setCurrentIndex(idx)
            # editor.diagramView[editor.currentTab].dropEvent(tabCurrent.model().__items)

    def iterItems(self, root):
        def recurse(parent):
            for row in range(parent.rowCount()):
                for column in range(parent.columnCount()):
                    child = parent.child(row, column)
                    yield child
                    try:
                        if child.hasChildren():
                            yield from recurse(child)
                    except Exception as er:
                        pass
        if root is not None:
            yield from recurse(root)

    def indexItems(self, root, cat, item):
        for row in range(root.rowCount()):
            for column in range(root.columnCount()):
                child = root.child(row, column)
                try:
                    if child.hasChildren():
                        if child.text() == cat:
                            for row2 in range(child.rowCount()):
                                for column2 in range(child.columnCount()):
                                    child2 = child.child(row2, column2)
                                    try:
                                        if child2.text() == item:
                                            return row, row2
                                    except Exception as er:
                                        pass
                except Exception as er:
                    pass
        return 0, 0

    def searchResult2(self):
        pass

    def startLink(self, port, format, pos):
        self.startConnection = Connection('', port, None, format)
        self.fromPort = port
        self.editText("start connection : {} {} {} {} </span>"
                      .format(port.unit, port.name, port.typeio, port.format),
                      10, 600, '003300', False, False)

    def deleteItemsLoop(self, item):
        for keyF, valueF in self.listTools[self.currentTab].items():
            if 'F' in keyF:
                if item.unit in valueF:
                    tmplistTools = valueF
                    tmplistTools.remove(item.unit)
                    self.listTools[self.currentTab][keyF] = tmplistTools
            elif 'I' in keyF:
                if item.unit in valueF[0]:
                    tmplistTools = valueF[0]
                    tmplistTools.remove(item.unit)
                    self.listTools[self.currentTab][keyF] = [tmplistTools, valueF[1]]
                if item.unit in valueF[1]:
                    tmplistTools = valueF[1]
                    tmplistTools.remove(item.unit)
                    self.listTools[self.currentTab][keyF] = [valueF[0], tmplistTools]

    def deleteLinksLoop(self, item):

        for keyF, valueF in self.listTools[self.currentTab].items():
            if 'F' in keyF:
                if item.name in valueF:
                    tmplistTools = valueF
                    tmplistTools.remove(item.name)
                    self.listTools[self.currentTab][keyF] = tmplistTools
            elif 'I' in keyF:
                if item.name in valueF[0]:
                    tmplistTools = valueF[0]
                    tmplistTools.remove(item.name)
                    self.listTools[self.currentTab][keyF] = [tmplistTools, valueF[1]]
                if item.name in valueF[1]:
                    tmplistTools = valueF[1]
                    tmplistTools.remove(item.name)
                    self.listTools[self.currentTab][keyF] = [valueF[0], tmplistTools]

    def loopMouseMoveEvent(self, item, pos):
        item.moved = True
        if not item.preview:
            listTypeItems = []
            itms = self.diagramScene[self.currentTab].items(pos)  # !!! intermittent bug

            for elem in itms:
                if type(elem) is ForLoopItem:
                    listTypeItems.append(elem)

            if listTypeItems:
                if len(listTypeItems) > 1:
                    postmp = None
                    elemtmp = None
                    try:
                        ind = 0
                        if item.currentLoop.loopIf:
                            if item.currentLoop.elemProxy.currentText() == 'False':
                                ind = 1
                        item.currentLoop.normalState()
                        item.currentLoop.IteminLoop(item.unit, False, ind)
                        item.currentLoop = None
                        item.caseFinal = False
                    except Exception as e:
                        pass
                    for lsElem in listTypeItems:
                        if not postmp:
                            postmp = lsElem.pos()
                            elemtmp = lsElem

                        elif postmp.x() < lsElem.pos().x():
                            postmp = lsElem.pos()
                            elemtmp = lsElem
                else:
                    elemtmp = listTypeItems[0]
                    try:
                        ind = 0
                        if item.currentLoop.loopIf:
                            if item.currentLoop.elemProxy.currentText() == 'False':
                                ind = 1
                        item.currentLoop.normalState()
                        item.currentLoop.IteminLoop(item.unit, False, ind)
                        item.currentLoop = None
                        item.caseFinal = False
                    except Exception as e:
                        pass

                item.currentLoop = elemtmp
                item.currentLoop.activeState()
                item.caseFinal = True
            else:
                if item.currentLoop:
                    ind = 0
                    if item.currentLoop.loopIf:
                        if item.currentLoop.elemProxy.currentText() == 'False':
                            ind = 1
                    item.currentLoop.normalState()
                    item.currentLoop.IteminLoop(item.unit, False, ind)
                    item.currentLoop = None
                    item.caseFinal = False
            item.moved = True

    def loopMouseReleaseEvent(self, item, otherItems):
        if item.currentLoop:
            ind = 0
            if item.currentLoop.loopIf:
                if item.currentLoop.elemProxy.currentText() == 'False':
                    ind = 1
            item.currentLoop.IteminLoop(item.unit, True, ind)
            if otherItems:
                self.loopMultipleItems(item, ind)
            item.currentLoop.normalState()
#             item.currentLoop.setDimensionLoop()
            item.currentLoop.resize_frame(ind)
            item.currentLoop = None
            item.caseFinal = False
        if item.moved:
            UpdateUndoRedo()
            item.moved = False

    def loopMultipleItems(self, item, ind):
        items = self.diagramScene[editor.currentTab].selectedItems()
        listItemsInLoopInternal = []
        if len(items) > 1:
            for el in items:
                # if (not type(el) in [Slide, CommentsItem]
                #     and el.unit not in item.unit):
                if not type(el) in [Slide, CommentsItem]:
                    if 'F' in el.unit:
                        listItemsInLoopInternal.extend(editor.listTools[editor.currentTab][el.unit])
                    elif 'I' in el.unit:
                        listItemsInLoopInternal.extend(editor.listTools[editor.currentTab][el.unit][0])
                        listItemsInLoopInternal.extend(editor.listTools[editor.currentTab][el.unit][1])
            for el in items:
                if not type(el) in [Slide, CommentsItem]:
                    if el.unit not in listItemsInLoopInternal:
                        item.currentLoop.IteminLoop(el.unit, True, ind)
                        item.currentLoop.normalState()

    def sceneMouseMoveEvent(self, event):
        # self.touchF = (int(event.modifiers()) == (Qt.KeyboardModifier.ControlModifier))
        if self.startConnection:
            pos = event.scenePos()
            self.startConnection.setEndPos(pos)
            cur_scene = self.diagramScene[self.currentTab]
            cur_view = self.diagramView[self.currentTab]
            items = cur_scene.items(pos)
            # cur_view.viewport().setCursor(QCursor(ItemMouse.CROSSCURSOR.value))
            if items:
                for item in items:
                    if type(item) is Port:
                        cur_view.viewport().setCursor(QCursor(ItemMouse.HORCURSOR.value))
                        break
                    elif type(item) in [ForLoopItem, ScriptItem]:
                        if self.fromPort.typeio == 'out':
                            if abs(event.scenePos().x() - item.scenePos().x()) <= 4:
                                cur_view.viewport().setCursor(QCursor(ItemMouse.ALLCURSOR.value))
                                break
                            else:
                                cur_view.viewport().setCursor(QCursor(ItemMouse.CROSSCURSOR.value))
                                break
                        elif self.fromPort.typeio == 'in':
                            if abs(event.scenePos().x() - (item.scenePos().x() + item.rect().width())) <= 4:
                                cur_view.viewport().setCursor(QCursor(ItemMouse.ALLCURSOR.value))
                                break
                            else:
                                cur_view.viewport().setCursor(QCursor(ItemMouse.CROSSCURSOR.value))
                                break
                    else:
                        cur_view.viewport().setCursor(QCursor(ItemMouse.CROSSCURSOR.value))
                        break
            else:
                cur_view.viewport().setCursor(QCursor(ItemMouse.CROSSCURSOR.value))

    def sceneMouseReleaseEvent(self, event):
        # self.touchF = (int(event.modifiers()) == (Qt.KeyboardModifier.ControlModifier))
        self.analyze_connection(event)

    def analyze_connection(self, event):

        if self.startConnection:
            pos = event.scenePos()
            items = self.diagramScene[self.currentTab].items(pos)
            nt = self.startConnection.link.name
            tmpformat = ''
            linkcurrent = ''

            for item in items:
                if type(item) is LinkItem:
                    if item.name == nt:
                        linkcurrent = item
                if type(item) is ForLoopItem:
                    if (self.fromPort.typeio == 'out' and
                            ('_' in self.fromPort.format or 'I' in item.unit) and
                            'tuple' not in self.fromPort.format and 'unkn' not in self.fromPort.format and
                            abs(event.scenePos().x() - (item.scenePos().x())) <= 4):
                        ind = item.addTunnelInputAuto(self.fromPort.format)
                        item = item.inputs[ind]
                    elif (self.fromPort.typeio == 'in' and
                            ('_' in self.fromPort.format or 'I' in item.unit) and
                          'tuple' not in self.fromPort.format and 'unkn' not in self.fromPort.format and
                          abs(event.scenePos().x() - (item.scenePos().x() + item.rect().width())) <= 4):
                        ind = item.addTunnelOutputAuto(self.fromPort.format)
                        item = item.outputs[item.nbin + ind]
                elif type(item) is ScriptItem:
                    if (self.fromPort.typeio == 'out' and 'unkn' not in self.fromPort.format and
                            abs(event.scenePos().x() - (item.scenePos().x())) <= 4):
                        namevar = self.fromPort.unit + '_' + self.fromPort.name
                        name_getted = True
                        lst_name = []
                        for inp in item.inputs:
                            lst_name.append(inp.name)
                        for i in range(len(lst_name)):
                            if namevar in lst_name:
                                namevar += str(i)
                            else:
                                break
                        c = input_output_setName(item.unit, 'input', item.inputs, namevar)
                        c.exec()
                        if c.getNewValues():
                            namevar = c.getNewValues()
                            item.add_Input(namevar, self.fromPort.format)
                            item = item.inputs[-1]
                    elif (self.fromPort.typeio == 'in' and 'unkn' not in self.fromPort.format and
                          abs(event.scenePos().x() - (item.scenePos().x() + item.rect().width())) <= 4):
                        namevar = self.fromPort.unit + '_' + self.fromPort.name
                        name_getted = True
                        lst_name = []
                        for inp in item.outputs:
                            lst_name.append(inp.name)
                        for i in range(len(lst_name)):
                            if namevar in lst_name:
                                namevar += str(i)
                            else:
                                break
                        c = input_output_setName(item.unit, 'output', item.outputs, namevar)
                        c.exec()
                        if c.getNewValues():
                            namevar = c.getNewValues()
                            item.add_Output(namevar, self.fromPort.format)
                            item = item.outputs[-1]

                if type(item) is Port:
                    portcurrent = item
                    tmpname = item.name
                    tmpunit = item.unit
                    tmptypeio = item.typeio
                    tmpformat = item.format
                    if 'enumerate' in tmpformat:
                        tmpformat = tmpformat[10:]
                    self.editText("try to connect to : {} {} {} {} </span>"
                                  .format(tmpunit, tmpname, tmptypeio, tmpformat),
                                  10, 600, '003300', False, False)
                    self.startConnection.setToPort(item)
                    break

            if 'enumerate' in self.fromPort.format:
                self.fromPort.format = self.fromPort.format[10:]

            if self.startConnection.toPort is None:
                self.startConnection.delete()
                self.startConnection = None
                return

            if self.fromPort.typeio == 'out':
                a = self.fromPort.unit
                b = self.fromPort.name
                c = tmpunit
                d = tmpname
            else:
                a = tmpunit
                b = tmpname
                c = self.fromPort.unit
                d = self.fromPort.name

            if self.startConnection.pos1 == self.startConnection.pos2:
                self.startConnection.delete()
            elif tmptypeio == self.fromPort.typeio:
                self.startConnection.delete()
                self.editText('Connection impossible : same type of connector (input=input or output=output)',
                              10, 600, 'ff0000', False, True)
            elif tmpformat == 'unkn' and self.fromPort.format == 'unkn':
                self.startConnection.delete()
                self.editText('Connection impossible : unknow plug to unknow plug',
                              10, 600, 'ff0000', False, True)
            elif (tmpformat == 'unkn' and 'A' in self.fromPort.unit) or (
                    self.fromPort.format == 'unkn' and 'A' in tmpunit):
                self.startConnection.delete()
                self.editText('Connection impossible : constant to connector',
                              10, 600, 'ff0000', False, True)
            elif ('U' in tmpunit or 'M' in tmpunit) and tmpunit == self.fromPort.unit:
                self.startConnection.delete()
                self.editText('Connection impossible : input to output of the same block',
                              10, 600, 'ff0000', False, True)
            elif not self.allowedConnection(a, b, c, d):
                self.startConnection.delete()
                self.editText('Connection impossible : interconnection with If structure forbidden',
                              10, 600, 'ff0000', False, True)
            elif tmpformat == 'unknunkn':
                self.startConnection.delete()
                self.editText('Connection impossible : connector to If structure in mode unknow forbidden',
                              10, 600, 'ff0000', False, True)
            else:
                if (tmpformat != 'unkn' and
                        self.fromPort.format != 'unkn' and
                        tmpformat != self.fromPort.format and
                        'tuple' not in tmpformat and
                        'tuple' not in self.fromPort.format):
                    self.editText('Warning : connection with different formats/types',
                                  10, 600, 'ff8f00', False, False)

                inAlready = False
                indiceLoopIf = 0  # can connect 2 links for LoopIf out
                for ele in self.listNodes[self.currentTab]:
                    tmp = self.listNodes[self.currentTab][ele]
                    tmp = tmp[tmp.index('#Node#') + 6:len(tmp)]
                    if tmp == c + ":" + d:
                        if 'I' in c:
                            indiceLoopIf += 1
                        if indiceLoopIf == 0 or indiceLoopIf == 2:
                            self.startConnection.delete()
                            self.editText('Connection impossible : input port already taken',
                                          10, 600, 'ff0000', False, True)
                            inAlready = True
                            break

                if not inAlready:
                    if 'U' in c:
                        listVal = self.listBlocks[self.currentTab][c]
                        ###################################################
                        name = listVal[0]
                        category = listVal[1]
                        cat = category.split('.')
                        listEnter = self.getlib()[name][1][0]
                        listValDefault = self.getlib()[name][1][1]
                        if not listValDefault:
                            listValDefault = ()
                        if len(listEnter) != len(listVal[2][1]):
                            if '_dyn' in name:
                                listEnter = listVal[2][0]
                                listValDefault = listVal[2][1]
                            else:
                                pathYml = os.path.dirname(os.path.realpath(__file__))
                                pathYml = os.path.join(pathYml, '../modules', cat[0], cat[1] + ".yml")
                                if os.path.exists(pathYml):
                                    with open(pathYml, 'r', encoding='utf8') as stream:
                                        dicts = yaml.load(stream, yaml.FullLoader)
                                        for el in dicts[name]:
                                            if el in listVal[2][0]:
                                                listEnter = (*listEnter, el)
                                                if type(dicts[name][el]).__name__ == 'str':
                                                    if 'enumerate' in dicts[name][el]:
                                                        listValDefault = (*listValDefault, dicts[name][el])
                                                    else:
                                                        try:
                                                            listValDefault = (*listValDefault, eval(dicts[name][el]))
                                                        except Exception as e:
                                                            listValDefault = (*listValDefault, dicts[name][el])
                                                else:
                                                    try:
                                                        listValDefault = (*listValDefault, eval(dicts[name][el]))
                                                    except Exception as e:
                                                        listValDefault = (*listValDefault, dicts[name][el])

                        ###################################################
                        newList = []
                        for i in range(len(listEnter)):
                            if listEnter[i] == d:
                                oldVal = listValDefault[i]
                                newList.append('Node(' + nt + ')')
                            else:
                                newList.append(listVal[2][1][i])
                        ###################################################
                        del self.listBlocks[self.currentTab][c]
                        self.listBlocks[self.currentTab][c] = (listVal[0], listVal[1], (listVal[2][0], newList, listVal[2][2], listVal[2][3]))

                    if 'M' in c:
                        listVal = self.listSubMod[self.currentTab][c]

                        ###################################################
                        mod = listVal[0]
                        ind = listVal[1][0].index(d)
                        newList = []
                        for i in range(len(listVal[1][1])):
                            if i == ind:
                                oldVal = self.libSubMod[mod][1][i]
                                newList.append('Node(' + nt + ')')
                            else:
                                newList.append(listVal[1][1][i])
                        del self.listSubMod[self.currentTab][c]
                        self.listSubMod[self.currentTab][c] = (listVal[0], (listVal[1][0], newList, listVal[1][2], listVal[1][3]), listVal[2])
                    changeColorLink = False

                    if 'F' in c or 'I' in c or 'S' in c or 'J' in c:
                        if tmpformat == "unkn":
                            tmpformat = self.fromPort.format
                        if 'int' in tmpformat:
                            oldVal = 0
                        elif 'float' in tmpformat:
                            oldVal = 0.0
                        elif 'str' in tmpformat:
                            oldVal = ''
                        elif 'path' in tmpformat:
                            oldVal = 'path'
                        elif 'bool' in tmpformat:
                            oldVal = True
                        elif 'tuple' in tmpformat:
                            oldVal = (0,)

                        if 'list' in tmpformat:
                            oldVal = [oldVal]
                        elif 'array' in tmpformat:
                            oldVal = [[oldVal]]

                    if 'I' in a and 'I' in c:
                        for item in items:
                            if type(item) is ForLoopItem and item.unit == a:
                                tmplistTools = self.listTools[self.currentTab][a]
                                if item.elemProxy.currentText() == 'True':
                                    tmp = tmplistTools[0]
                                    tmp.append(nt)
                                    self.listTools[self.currentTab][a] = [tmp, tmplistTools[1]]
                                else:
                                    tmp = tmplistTools[1]
                                    tmp.append(nt)
                                    self.listTools[self.currentTab][a] = [tmplistTools[0], tmp]

                    if tmpformat == 'unkn' or self.fromPort.format == 'unkn':
                        if tmpformat in 'unkn':
                            tmpformat = self.fromPort.format
                        else:
                            self.fromPort.format = tmpformat
                            changeColorLink = True

                    for types in TypeColor:
                        if types.name in tmpformat:
                            color = types.value

                    for types in TypeColor:
                        if types.name in self.fromPort.format:
                            color2 = types.value

                    if 'C' in a and b != 'unkn':
                        b = self.listConnects[self.currentTab][a][1]

                    if 'C' in a and b == 'unkn':
                        b = d
                        mm = True
                        suffix = 0
                        ref = b
                        while mm:
                            found = False
                            for ele in self.listConnects[self.currentTab].keys():
                                if b in self.listConnects[self.currentTab][ele]:
                                    suffix += 1
                                    b = ref + '_' + str(suffix)
                                    found = True
                            if not found:
                                mm = False

                        if self.fromPort.typeio == 'out':
                            portcurrent = self.fromPort
                        portcurrent.setBrush(color)
                        portcurrent.format = tmpformat
                        portcurrent.name = b
                        portcurrent.label.setPlainText(b)
                        portcurrent.label.setPos(portcurrent.pos().x() - 160 - portcurrent.label.boundingRect().size().width(),
                                                 portcurrent.label.pos().y())
                        tmp = self.listConnects[self.currentTab][a]
                        del self.listConnects[self.currentTab][a]
                        self.listConnects[self.currentTab][a] = (tmp[0], b, tmpformat, oldVal)

                    if 'C' in c and d == 'unkn':
                        d = b
                        mm = True
                        suffix = 0
                        ref = d
                        while mm:
                            found = False
                            for ele in self.listConnects[self.currentTab].keys():
                                if d in self.listConnects[self.currentTab][ele]:
                                    suffix += 1
                                    d = ref + '_' + str(suffix)
                                    found = True
                            if not found:
                                mm = False
                        if self.fromPort.typeio == 'in':
                            portcurrent = self.fromPort
                        portcurrent.format = tmpformat
                        portcurrent.setBrush(color)
                        portcurrent.name = d
                        portcurrent.label.setPlainText(d)
                        tmp = self.listConnects[self.currentTab][c]
                        del self.listConnects[self.currentTab][c]
                        self.listConnects[self.currentTab][c] = (tmp[0], d, tmpformat)

                    if 'P' in c:
                        if self.fromPort.typeio == 'in':
                            portcurrent = self.fromPort
                        portcurrent.format = tmpformat
                        portcurrent.setBrush(color)
                        tmp = self.listProbes[self.currentTab][c]
                        del self.listProbes[self.currentTab][c]
                        self.listProbes[self.currentTab][c] = (tmpformat, tmp[1])

                    self.listNodes[self.currentTab][nt] = a + ':' + b + '#Node#' + c + ':' + d

                    # attribute constants combobox value automatically ######################
                    if 'A' in a and 'enumerate' in str(oldVal):
                        tmpitems = self.diagramScene[self.currentTab].items()
                        for gh in tmpitems:
                            if type(gh) is Constants:
                                if gh.unit == a and type(gh.elemProxy) is Constants_Combo:
                                    lst = []
                                    for ij in list(eval(oldVal)):
                                        lst.append(ij[1])
                                        gh.elemProxy.clear()
                                        gh.elemProxy.addItems(lst)
                                        gh.elemProxy.txt = "enumerate(" + str(tuple(newList)) + ")"
                                        gh.elemProxy.value = str(newList[0])
                                        gh.elemProxy.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
                                        gh.elemProxy.adjustSize()
                                        gh.form = "enumerate(" + str(tuple(lst)) + ")"
                                        gh.changeCombo()
                                        del self.listConstants[self.currentTab][gh.unit]
                                        self.listConstants[self.currentTab][gh.unit] = (gh.elemProxy.txt, gh.elemProxy.value, gh.label)

                    #################################################################################

                    if changeColorLink:
                        if linkcurrent:
                            linkcurrent.setPen(QPen(color, DimLink.simple.value))
                        else:
                            linkcurrent = self.startConnection.link
                        if 'list' in str(tmpformat):
                            linkcurrent.setPen(QPen(color, DimLink.list.value))
                            linkcurrent.bislink.setPen(QPen(Qt.PenStyle.NoPen))
                            linkcurrent.weight = DimLink.list.value
                        elif 'array' in str(tmpformat):
                            linkcurrent.setPen(QPen(color, DimLink.array.value))
                            linkcurrent.bislink.setPen(QPen(ItemColor.BIS_LINK.value, DimLink.bis.value, Qt.PenStyle.SolidLine))
                            linkcurrent.weight = DimLink.array.value
                        else:
                            linkcurrent.setPen(QPen(color, DimLink.simple.value))
                            linkcurrent.bislink.setPen(QPen(Qt.PenStyle.NoPen))
                            linkcurrent.weight = DimLink.simple.value
                        linkcurrent.linkTxt.setDefaultTextColor(color)
                        linkcurrent.linkShow.setPen(QPen(color, 2))
                        linkcurrent.linkShow.setBrush(color)
                        linkcurrent.color = color

                    self.editText("Connection ok", 10, 600, '003300', False, True)
                    UpdateUndoRedo()
                    Menu().btnPressed(QAction('Refresh Diagram'))

            self.startConnection = None

    def allowedConnection(self, unitA, portA, unitB, portB):
        posA, posB = [], []
        self.current_if, self.current_it = "", ""

        def searchIf(list_item):
            list_out = []
            for vf in list_item:
                if 'F' in vf:
                    tmp_item = editor.listTools[editor.currentTab][vf]
                    list_out.extend(searchIf(tmp_item))
                if vf in self.current_it:
                    list_out.append(self.current_if)
                    break
            return list_out

        for ki, vi in editor.listTools[editor.currentTab].items():
            if 'I' in ki:
                ext_vi = vi[0] + vi[1]
                self.current_if = ki
                self.current_it = unitA
                if unitA in ext_vi or (unitA in ki and 'in' in portA):
                    posA.append(ki)
                else:
                    posA.extend(searchIf(ext_vi))
                self.current_it = unitB
                if unitB in ext_vi or (unitB in ki and 'out' in portB):
                    posB.append(ki)
                else:
                    posB.extend(searchIf(ext_vi))
        if posA and posB:
            if posA[0] != posB[0]:
                return False
        if (posA and not posB) or (not posA and posB):
            return False
        return True

    def editText(self, text, font_size, font_weight, text_color, refresh, line_space):
        br = ''
        if line_space:
            br = '<br>'
        if refresh:
            self.textEdit.clear()
        self.textEdit.addTxt("<span style=\" font-size:{}pt;"
                             "font-weight:{}; color:#{};\" >"
                             "{} </span>{}"
                             .format(font_size, font_weight, text_color, text, br))


class Port(QGraphicsRectItem):

    def __init__(self, name, typeio, format, unit, showlabel, isMod, dx, dy, parent=None):

        if 'tunnel' not in typeio:
            self.rectgl = QRectF(-7, -7, 12.0, 12.0)
        else:
            self.rectgl = QRectF(-15, -12, 50.0, 40.0)

        QGraphicsRectItem.__init__(self, self.rectgl, parent)

        self.setCursor(QCursor(ItemMouse.HORCURSOR.value))

        self.name = name
        self.unit = unit
        self.typeio = typeio
        self.format = format
        self.isMod = isMod
        self.dx, self.dy = dx, dy
        self.posCallbacks = []

        if isMod:
            self.setAcceptHoverEvents(True)
            self.setFlag(self.GraphicsItemFlag.ItemSendsScenePositionChanges, True)
            self.setFlag(self.GraphicsItemFlag.ItemIsFocusable, True)
        color = ItemColor.DEFAULTTEXTCOLOR.value

        for types in TypeColor:
            if types.name in format:
                color = types.value

        self.setBrush(QBrush(color))

        if showlabel:
            self.label = QGraphicsTextItem(name, self)
            # self.label.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
            # self.label.setHtml("<div style='background-color:#aaaaaa;'> " + name + " </div>")
            self.label.setFont(QFont("Times", 12, QFont.Weight.Bold))
            if self.typeio == 'in':
                self.label.setDefaultTextColor(ItemColor.TEXT_PORT_LABEL_INPUT.value)
                self.label.setPos(dx, dy)
            elif self.typeio == 'out':
                self.label.setDefaultTextColor(ItemColor.TEXT_PORT_LABEL_OUTPUT.value)
                self.label.setPos(-self.label.boundingRect().size().width() - dx, dy)

    def itemChange(self, change, value):
        if change == self.GraphicsItemChange.ItemScenePositionHasChanged:
            for cb in self.posCallbacks:
                cb(value)
            return value
        return super(Port, self).itemChange(change, value)

    def hoverEnterEvent(self, event):
        pos = event.screenPos()
        self.setToolTip("<span style=\"background-color: #ffffff;\">format: <b>{}</b></span>".format(self.format))
        # return QGraphicsRectItem.hoverEnterEvent(self, event)

    def mousePressEvent(self, event):
        if self.isMod and event.button() == Qt.MouseButton.LeftButton:
            editor.startLink(self, self.format, event.pos())

    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key.Key_W and not self.key_pressed:
    #         editor.startLink(self, self.format, (self.dx, self.dy))
    #         self.key_pressed = True
        # return QGraphicsRectItem.keyPressEvent(self, event)

    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key.Key_W:
    #         pyautogui.click(button='left', interval=0.25)
        # return QGraphicsRectItem.keyPressEvent(self, *args, **kwargs)

    def contextMenuEvent(self, event):
        ac, cp = None, None
        if self.isMod:
            menu = QMenu()
            if ('F' in self.unit or 'I' in self.unit):
                if 'val' not in self.name:
                    ac = menu.addAction('Delete this tunnel')
                    ac.triggered.connect(self.deleteTunnel)
                    ct = menu.addAction('Change format')
                    ct.triggered.connect(self.changeTunnel)
            elif ('S' in self.unit or 'J' in self.unit):
                ac = menu.addAction('Delete this port')
                ac.triggered.connect(self.deletePort)
                cf = menu.addAction('Change format')
                cf.triggered.connect(self.changeFormatScript)
            if self.typeio == 'out' and 'A' not in self.unit:
                cp = menu.addAction('add Value Probe')
                cp.triggered.connect(self.addValueP)
                cp = menu.addAction('add Type Probe')
                cp.triggered.connect(self.addTypeP)
                cp = menu.addAction('add Length Probe')
                cp.triggered.connect(self.addLengthP)
                menu.addSeparator()
                cp = menu.addAction('add Print block')
                cp.triggered.connect(self.addPrint)
            elif (self.format not in ['list_bool', 'array_bool', 'list_path', 'array_path', 'dict'] and
                  # 'tuple' not in self.format and
                  'A' not in self.unit):
                yet = False
                for key, val in editor.listNodes[editor.currentTab].items():
                    tmpVal = val[val.index("#Node#") + 6:]
                    if self.unit + ':' + self.name == tmpVal:
                        yet = True
                if not yet:
                    cp = menu.addAction('add constant for this port')
                    cp.triggered.connect(self.addConstant)
        if ac or cp:
            menu.exec(event.screenPos())

#         event.accept()
#         return QGraphicsRectItem.contextMenuEvent(self, event)

    def changeFormatScript(self):
        cur_item = editor.listItems[editor.currentTab][self.unit]
        if self.typeio == 'in':
            c = define_inputs_outputs(self.unit, 'input', cur_item.inputs, self.name)

        else:
            c = define_inputs_outputs(self.unit, 'output', cur_item.outputs, self.name)
        c.exec()

        if c.getNewValues():
            old_name = self.name
            listEnter = editor.libTools[editor.currentTab][self.unit][0]
            listOut = editor.libTools[editor.currentTab][self.unit][1]
            tmpEnter, tmpOut = listEnter, listOut

            for types in TypeColor:
                if types.name in c.getNewValues()[1]:
                    color = types.value
            self.setBrush(color)
            self.label.setPlainText(c.getNewValues()[0])

            if self.typeio == 'in':
                self.label.setPos(5 - self.label.boundingRect().width(), -28)
                for i in range(len(listEnter)):
                    if listEnter[i][0] == self.name:
                        listEnter[i] = [c.getNewValues()[0], 'in', c.getNewValues()[1]]
                        break
            else:
                self.label.setPos(-8, -28)
                for i in range(len(listOut)):
                    if listOut[i][0] == self.name:
                        tmpOut[i] = [c.getNewValues()[0], 'out', c.getNewValues()[1]]
                        break
            self.name = c.getNewValues()[0]
            self.format = c.getNewValues()[1]

            editor.libTools[editor.currentTab][self.unit] = [listEnter, tmpOut]
            self.inout = [listEnter, tmpOut]

            old_inf = '{}:{}'.format(self.unit, old_name)
            new_inf = '{}:{}'.format(self.unit, self.name)

            for lst_nd, lst_link in editor.listNodes[editor.currentTab].items():
                a, b, c = lst_link.split('#')
                if self.typeio == 'in' and old_inf == c:
                    editor.listNodes[editor.currentTab][lst_nd] = '{}#Node#{}'.format(a, new_inf)
                    break
                elif self.typeio == 'out' and old_inf == a:
                    editor.listNodes[editor.currentTab][lst_nd] = '{}#Node#{}'.format(new_inf, c)
                    break
                # if old_inf in lst_link:
                #     editor.listNodes[editor.currentTab][lst_nd] = lst_link.replace(old_inf, new_inf)
                #     if self.typeio == 'in':
                #         break

            UpdateUndoRedo()

    def alphaNumOrder(self, string):
        return ''.join([format(int(x), '05d') if x.isdigit()
                       else x for x in re.split(r'(\d+)', string)])

    def changeTunnel(self):
        if 'I' in self.unit:
            c = defineTunnels(self.name, 'If', self.format)
        else:
            c = defineTunnels(self.name, 'For_sequential', self.format)
        c.exec()

        if c.getNewValues():
            format = c.getNewValues()[0]
            typein = c.getNewValues()[1] + '_'
            typein = typein.replace('simple_', '')
            typeout = c.getNewValues()[2] + '_'
            typeout = typeout.replace('simple_', '')

            for types in TypeColor:
                if types.name in format:
                    color = types.value

            cur_item = editor.listItems[editor.currentTab][self.unit]

            inputs = cur_item.inputs
            outputs = cur_item.outputs
            indice = 0
            for lst in inputs:
                if lst.name == self.name:
                    portIn = lst
                    inputs.remove(lst)
                    break
                else:
                    indice += 1
            for lst in outputs:
                if lst.name == self.name:
                    portOut = lst
                    outputs.remove(lst)
                    break

            portIn.format = typein + format
            portOut.format = typeout + format

            portIn.setBrush(color)
            portOut.setBrush(color)

            inputs.append(portIn)
            outputs.append(portOut)

            inputs.sort(key=lambda x: self.alphaNumOrder(x.name))
            outputs.sort(key=lambda x: self.alphaNumOrder(x.name))
            # inputs.sort(key=lambda x: x.name)
            # outputs.sort(key=lambda x: x.name)

            cur_item.inputs = inputs
            cur_item.outputs = outputs

            editor.listItems[editor.currentTab][self.unit] = cur_item

            listEnter = editor.libTools[editor.currentTab][self.unit][0]
            listOut = editor.libTools[editor.currentTab][self.unit][1]

            if 'in' in self.name:
                listEnter[indice] = [[portIn.name, portIn.typeio, portIn.format], [portOut.name, portOut.typeio, portOut.format]]
            else:
                if 'I' in self.unit:
                    listOut[indice - len(inputs) + 1] = [[portIn.name, portIn.typeio, portIn.format], [portOut.name, portOut.typeio, portOut.format]]
                else:
                    listOut[indice - len(inputs)] = [[portIn.name, portIn.typeio, portIn.format], [portOut.name, portOut.typeio, portOut.format]]

            editor.libTools[editor.currentTab][self.unit] = [listEnter, listOut]

            UpdateUndoRedo()

    def deleteTunnel(self):
        editor.listItems[editor.currentTab][self.unit].deleteTunnel(self.name)

    def deletePort(self):
        editor.listItems[editor.currentTab][self.unit].deletePort(self.name, self.typeio)

    def addConstant(self):
        if 'U' in self.unit:
            it = self.addConstantBlock()
        elif 'M' in self.unit:
            it = self.addConstantSubMod()
        elif 'I' in self.unit or 'S' in self.unit or 'J' in self.unit or 'F' in self.unit:
            it = self.addConstantStr()
        editor.loopMouseMoveEvent(it, it.scenePos())
        editor.loopMouseReleaseEvent(it, False)

    def addConstantBlock(self):
        nameClass = editor.listItems[editor.currentTab][self.unit].name
        listEnter = editor.listBlocks[editor.currentTab][self.unit][2][0]
        indx = listEnter.index(self.name)
        val = editor.listBlocks[editor.currentTab][self.unit][2][1][indx]
        if 'enumerate' in self.format:
            for lst in range(len(listEnter)):
                if listEnter[lst] == self.name:
                    try:
                        self.format = editor.getlib()[nameClass][1][1][lst]
                    except Exception as e:
                        self.format = self.getEnumerateFromYml()
            val = self.format[11:self.format.index(',')]
        if ('list' in self.format or 'array' in self.format) and 'enumerate' not in self.format:
            if 'list_int' in self.format:
                val = (-100, [0, 0], 100)
                f = 2
            elif 'list_float' in self.format:
                val = (-100.0, [0.0, 0.0], 100.0)
                f = 2
            elif 'list_str' in self.format:
                val = ['', '']
                f = 2
            elif 'array_int' in self.format:
                val = (-100, [[0, 0], [0, 0]], 100)
                f = 1
            elif 'array_float' in self.format:
                val = (-100.0, [[0.0, 0.0], [0.0, 0.0]], 100.0)
                f = 1
            elif 'array_str' in self.format:
                val = [['', ''], ['', '']]
                f = 1
            a1 = Clusters('newCluster', 115, 33, val, self.format, self.name, True)
            a1.setPos(self.mapToScene(self.boundingRect().x() - 300, self.boundingRect().y()))
            a1.outputs[0].setPos(2 * a1.w - 10, a1.h / f)
        else:
            a1 = Constants('newConstant', 80, 30, val, self.format, self.name, True)
            a1.setPos(self.mapToScene(self.boundingRect().x() - 100, self.boundingRect().y()))
        editor.diagramScene[editor.currentTab].addItem(a1)
        editor.listItems[editor.currentTab][a1.unit] = a1
        if 'enumerate' in self.format:
            self.format = 'enumerate_str'
        startConnection = Connection('',
                                     a1.outputs[0],
                                     self,
                                     self.format)
        startConnection.setEndPos(self.scenePos())
        startConnection.setToPort(self)
        editor.listNodes[editor.currentTab][startConnection.link.name] = a1.unit + ':' + '#Node#' + self.unit + ':' + self.name

        listVal = editor.listBlocks[editor.currentTab][self.unit]
        newList = []
        for i in range(len(listEnter)):
            if listEnter[i] == self.name:
                newList.append('Node(' + startConnection.link.name + ')')
            else:
                newList.append(listVal[2][1][i])

        del editor.listBlocks[editor.currentTab][self.unit]
        editor.listBlocks[editor.currentTab][self.unit] = (listVal[0], listVal[1], (listVal[2][0], newList, listVal[2][2], listVal[2][3]))
        # UpdateUndoRedo()
        return a1

    def addConstantSubMod(self):
        nameClass = editor.listItems[editor.currentTab][self.unit].name
        listEnter = editor.listSubMod[editor.currentTab][self.unit][1][0]
        indx = listEnter.index(self.name)
        val = editor.listSubMod[editor.currentTab][self.unit][1][1][indx]
        if 'enumerate' in self.format:
            for lst in range(len(listEnter)):
                if listEnter[lst] == self.name:
                    self.format = editor.libSubMod[nameClass][1][lst]
            val = self.format[11:self.format.index(',')]

        if 'list' in self.format or 'array' in self.format:
            if 'list_int' in self.format:
                val = (-100, [0, 0], 100)
                f = 2
            elif 'list_float' in self.format:
                val = (-100.0, [0.0, 0.0], 100.0)
                f = 2
            elif 'list_str' in self.format:
                val = ['', '']
                f = 2
            elif 'array_int' in self.format:
                val = (-100, [[0, 0], [0, 0]], 100)
                f = 1
            elif 'array_float' in self.format:
                val = (-100.0, [[0.0, 0.0], [0.0, 0.0]], 100.0)
                f = 1
            elif 'array_str' in self.format:
                val = [['', ''], ['', '']]
                f = 1
            a1 = Clusters('newCluster', 115, 33, val, self.format, self.name, True)
            a1.setPos(self.mapToScene(self.boundingRect().x() - 300, self.boundingRect().y()))
            a1.outputs[0].setPos(2 * a1.w - 10, a1.h / f)
        else:
            a1 = Constants('newConstant', 80, 30, val, self.format, self.name, True)
            a1.setPos(self.mapToScene(self.boundingRect().x() - 100, self.boundingRect().y()))

        # a1 = Constants('newConstant', 80, 30, val, self.format, self.name, True)
        # a1.setPos(self.mapToScene(self.boundingRect().x() - 100, self.boundingRect().y()))
        editor.diagramScene[editor.currentTab].addItem(a1)
        editor.listItems[editor.currentTab][a1.unit] = a1
        if 'enumerate' in self.format:
            self.format = 'enumerate_str'
        startConnection = Connection('',
                                     a1.outputs[0],
                                     self,
                                     self.format)
        startConnection.setEndPos(self.scenePos())
        startConnection.setToPort(self)
        editor.listNodes[editor.currentTab][startConnection.link.name] = a1.unit + ':' + '#Node#' + self.unit + ':' + self.name

        listVal = editor.listSubMod[editor.currentTab][self.unit]
        newList = []
        for i in range(len(listEnter)):
            if listEnter[i] == self.name:
                newList.append('Node(' + startConnection.link.name + ')')
            else:
                newList.append(listVal[1][1][i])

        del editor.listSubMod[editor.currentTab][self.unit]
        editor.listSubMod[editor.currentTab][self.unit] = (listVal[0], (listVal[1][0], newList, listVal[1][2], listVal[1][3]), listVal[2])
        UpdateUndoRedo()
        return a1

    def addConstantStr(self):
        # if 'int' in self.format:
        #     val = 0
        # elif 'float' in self.format:
        #     val = 0.0
        # elif 'str' in self.format:
        #     val = 'your text'
        # elif 'path' in self.format:
        #     val = 'path'
        # elif 'bool' in self.format:
        #     val = True
        # a1 = Constants('newConstant', 80, 30, val, self.format, self.name, True)
        # a1.setPos(self.mapToScene(self.boundingRect().x() - 100, self.boundingRect().y()))

        if 'list' in self.format or 'array' in self.format:
            if 'list_int' in self.format:
                val = (-100, [0, 0], 100)
                f = 2
            elif 'list_float' in self.format:
                val = (-100.0, [0.0, 0.0], 100.0)
                f = 2
            elif 'list_str' in self.format:
                val = ['', '']
                f = 2
            elif 'array_int' in self.format:
                val = (-100, [[0, 0], [0, 0]], 100)
                f = 1
            elif 'array_float' in self.format:
                val = (-100.0, [[0.0, 0.0], [0.0, 0.0]], 100.0)
                f = 1
            elif 'array_str' in self.format:
                val = [['', ''], ['', '']]
                f = 1
            a1 = Clusters('newCluster', 115, 33, val, self.format, self.name, True)
            a1.setPos(self.mapToScene(self.boundingRect().x() - 300, self.boundingRect().y()))
            a1.outputs[0].setPos(2 * a1.w - 10, a1.h / f)
        else:
            if 'int' in self.format:
                val = 0
            elif 'float' in self.format:
                val = 0.0
            elif 'str' in self.format:
                val = 'your text'
            elif 'path' in self.format:
                val = 'path'
            elif 'bool' in self.format:
                val = True
            elif 'tuple' in self.format:
                val = (0,)
            a1 = Constants('newConstant', 80, 30, val, self.format, self.name, True)
            a1.setPos(self.mapToScene(self.boundingRect().x() - 100, self.boundingRect().y()))

        editor.diagramScene[editor.currentTab].addItem(a1)
        editor.listItems[editor.currentTab][a1.unit] = a1

        startConnection = Connection('',
                                     a1.outputs[0],
                                     self,
                                     self.format)
        startConnection.setEndPos(self.scenePos())
        startConnection.setToPort(self)
        editor.listNodes[editor.currentTab][startConnection.link.name] = a1.unit + ':' + '#Node#' + self.unit + ':' + self.name

        UpdateUndoRedo()
        return a1

    def addValueP(self):
        self.addProbe('Value')

    def addTypeP(self):
        self.addProbe('Type')

    def addLengthP(self):
        self.addProbe('Length')

    def addProbe(self, name):
        b1 = Probes('new', self.format, name, True)
        b1.setPos(self.mapToScene(self.boundingRect().x() + 100, self.boundingRect().y()))
        editor.diagramScene[editor.currentTab].addItem(b1)
        editor.listItems[editor.currentTab][b1.unit] = b1
        toPort = b1.inputs[0]
        startConnection = Connection('',
                                     self,
                                     toPort,
                                     self.format)
        startConnection.setEndPos(toPort.scenePos())
        startConnection.setToPort(toPort)
        editor.listNodes[editor.currentTab][startConnection.link.name] = self.unit + ':' + self.name + '#Node#' + b1.unit + ':' + toPort.name

        if 'F' in self.unit and 'in' in self.name:
            curF = editor.listItems[editor.currentTab][self.unit]
            curF.IteminLoop(b1.unit, True, 0)
        elif 'I' in self.unit and 'in' in self.name:
            ind = 0
            curI = editor.listItems[editor.currentTab][self.unit]
            if curI.elemProxy.currentText() == 'False':
                ind = 1
            curI.IteminLoop(b1.unit, True, ind)
        editor.loopMouseMoveEvent(b1, self.scenePos())
        editor.loopMouseReleaseEvent(b1, False)

    def addPrint(self):
        if 'tuple' in self.format:
            name = 'Print_tuple'
        else:
            name = 'Print_' + self.format
            name = name.replace('list_', '')
            name = name.replace('array_', '')
        b1 = ProcessItem('newBlock',
                         name,
                         editor.getlib()[name][0],
                         150, 80,
                         editor.getlib()[name][1]).getBlocks()
        b1.setPos(self.mapToScene(self.boundingRect().x() + 100, self.boundingRect().y()))
        inp = b1.inputs
        for fd in inp:
            if fd.name != 'comment':
                toPort = fd
        editor.diagramScene[editor.currentTab].addItem(b1)
        editor.listItems[editor.currentTab][b1.unit] = b1

        startConnection = Connection('',
                                     self,
                                     toPort,
                                     self.format)
        startConnection.setEndPos(toPort.scenePos())
        startConnection.setToPort(toPort)
        editor.listNodes[editor.currentTab][startConnection.link.name] = self.unit + ':' + self.name + '#Node#' + b1.unit + ':' + toPort.name

        listVal = editor.listBlocks[editor.currentTab][b1.unit]
        listEnter = editor.getlib()[name][1][0]
        newList = []
        for i in range(len(listEnter)):
            if listEnter[i] != 'comment':
                newList.append('Node(' + startConnection.link.name + ')')
            else:
                newList.append(listVal[2][1][i])

        del editor.listBlocks[editor.currentTab][b1.unit]
        editor.listBlocks[editor.currentTab][b1.unit] = (listVal[0], listVal[1], (listVal[2][0], newList, listVal[2][2], listVal[2][3]))
        UpdateUndoRedo()

    def getEnumerateFromYml(self):
        pathBlock = editor.listBlocks[editor.currentTab][self.unit][1].split('.')
        classBlock = editor.listBlocks[editor.currentTab][self.unit][0]
        pathYml = os.path.dirname(os.path.realpath(__file__))
        pathYml = os.path.join(pathYml, '../modules', pathBlock[0], pathBlock[1] + ".yml")
        if os.path.exists(pathYml):
            with open(pathYml, 'r', encoding='utf8') as stream:
                dicts = yaml.load(stream, yaml.FullLoader)
        en = dicts[classBlock][self.name]
        return en


class PreviewBlock(QGraphicsView):

    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)

        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

        self.setEnabled(True)
        self.scalefactor = 1

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            adj = 0.1777
        else:
            adj = -0.1777

        self.scalefactor += adj
        self.scale(1 + adj, 1 + adj)


class Probes(QGraphicsPolygonItem):
    def __init__(self, unit='', format='unkn', label='', isMod=True, parent=None):
        super(Probes, self).__init__(parent)
        self.setCursor(QCursor(ItemMouse.HANDLETOPITEM.value))

        self.label = label
        self.isMod = isMod
        self.format = format
        self.setZValue(2)
        self.preview = False
        self.caseFinal = False
        self.currentLoop = None
        self.moved = False

        if isMod:
            self.setAcceptHoverEvents(True)
            self.setFlags(self.GraphicsItemFlag.ItemIsSelectable | self.GraphicsItemFlag.ItemIsMovable | self.GraphicsItemFlag.ItemIsFocusable | self.GraphicsItemFlag.ItemSendsGeometryChanges)

        if unit == 'new':
            ProbeExist = True
            inc = 0
            while ProbeExist:
                if 'P' + str(inc) in editor.listProbes[editor.currentTab]:
                    inc += 1
                else:
                    ProbeExist = False
            self.unit = 'P' + str(inc)
        else:
            self.unit = unit

        polyhead = QPolygonF([QPointF(0, 8), QPointF(20, 0), QPointF(70, 0),
                              QPointF(70, 26), QPointF(20, 26), QPointF(0, 18)])
        self.setPolygon(polyhead)

        self.setPen(QPen(ItemColor.FRAME_PROBE.value, 3))
        self.setBrush(QBrush(Qt.GlobalColor.darkGray))

        lab = QGraphicsTextItem(self.unit, self)
        lab.setDefaultTextColor(ItemColor.DEFAULTTEXTCOLOR.value)
        lab.setPos(75, 0)

        self.inputs = []
        self.outputs = None
        input = Port(label, 'in', format, self.unit, True, isMod, 10, -15, self)
        input.setPos(0, 13)
        self.inputs.append(input)

        if isMod:
            editor.listProbes[editor.currentTab][self.unit] = (format, label)

    def contextMenuEvent(self, event):
        if not self.isSelected():
            return
        if self.isMod:
            menu = QMenu()
            de = menu.addAction('Delete')
            de.triggered.connect(self.deleteItem)
            menu.exec(event.screenPos())

    def itemChange(self, *args, **kwargs):
        gridSize = ItemGrid.SPACEGRID.value
        if args[0] == self.GraphicsItemChange.ItemPositionHasChanged:
            xV = round(args[1].x() / gridSize) * gridSize
            yV = round(args[1].y() / gridSize) * gridSize
            self.setPos(QPointF(xV, yV))
        return QGraphicsRectItem.itemChange(self, *args, **kwargs)

    def mouseMoveEvent(self, mouseEvent):
        mouseEvent.accept()
        editor.loopMouseMoveEvent(self, mouseEvent.scenePos())
        return QGraphicsPolygonItem.mouseMoveEvent(self, mouseEvent)

    def mouseReleaseEvent(self, event):
        editor.loopMouseReleaseEvent(self, True)
        return QGraphicsPolygonItem.mouseReleaseEvent(self, event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            self.setPos(self.x(), self.y() - 1)
        if event.key() == Qt.Key.Key_Down:
            self.setPos(self.x(), self.y() + 1)
        if event.key() == Qt.Key.Key_Left:
            self.setPos(self.x() - 1, self.y())
        if event.key() == Qt.Key.Key_Right:
            self.setPos(self.x() + 1, self.y())

    def deleteItem(self):
        for elem in editor.diagramView[editor.currentTab].items():
            if type(elem) is LinkItem:
                if editor.listNodes[editor.currentTab][elem.name].find(self.unit + ':') != -1:
                    BlockCreate.deletelink(self, elem, self.unit)
        editor.diagramScene[editor.currentTab].removeItem(self)
        del editor.listProbes[editor.currentTab][self.unit]
        del editor.listItems[editor.currentTab][self.unit]
        editor.deleteItemsLoop(self)


class ProcessItem():

    def __init__(self, unit='newBlock', name='Untitled', category='untitled', w=150, h=80, *inout, parent=None):

        self.category = category
        self.name = name
        self.unit = unit

        if unit in 'newBlock':
            BlockExist = True
            inc = 0
            while BlockExist:
                if 'U' + str(inc) in editor.listBlocks[editor.currentTab]:
                    inc += 1
                else:
                    BlockExist = False
            self.unit = 'U' + str(inc)
        else:
            self.unit = unit

        listVal = inout[0]

        cat = category.split('.')
        listEnter = editor.getlib()[self.name][1][0]
        listValDefault = editor.getlib()[self.name][1][1]
        if not listValDefault:
            listValDefault = ()
        if len(listEnter) != len(listVal[0]):
            if '_dyn' in self.name:
                listVal = inout[0][1]
                tmpList = []
                for indDef in listValDefault:
                    tmpList.append(indDef)
                for i in range(len(listValDefault), len(listVal)):
                    tmpList.append(tmpList[-1])
                listValDefault = tmpList
            else:
                pathYml = os.path.dirname(os.path.realpath(__file__))
                pathYml = os.path.join(pathYml, '../modules', cat[0], cat[1] + ".yml")
                if os.path.exists(pathYml):
                    with open(pathYml, 'r', encoding='utf8') as stream:
                        dicts = yaml.load(stream, yaml.FullLoader)
                        for el in dicts[name]:
                            if el in listVal[0]:
                                listEnter = (*listEnter, el)
                                istuple = False
                                try:
                                    if type(eval(dicts[name][el])).__name__ == 'tuple':
                                        listValDefault = (*listValDefault, eval(dicts[name][el]))
                                        istuple = True
                                except Exception as err:
                                    istuple = False
                                if not istuple:
                                    if type(dicts[name][el]).__name__ == 'str':
                                        if 'enumerate' in dicts[name][el]:
                                            listValDefault = (*listValDefault, dicts[name][el])
                                        else:
                                            try:
                                                listValDefault = (*listValDefault, str(eval(dicts[name][el])))
                                            except Exception as e:
                                                listValDefault = (*listValDefault, str(dicts[name][el]))
                                    else:
                                        try:
                                            listValDefault = (*listValDefault, eval(dicts[name][el]))
                                        except Exception as e:
                                            listValDefault = (*listValDefault, dicts[name][el])

        ###############################################################################
        newVal = []
        if inout[0][1]:
            for it in inout[0][1]:
                if type(it).__name__ == 'str':
                    if 'enumerate' in it:
                        newVal.append(list(eval(it))[0][1])
                    else:
                        newVal.append(it)
                else:
                    newVal.append(it)
        ###############################################################################
        self.block = BlockCreate(self.name, self.unit, self.category, w, h, listValDefault, True, *inout)
        editor.listBlocks[editor.currentTab][self.unit] = (name, category, (inout[0][0], newVal, inout[0][2], inout[0][3]))
        ###############################################################################

    def getBlocks(self):
        return self.block


class ProgressBar(QProgressBar):

    def __init__(self, *args, **kwargs):
        super(ProgressBar, self).__init__(*args, **kwargs)
        self.setValue(0)
        if self.minimum() != self.maximum():
            self.timer = QTimer(self, timeout=self.onTimeout)
            self.timer.start(randint(1, 3) * 1000)

    def onTimeout(self):
        if self.value() >= 100:
            self.timer.stop()
            self.timer.deleteLater()
            del self.timer
            return
        self.setValue(self.value() + 1)


class ProgressImage(QProgressBar):

    def __init__(self, *args, **kwargs):
        super(ProgressImage, self).__init__(*args, **kwargs)
        self.setStyleSheet('''
                           #BlueProgressBar::chunk {
                           background-color: #2196F3;
                           width: 10px;
                           margin: 0.5px;}
                           ''')
        self.setValue(0)
        QApplication.processEvents()

        if self.minimum() != self.maximum():
            self.timer = QTimer(self, timeout=self.onTimeout)
            self.timer.start(randint(1, 3) * 1000)

    def onTimeout(self):
        if self.value() >= 100:
            self.timer.stop()
            self.timer.deleteLater()
            del self.timer
            return
        self.setValue(self.value() + 1)


class ProgressTasks(QWidget):

    def __init__(self, wind, parent=None):
        super(ProgressTasks, self).__init__(wind)
        screen_center = editor.size()
        self.setWindowTitle('Progress process')
        self.setStyleSheet("background-color:white;")
        self.resize(400, 80)
        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.label = QLabel()
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(-100, 0, 350, 30)
        self.pbar.setValue(0)
        self.button_stop = QPushButton('Stop')
        self.button_stop.setCheckable(True)
        self.button_stop.clicked.connect(self.buttonStop)
        # self.args += (self.button_stop,)
        # self.button_stop.clicked.connect(self.runner.kill)
        vbx = QVBoxLayout()
        hbx = QHBoxLayout()
        hbx.addWidget(self.pbar)
        hbx.addWidget(self.button_stop)
        vbx.addWidget(self.label)
        vbx.addLayout(hbx)
        self.setLayout(vbx)
        self.move(int(screen_center.width() / 2), int(screen_center.height() / 2))
        self.show()
        time.sleep(0.1)

    def buttonStop(self):
        self.close()


class SaveDiagram(QTextEdit):

    def __init__(self, parent=None):
        super(SaveDiagram, self).__init__(parent)
        listCodeScript = {}

        self.append('[diagram]')
        for item in editor.diagramView[editor.currentTab].items():
            try:
                coord = item.pos()
            except Exception as e:
                coord = item.sceneBoundingRect()

            args, vals = [], []

            if type(item) is BlockCreate:
                if item.category:
                    rect = item.rect()
                    args = ["block", "category", "class", "valInputs", "RectF"]
                    vals = [item.unit, item.category,
                            item.name, str(editor.listBlocks[editor.currentTab][item.unit][2]),
                            str((coord.x(), coord.y(), rect.width(), rect.height()))]
                else:
                    rect = item.rect()
                    args = ["submod", "nameMod", "catMod", "valInputs", "RectF"]
                    vals = [item.unit, item.name, str(editor.listSubMod[editor.currentTab][item.unit][2]),
                            str(editor.listSubMod[editor.currentTab][item.unit][1]),
                            str((coord.x(), coord.y(), rect.width(), rect.height()))]

            elif type(item) is LinkItem:
                try:
                    self.append('link=[' + item.name + '] node=[' +
                                editor.listNodes[editor.currentTab][item.name] + ']')
                except Exception as err:
                    pass

            elif type(item) is ConnectorItem:
                if 'in' in item.inout:
                    args = ["connt", "name", "type", "format", "valOut", "RectF"]
                    vals = [str(item.connct), str(editor.listConnects[editor.currentTab][item.connct][1]),
                            str(item.inout), str(editor.listConnects[editor.currentTab][item.connct][2]),
                            str(editor.listConnects[editor.currentTab][item.connct][3]),
                            str((coord.x(), coord.y(), 70, 24))]
                else:
                    args = ["connt", "name", "type", "format", "RectF"]
                    vals = [str(item.connct), str(editor.listConnects[editor.currentTab][item.connct][1]),
                            str(item.inout), str(editor.listConnects[editor.currentTab][item.connct][2]),
                            str((coord.x(), coord.y(), 70, 24))]

            elif type(item) is Probes:
                args = ["probe", "label", "format", "RectF"]
                vals = [str(item.unit), str(editor.listProbes[editor.currentTab][item.unit][1]),
                        str(editor.listProbes[editor.currentTab][item.unit][0]),
                        str((coord.x(), coord.y(), 70, 24))]

            elif type(item) is CommentsItem:
                rect = item.rect()
                comm = item.label.toPlainText()
                args = ["comments", "RectF", "text"]
                vals = ["", str((coord.x(), coord.y(), rect.width(), rect.height())), repr(comm)]

            elif type(item) is ForLoopItem:
                rect = item.rect()
                if 'F' in item.unit:
                    try:
                        args = ["loopFor", "inputs", "outputs", "listItems", "RectF"]
                        vals = [str(item.unit), str(editor.libTools[editor.currentTab][item.unit][0]),
                                str(editor.libTools[editor.currentTab][item.unit][1]),
                                str(editor.listTools[editor.currentTab][item.unit]),
                                str((coord.x(), coord.y(), rect.width(), rect.height()))]
                    except Exception as e:
                        pass
                else:
                    try:
                        args = ["loopIf", "inputs", "outputs", "listItems", "RectF"]
                        vals = [str(item.unit), str(editor.libTools[editor.currentTab][item.unit][0]),
                                str(editor.libTools[editor.currentTab][item.unit][1]),
                                str(editor.listTools[editor.currentTab][item.unit]),
                                str((coord.x(), coord.y(), rect.width(), rect.height()))]
                    except Exception as e:
                        pass

            elif type(item) in [Constants, Checkbox, Imagebox]:
                rect = item.rect()
                if type(item.elemProxy) is Constants_Combo:
                    value = repr(item.elemProxy.currentText())
                elif type(item.elemProxy) in [Constants_text]:
                    if item.format == "list_path":
                        value = item.elemProxy.toPlainText()
                        value = value.split('\n')
                    else:
                        value = repr(item.elemProxy.toPlainText())
                elif type(item.elemProxy) in [Constants_tuple]:
                    try:
                        value = eval(item.elemProxy.toPlainText())
                    except Exception as err:
                        value = item.elemProxy.toPlainText()
                elif type(item.elemProxy) in [Constants_float, Constants_int]:
                    value = (item.elemProxy.minimum(),
                             item.elemProxy.value(),
                             item.elemProxy.maximum())
                elif type(item.elemProxy) is QWidget:
                    value = item.listItemsBox
                elif type(item.elemProxy) is QLabel:
                    value = item.pathImage
                args = ["constant", "value", "format", "label", "RectF"]
                if item.form == bool:
                    if value == 'True':
                        newvalue = True
                    else:
                        newvalue = False
                else:
                    newvalue = str(value)
                vals = [str(item.unit), newvalue, str(item.form), str(item.label),
                        str((coord.x(), coord.y(), rect.width(), rect.height()))]
            elif type(item) is Clusters:
                rect = item.rect()
                if item.format == 'str':
                    value = repr(item.val)
                else:
                    value = item.val
                args = ["cluster", "value", "format", "label", "RectF"]
                vals = [str(item.unit), str(value), str(item.format), str(item.label),
                        str((coord.x(), coord.y(), rect.width(), rect.height()))]
            elif type(item) is ScriptItem:
                listCodeScript[item.unit] = item.elemProxy.toPlainText()
                rect = item.rect()
                self.append('script=[' +
                            str(item.unit) +
                            '] title=[' + item.name +
                            '] inputs=' + str(editor.libTools
                                              [editor.currentTab]
                                              [item.unit][0]) +
                            ' outputs=' + str(editor.libTools
                                              [editor.currentTab]
                                              [item.unit][1]) +
                            ' code=[' + "your code" + '] RectF=[' +
                            str((coord.x(),
                                 coord.y(),
                                 rect.width(),
                                 rect.height())) +
                            ']')
            elif type(item) is StopExecution:
                # rect = item.rect()
                args = ["stopexec", "RectF"]
                vals = [item.unit, str((coord.x(), coord.y(), 80, 80))]

            if args:
                self.append(SetValueInBrackets(args, vals).getNewLine())

        if listCodeScript:
            for line in LoadCodeScript().writeListScript().split('\n'):
                self.append(line)


class ScriptItem(QGraphicsRectItem):

    def __init__(self, unit, name, w, h, isMod, loading, *inout, parent=None):
        super(ScriptItem, self).__init__(None)
        self.setCursor(QCursor(ItemMouse.HANDLETOPITEM.value))
        self.normalState()
        self.changed = False
        if not loading:
            self.loading = False
        else:
            self.loading = loading
        # self.setFlags(self.GraphicsItemFlag.ItemIsSelectable | self.GraphicsItemFlag.ItemIsMovable | self.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setZValue(-1)
        self.unit = unit
        self.w, self.h = w, h
        self.wmin, self.hmin = 80.0, 0.0
        self.nbin, self.nbout = 0, 0
        self.moved = False
        self.isMod = isMod
        self.preview = False
        self.loopIf = False
        self.name = name
        if not inout:
            inout = [[], []]
        self.inout = inout

        self.setAcceptHoverEvents(True)

        self.caseFinal = False
        self.currentLoop = None

        if unit == 'newScript':
            ScriptExist = True
            inc = 0
            while ScriptExist:
                if 'S' + str(inc) in editor.listTools[editor.currentTab]:
                    inc += 1
                else:
                    ScriptExist = False
            self.unit = 'S' + str(inc)
        elif unit == 'newMacro':
            ScriptExist = True
            inc = 0
            while ScriptExist:
                if 'J' + str(inc) in editor.listTools[editor.currentTab]:
                    inc += 1
                else:
                    ScriptExist = False
            self.unit = 'J' + str(inc)
        else:
            self.unit = unit

        self.inputs, self.outputs = [], []
        if self.isMod:
            editor.listTools[editor.currentTab][self.unit] = []
            editor.libTools[editor.currentTab][self.unit] = [[], []]
            if inout:
                editor.libTools[editor.currentTab][self.unit] = inout
                for i in range(0, len(inout[0])):
                    self.updateInput(inout[0][i])
                for i in range(0, len(inout[1])):
                    self.updateOutput(inout[1][i])

        factorh = 20
        self.hmin = factorh * len(self.inputs)
        if self.hmin < factorh * len(self.outputs):
            self.hmin = factorh * len(self.outputs)

        self.label = QGraphicsTextItem(name, self)
        self.label.setFont(QFont('Arial', 8))
        self.label.setDefaultTextColor(ItemColor.TEXT_LOOP.value)

        self.nameUnit = QGraphicsTextItem(self.unit, self)
        self.nameUnit.setDefaultTextColor(ItemColor.DEFAULTTEXTCOLOR.value)

        class TextEditPy(QTextEdit):

            # def __init__(self):
            #     super(TextEditPy, self).__init__(parent)
            #     self.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

            def keyPressEvent(self, event):
                if event.key() == (Qt.Key.Key_Tab):
                    self.insertPlainText(' ' * 4)
                    return
                super(TextEditPy, self).keyPressEvent(event)

        if self.isMod:
            self.setFlags(self.GraphicsItemFlag.ItemIsSelectable | self.GraphicsItemFlag.ItemIsMovable | self.GraphicsItemFlag.ItemIsFocusable | self.GraphicsItemFlag.ItemSendsGeometryChanges)
        # self.elemProxy = QTextEdit()
        self.elemProxy = TextEditPy()
        self.elemProxy.mouseReleaseEvent = self.deselect
        self.elemProxy.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.elemProxy.installEventFilter(editor)
        if 'S' in self.unit:
            PythonHighlighter(self.elemProxy)
        self.elemProxy.textChanged.connect(self.text_changed)
        self.proxyWidget = QGraphicsProxyWidget(self, Qt.WindowType.Widget)
        self.proxyWidget.setWidget(self.elemProxy)
        self.proxyWidget.setPos(5, 5)

        x, y = self.newSize(self.w, self.h)

        if self.isMod:
            self.resize = Slide(self)
            self.resize.setPos(x, y)
            self.resize.posChangeCallbacks.append(self.newSize)  # Connect the callback
            self.resize.setFlag(self.resize.GraphicsItemFlag.ItemIsSelectable, True)
            self.resize.wmin = self.wmin
            self.resize.hmin = self.hmin

    def text_changed(self):
        if not self.loading:
            self.changed = True
        self.loading = False

    def deselect(self, event):
        editor.diagramScene[editor.currentTab].clearSelection()
        self.elemProxy.setEnabled(True)
        # editor.listItemStored.clear()
        # del editor.listCommentsStored[:]

    def normalState(self):
        self.setPen(QPen(ItemColor.FRAME_LOOP_NORMAL.value, 8))

    def activeState(self):
        self.setPen(QPen(ItemColor.FRAME_LOOP_ACTIVED.value, 8))

    def hoverLeaveEvent(self, event):
        if self.changed:
            UpdateUndoRedo()
        self.changed = False
        # return QGraphicsRectItem.hoverLeaveEvent(self, *args, **kwargs)

    def itemChange(self, *args, **kwargs):
        gridSize = ItemGrid.SPACEGRID.value
        if args[0] == self.GraphicsItemChange.ItemPositionHasChanged:
            xV = round(args[1].x() / gridSize) * gridSize
            yV = round(args[1].y() / gridSize) * gridSize
            self.setPos(QPointF(xV, yV))
        return QGraphicsRectItem.itemChange(self, *args, **kwargs)

    def keyPressEvent(self, keyEvent):
        if keyEvent.key() == Qt.Key.Key_Up:
            self.setPos(self.x(), self.y() - 1)
        if keyEvent.key() == Qt.Key.Key_Down:
            self.setPos(self.x(), self.y() + 1)
        if keyEvent.key() == Qt.Key.Key_Left:
            self.setPos(self.x() - 1, self.y())
        if keyEvent.key() == Qt.Key.Key_Right:
            self.setPos(self.x() + 1, self.y())
        return QGraphicsRectItem.keyPressEvent(self, keyEvent)

    def mousePressEvent(self, event):
        if self.isMod:
            if event.button() == Qt.MouseButton.LeftButton:
                # editor.diagramScene[editor.currentTab].clearSelection()
                self.setSelected(True)

            if event.button() == Qt.MouseButton.RightButton:
                self.setSelected(True)

            # UpdateUndoRedo()
        return QGraphicsRectItem.mousePressEvent(self, event)

    def mouseMoveEvent(self, mouseEvent):
        mouseEvent.accept()
        editor.loopMouseMoveEvent(self, mouseEvent.scenePos())
        return QGraphicsRectItem.mouseMoveEvent(self, mouseEvent)

    def mouseReleaseEvent(self, event):
        editor.loopMouseReleaseEvent(self, True)
        return QGraphicsRectItem.mouseReleaseEvent(self, event)

#     def hoverEnterEvent(self, event):
#         self.setSelected(True)
#         return QGraphicsRectItem.hoverEnterEvent(self, event)
#
#     def hoverLeaveEvent(self, event):
#         self.setSelected(False)
#         return QGraphicsRectItem.hoverLeaveEvent(self, event)

    def newSize(self, w, h):
        # Limit the block size:
        if h < self.hmin:
            h = self.hmin
        if h < 10:
            h = 10
        if w < self.wmin or w < 10:
            w = self.wmin
        if w < 10:
            w = 10

        w, h = int(w), int(h)
        self.setRect(0.0, 0.0, w, h)
        self.elemProxy.setMinimumSize(w - 10, h - 10)
        self.elemProxy.setMaximumSize(w - 10, h - 10)
        self.elemProxy.resize(w - 10, h - 10)
        self.label.setPos(0, -40)
        if self.nbin > 0:
            y = (h) / (self.nbin + 1)
            dy = (h) / (self.nbin + 1)
            for inp in range(len(self.inputs)):
                self.inputs[inp].setPos(-9, y)
                y += dy
        if self.nbout > 0:
            y = (h) / (self.nbout + 1)
            dy = (h) / (self.nbout + 1)
            for outp in range(len(self.outputs)):
                self.outputs[outp].setPos(w + 11, y)
                y += dy
        rect = self.nameUnit.boundingRect()
        lw, lh = rect.width(), rect.height()
        lx = (w - lw) / 2
        ly = (h)
        self.nameUnit.setPos(lx, ly)
        self.w = w
        self.h = h
        return w, h

    def updateSize(self):
        factorh = 20
        hmin = factorh * len(self.inputs)
#         w = self.boundingRect().width()
#         h = self.boundingRect().height()
        w = self.w
        h = self.h

        self.hmin = hmin

        if h < hmin:
            h = hmin
        hmin = factorh * len(self.outputs)

        if self.hmin < hmin:
            self.hmin = hmin
        if h < hmin:
            h = hmin
        if w < 100:
            w = 100

        x, y = self.newSize(w, h)
        return x, y

    def contextMenuEvent(self, event):
        if event.isAccepted:
            pass
        if self.isMod:
            menu = QMenu()
            intu = menu.addAction('Add input')
            intu.triggered.connect(self.add_InputManual)
            outtu = menu.addAction('Add output')
            outtu.triggered.connect(self.add_OutputManual)
            if 'J' in self.unit:
                outtu.setEnabled(False)
            de = menu.addAction('Delete')
            de.triggered.connect(self.deleteItem)
            ct = menu.addAction('Change title')
            ct.triggered.connect(self.changeTitle)
            menu.exec(event.screenPos())
#             event.accept()
#             return QGraphicsRectItem.contextMenuEvent(self, event)

    def deleteItem(self):
        editor.diagramScene[editor.currentTab].removeItem(self)
        for elem in editor.diagramView[editor.currentTab].items():
            if type(elem) is LinkItem:
                if editor.listNodes[editor.currentTab][elem.name].find(self.unit + ':') != -1:
                    BlockCreate.deletelink(self, elem, self.unit)
        del editor.listTools[editor.currentTab][self.unit]
        del editor.libTools[editor.currentTab][self.unit]
        del editor.listItems[editor.currentTab][self.unit]
        editor.deleteItemsLoop(self)
#         UpdateUndoRedo()

    def changeTitle(self):
        c = changeTitle(self.name, self.nameUnit.toPlainText())
        c.exec()
        if c.getNewValues():
            self.name = c.getNewValues()
            self.label.setPlainText(c.getNewValues())

    def add_InputManual(self):
        c = define_inputs_outputs(self.unit, 'input', self.inputs, '')
        c.exec()

        if c.getNewValues():
            self.add_Input(c.getNewValues()[0], c.getNewValues()[1])

    def add_Input(self, varname, format):
        self.nbin += 1
        portIn = Port(varname, 'in', format, self.unit, True, True, -18, -25, self)
        portIn.label.setPos(5 - portIn.label.boundingRect().width(), -28)
        self.inputs.append(portIn)
        x, y = self.updateSize()

        listEnter = editor.libTools[editor.currentTab][self.unit][0]
        listOut = editor.libTools[editor.currentTab][self.unit][1]
        if listEnter:
            listEnter.append([portIn.name, portIn.typeio, portIn.format])
        else:
            listEnter = [[portIn.name, portIn.typeio, portIn.format]]

        editor.libTools[editor.currentTab][self.unit] = [listEnter, listOut]
        self.inout = [listEnter, listOut]
        UpdateUndoRedo()

    def add_OutputManual(self):
        c = define_inputs_outputs(self.unit, 'output', self.outputs, '')
        c.exec()

        if c.getNewValues():
            self.add_Output(c.getNewValues()[0], c.getNewValues()[1])

    def add_Output(self, varname, format):
        self.nbout += 1
        portOut = Port(varname, 'out', format, self.unit, True, True, -24, -25, self)
        portOut.label.setPos(-8, -28)
        self.outputs.append(portOut)
        x, y = self.updateSize()

        listEnter = editor.libTools[editor.currentTab][self.unit][0]
        listOut = editor.libTools[editor.currentTab][self.unit][1]

        if listOut:
            listOut.append([portOut.name, portOut.typeio, portOut.format])
        else:
            listOut = [[portOut.name, portOut.typeio, portOut.format]]

        editor.libTools[editor.currentTab][self.unit] = [listEnter, listOut]
        self.inout = [listEnter, listOut]
        UpdateUndoRedo()

    def updateInput(self, inp):
        self.nbin += 1
        portIn = Port(inp[0], 'in', inp[2], self.unit, True, True, -18, -25, self)
        portIn.label.setPos(5 - portIn.label.boundingRect().width(), -28)
        self.inputs.append(portIn)

    def updateOutput(self, outp):
        self.nbout += 1
        portOut = Port(outp[0], 'out', outp[2], self.unit, True, True, -24, -25, self)
        portOut.label.setPos(-8, -28)
        self.outputs.append(portOut)

    def deletePort(self, name, typeio):

        for elem in editor.diagramView[editor.currentTab].items():
            if type(elem) is Port:
                if elem.name == name and elem.unit == self.unit and elem.typeio == typeio:
                    editor.diagramScene[editor.currentTab].removeItem(elem)
                    if elem.typeio == 'in':
                        self.inputs.remove(elem)
                    else:
                        self.outputs.remove(elem)
            if type(elem) is LinkItem:
                a = editor.listNodes[editor.currentTab][elem.name]
                if typeio == 'in':
                    b = a[a.index("#Node#") + 6:]
                else:
                    b = a[0:a.index("#Node#")]
                if (self.unit + ':' + name) == b:
                    BlockCreate.deletelink(self, elem, self.unit)

        x, y = self.updateSize()

        listEnter = editor.libTools[editor.currentTab][self.unit][0]
        listOut = editor.libTools[editor.currentTab][self.unit][1]

        if 'in' in typeio:
            self.nbin -= 1
            try:
                c = 0
                for le in listEnter:
                    if le[0] == name:
                        del listEnter[c]
                        break
                    c += 1
            except Exception as e:
                pass
        elif 'out' in typeio:
            self.nbout -= 1
            try:
                c = 0
                for lo in listOut:
                    if lo[0] == name:
                        del listOut[c]
                        break
                    c += 1
            except Exception as e:
                pass

        del editor.libTools[editor.currentTab][self.unit]
        editor.libTools[editor.currentTab][self.unit] = [listEnter, listOut]
        # editor.listItems[editor.currentTab][self.unit] = self
        UpdateUndoRedo()


class scrollTools(QScrollArea):
    def __init__(self, treeview, parent=None):
        super(scrollTools, self).__init__(parent)
        # self.treeview = treeview
        self.setWidgetResizable(True)
        self.setWidget(treeview)


class searchInitialValueBlock:
    def __init__(self, className, inputName):
        inout = editor.getlib()[className]
        listEnter = inout[1][0]
        listValDefault = inout[1][1]
        self.val = ''
        if inputName in listEnter:
            self.val = listValDefault[listEnter.index(inputName)]
        else:
            if '_dyn' in className:
                self.val = listValDefault[-1]
            else:
                category = inout[0]
                cat = category.split('.')
                pathYml = os.path.dirname(os.path.realpath(__file__))
                pathYml = os.path.join(pathYml, '../modules', cat[0], cat[1] + ".yml")
                if os.path.exists(pathYml):
                    with open(pathYml, 'r', encoding='utf8') as stream:
                        dicts = yaml.load(stream, yaml.FullLoader)
                        self.val = dicts[className][inputName]

    def getValue(self):
        return self.val


class searchInitialValueSubMod:
    def __init__(self, className, inputName):
        inout = editor.libSubMod[className]
        listEnter = inout[0]
        listValDefault = inout[1]
        self.val = listValDefault[listEnter.index(inputName)]

    def getValue(self):
        return self.val


# class selectionArea(QGraphicsRectItem):
#     def __init__(self, parent=None):
#         super(selectionArea, self).__init__(parent)
#         # self.setPen(QPen(ItemColor.BACKGROUND.value, 2, Qt.PenStyle.DashLine))
#         # self.setFlags(self.GraphicsItemFlag.ItemIsSelectable | self.GraphicsItemFlag.ItemIsMovable | self.GraphicsItemFlag.ItemSendsGeometryChanges)
#         # self.setRect(0.0, 0.0, 500, 500)
#         self.updateDimension()
#
#     def updateDimension(self):
#         for lstItems in editor.diagramScene[editor.currentTab].selectedItems():
#             if type(lstItems) not in [Slide]:
#                 print(lstItems)


class SharedMemoryManager():

    def __init__(self, empt):
        self.file_shm = os.path.join(os.path.expanduser('~'), '.skrypy', 'list_shm.yml')
        if empt:
            box = QMessageBox().question(editor,
                                         "Shared Memory",
                                         "Clear shared memory ?    ",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if box == QMessageBox.StandardButton.Yes:
                self.toempty()
        else:
            self.readList()

    def readList(self):
        editor.shm.clear()
        data = {}
        if os.path.exists(self.file_shm):
            with open(self.file_shm, 'r') as file_yml:
                try:
                    data = yaml.load(file_yml, Loader=yaml.SafeLoader)
                except Exception as err:
                    print('error reading shared memory:', err)
                    os.remove(self.file_shm)
                    return
            if bool(data):
                for ek, ev in data.items():
                    editor.shm.append("<span style=\" \
                                       font-family:'Monospace'; \
                                       font-size:10pt; \
                                       font-weight:400; \
                                       color:orange;\"> \
                                       {} = {} </span><br>".format(ek, ev))
            else:
                os.remove(self.file_shm)

    def toempty(self):
        editor.shm.clear()
        if os.path.exists(self.file_shm):
            os.remove(self.file_shm)


class ShowLegend:

    def __init__(self):

        pos1X, pos1Y, pos2X, pos2Y = 0, 0, 60, 0
        labColum = 'simple            list              array'
        textColumn = QGraphicsTextItem(labColum, parent=None)
        textColumn.setDefaultTextColor(ItemColor.DEFAULTTEXTCOLOR.value)
        textColumn.setFont(QFont("Times", 12, QFont.Weight.Bold))
        textColumn.setPos(pos1X, pos1Y - 40)
        editor.legendScene.addItem(textColumn)

        for types in TypeColor:
            if types != TypeColor.unkn:
                color = types.value
                for i in [2, 5, 8]:
                    if not (i > 2 and types.name in ['dict', 'tuple']):
                        line = QGraphicsPathItem()
                        bisLine = QGraphicsPathItem()
                        link = QGraphicsPolygonItem()

                        line.setPen(QPen(color, i))
                        link.setPen(QPen(color, 2))
                        link.setBrush(color)
                        off = 6
                        posPolygon = QPolygonF(
                            [QPointF(-off + (pos2X + pos1X) / 2, -off + pos1Y),
                             QPointF((pos2X + pos1X) / 2, pos1Y),
                             QPointF(-off + (pos2X + pos1X) / 2, off + pos1Y)])
                        link.setPolygon(posPolygon)

                        if i == 8:
                            bisLine.setPen(QPen(ItemColor.BIS_LINK.value,
                                                3,
                                                Qt.PenStyle.SolidLine))
                        else:
                            bisLine.setPen(QPen(Qt.PenStyle.NoPen))

                        path = QPainterPath()
                        start_x, start_y = pos1X, pos1Y
                        end_x, end_y = pos2X, pos2Y
                        ctrl1_x = pos1X + (pos2X - pos1X) * 0.5
                        ctrl1_y = pos1Y
                        ctrl2_x = pos2X + (pos1X - pos2X) * 0.5
                        ctrl2_y = pos2Y
                        path.moveTo(start_x, start_y)
                        path.cubicTo(ctrl1_x,
                                     ctrl1_y,
                                     ctrl2_x,
                                     ctrl2_y,
                                     end_x,
                                     end_y)

                        line.setPath(path)
                        bisLine.setPath(path)

                        editor.legendScene.addItem(link)
                        editor.legendScene.addItem(line)
                        editor.legendScene.addItem(bisLine)

                    pos1X = pos1X + 80
                    pos2X = pos1X + 60

                if types.name != 'float':
                    txtLab = types.name
                else:
                    txtLab = types.name + ', ndarray or tensor'

                textRow = QGraphicsTextItem(txtLab, parent=None)
                textRow.setDefaultTextColor(QColor(color))
                textRow.setFont(QFont("Times", 12, QFont.Weight.Bold))
                textRow.setPos(pos1X, pos1Y - 15)

                editor.legendScene.addItem(textRow)

                pos1X, pos1Y = 0, pos1Y + 20
                pos2X, pos2Y = 60, pos1Y

        editor.legendDiagram.setEnabled(True)
        editor.legendDiagram.setInteractive(False)


class Slide(QGraphicsPolygonItem):

    def __init__(self, parent=None):
        super(Slide, self).__init__(QPolygonF([QPointF(-12, -2), QPointF(-2, -2), QPointF(-2, -12)]), parent)
        self.posChangeCallbacks = []
        self.setBrush(QBrush(Qt.GlobalColor.green))
        self.setFlag(self.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(self.GraphicsItemFlag.ItemSendsScenePositionChanges, True)
        self.setCursor(QCursor(ItemMouse.DIAGCURSOR.value))
        self.effectiveOpacity()
        self.setOpacity(0.6)
        self.ongrid = False

        self.wmin, self.hmin = 0.0, 0.0

    def itemChange(self, change, value):
        if change == self.GraphicsItemChange.ItemPositionChange:
            self.x, self.y = value.x(), value.y()
            if abs(self.x) < self.wmin:
                self.x = self.wmin
            if abs(self.y) < self.hmin:
                self.y = self.hmin

            for cb in self.posChangeCallbacks:
                res = cb(self.x, self.y)
                if res:
                    self.x, self.y = res
                    if self.x < self.wmin:
                        self.x = self.wmin
                    if self.y < self.hmin:
                        self.y = self.hmin
                    if self.ongrid:
                        gridSize = ItemGrid.SPACEGRID.value
                        self.x, self.y = round(self.x / gridSize) * gridSize, round(self.y / gridSize) * gridSize
                    value = QPointF(self.x, self.y)
            return value
        return super(Slide, self).itemChange(change, value)

    def mouseReleaseEvent(self, mouseEvent):
        self.setSelected(False)
        self.setPos(self.x, self.y)
        UpdateUndoRedo()
        return QGraphicsPolygonItem.mouseReleaseEvent(self, mouseEvent)


class ssh_diagram_execution():

    def __init__(self, source, mode, cluster):
        editor.console.clear()
        self.source = source
        self.mode = mode
        self.cluster = cluster
        if not cluster:
            c = servers_window('exec', None)
            c.exec()
        else:
            c = servers_window('exec', cluster)

        if c.get_params():
            self.execution_ssh(c.get_params())

    class passwd_dialog():
        def __init__(self, host_name):
            current_dir_path = os.path.abspath(os.path.join(__file__, "../.."))
            source_disp = os.path.join(current_dir_path, 'api', 'dialog_pwd.py')
            p = subprocess.run([sys.executable, source_disp, host_name], shell=False, check=False, capture_output=True, text=True)
            self.pwd = p.stdout.strip()

        def passwd(self: 'str'):
            return self.pwd

    def execution_ssh(self, param_ssh):
        # host_password = self.passwd_dialog(param_ssh[0]).passwd()
        # if host_password == 'None':
        #     return

        col = '\x1b[38;2;0;100;255m'

        diagram = []
        host_name = param_ssh[0]
        host_skrypy_path = param_ssh[1]
        host_path = param_ssh[2]
        n_cpu = int(param_ssh[3])
        opx = param_ssh[4]
        if opx:
            opx = '-X'
        else:
            opx = ''
        pre_exec = param_ssh[5]
        host_password = param_ssh[6]
        if not host_password:
            host_password = self.passwd_dialog(param_ssh[0]).passwd()
            if host_password == 'None':
                return
        if not self.cluster:
            self.cluster = param_ssh[7]

        host = host_name
        hnm = host.split()

        cmd_base = ['sshpass', '-p', host_password, 'ssh']
        if len(hnm) == 2:
            cmd_base.extend(['-o', 'ProxyCommand={}'.format('sshpass -p {} ssh -W %h:%p {}'.format(host_password, hnm[0].strip())), hnm[1]])
        else:
            cmd_base.append(host)

        # check if cluster can be connected
        proc = subprocess.Popen(cmd_base, stdout=subprocess.PIPE, shell=False)
        timer = Timer(2, proc.kill)
        col = '\x1b[38;2;255;0;0m'
        try:
            timer.start()
            stdout, stderr = proc.communicate()
            if not stdout.decode('UTF-8'):
                print('{}Connection problem with {}\x1b[0m'.format(col, host_name))
                return
        except Exception as err:
            print('{}Connection problem with {}\x1b[0m'.format(col, host_name))
            return
        finally:
            timer.cancel()

        # search conda source in the cluster
        # if 'conda' in pre_exec:
        #     conda_path = self.searchSourceConda(host_name, host_password)
        #     if conda_path:
        #         pre_exec = 'source {}\n'.format(conda_path) + pre_exec
        #     else:
        #         print("Conda source path not found on cluster !!")

        for lst_dgr in self.source:
            diagram.append(os.path.join(host_path, os.path.basename(lst_dgr)))

        p1 = subprocess.Popen(['echo', host_password], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        cmd_base = ['sshpass', '-p', host_password, 'scp']
        if len(hnm) == 2:
            cmd_base.extend(['-o', 'ProxyCommand={}'.format('sshpass -p {} ssh -W %h:%p {}'.format(host_password, hnm[0].strip()))])
            host_name = hnm[1]
        # else:
        #     cmd_base.append(host)

        # shared memory transfert ##########################
        yaml_file = os.path.join(os.path.expanduser("~"), '.skrypy', 'list_shm.yml')
        dest = "{}:{}".format(host_name, '~/.skrypy/')
        if os.path.exists(yaml_file):
            cmd_comp = cmd_base.copy()
            cmd_comp.extend([yaml_file, dest])
            print(" ".join(cmd_comp[3:]))
            # cmd = ['sshpass', '-p', host_password.strip(), 'scp', yaml_file, dest]
            # print(" ".join(cmd[3:]))
            # p1 = subprocess.Popen(['echo',host_password], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p2 = subprocess.Popen(cmd_comp, stdin=p1.stdout, stdout=subprocess.PIPE)
            self.output = p2.stdout.read().decode()
            p2.communicate()
            p2.wait()
            print('shared memory transfert done')

        # diagram transfert ################################
        dest = "{}:{}".format(host_name, host_path)
        print('dest=', dest)
        for src_dgr in self.source:
            cmd_comp = cmd_base.copy()
            cmd_comp.extend([src_dgr.strip(), dest])
            print(" ".join(cmd_comp[3:]))
            # cmd = ['sshpass', '-p', host_password.strip(), 'scp', src_dgr.strip(), dest]
            # print(" ".join(cmd[3:]))
            # p1 = subprocess.Popen(['echo',host_password], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p3 = subprocess.Popen(cmd_comp, stdin=p1.stdout, stdout=subprocess.PIPE)
            self.output = p3.stdout.read().decode()
            p3.communicate()
            p3.wait()
            print('diagram transfert done')

        # diagram execution on server #####################
        path_ssh_cmd_file = os.path.join(os.path.expanduser('~'), '.skrypy', 'ssh_command.sh')
        diagram = str(diagram).replace(' ', '')

        if 'gricad' in self.cluster:
            with open(path_ssh_cmd_file, 'w') as fssh:
                fssh.write(pre_exec + "\n")
                fssh.write("cd {}\n".format(host_skrypy_path))
                fssh.write("source /applis/site/guix-start.sh\n")
                fssh.write("python3 Execution_ssh.py {} {} {} {} {} {}\n".format(host_path, diagram, n_cpu, self.mode, opx, self.cluster))
                fssh.write("echo\n")
                # fssh.write("echo \"\033[1;34mfinished.. you can close this window\033[0m\"\n")
                # fssh.write("echo \n")
                fssh.write("exit\n")
        else:
            with open(path_ssh_cmd_file, 'w') as fssh:
                fssh.write(pre_exec + "\n")
                fssh.write("cd {}\n".format(host_skrypy_path))
                fssh.write("source bin/activate\n")
                fssh.write("cd skrypy\n")
                fssh.write("python3 Execution_ssh.py {} {} {} {} {} {}\n".format(host_path, diagram, n_cpu, self.mode, opx, self.cluster))
                fssh.write("deactivate\n")
                fssh.write("echo\n")
                # fssh.write("echo \"\033[1;34mfinished.. you can close this window\033[0m\"\n")
                # fssh.write("echo \n")
                fssh.write("exit\n")

        # sd = os.system(f"gnome-terminal --title=\"" + param_ssh[0] + "\" --wait -- bash -c \"sshpass -p " + host_password.strip() + " ssh " + opx +
        #           " " + host_name + " < ~/.skrypy/ssh_command.sh; bash\"")

        password = host_password.strip()
        file_cmd = os.path.expanduser("~")
        file_cmd = os.path.join(file_cmd, ".skrypy", "ssh_command.sh")
        if opx:
            opt = opx + 'q'
        else:
            opt = '-q'

        cmd_base = ['sshpass', '-p', password, 'ssh', opt]
        if len(hnm) == 2:
            cmd_base.extend(['-o', 'ProxyCommand={}'.format('sshpass -p {} ssh -W %h:%p {}'.format(password, hnm[0].strip())), hnm[1]])
        else:
            cmd_base.append(host)
        cmd_comp = cmd_base.copy()
        with open(file_cmd) as process_stdin:
            # cmd = ["sshpass", "-p", password, "ssh", opt, host_name, "--", "bash", "-s"]
            # print(" ".join(cmd[3:]))
            cmd_comp.extend(["--", "bash", "-s"])
            print(" ".join(cmd_comp[3:]))
            p4 = subprocess.Popen(cmd_comp, stdin=process_stdin, stdout=subprocess.PIPE)
            out, err = p4.communicate()
            print('Execution error:', out.decode())
        col = '\x1b[38;2;50;250;50m'
        # print("execution on {} finished".format(host_name))
        print('{}execution on {} finished\033[0m'.format(col, host_name))
        for lst_dgr in self.source:
            print('    - {}{}\033[0m'.format(col, os.path.basename(lst_dgr)))

        # download shared memory from cluster ###################################
        cmd_base = ['sshpass', '-p', password, 'scp', '-q']
        if len(hnm) == 2:
            cmd_base.extend(['-o', 'ProxyCommand={}'.format('sshpass -p {} ssh -W %h:%p {}'.format(password, hnm[0].strip()))])
        # else:
        #     cmd_base.append(host)

        source = "{}:{}".format(host_name, '~/.skrypy/list_shm.yml')
        dest = os.path.expanduser("~")
        dest = os.path.join(dest, ".skrypy")
        cmd_comp = cmd_base.copy()
        cmd_comp.extend([source.strip(), dest.strip()])
        # cmd = ['sshpass', '-p', host_password.strip(), 'scp', source.strip(), dest.strip()]
        # print(" ".join(cmd[3:]))
        p5 = subprocess.Popen(cmd_comp, stdin=p1.stdout, stdout=subprocess.PIPE)
        # self.output = p5.stdout.read().decode()
        p5.communicate()
        p5.wait()
        if p4.returncode == 0:
            print('download shared memory done')
        else:
            print('download shared memory error !!, code ' + str(p4.returncode))

        # remove list_shme.yaml from cluster #######################################
        cmd_base = ['sshpass', '-p', password, 'ssh']
        if len(hnm) == 2:
            cmd_base.extend(['-o', 'ProxyCommand={}'.format('sshpass -p {} ssh -W %h:%p {}'.format(password, hnm[0].strip())), hnm[1]])
        else:
            cmd_base.append(host_name)
        cmd_comp = cmd_base.copy()
        cmd_comp.append("rm ~/.skrypy/list_shm.yml")
        # cmd = ['sshpass', '-p', host_password.strip(), 'ssh', host_name, "rm ~/.skrypy/list_shm.yml"]
        p6 = subprocess.Popen(cmd_comp, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        # display new list
        SharedMemoryManager(False)

    def searchSourceConda(self, nhst, phst):
        conda_path = None

        stdout, stderr = subprocess.Popen(['sshpass', '-p', phst, 'ssh', nhst, 'test -e ~/.skrypy/env_parameters.txt; echo $?'], stdout=subprocess.PIPE).communicate()
        if not bool(int(stdout[:-1])):
            stdout, stderr = subprocess.Popen(['sshpass', '-p', phst, 'ssh', nhst, 'cat ~/.skrypy/env_parameters.txt'], stdout=subprocess.PIPE).communicate()
            textin = stdout.decode()
            ind = textin.find('CONDASOURCE')
            if ind != -1:
                conda_path = textin[ind:]
                conda_path = conda_path[12:conda_path.index('\n')]
                print("Conda found on the cluster:", conda_path)
        return conda_path


class SubWindowManager(QMdiSubWindow):

    signal1 = pyqtSignal(object)
    signal2 = pyqtSignal(str, int)

    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.windowNumber = 0
        # for action in self.systemMenu().actions():
        #     if action.shortcut() == QKeySequence("Ctrl+w"):
        #         action.setShortcut(QKeySequence())

    @pyqtSlot(str)
    def closeEvent(self, event):
        title = self.windowTitle()
        if '*' in title:
            msg = QMessageBox(editor)
            msg.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
            msg.setText("Save changes in " + title + " ?")
            # reply = msg.question(
            #     self,
            #     'Save diagram',
            #     "Save changes in " + title + " ?",
            #     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            # )
            msg.setIcon(QMessageBox.Icon.Question)
            msg.setStandardButtons(QMessageBox.StandardButton.Yes |
                                   QMessageBox.StandardButton.No |
                                   QMessageBox.StandardButton.Cancel)
            msg.setDefaultButton(QMessageBox.StandardButton.No)
            # msg.setWindowFlags(Qt.WindowType.Window |
            #                    Qt.WindowType.WindowCloseButtonHint |
            #                    Qt.WindowType.WindowMinimizeButtonHint |
            #                    Qt.WindowType.WindowMaximizeButtonHint |
            #                    Qt.WindowType.WindowTitleHint)
            
            reply = msg.exec()

            if reply == QMessageBox.StandardButton.Yes:
                answ = editor.menub.btnPressed(QAction('Save Diagram'))
                if answ == 'yes':
                    self.signal1.emit(self)
                    event.accept()
                else:
                    event.ignore()
            elif reply == QMessageBox.StandardButton.No:
                self.signal1.emit(self)
                event.accept()
            else:
                event.ignore()
        else:
            self.signal1.emit(self)
            event.accept()
        # QMdiSubWindow.closeEvent(self, event)

    def focusInEvent(self, event):
        self.signal2.emit(self.windowTitle(), self.windowNumber)
        QMdiSubWindow.focusInEvent(self, event)


class Start_environment():

    def __init__(self, showing=False, parent=None):
        env_file = os.path.join(os.path.expanduser('~'), '.skrypy', 'env_parameters.txt')
        list_env = {}
        if showing:
            print("{}\nEnvironment variables reloaded:".format('\x1b[38;2;50;250;50m'))
        if os.path.exists(env_file):
            with open(env_file, 'r') as stream:
                for line in stream:
                    line_str = line.rstrip()
                    if line_str:
                        if '#' not in line and ('export' in line or 'sh ' in line):
                            if 'export PATH=' in line:
                                line_mod = line.replace('export', '').replace('$PATH:', '').replace('PATH=', '').strip()
                                if 'PATH' not in list_env.keys():
                                    list_env['PATH'] = line_mod
                                else:
                                    list_env['PATH'] += os.pathsep + line_mod
                            elif 'sh ' in line[0:3]:
                                line_mod = line[2:].strip()
                                list_env['sh'] = line_mod
                            elif '=' in line:
                                line_mode = line.split('=')
                                line_mode[0] = line_mode[0].replace('export', '').strip()
                                list_env[line_mode[0]] = line_mode[1]

            for kenv, venv in list_env.items():
                if kenv == 'sh':
                    try:
                        os.popen('sh ' + venv)
                    except Exception as err:
                        print(err)
                elif kenv == 'PATH':
                    os.environ['PATH'] += os.pathsep + venv
                else:
                    os.environ[kenv] = venv
                if showing:
                    print(kenv, venv.strip())
        if showing:
            print("\x1b[0m")


class StopExecution(QGraphicsPolygonItem):

    def __init__(self, unit='', isMode=True, parent=None):
        super(StopExecution, self).__init__(parent)

        if unit == 'newStopExec':
            StopExist = True
            inc = 0
            while StopExist:
                if 'E' + str(inc) in editor.listStopExec[editor.currentTab]:
                    inc += 1
                else:
                    StopExist = False
            self.unit = 'E' + str(inc)

        else:
            self.unit = unit

        self.inputs, self.outputs = [], []
        self.isMode = isMode

        polyhead = QPolygonF([QPointF(0, 0), QPointF(20, 20), QPointF(60, 20), QPointF(80, 0),
                              QPointF(80, -40), QPointF(60, -60), QPointF(20, -60), QPointF(0, -40)])

        self.editStopItem()
        self.setPolygon(polyhead)

        if isMode:
            editor.listStopExec[editor.currentTab][self.unit] = ()

        self.setZValue(0)
        self.caseFinal = False
        self.currentLoop = None
        self.moved = False
        self.preview = False

    def editStopItem(self):
        self.setPen(QPen(ItemColor.FRAME_CONNECT.value, 2))
        self.setBrush(QBrush(Qt.GlobalColor.red))
        if self.isMode:
            self.setFlags(self.GraphicsItemFlag.ItemIsSelectable | self.GraphicsItemFlag.ItemIsMovable | self.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setCursor(QCursor(ItemMouse.HANDLETOPITEM.value))

        self.label = QGraphicsTextItem('Stop', self)
        self.label.setDefaultTextColor(ItemColor.DEFAULTTEXTCOLOR.value)
        rect = self.label.boundingRect()
        lw, lh = rect.width(), rect.height()
        lx1 = 20
        ly1 = -35

        self.nameStp = QGraphicsTextItem(self.unit, self)
        self.nameStp.setDefaultTextColor(ItemColor.DEFAULTTEXTCOLOR.value)
        rect = self.nameStp.boundingRect()
        lw, lh = rect.width(), rect.height()
        lx2 = lw + 5
        ly2 = 20

        self.setFlag(self.GraphicsItemFlag.ItemIsFocusable, True)

        self.label.setPos(lx1, ly1)
        self.nameStp.setPos(lx2, ly2)

    def itemChange(self, *args, **kwargs):
        gridSize = ItemGrid.SPACEGRID.value
        if args[0] == self.GraphicsItemChange.ItemPositionHasChanged:
            xV = round(args[1].x() / gridSize) * gridSize
            yV = round(args[1].y() / gridSize) * gridSize
            self.setPos(QPointF(xV, yV))
        return QGraphicsRectItem.itemChange(self, *args, **kwargs)

    def mouseMoveEvent(self, mouseEvent):
        mouseEvent.accept()
        editor.loopMouseMoveEvent(self, mouseEvent.scenePos())
        return QGraphicsRectItem.mouseMoveEvent(self, mouseEvent)

    def mouseReleaseEvent(self, event):
        editor.loopMouseReleaseEvent(self, True)
        return QGraphicsRectItem.mouseReleaseEvent(self, event)

    def deleteItem(self):
        editor.diagramScene[editor.currentTab].removeItem(self)
        del editor.listStopExec[editor.currentTab][self.unit]
        del editor.listItems[editor.currentTab][self.unit]
        editor.deleteItemsLoop(self)


class SubProcessItem():

    def __init__(self, unit='newSubMod', nameSubModule='', w=150, h=80, *inout, parent=None):
        self.name = nameSubModule
        self.unit = 'M0'
        self.w = w
        self.h = h
        self.inout = inout

        self.inputs, self.outputs = [], []

        listlabelIn = []
        listVal = []
        listlabelOut = []
        listForm = []

        wminIn = 0.0
        wminOut = 0.0

        if unit in 'newSubMod' or unit in 'pastSubmod':
            SubModExist = True
            inc = 0
            while SubModExist:
                if 'M' + str(inc) in editor.listSubMod[editor.currentTab]:
                    inc += 1
                else:
                    SubModExist = False
            self.unit = 'M' + str(inc)
            if unit in 'newSubMod':
                inout = (editor.libSubMod[self.name],)

        else:
            self.unit = unit

        listVal = editor.libSubMod[self.name][1]
        newVal = []
        for it in inout[0][1]:
            if type(it).__name__ == 'enumerate':
                newVal.append(list(it)[0][1])
            else:
                newVal.append(it)
        self.subBlock = BlockCreate(self.name, self.unit, None, w, h, listVal, True, *inout)
        editor.listSubMod[editor.currentTab][self.unit] = (self.name, (inout[0][0], newVal, inout[0][2], inout[0][3]), editor.libSubMod[self.name][4])

    def getSubblocks(self):
        return self.subBlock


class TextInfo(QTextEdit):

    def __init__(self, parent=None):
        super(TextInfo, self).__init__(parent)
        self.setReadOnly(True)
        # self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.text = ''

    def addTxt(self, txt):
        self.append(txt)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def text(self):
        return self.document().toPlainText()


class ThreadDiagram(QRunnable):

    def __init__(self, name, args, wind, parent=None):
        super(ThreadDiagram, self).__init__()
        self.name = name
        self.args = args
        self.wind = wind
        self.window_progressBar()
        self.pipe_exec = execution2()
        self.pipe_exec.update_progress.connect(self.update_progressBar)
        with open(os.path.join(os.path.expanduser('~'), '.skrypy', 'list_process.tmp'), 'w') as f:
            # list_proc = f.readlines()
            f.write('{}{}{}\n'.format('Process Name', ' ' * 10, 'ID'))

    @pyqtSlot()
    def run(self):
        self.pipe_exec.go_execution(*self.args)

    def update_progressBar(self, value, text):
        self.label.setText(text)
        self.pbar.setValue(value)

    def window_progressBar(self):
        screen_center = editor.size()
        self.winBar = QWidget(self.wind)
        self.winBar.setWindowTitle('Progress process')
        self.winBar.setStyleSheet("background-color:white;")
        self.winBar.resize(400, 80)
        self.winBar.setWindowFlags(Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.label = QLabel()
        self.pbar = QProgressBar(self.winBar)
        self.pbar.setGeometry(-100, 0, 350, 30)
        self.pbar.setValue(0)
        # self.button_stop = QPushButton('Stop pipeline')
        # self.button_stop.setCheckable(True)
        # self.button_stop.clicked.connect(self.buttonStop)
        # self.args += (self.button_stop,)
        # self.button_stop.clicked.connect(self.runner.kill)
        vbx = QVBoxLayout()
        hbx = QHBoxLayout()
        hbx.addWidget(self.pbar)
        # hbx.addWidget(self.button_stop)
        vbx.addWidget(self.label)
        vbx.addLayout(hbx)
        self.winBar.setLayout(vbx)
        self.winBar.move(int(-200 + screen_center.width() / 2), int(screen_center.height() / 2))
        self.winBar.show()
        # time.sleep(0.1)
        # current_dir_path = os.path.dirname(os.path.realpath(__file__))
        # source_disp = os.path.join(current_dir_path, 'systemControl.py')
        # self.sysctrl = subprocess.Popen([sys.executable,
        #                                  source_disp,
        #                                  self.name,
        #                                  str(os.getpid()),
        #                                  str(screen_center.width()),
        #                                  str(screen_center.height())])

    def buttonStop(self):
        self.pipe_exec.check_button(True)
        # self.winBar.close()


class ToolBar(QToolBar):
    def __init__(self, parent=None):
        QToolBar.__init__(self, parent)
        self.setStyleSheet('''
                            QToolButton:!hover {background-color:lightgray}
                            QToolBar {background: transparent}
                            QToolBar::separator {background-color: transparent; width: 10}
                            ''')
        self.setFixedHeight(50)
        path_relatif = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        list_toolbar_menu = [('New Diagram', 'newDiagram.png', '(Ctrl+N)'), ('Open Diagram', 'open_diagram.png', '(Ctrl+O)'), ('Save Diagram', 'save_diagram.png', '(Ctrl+S)'),
                             ('Save Diagram As...', 'saveAs_diagram.png', ''), ('separator',),
                             ('Undo', 'undo.png', '(Ctrl+Z)'), ('Redo', 'redo.png', '(Ctrl+Y)'),
                             ('Copy', 'copy.png', '(Ctrl+C)'), ('Paste', 'paste.png', '(Ctrl+D)'),
                             ('Refresh Diagram', 'refresh.png', ''), ('separator',), ('Analyze this Diagram', 'analyze_diagram.png', '(Ctrl+A)'),
                             ('Run this Diagram', 'run.png', '(Ctrl+R)'), ('Run this Diagram in Threading mode', 'run_thread.png', '(Ctrl+T)'),
                             ('Run multiple Diagrams', 'run_multiple.png', '(Ctrl+M)'), ('separator',),
                             ('Run this Diagram on cluster HPC', 'run_ssh.png', ''), ('Run this Diagram in Threading mode on cluster HPC', 'run_thread_ssh.png', ''),
                             ('Run multiple Diagrams on cluster HPC', 'run_multiple_ssh.png', ''), ('separator',),
                             ('Run multiple Diagrams alternately', 'run_multiple_altern.png', ''), ('separator',),
                             ('Show/hide Tools', 'tools.png', ''), ('Show/hide Console', 'console.png', ''), ('Show/hide Progress', 'Items.png', ''), ('separator',),
                             ('Cascade', 'windowsCascade.png', '(Ctrl+F)'), ('Tiled', 'windowsTile.png', '(Ctrl+G)'), ('Maximized', 'windowsMax.png', '(Ctrl+H)'),
                             ('separator',), ('Fit to window', 'fitWindow.png', '(f)')]

        for list_menu in list_toolbar_menu:
            if list_menu[0] == 'separator':
                self.addSeparator()
            else:
                pathbkg = os.path.join(path_relatif, 'ressources', list_menu[1])
                txto = list_menu[0]
                tools_diagr = QAction(QIcon(pathbkg), txto + ' ' + list_menu[2], self)
                tools_diagr.triggered.connect(partial(self.action, txto))
                self.addAction(tools_diagr)

        self.mainLayout = QGridLayout()
        self.check_box1 = QCheckBox("Auto fit")
        self.check_box1.setChecked(False)
        editor.autofit = False
    #     self.check_box2 = QCheckBox("Tiled")
    #     self.check_box3 = QCheckBox("Maximize")
        self.check_box1.stateChanged.connect(self.uncheck)
    #     self.check_box2.stateChanged.connect(self.uncheck)
    #     self.check_box3.stateChanged.connect(self.uncheck)
        check_container = QWidget()
        check_container.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
    #     label = QLabel("View mode : ")
    #     # label.setFont(QFont("Times", 12))
    #     self.mainLayout.addWidget(label, 0, 0)
        self.mainLayout.addWidget(self.check_box1, 0, 1)
    #     self.mainLayout.addWidget(self.check_box2, 0, 2)
    #     self.mainLayout.addWidget(self.check_box3, 0, 3)
    #     # self.setLayout(self.mainLayout)
        wid = QWidget()
        wid.setLayout(self.mainLayout)
        self.addWidget(wid)

    def uncheck(self, state):
        editor.autofit = self.check_box1.isChecked()
        if editor.autofit:
            editor.windActivation()
        # if state == Qt.CheckState.Checked:
    #         if self.sender() == self.check_box1:
    #             self.check_box2.setChecked(False)
    #             self.check_box3.setChecked(False)
    #         elif self.sender() == self.check_box2:
    #             self.check_box1.setChecked(False)
    #             self.check_box3.setChecked(False)
    #         elif self.sender() == self.check_box3:
    #             self.check_box1.setChecked(False)
    #             self.check_box2.setChecked(False)

    def action(self, txt_action):
        Menu().btnPressed(QAction(txt_action))


class TreeLibrary(QTreeView):

    def __init__(self):
        super(TreeLibrary, self).__init__()
        # model = QStandardItemModel()
        # self.setModel(model)
        self.setColumnWidth(0, 100)
        self.loading = False

    def __new__(self, *args, **kwargs):
        self.loading = False
        return QTreeView.__new__(self, *args, **kwargs)

    def return_clicked(self):
        self.button_clicked.emit('return')

    # def contextMenuEvent(self, event):
    #     menu = QMenu()
    #     ind = self.currentIndex()
    #     root = self.model().data(ind)
    #     name = self.model().name
    #     if name in 'blocks_subModules':
    #         if root in editor.libSubMod.keys():
    #             text_menu = 'Delete this item'
    #         else:
    #             text_menu = 'Delete all contained items'
    #         rs = menu.addAction(text_menu)
    #         rs.triggered.connect(self.deleteSubMod)
    #         menu.addSeparator()
    #     menu.exec(QCursor.pos())

    def deleteSubMod(self):
        pass

    def deleteAllSubMod(self):
        pass

    def selectionChanged(self, *args, **kwargs):
        try:
            index = self.selectedIndexes()
            for elem in editor.previewScene.items():
                editor.previewScene.removeItem(elem)
            if index and not self.loading:
                self.getSelectedItem()
        except Exception as e:
            pass
        return QTreeView.selectionChanged(self, *args, **kwargs)

    def getSelectedItem(self):
        index = self.selectedIndexes()[0]
        crawler = index.model().itemFromIndex(index)
        name = crawler.text()
        sel = crawler.text()
        mimidat = index.model().name
        if mimidat in 'mod_SubMod':
            if sel not in editor.listCategory:
                b1 = BlockCreate(name, '', editor.getlib()[name][0], 150, 80, editor.getlib()[name][1][1], False, editor.getlib()[name][1])
                b1.preview = True
                textSource = 'Source : ' + editor.getlib()[name][0]
                self.showModel(b1, textSource)
            else:
                for elem in editor.previewScene.items():
                    editor.previewScene.removeItem(elem)

        elif mimidat in 'blocks_subModules':
            if sel not in editor.listCategorySubMod:
                bm = BlockCreate(name, '', None, 150, 80, editor.libSubMod[name][1], False, editor.libSubMod[name])
                self.showModel(bm, '')
            else:
                for elem in editor.previewScene.items():
                    editor.previewScene.removeItem(elem)

        elif mimidat in 'structures_tools':
            if sel not in editor.listCategoryTools:
                if "Constant" in name:
                    if 'string' in name:
                        val = 'your text'
                        form = 'str'
                    elif 'integer' in name:
                        val = 0
                        form = 'int'
                    elif 'float' in name:
                        val = 0.0
                        form = 'float'
                    elif 'combobox' in name:
                        form = "enumerate(('item1','item2','item3'))"
                        val = 'item1'
                    elif 'boolean' in name:
                        val = True
                        form = 'bool'
                    elif 'path' in name:
                        val = 'path'
                        form = 'path'
                    elif 'tuple' in name:
                        val = (0,)
                        form = ('tuple')
                    bc = Constants('', 80, 30, val, form, '', False)
                elif 'Cluster' in name:
                    if 'string' in name:
                        val = ['text1', 'text2']
                        form = 'list_str'
                    elif 'integer' in name:
                        val = (0, [[1, 2], [5, 9]], 0)
                        form = 'array_int'
                    elif 'float' in name:
                        val = (0.0, [[1.0, 0.2], [5.5, 9.9]], 0.0)
                        form = 'array_float'
                    bc = Clusters('', 115, 33, val, form, '', False)
                elif 'Comments' in name:
                    bc = CommentsItem(200, 100, 'your comments', False)
                elif 'For' in name:
                    bc = ForLoopItem('', name, 400, 400, False, [], [])
                elif 'If' in name:
                    bc = ForLoopItem('', name, 400, 400, False, [], [])
                elif 'Script' in name:
                    bc = ScriptItem('', name, 400, 400, False, False)
                elif 'Macro' in name:
                    bc = ScriptItem('', name, 400, 400, False, False)
                elif 'Checkbox' in name:
                    bc = Checkbox('', ['item1', 'item2'], '', False)
                elif 'Imagebox' in name:
                    bc = Imagebox('', 'path', '', False)
                elif 'Pathbox' in name:
                    bc = Constants('', 80, 30, ['/tmp', '/usr/bin'], 'list_path', '', False)
                elif name in ['Value', 'Type', 'Length']:
                    bc = Probes('', 'unkn', name, False)
                elif 'Connector' in name:
                    if "input" in name:
                        bc = ConnectorItem('', 'C0', 70, 26, 'in', 'unkn', '', False)
                    else:
                        bc = ConnectorItem('', 'C0', 70, 26, 'out', 'unkn', '', False)
                elif 'Stop' in name:
                    bc = StopExecution('', False)

                self.showModel(bc, name)

    def showModel(self, item, text):
        editor.previewScene.clear()
        editor.previewDiagram.scene().addItem(item)
        editor.previewDiagram.scene().update()

        rec = item.boundingRect()
        height = rec.height() / 2

        if item.inputs:
            if isinstance(item.inputs, list):
                if len(item.inputs) > 10:
                    posX = 100
                else:
                    posX = 50
                i = 0
                for inp in item.inputs:
                    posY = (((len(item.inputs) - 1) / 2) - i) * height / len(item.inputs)
                    self.drawLink(inp, -posX, posY)
                    i += 1
            else:
                posX, posY = 50, 0
                self.drawLink(item.inputs, -posX, posY)

        if item.outputs:
            if isinstance(item.outputs, list):
                if len(item.outputs) > 10:
                    posX = 100
                else:
                    posX = 50
                i = 0
                for inp in item.outputs:
                    posY = (((len(item.outputs) - 1) / 2) - i) * height / len(item.outputs)
                    self.drawLink(inp, posX, posY)
                    i += 1
            else:
                posX, posY = 50, 0
                self.drawLink(item.outputs, posX, posY)

        textSource = QGraphicsTextItem(text, item)
        textSource.setDefaultTextColor(ItemColor.DEFAULTTEXTCOLOR.value)
        textSource.setFont(QFont("Times", 14, QFont.Weight.Bold))
        textSource.setPos(rec.x() + (rec.width() / 2) - (textSource.boundingRect().width() / 2), rec.y() + rec.height() + 20)

        editor.previewScene.setSceneRect(editor.previewScene.itemsBoundingRect())
        editor.previewDiagram.centerOn(0, 0)
#         editor.previewDiagram.fitInView(rec.x(), rec.y(), rec.width() , rec.height(), Qt.AspectRatioMode.KeepAspectRatio)
        editor.previewDiagram.fitInView(editor.previewScene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        editor.previewDiagram.scale(0.8, 0.8)

    def drawLink(self, inp, posX, posY):
        format = inp.format
        link = QGraphicsPathItem()
        bislink = QGraphicsPathItem()

        for types in TypeColor:
            if types.name in format:
                color = types.value

        if 'list' in str(format):
            link.setPen(QPen(color, 5))
            bislink.setPen(QPen(Qt.PenStyle.NoPen))

        elif 'array' in str(format):
            link.setPen(QPen(color, 8))
            bislink.setPen(QPen(ItemColor.BIS_LINK.value, 3, Qt.PenStyle.SolidLine))

        else:
            link.setPen(QPen(color, 2))
            bislink.setPen(QPen(Qt.PenStyle.NoPen))

        path = QPainterPath()
        pos2X, pos2Y = inp.scenePos().x(), inp.scenePos().y() - 1
        pos1X, pos1Y = pos2X + posX, pos2Y - posY
        start_x, start_y = pos1X, pos1Y
        end_x, end_y = pos2X, pos2Y
        ctrl1_x, ctrl1_y = pos1X + (pos2X - pos1X) * 0.7, pos1Y
        ctrl2_x, ctrl2_y = pos2X + (pos1X - pos2X) * 0.7, pos2Y
        path.moveTo(start_x, start_y)
        path.cubicTo(ctrl1_x, ctrl1_y, ctrl2_x, ctrl2_y, end_x, end_y)

        link.setPath(path)
        bislink.setPath(path)

        editor.previewDiagram.scene().addItem(link)
        editor.previewDiagram.scene().addItem(bislink)


class TypeColor(Enum):
    str = QColor(200, 0, 250, 255)
    float = QColor(200, 100, 0, 255)
    int = QColor(0, 100, 255, 255)
    path = QColor(255, 100, 100, 255)
    bool = QColor(100, 200, 100, 255)
    dict = QColor(250, 250, 50, 255)
    tuple = QColor(140, 140, 140, 255)
    unkn = QColor(255, 255, 255, 255)


class UpdateList:

    def __init__(self, txt):
        editor.listNodes[editor.currentTab].clear()
        editor.listBlocks[editor.currentTab].clear()
        editor.listSubMod[editor.currentTab].clear()
        editor.listConnects[editor.currentTab].clear()
        editor.listConstants[editor.currentTab].clear()
        editor.listProbes[editor.currentTab].clear()
        editor.listTools[editor.currentTab].clear()
        editor.libTools[editor.currentTab].clear()
        listUnit = []

        for line in txt.splitlines():
            unit = ''

            if line[0:4] == 'link':
                args = ["link", "node"]
                unit, line = GetValueInBrackets(line, args).getValues()
                editor.listNodes[editor.currentTab][unit] = line

            elif line[0:5] == 'block':
                args = ["block", "category", "class", "valInputs", "RectF"]
                unit, cat, classs, Vinput, pos = GetValueInBrackets(line, args).getValues()
                editor.listBlocks[editor.currentTab][unit] = (classs, cat, eval(Vinput))

            elif line[0:6] == 'submod':
                args = ["submod", "nameMod", "catMod", "valInputs", "RectF"]
                unit, nameMod, catMod, Vinput, pos = GetValueInBrackets(line, args).getValues()
                editor.listSubMod[editor.currentTab][unit] = (nameMod, eval(Vinput), catMod)

            elif line[0:5] == 'connt':
                args = ["connt", "name", "type", "format", "valOut", "RectF"]
                unit, name, typ, form, Vinput, pos = GetValueInBrackets(line, args).getValues()
                Vinput = ''
                try:
                    line = line[line.index('valOut=') + 8:len(line)]
                    Vinput = line[0:line.index('] RectF=')]
                except Exception as e:
                    pass

                if 'in' in typ:
                    editor.listConnects[editor.currentTab][unit] = (typ, name, form, Vinput)
                else:
                    editor.listConnects[editor.currentTab][unit] = (typ, name, form)

            elif line[0:8] == 'constant':
                args = ["constant", "value", "format", "label", "RectF"]
                unit, vout, fort, lab, pos = GetValueInBrackets(line, args).getValues()
                if fort == 'bool':
                    vout = eval(vout)
                if not fort:
                    fort = ''
                try:
                    editor.listConstants[editor.currentTab][unit] = (fort, eval(vout), lab)
                except Exception as e:
                    editor.listConstants[editor.currentTab][unit] = (fort, vout, lab)

            elif line[0:7] == 'cluster':
                args = ["cluster", "value", "format", "label", "RectF"]
                unit, vout, fort, lab, pos = GetValueInBrackets(line, args).getValues()
                try:
                    editor.listConstants[editor.currentTab][unit] = (fort, eval(vout), lab)
                except Exception as e:
                    editor.listConstants[editor.currentTab][unit] = (fort, vout, lab)

            elif line[0:7] == 'loopFor':
                args = ["loopFor", "inputs", "outputs", "listItems", "RectF"]
                unit, inp, outp, listIt, pos = GetValueInBrackets(line, args).getValues()
                editor.listTools[editor.currentTab][unit] = eval(listIt)
                editor.libTools[editor.currentTab][unit] = (eval(inp), eval(outp))

            elif line[0:6] == 'loopIf':
                args = ["loopIf", "inputs", "outputs", "listItems", "RectF"]
                unit, inp, outp, listIt, pos = GetValueInBrackets(line, args).getValues()

                editor.listTools[editor.currentTab][unit] = eval(listIt)
                editor.libTools[editor.currentTab][unit] = (eval(inp), eval(outp))

            elif line[0:6] == 'script':
                args = ["script", "title", "inputs", "outputs", "code", "RectF"]
                unit, tit, inp, outp, code, pos = GetValueInBrackets(line, args).getValues()
                inp = "[" + inp + "]"
                outp = "[" + outp + "]"
                editor.listTools[editor.currentTab][unit] = code
                editor.libTools[editor.currentTab][unit] = (eval(inp), eval(outp))
            elif line[0:5] == 'probe':
                args = ["probe", "label", "format", "RectF"]
                unit, label, form, pos = GetValueInBrackets(line, args).getValues()
                editor.listProbes[editor.currentTab][unit] = (form, label)
            elif line[0:8] == 'stopexec':
                args = ["stopexec", "RectF"]
                unit, pos = GetValueInBrackets(line, args).getValues()
                editor.listStopExec[editor.currentTab][unit] = ()

            if unit:
                listUnit.append(unit)

        listItemsTmp = editor.listItems[editor.currentTab].copy()
        for lstUnit in listItemsTmp.keys():
            if lstUnit not in listUnit:
                del editor.listItems[editor.currentTab][lstUnit]


class UpdateUndoRedo:

    def __init__(self):
        # editor.listItemStored.clear()
        # del editor.listCommentsStored[:]
        try:
            dd = editor.pointTyping[editor.currentTab]
        except Exception as err:
            return
        for i in range(editor.pointTyping[editor.currentTab] + 1,
                       len(editor.undoredoTyping[editor.currentTab])):
            del editor.undoredoTyping[editor.currentTab][i]
        editor.pointTyping[editor.currentTab] += 1
        self.diagram = SaveDiagram().toPlainText()
        editor.undoredoTyping[editor.currentTab][editor.pointTyping[editor.currentTab]] = \
            self.diagram
        currentTitle = editor.getSubWindowCurrentTitle()
        self.titlesavetmp = currentTitle
        try:
            if (currentTitle[-1] != '*' and len(editor.undoredoTyping[editor.currentTab]) > 1):
                currentTitle = '{}{}'.format(currentTitle, '*')
                editor.setSubWindowCurrentTitle(currentTitle)
        except Exception as err:
            print('error UpdateUndoRedo:', err)
        try:
            self.save_tempfile()
        except Exception as err:
            pass

    def save_tempfile(self):
        self.titlesavetmp = self.titlesavetmp.replace('*', '').strip()
        if not self.titlesavetmp.endswith('.dgr'):
            self.titlesavetmp += '.dgr'
        dest = os.path.join(os.path.expanduser('~'), '.main', 'temp_file', self.titlesavetmp)
        f = open(dest, 'w')
        f.write(self.diagram)
        f.close()


class ValueZ2:

    def __init__(self):
        listZ = {}
        lst = editor.listTools[editor.currentTab]

        keyZ = []
        uniZ = []
        for keyList, valList in editor.listTools[editor.currentTab].items():
            keyZ.append(keyList)
            if 'I' in keyList:
                uniZ.append(valList[0])
                uniZ.append(valList[1])
            else:
                uniZ.append(valList)

        uniZ = [item for sublist in uniZ for item in sublist]

        listLowNivel = list(set(keyZ) - set(uniZ))

        ind = 0
        while uniZ:
            for le in listLowNivel:
                listZ[le] = ind
                if 'I' in le:
                    for le2 in lst[le][0]:
                        listZ[le2] = ind + 1
                        uniZ.remove(le2)
                    for le2 in lst[le][1]:
                        listZ[le2] = ind + 1
                        uniZ.remove(le2)
                else:
                    for le2 in lst[le]:
                        listZ[le2] = ind + 1
                        uniZ.remove(le2)
                keyZ.remove(le)
            listLowNivel = list(set(keyZ) - set(uniZ))
            ind += 1

        for its in editor.diagramView[editor.currentTab].items():
            try:
                its.setZValue(listZ[its.unit])
            except Exception as e:
                pass

        for its in editor.diagramView[editor.currentTab].items():
            if type(its) is ForLoopItem:
                if 'I' in its.unit:
                    tmp = its.elemProxy.currentText()
                    its.elemProxy.newValue()
                    its.elemProxy.setCurrentText(tmp)
