# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


import csv

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
import pandas as pd

from .dialog_test_server_ui import Ui_DialogTestServer


class DialogTestServer(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._ui = Ui_DialogTestServer()
        self._ui.setupUi(self)

        # self._ui.buttonLoad.clicked.connect(self.on_buttonLoad_clicked)
        # self._ui.buttonRun.clicked.connect(self.on_buttonRun_clicked)
        # self._ui.buttonPause.clicked.connect(self.on_buttonPause_clicked)
        # self._ui.buttonStop.clicked.connect(self.on_buttonStop_clicked)

    @pyqtSlot()
    def on_buttonLoad_clicked(self):
        csv_file, filter_type = QtWidgets.QFileDialog.getOpenFileName(
            self, '选择一个文件', QtCore.QDir.currentPath(), 'csv文件(*.csv)'
        )
        self._ui.labelFile.setText(csv_file)
        self._ui.tablePrice.clearContents()
        # df: pd.DataFrame = pd.read_csv(csv_file)
        # for i in range(df.size):
        #     item = QtWidgets.QTableWidgetItem()

    @pyqtSlot()
    def on_buttonRun_clicked(self):
        pass

    @pyqtSlot()
    def on_buttonPause_clicked(self):
        pass

    @pyqtSlot()
    def on_buttonStop_clicked(self):
        pass
