# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Any, Dict, List, Tuple
from enum import Enum

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot

from .dialog_exchange_selector_ui import Ui_DialogExchangeSelector
from ..utility import get_exchange_name_list, get_exchange_symbol_by_name


class DialogExchangeSelector(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.result: List[str] = []
        self._ui = Ui_DialogExchangeSelector()
        self._ui.setupUi(self)

        for exchange_name in get_exchange_name_list():
            item_exchange_name = QtWidgets.QListWidgetItem(exchange_name)
            item_exchange_name.setCheckState(QtCore.Qt.Unchecked)
            self._ui.listExchange.addItem(item_exchange_name)

    def on_buttonBox_accepted(self) -> None:
        for index in range(self._ui.listExchange.count()):
            if self._ui.listExchange.item(index).checkState() == QtCore.Qt.Checked:
                self.result.append(get_exchange_symbol_by_name(self._ui.listExchange.item(index).text()))
        self.accept()
