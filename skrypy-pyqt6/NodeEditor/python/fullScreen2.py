from PyQt6.Qt import QPointF
from PyQt6.QtCore import Qt, QEvent, QPoint
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QGraphicsView


class SubWindow(QDialog):
    def __init__(self, diagram_scene, editor):
        super(SubWindow, self).__init__()
        self.__prevMousePos = QPoint(0, 0)
        self.diagram_view = Diagramview(diagram_scene)
        self.diagram_view.setScene(diagram_scene)
        # self.setWindowFlags(Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        # self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint)
        layoutDiagram = QVBoxLayout()
        layoutDiagram.addWidget(self.diagram_view)
        self.setLayout(layoutDiagram)
        self.showFullScreen()

    def mouseDoubleClickEvent(self, event):
        try:
            pos = event.pos()
            itms = self.diagram_view.items(pos)
            if len(itms) != 0:
                SubWindow.mouseDoubleClickEvent(self, event)
            else:
                self.close()
        except Exception as err:
            pass

    def closeEvent(self, event):
        return QDialog.closeEvent(self, event)


class Diagramview(QGraphicsView):
    def __init__(self, scene, parent=None):
        QGraphicsView.__init__(self, scene, parent)
        self.setScene(scene)
        self.scalefactor = 1
        self.setBackgroundBrush(QColor(30, 30, 30, 255))
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        self.centerOn(0, 0)
        self.fitInView(scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.scale(2.0, 2.0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setMouseTracking(True)

        self.scene().setSceneRect(self.scene().itemsBoundingRect())

    # def drawBackground(self, painter, rect):
    #     gridSize = 100
    #     pen = QPen(QColor(100, 100, 230))
    #     pen.setWidth(2)
    #     painter.setPen(pen)
    #     left = int(rect.left()) - (int(rect.left()) % gridSize)
    #     top = int(rect.top()) - (int(rect.top()) % gridSize)
    #     for x in range(left, int(rect.right()), gridSize):
    #         for y in range(top, int(rect.bottom()), gridSize):
    #             painter.drawPoints(QPointF(x,y))

    def mousePressEvent(self, event):
        if event.button() == Qt.MidButton:
            self.__prevMousePos = event.pos()
        self.horizontalScrollBar().setEnabled(True)
        self.verticalScrollBar().setEnabled(True)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MidButton:
            offset = self.__prevMousePos - event.pos()
            self.__prevMousePos = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + offset.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() + offset.y())
        QGraphicsView.mouseMoveEvent(self, event)

    def wheelEvent(self, event):
        self.horizontalScrollBar().setEnabled(False)
        self.verticalScrollBar().setEnabled(False)
        adj = 0.1777
        if event.angleDelta().y() < 0:
            adj = -adj
        self.scalefactor += adj
        self.scale(1 + adj, 1 + adj)
        rectBounds = self.scene().itemsBoundingRect()
        self.scene().setSceneRect(rectBounds.x() - 200, rectBounds.y() - 200, rectBounds.width() + 400, rectBounds.height() + 400)
        QGraphicsView.wheelEvent(self, event)
