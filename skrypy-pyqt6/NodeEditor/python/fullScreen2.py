# from PyQt5.QtCore import QPoint, QLineF
# from PyQt5.QtGui import QColor, QPen
# from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGraphicsView
# from PyQt5.Qt import QLabel, Qt, QPainter, QEvent
from enum import Enum
import math
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QGraphicsView, QLabel
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QLineF, QPoint


class SubWindow(QDialog):
    def __init__(self, diagram_scene, editor, title):
        super(SubWindow, self).__init__()
        self.scalefactor = 1
        self.__prevMousePos = QPoint(0, 0)
        message = QLabel(title)
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.diagram_view = DiagramView(diagram_scene, self)
        # self.diagram_view.setScene(diagram_scene)
        # self.diagram_view.viewport().installEventFilter(self)

        # self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint)
        layoutDiagram = QVBoxLayout()
        layoutDiagram.addWidget(message)
        layoutDiagram.addWidget(self.diagram_view)
        self.setLayout(layoutDiagram)
        self.showFullScreen()

    # def eventFilter(self, source, event):
    #     if (source == self.diagram_view.viewport()):
    #         if (event.type() == QEvent.Wheel):
    #             return True
    #         elif (event.type() == QEvent.MouseButtonPress):
    #             self.mousePressEvent(event)
    #         elif (event.type() == QEvent.MouseButtonRelease):
    #             self.mouseReleaseEvent(event)
    #     return False

    def mouseDoubleClickEvent(self, event):
        try:
            pos = event.pos()
            itms = self.diagram_view.items(pos)
            if len(itms) != 0:
                SubWindow.mouseDoubleClickEvent(self, event)
            else:
                self.close()
        except Exception as err:
            print(err)

    def closeEvent(self, event):
        return QDialog.closeEvent(self, event)


class DiagramView(QGraphicsView):

    def __init__(self, scene, dialog, parent=None):
        super().__init__(scene, parent)

        self.dialog = dialog

        self.setBackgroundBrush(QColor(30, 30, 30))
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)

        # comportement standard d'éditeur
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        self._panning = False
        self._panStart = QPoint()

        self.base_grid = 20
        self.major_step = 5

        self.pen_minor = QPen(ItemColor.GRID_MINOR.value)
        self.pen_major = QPen(ItemColor.GRID_MAJOR.value)
        self.pen_axis = QPen(ItemColor.GRID_AXIS.value)

    # ---------------------------
    # PAN (bouton milieu)
    # ---------------------------

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.MiddleButton:
            self._panning = True
            self._panStart = event.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()
            return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):

        if self._panning:
            delta = event.pos() - self._panStart
            self._panStart = event.pos()
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - delta.x()
            )
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - delta.y()
            )
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.MouseButton.MiddleButton:
            self._panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
            event.accept()
            return

        super().mouseReleaseEvent(event)

    # ---------------------------
    # ZOOM (roulette)
    # ---------------------------

    def wheelEvent(self, event):

        zoomFactor = 1.15

        if event.angleDelta().y() > 0:
            self.scale(zoomFactor, zoomFactor)
        else:
            self.scale(1 / zoomFactor, 1 / zoomFactor)

    # ---------------------------
    # GRID
    # ---------------------------

    def drawBackground(self, painter, rect):

        super().drawBackground(painter, rect)

        zoom = self.transform().m11()

        grid = self.base_grid
        while grid * zoom < 15:
            grid *= 2

        left = math.floor(rect.left() / grid) * grid
        top = math.floor(rect.top() / grid) * grid

        minor = []
        major = []

        x = left
        while x < rect.right():

            if int(x / grid) % self.major_step == 0:
                major.append(QLineF(x, rect.top(), x, rect.bottom()))
            else:
                minor.append(QLineF(x, rect.top(), x, rect.bottom()))

            x += grid

        y = top
        while y < rect.bottom():

            if int(y / grid) % self.major_step == 0:
                major.append(QLineF(rect.left(), y, rect.right(), y))
            else:
                minor.append(QLineF(rect.left(), y, rect.right(), y))

            y += grid

        painter.setPen(self.pen_minor)
        painter.drawLines(minor)

        painter.setPen(self.pen_major)
        painter.drawLines(major)

        painter.setPen(self.pen_axis)
        painter.drawLine(QLineF(0, rect.top(), 0, rect.bottom()))
        painter.drawLine(QLineF(rect.left(), 0, rect.right(), 0))


class ItemColor(Enum):

    BACKGROUND = QColor(30, 30, 30, 255)
    GRID_MINOR = QColor(80, 60, 60, 100)
    GRID_MAJOR = QColor(120, 100, 100, 100)
    GRID_AXIS = QColor(150, 80, 80, 100)
