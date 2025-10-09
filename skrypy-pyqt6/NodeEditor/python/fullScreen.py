from PyQt6.QtCore import Qt, QEvent, QPoint
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QVBoxLayout, QGraphicsView, QLabel, QDialog


class SubWindow(QDialog):
    def __init__(self, diagram_scene, editor, title):
        super(SubWindow, self).__init__()
        self.scalefactor = 1
        self.__prevMousePos = QPoint(0, 0)
        message = QLabel(title)
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.diagram_scene = diagram_scene
        self.diagram_view = QGraphicsView()
        self.diagram_view.setBackgroundBrush(QColor(30, 30, 30, 255))
        self.diagram_view.setMouseTracking(True)
        self.diagram_view.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        self.diagram_scene.setSceneRect(self.diagram_scene.itemsBoundingRect())
        self.diagram_view.centerOn(0, 0)
        self.diagram_view\
            .fitInView(self.diagram_scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.diagram_view.viewport().installEventFilter(self)
        self.diagram_view.scale(0.4, 0.4)
        self.diagram_view.setScene(self.diagram_scene)
        # self.setWindowFlags(Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        # self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint)
        layoutDiagram = QVBoxLayout()
        layoutDiagram.addWidget(message)
        layoutDiagram.addWidget(self.diagram_view)
        self.setLayout(layoutDiagram)
        self.showFullScreen()
        self.middle_mouse_pressed = False

    def eventFilter(self, source, event):
        if (source == self.diagram_view.viewport()):
            if (event.type() == QEvent.Type.Wheel):
                self.handle_wheel_event(event)
                return True
            elif (event.type() == QEvent.Type.MouseMove):
                self.mouseMouveDiagram(event)
                # return False
        return False

    def handle_wheel_event(self, event):
        self.diagram_view.horizontalScrollBar().setEnabled(False)
        self.diagram_view.verticalScrollBar().setEnabled(False)
        adj = 0.1777
        if event.angleDelta().y() < 0:
            adj = -adj
        self.scalefactor += adj
        self.diagram_view.scale(1 + adj, 1 + adj)
        rectBounds = self.diagram_view.scene().itemsBoundingRect()
        self.diagram_view.scene().setSceneRect(rectBounds.x() - 200, rectBounds.y() - 200, rectBounds.width() + 400, rectBounds.height() + 400)

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
        
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middle_mouse_pressed = False
        QDialog.mouseReleaseEvent(self, event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middle_mouse_pressed = True
            self.__prevMousePos = event.pos()
        self.diagram_view.horizontalScrollBar().setEnabled(True)
        self.diagram_view.verticalScrollBar().setEnabled(True)

    def mouseMouveDiagram(self, event):
        if self.middle_mouse_pressed:
            offset = self.__prevMousePos - event.pos()
            self.__prevMousePos = event.pos()
            self.diagram_view.horizontalScrollBar().setValue(self.diagram_view.horizontalScrollBar().value() + offset.x())
            self.diagram_view.verticalScrollBar().setValue(self.diagram_view.verticalScrollBar().value() + offset.y())
        else:
            super(SubWindow, self).mouseMoveEvent(event)

    def closeEvent(self, event):
        return QDialog.closeEvent(self, event)
