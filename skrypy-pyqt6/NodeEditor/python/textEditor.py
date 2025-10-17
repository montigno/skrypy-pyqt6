import sys
import re
import os

from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QAction, QIcon,\
    QColor, QFont
from PyQt6.QtWidgets import QMainWindow, QToolBar, QMessageBox, QStatusBar,\
    QTextEdit
from PyQt6.QtCore import QSize


class BashHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#007acc"))
        keyword_format.setFontWeight(QFont.Weight.Bold)
        keywords = ["echo", "ls", "cd", "cat", "grep"]

        self.rules = [(re.compile(rf"\b{kw}\b"), keyword_format) for kw in keywords]

        # Format des commentaires
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#008000"))

        self.rules.append((re.compile(r"#.*"), comment_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            for match in pattern.finditer(text):
                start, end = match.span()
                self.setFormat(start, end - start, fmt)


class TextEditor(QMainWindow):
    def __init__(self, parent=None):
        super(TextEditor, self).__init__(parent)

        self.setWindowTitle("Editor")
        self.setGeometry(200, 200, 800, 600)

        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        # Ajouter le coloriseur syntaxique
        # self.highlighter = PythonHighlighter(self.text_edit.document())
        self.highlighter = BashHighlighter(self.text_edit.document())

        self.current_file = self.getEnvFile()
        self.modifie = False

        # self.creer_menu()
        self.menu_toolbar()
        self.create_statusbar()
        self.open_file()

        self.text_edit.textChanged.connect(self.on_text_changed)
        
    def getEnvFile(self):
        env_file = os.path.expanduser('~')
        env_file = os.path.join(env_file, '.skrypy', 'env_parameters.txt')
        return env_file
        
    def menu_toolbar(self):
        toolbar = QToolBar("Tools Bar")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)

        save_action = QAction(QIcon.fromTheme("document-save"), "Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)

        undo_action = QAction(QIcon.fromTheme("edit-undo"), "Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.text_edit.undo)

        redo_action = QAction(QIcon.fromTheme("edit-redo"), "Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.text_edit.redo)
        
        quit_action = QAction(QIcon.fromTheme("application-exit"), "Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)

        toolbar.addAction(save_action)
        toolbar.addSeparator()
        toolbar.addAction(undo_action)
        toolbar.addAction(redo_action)
        toolbar.addAction(quit_action)
        
    def create_statusbar(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Ready")
        
    def open_file(self):
        if self.current_file:
            try:
                with open(self.current_file, 'r', encoding='utf-8') as f:
                    contenu = f.read()
                self.text_edit.setPlainText(contenu)
                # self.current_file = chemin
                self.modifie = False
                self.status.showMessage(f"File opened : {self.current_file}")
                self.setWindowTitle(f"Editor - {self.current_file}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Unable to open file :\n{e}")
        
    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(self.text_edit.toPlainText())
                self.modifie = False
                self.status.showMessage(f"File saved: {self.current_file}")
                titre = self.windowTitle()
                if titre.endswith("*"):
                    self.setWindowTitle(titre[:-1])
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Unable to save :\n{e}")
        else:
            self.current_file = self.getEnvFile()
            self.save_as()
            
    def save_as(self):
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(self.text_edit.toPlainText())
                # self.current_file = chemin
                self.modifie = False
                self.status.showMessage(f"File saved : {self.current_file}")
                self.setWindowTitle(f"Editor - {self.current_file}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Unable to save :\n{e}")
            
    def on_text_changed(self):
        if not self.modifie:
            self.modifie = True
            titre = self.windowTitle()
            if not titre.endswith("*"):
                self.setWindowTitle(titre + " *")
            self.status.showMessage("Modified")
            
    def closeEvent(self, event):
        if self.modifie:
            reponse = QMessageBox.question(
                self, "Quitter",
                "The document contains unsaved changes.\nSave before exiting ?",
                QMessageBox.Icon.Yes | QMessageBox.Icon.No | QMessageBox.Icon.Cancel
            )
            if reponse == QMessageBox.Icon.Yes:
                self.save_file()
            elif reponse == QMessageBox.Icon.Cancel:
                event.ignore()
                return
        event.accept()
        
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = TextEditor()
#     window.show()
#     sys.exit(app.exec_())
