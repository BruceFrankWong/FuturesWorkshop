# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Any, Dict, List
import copy

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot

from .dialog_preference_ui import Ui_DialogPreference
from ..config import CONFIGS, get_exchange_symbol_by_name, load_config, save_config


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
        for item in self.configs_backup['exchange']:
            widget_item = QtWidgets.QListWidgetItem(self.configs_backup[item]['name'])
            self._ui.listExchange.addItem(widget_item)

    @pyqtSlot(QtWidgets.QListWidgetItem, QtWidgets.QListWidgetItem)
    def on_listExchange_currentItemChanged(self,
                                           current: QtWidgets.QListWidgetItem,
                                           previous: QtWidgets.QListWidgetItem):
        exchange_symbol: str = get_exchange_symbol_by_name(current.text())
        row: int = 0
        self._ui.tableProduct.clearContents()
        self._ui.tableProduct.setRowCount(0)
        for i in range(len(self.column_width_of_table_position)):
            self._ui.tableProduct.setColumnWidth(i, self.column_width_of_table_position[i])
        for product in CONFIGS[exchange_symbol]['product']:
            self._ui.tableProduct.insertRow(row)
            item = QtWidgets.QTableWidgetItem(CONFIGS[exchange_symbol][product]['name'])
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self._ui.tableProduct.setItem(row, 0, item)
            item = QtWidgets.QTableWidgetItem(product)
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self._ui.tableProduct.setItem(row, 1, item)
            item = QtWidgets.QTableWidgetItem(str(CONFIGS[exchange_symbol][product]['fluctuation']))
            item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self._ui.tableProduct.setItem(row, 2, item)
            item = QtWidgets.QTableWidgetItem(str(CONFIGS[exchange_symbol][product]['multiplier']))
            item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self._ui.tableProduct.setItem(row, 3, item)
            item = QtWidgets.QTableWidgetItem(str(CONFIGS[exchange_symbol][product]['long']))
            item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            self._ui.tableProduct.setItem(row, 4, item)
            item = QtWidgets.QTableWidgetItem(str(CONFIGS[exchange_symbol][product]['short']))
            item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            self._ui.tableProduct.setItem(row, 5, item)
            row += 1

    @pyqtSlot(int, int)
    def on_tableProduct_cellDoubleClicked(self, row, column):
        print(f'row={row}, column={column}, value={self._ui.tableProduct.item(row, column).text()}')
        # exchange_symbol: str = get_exchange_symbol_by_name(self._ui.listExchange.currentItem().text())
        # product_symbol: str = self._ui.tableProduct.item(row, 1).text()
        # k: str = 'long' if column == 4 else 'short'
        # self.configs_backup[exchange_symbol][product_symbol][k] = self._ui.tableProduct.item(row, column).text()

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        save_config(self.configs_backup)
        CONFIGS.update(self.configs_backup)

    @pyqtSlot()
    def on_buttonBox_rejected(self):
        self.configs_backup = copy.deepcopy(CONFIGS)
