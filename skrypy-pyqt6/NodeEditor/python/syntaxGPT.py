import sys
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
from PyQt6.QtWidgets import QApplication, QPlainTextEdit

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.rules = []

        # Python keywords
        keywords = [
            "and","as","assert","break","class","continue","def","del","elif","else",
            "except","False","finally","for","from","global","if","import","in","is",
            "lambda","None","nonlocal","not","or","pass", "print", "raise","return","True",
            "try","while","with","yield"
        ]

        kw_pattern = r'\b(' + '|'.join(keywords) + r')\b'
        kw_fmt = QTextCharFormat()
        kw_fmt.setForeground(QColor("blue"))
        # kw_fmt.setFontWeight(QFont.Weight.Bold)
        self.rules.append((QRegularExpression(kw_pattern), kw_fmt))

        # chaînes simples (guillemets simples ou doubles)
        str_fmt = QTextCharFormat()
        str_fmt.setForeground(QColor("magenta"))
        self.rules.append((QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'), str_fmt))
        self.rules.append((QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'"), str_fmt))

        # commentaires (du # à la fin de la ligne)
        com_fmt = QTextCharFormat()
        com_fmt.setForeground(QColor("darkGreen"))
        self.rules.append((QRegularExpression(r'#.*'), com_fmt))

        # nombres (entiers / flottants simples)
        num_fmt = QTextCharFormat()
        num_fmt.setForeground(QColor("darkRed"))
        self.rules.append((QRegularExpression(r'\b\d+(\.\d+)?\b'), num_fmt))

    def highlightBlock(self, text: str) -> None:
        # highlightBlock est appelé pour chaque bloc (ligne). les positions sont relatives à `text`.
        for pattern, fmt in self.rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                m = it.next()
                start = m.capturedStart(0)
                length = m.capturedLength(0)
                if length > 0:
                    self.setFormat(start, length, fmt)