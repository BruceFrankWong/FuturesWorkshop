# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Any, Dict, List
import copy

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot

from .dialog_preference_ui import Ui_DialogPreference
from ..config import CONFIGS, load_config, save_config
from ..utility import get_exchange_symbol_by_name, get_product_name_by_symbol


class DialogPreference(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._ui = Ui_DialogPreference()
        self._ui.setupUi(self)

        self.column_width_of_table_position: List[int] = [
            110, 50, 60, 50, 40, 40
        ]
        for i in range(len(self.column_width_of_table_position)):
            self._ui.tableProduct.setColumnWidth(i, self.column_width_of_table_position[i])

        self.configs_backup: Dict[str, Any] = copy.deepcopy(CONFIGS)

        self._ui.listExchange.clear()
        for item in self.configs_backup['exchange']['info']:
            widget_item = QtWidgets.QListWidgetItem(item['name'])
            self._ui.listExchange.addItem(widget_item)

        self._ui.tableProduct.cellChanged.connect(self.on_modified)

    @pyqtSlot(QtWidgets.QListWidgetItem, QtWidgets.QListWidgetItem)
    def on_listExchange_currentItemChanged(self,
                                           current: QtWidgets.QListWidgetItem,
                                           previous: QtWidgets.QListWidgetItem):
        self._ui.tableProduct.cellChanged.disconnect(self.on_modified)
        exchange_symbol: str = get_exchange_symbol_by_name(current.text())
        row: int = 0
        self._ui.tableProduct.clearContents()
        self._ui.tableProduct.setRowCount(0)
        for i in range(len(self.column_width_of_table_position)):
            self._ui.tableProduct.setColumnWidth(i, self.column_width_of_table_position[i])
        product_symbol_list: List[str] = self.configs_backup['exchange'][exchange_symbol]
        for product_symbol in product_symbol_list:
            self._ui.tableProduct.insertRow(row)
            item = QtWidgets.QTableWidgetItem(get_product_name_by_symbol(product_symbol))
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self._ui.tableProduct.setItem(row, 0, item)
            item = QtWidgets.QTableWidgetItem(product_symbol)
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self._ui.tableProduct.setItem(row, 1, item)
            item = QtWidgets.QTableWidgetItem(str(self.configs_backup['product'][product_symbol]['fluctuation']))
            item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self._ui.tableProduct.setItem(row, 2, item)
            item = QtWidgets.QTableWidgetItem(str(self.configs_backup['product'][product_symbol]['multiplier']))
            item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self._ui.tableProduct.setItem(row, 3, item)
            item = QtWidgets.QTableWidgetItem(str(self.configs_backup['stop_loss'][product_symbol]['long']))
            item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            self._ui.tableProduct.setItem(row, 4, item)
            item = QtWidgets.QTableWidgetItem(str(self.configs_backup['stop_loss'][product_symbol]['short']))
            item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            self._ui.tableProduct.setItem(row, 5, item)
            row += 1
        self._ui.tableProduct.cellChanged.connect(self.on_modified)

    def on_modified(self, row: int, column: int):
        product_symbol: str = self._ui.tableProduct.item(row, 1).text()
        long_or_short: str = 'long' if column == 4 else 'short'
        self.configs_backup['stop_loss'][product_symbol][long_or_short] = int(
            self._ui.tableProduct.item(row, column).text()
        )

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        CONFIGS.update(self.configs_backup)
        save_config()

    @pyqtSlot()
    def on_buttonBox_rejected(self):
        self.configs_backup = copy.deepcopy(CONFIGS)
