import sys
from PyQt6 import QtCore, QtGui, QtWidgets


def format(color, style=''):
    """Return a QTextCharFormat with the given attributes."""
    _color = QtGui.QColor()
    _color.setNamedColor(color)

    _format = QtGui.QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QtGui.QFont.Weight.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)
    return _format


# Syntax styles
STYLES = {
    'keyword': format('blue'),
    'operator': format('red'),
    'brace': format('darkGray'),
    'defclass': format('black', 'bold'),
    'string': format('magenta'),
    'string2': format('magenta'),  # same colrr for triple quotes
    'comment': format('darkGreen', 'italic'),
    'self': format('black', 'italic'),
    'numbers': format('brown'),
}


class PythonHighlighter(QtGui.QSyntaxHighlighter):
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

    def __init__(self, parent: QtGui.QTextDocument) -> None:
        super().__init__(parent)

        # Multi-line string delimiters
        self.tri_single = (QtCore.QRegularExpression("'''"), 1, STYLES['string2'])
        self.tri_double = (QtCore.QRegularExpression('"""'), 2, STYLES['string2'])

        # Highlighting rules
        rules = []
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
                  for w in PythonHighlighter.keywords]
        rules += [(r'%s' % o, 0, STYLES['operator'])
                  for o in PythonHighlighter.operators]
        rules += [(r'%s' % b, 0, STYLES['brace'])
                  for b in PythonHighlighter.braces]

        rules += [
            (r'\bself\b', 0, STYLES['self']),
            (r'\bdef\b\s*(\w+)', 1, STYLES['defclass']),
            (r'\bclass\b\s*(\w+)', 1, STYLES['defclass']),
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),
            (r'#[^\n]*', 0, STYLES['comment']),
        ]

        self.rules = [(QtCore.QRegularExpression(pat), index, fmt)
                      for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text."""
        for expression, nth, fmt in self.rules:
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                index = match.capturedStart(nth)
                length = match.capturedLength(nth)
                self.setFormat(index, length, fmt)

        self.setCurrentBlockState(0)

        # Handling multi-line and unclosed strings
        in_multiline = (
            self.match_multiline(text, *self.tri_single) or self.match_multiline(text, *self.tri_double)
        )

        # Fix: Detects unclosed single strings
        if not in_multiline:
            single_quote_index = text.find("'")
            double_quote_index = text.find('"')

            # Détecte les guillemets ouverts sans fermeture sur la même ligne
            if single_quote_index != -1 and text.count("'", single_quote_index) % 2 == 1:
                self.setFormat(single_quote_index, len(text) - single_quote_index, STYLES['string'])
            elif double_quote_index != -1 and text.count('"', double_quote_index) % 2 == 1:
                self.setFormat(double_quote_index, len(text) - double_quote_index, STYLES['string'])

    def match_multiline(self, text, delimiter, in_state, style):
        """
        Handle highlighting of multi-line strings.
        Returns True if we're still inside a multi-line string.
        """
        start = 0
        if self.previousBlockState() != in_state:
            # Not already inside a multi-line string
            match_iter = delimiter.globalMatch(text)
            starts = []
            while match_iter.hasNext():
                match = match_iter.next()
                starts.append(match.capturedStart())

            if not starts:
                return False  # No delimiter on this line

            # Only start from first occurrence
            start = starts[0]
        else:
            start = 0

        while start < len(text):
            match_iter = delimiter.globalMatch(text, start + 3)
            end = -1
            while match_iter.hasNext():
                match = match_iter.next()
                end = match.capturedStart()
                break

            if end >= 0:
                length = end - start + 3
                self.setFormat(start, length, style)
                self.setCurrentBlockState(0)
                start = end + 3
            else:
                self.setFormat(start, len(text) - start, style)
                self.setCurrentBlockState(in_state)
                return True

        return False
