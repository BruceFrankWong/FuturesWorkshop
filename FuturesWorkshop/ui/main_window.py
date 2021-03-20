# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from PyQt5 import QtCore, QtGui, QtWidgets

from .main_window_ui import Ui_MainWindow
from .dialog_preference import DialogPreference


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._ui.actionPreference.triggered.connect(self.show_dialog_preference)
        self._ui.actionQuit.triggered.connect(QtWidgets.qApp.quit)

    def show_dialog_preference(self):
        dialog_preference = DialogPreference(self)
        dialog_preference.show()
