import numpy as np


class printProbe():
    def __init__(self, unit, lab, format, label, val, console):

        col = ''

        if console:
            if 'int' in format:
                col = '#0064FF'
            elif 'float' in format:
                col = '#C86400'
            elif 'tuple' in format:
                col = '#B4B4B4'
            elif 'str' in format:
                col = '#c800FA'
            elif 'bool' in format:
                col = '#32FA32'
            elif 'path' in format:
                col = '#FF6464'
            elif 'dict' in format:
                col = '#C8FA00'
        else:
            if 'int' in format:
                col = '\x1b[38;2;0;100;255m'
            elif 'float' in format:
                col = '\x1b[38;2;200;100;0m'
            elif 'tuple' in format:
                col = '\x1b[38;2;200;180;180m'
            elif 'str' in format:
                col = '\x1b[38;2;200;0;250m'
            elif 'bool' in format:
                col = '\x1b[38;2;50;250;50m'
            elif 'path' in format:
                col = '\x1b[38;2;255;100;100m'
            elif 'dict' in format:
                col = '\x1b[38;2;200;250;0m'

        if label == 'Type':
            tmpval = val
            continued = True
            if isinstance(tmpval, list):
                if val:
                    if isinstance(tmpval[0], list):
                        while continued:
                            if isinstance(tmpval, list):
                                tmpval = tmpval[0]
                            else:
                                val = 'array of ' + type(tmpval).__name__
                                continued = False
                    else:
                        val = 'list of ' + type(tmpval[0]).__name__

            else:
                val = type(tmpval).__name__
                if callable(tmpval):
                    val += ' method'

        elif label == 'Length':
            if isinstance(val, list):
                if val:
                    tmptxt = '('
                    tmpval = val
                    continued = True
                    if isinstance(tmpval, list):
                        while continued:
                            if isinstance(tmpval, list):
                                tmptxt += str(len(tmpval))
                                tmpval = tmpval[0]
                                tmptxt += ', '
                            else:
                                continued = False
                                tmptxt = tmptxt[0:-2]+')'
                    else:
                        tmptxt = '1'
                    val = tmptxt
            elif type(val).__name__ in ['ndarray', 'memmap']:
                val = val.shape
            elif isinstance(val, tuple):
                val = len(val)
            else:
                val = '1'

        else:
            if callable(val):
                val = str(val)[1:-1]

        if console:
            console.append("<span style=\" \
                            font-family:'Monospace'; \
                            font-size:10pt; \
                            font-weight:400; \
                            color:{};\"> \
                            {} ({}) : {} = {} </span>".format(col, unit, lab, label, str(val)))
        else:
            self.return_for_ssh = [col, unit, lab, label, str(val)]

    def getList(self):
        return self.return_for_ssh
