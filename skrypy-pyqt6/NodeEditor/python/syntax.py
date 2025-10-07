import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QTextCharFormat, QSyntaxHighlighter, QFont, QColor, QTextDocument
from PyQt6.QtCore import QRegularExpression


def format(color, style=''):
    """Return a QTextCharFormat with the given attributes."""
    _color = QColor()
    _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Weight.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


# Syntax styles that can be shared by all languages
STYLES = {
    'keyword': format('blue'),
    'operator': format('red'),
    'brace': format('darkGray'),
    'defclass': format('black', 'bold'),
    'string': format('magenta'),
    'string2': format('darkMagenta'),
    'comment': format('darkGreen', 'italic'),
    'self': format('black', 'italic'),
    'numbers': format('brown'),
}


class PythonHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for the Python language."""

    keywords = [
        'and', 'assert', 'break', 'class', 'continue', 'def',
        'del', 'elif', 'else', 'except', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in',
        'is', 'lambda', 'not', 'or', 'pass', 'print',
        'raise', 'return', 'try', 'while', 'yield',
        'None', 'True', 'False',
    ]

    operators = [
        '=', '==', '!=', '<', '<=', '>', '>=',
        '\\+', '-', '\\*', '/', '//', '\\%', '\\*\\*',
        '\\+=', '-=', '\\*=', '/=', '\\%=',
        '\\^', '\\|', '\\&', '\\~', '>>', '<<',
    ]

    braces = ['\\{', '\\}', '\\(', '\\)', '\\[', '\\]']

    def __init__(self, parent: QTextDocument) -> None:
        super().__init__(parent)

        self.tri_single = (QRegularExpression("'''"), 1, STYLES['string2'])
        self.tri_double = (QRegularExpression('"""'), 2, STYLES['string2'])

        rules = []

        rules += [(rf'\b{w}\b', 0, STYLES['keyword']) for w in PythonHighlighter.keywords]
        rules += [(o, 0, STYLES['operator']) for o in PythonHighlighter.operators]
        rules += [(b, 0, STYLES['brace']) for b in PythonHighlighter.braces]

        rules += [
            (r'\bself\b', 0, STYLES['self']),
            (r'\bdef\b\s+(\w+)', 1, STYLES['defclass']),
            (r'\bclass\b\s+(\w+)', 1, STYLES['defclass']),
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),
            (r'#[^\n]*', 0, STYLES['comment']),
        ]

        self.rules = [(QRegularExpression(pat), index, fmt) for pat, index, fmt in rules]

    def highlightBlock(self, text: str):
        self.tripleQuoutesWithinStrings = []

        for expression, nth, fmt in self.rules:
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                index = match.capturedStart(nth)
                length = len(match.captured(nth))
                self.setFormat(index, length, fmt)


        self.setCurrentBlockState(0)

        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text: str, delimiter: QRegularExpression, in_state: int, style: QTextCharFormat):
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        else:
            match = delimiter.match(text)
            if not match.hasMatch():
                return False
            start = match.capturedStart()
            add = match.capturedLength()

        while start >= 0:
            match = delimiter.match(text, start + add)
            if match.hasMatch():
                end = match.capturedStart()
                length = end - start + match.capturedLength()
                self.setCurrentBlockState(0)
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start
            self.setFormat(start, length, style)
            match = delimiter.match(text, start + length)
            if match.hasMatch():
                start = match.capturedStart()
            else:
                start = -1

        return self.currentBlockState() == in_state