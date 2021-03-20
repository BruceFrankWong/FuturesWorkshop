# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from PyQt5 import QtCore, QtGui, QtWidgets

from .main_window_ui import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._ui.actionQuit.triggered.connect(QtWidgets.qApp.quit)
