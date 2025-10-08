from NodeEditor.python.Diagram_Editor import LoadDiagram, Diagram_excution
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication
from main import Project_Irmage
import os
import sys
import unittest
from PyQt6.QtGui import QDrag


class mri_worksTest(unittest.TestCase):
    '''Test the main GUI'''

    def setUp(self):
        '''Create the GUI'''
        self_dir_path = os.path.dirname(os.path.realpath(__file__))
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication([])

        self.form = Project_Irmage(self_dir_path)
        self.form.show()
        self.ui = self.form.t.wdg

    def tearDown(self):
        for i in reversed(range(5)):
            print('\r' + 'The test will stop in', i+1, 'second', end=' ', flush=True)
            QTest.qWait(1000)
        self.form.close()

    def test_defaults(self):
        '''Test the ToolBar'''
        actions1 = self.ui.menut.actions()
        print('QToolBar menus:')
        for action in actions1:
            print(" " * 5, action.text())
            QTest.mouseClick(self.ui, Qt.MouseButton.LeftButton)
        print()

        actions2 = self.ui.menub.actions()
#         print(self.ui.menub.__dict__.keys())
        print('QMenuBar menus:')
        for action in actions2:
            print(" " * 5, action.text())
            QTest.mouseClick(self.ui, Qt.MouseButton.LeftButton)
        openDgr_act = self.ui.menub.menuDgr.actions()[1].text()
        QTest.mouseClick(self.ui, Qt.MouseButton.LeftButton)
        print()

        print('QPushButton:')
        print(" " * 5, 'main menu')
        QTest.mouseClick(self.ui.button_mainMenu, Qt.MouseButton.LeftButton)
        print(" " * 5, 'collapse')
        QTest.mouseClick(self.ui.coll_lib, Qt.MouseButton.LeftButton)
        print(" " * 5, 'expand')
        QTest.mouseClick(self.ui.exp_lib, Qt.MouseButton.LeftButton)
        print()

        print('Block search')
        self.ui.searchField.setText("fsl_FLIRT")
        self.ui.searchCurrent()
        self.ui.searchResult()
        print()

        # print('test drag & drop')
        # tabCurrent = self.ui.scrollTools.widget()
        # model = tabCurrent.model()
        # root = model.invisibleRootItem()
        # index = tabCurrent.selectedIndexes()[0]
        # print(model, root, index)
        # drag = QDrag()
        # mimeData = QMimeData()
        # mimeData.setData(index)
        # drag.setMimeData(mimeData)

        # curr_dir_path = os.path.dirname(os.path.realpath(__file__))
        # rep_test = os.path.join(curr_dir_path,
        #                         'NodeEditor',
        #                         'testUnits')
        # files_test = [os.path.join(rep_test, f) for f in os.listdir(rep_test) if os.path.isfile(os.path.join(rep_test, f))]
        # for file_test in files_test:
        #     if file_test.endswith(".dgr"):
        #         print('test file :', file_test)
        #         self.ui.addSubWindow(os.path.basename(file_test))
        #         f = open(file_test, 'r', encoding='utf8')
        #         txt = f.readlines()
        #         f.close()
        #         LoadDiagram(txt)
        #         self.ui.diagramView[self.ui.currentTab].fitInView(self.ui.diagramScene[self.ui.currentTab].sceneRect(),
        #                                                           Qt.AspectRatioMode.KeepAspectRatio)
        #         self.ui.diagramView[self.ui.currentTab].scale(0.8, 0.8)
        #         self.ui.diagramView[self.ui.currentTab].scene().clearSelection()
        #         self.ui.currentpathwork = file_test
        #         Diagram_excution(self.ui.mdi.currentSubWindow().windowTitle(), True)
        #         # Diagram_excution(self.ui.
        #         #                  tabsDiagram.
        #         #                  tabText(self.ui.currentTab), True)


if __name__ == "__main__":
    unittest.main()
