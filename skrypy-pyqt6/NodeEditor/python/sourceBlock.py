##########################################################################
# mriWorks - Copyright (C) IRMAGE/INSERM, 2020
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# https://cecill.info/licences/Licence_CeCILL_V2-en.html
# for details.
##########################################################################

from NodeEditor.python.syntax import PythonHighlighter
from PyQt6.QtGui import QFont, QFontMetrics
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QDialog, QScrollArea, QTextEdit
import importlib
import inspect


class seeCode(QDialog):
    def __init__(self, category, nameClass, parent=None):
        super(seeCode, self).__init__(parent)

        imp = importlib.import_module('NodeEditor.modules.' + category)
        importlib.reload(imp)
        MyClass = getattr(imp, nameClass)

        src = inspect.getsource(MyClass)

        # nb_line = QTextEdit()
        # txt_nb = [str(x) for x in range(1+len(src.splitlines()))]
        # nb_line.setText('\n'.join(txt_nb))

        self.setWindowTitle('Source code of ' + nameClass)
        layout = QHBoxLayout()
        txt = QTextEdit()
        txt.setReadOnly(True)
        txt.setPlainText(src)
        PythonHighlighter(txt)
        font = txt.document().defaultFont()
        fontMetrics = QFontMetrics(font)
        textSize = fontMetrics.size(0, txt.toPlainText())
        w = textSize.width() + 10
        h = 250
        txt.setMinimumSize(w, h)
        txt.resize(w, h)

        # layout.addWidget(nb_line)
        layout.addWidget(txt)
        self.setLayout(layout)
        self.setMinimumWidth(w + 50)


class getDocString():
    def __init__(self, category, nameClass, parent=None):
        self.src = ''
        modul = 'NodeEditor.modules.' + category
        imp = importlib.import_module(modul)
        importlib.reload(imp)
        try:
            MyClass = getattr(imp, nameClass)
        except Exception as err:
            print("this bloc doesn't exist or is moved")
            return

        if 'Nipype' in category and 'Config_nipype' not in category:
            try:
                modul2 = category.replace('_', '.', 1).lower()
                imp2 = importlib.import_module(modul2)
                # importlib.reload(imp2)
                nameClass2 = nameClass[nameClass.index('_') + 1:]
                MyClass2 = getattr(imp2, nameClass2)
                nip = True
                self.src = MyClass2.help(True)
                sub_src_1 = self.subtext('', self.src)
                sub_src_2 = self.subtext('Inputs::', self.src)
                sub_src_2 = sub_src_2.replace('[Mandatory]', '')
                sub_src_3 = self.subtext('Outputs::', self.src)
                sub_src_1 = "\n".join([ll.rstrip() for ll in sub_src_1.splitlines() if ll.strip()])
                sub_src_2 = "\n".join([ll.rstrip() for ll in sub_src_2.splitlines() if ll.strip()])
                sub_src_3 = "\n".join([ll.rstrip() for ll in sub_src_3.splitlines() if ll.strip()])
                self.src = '\n' + sub_src_1 + '\n\n' + sub_src_2 + '\n\n' + sub_src_3
            except Exception as err:
                print(err)

        self.src += '\n' + str(MyClass.__doc__)

        if not self.src:
            self.src = 'No docstring'

    def subtext(self, label, src):
        lst = ['Example', 'Inputs::', '[Optional]', 'Outputs::', 'References']
        result = src
        if label != '':
            lst.remove(label)
        result = result[result.index(label):]
        for i in lst:
            try:
                result = result[:result.index(i)]
            except Exception as err:
                pass
        return result

    def getComment(self):
        return self.src
