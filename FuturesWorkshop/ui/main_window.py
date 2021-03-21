# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Dict, List

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot

from .main_window_ui import Ui_MainWindow
from .dialog_preference import DialogPreference
from .dialog_test_server import DialogTestServer


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        column_width_of_table_position: List[int] = [
            130, 40, 60, 40, 60, 60, 60, 90
        ]
        for i in range(len(column_width_of_table_position)):
            self._ui.tablePosition.setColumnWidth(i, column_width_of_table_position[i])

        # hc: int = self._ui.tablePosition.horizontalHeader().count()
        # print(hc)
        # for i in range(hc):
        # self._ui.tablePosition.resizeColumnsToContents()
        for i in range(self._ui.tablePosition.horizontalHeader().count()):
            print(i, self._ui.tablePosition.horizontalHeader().sectionSize(i))

        # self._ui.actionTest.triggered.connect(self.show_dialog_test)
        # self._ui.actionPreference.triggered.connect(self.show_dialog_preference)
        self._ui.actionQuit.triggered.connect(QtWidgets.qApp.quit)

    @pyqtSlot()
    def on_actionPreference_triggered(self):
        dialog_preference = DialogPreference(self)
        dialog_preference.show()

    @pyqtSlot()
    def on_actionTest_triggered(self):
        dialog = DialogTestServer(self)
        dialog.show()
