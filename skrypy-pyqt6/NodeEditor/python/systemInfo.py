from PyQt6.QtWidgets import QApplication, QPlainTextEdit, \
    QVBoxLayout, QDialog
import sys


class diagramInfo(QDialog):
    def __init__(self, text, title, parent=None):
        super(diagramInfo, self).__init__(parent)

        self.top = 200
        self.left = 500
        self.width = 800
        self.height = 600
        self.setWindowTitle(title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #505050;
                color: #dcdcdc;
                border: 1px solid #555;
            }
            """)

        vbox = QVBoxLayout(self)
        self.plainText = QPlainTextEdit()
        # self.plainText.setPlaceholderText("This is some text for our plaintextedit")
        self.plainText.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.plainText.setReadOnly(True)
        vbox.addWidget(self.plainText)
        self.setText(text)

        self.setLayout(vbox)

    def setText(self, text):

        self.plainText.appendPlainText(text)
        self.plainText.setUndoRedoEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dispInfo = diagramInfo(sys.argv[1], sys.argv[2])
    dispInfo.show()
    sys.exit(app.exec())
