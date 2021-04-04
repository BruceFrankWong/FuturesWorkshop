# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Dict, List

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot

from .dialog_product_selector_ui import Ui_DialogProductSelector
from ..config import CONFIGS
from ..utility import (
    get_exchange_name_list,
    get_exchange_symbol_by_name,
    get_product_symbol_list,
    get_product_name_by_symbol
)


class DialogProductSelector(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._ui = Ui_DialogProductSelector()
        self._ui.setupUi(self)

        self.result: List[str] = []

        # Initialize <self.product_check_dict>.
        self.product_check_dict: Dict[str, bool] = {}
        for product_symbol in get_product_symbol_list():
            self.product_check_dict[product_symbol] = False

        # Set column width of tableProduct.
        self.column_width_of_table_product: List[int] = [
            25, 120, 60
        ]
        for i in range(len(self.column_width_of_table_product)):
            self._ui.tableProduct.setColumnWidth(i, self.column_width_of_table_product[i])

        # Load items of listExchange.
        for exchange_name in get_exchange_name_list():
            item_exchange_name = QtWidgets.QListWidgetItem(exchange_name)
            self._ui.listExchange.addItem(item_exchange_name)

    def save_check_status(self):
        # Save selected item into self.result
        for i in range(self._ui.tableProduct.rowCount()):
            if self._ui.tableProduct.item(i, 0).checkState() == QtCore.Qt.Checked:
                self.product_check_dict[
                    self._ui.tableProduct.item(i, 2).text()
                ] = True

    @pyqtSlot(QtWidgets.QListWidgetItem, QtWidgets.QListWidgetItem)
    def on_listExchange_currentItemChanged(self,
                                           current: QtWidgets.QListWidgetItem,
                                           previous: QtWidgets.QListWidgetItem):
        self.save_check_status()

        exchange_symbol: str = get_exchange_symbol_by_name(current.text())
        row: int = 0
        self._ui.tableProduct.clearContents()
        self._ui.tableProduct.setRowCount(0)

        product_symbol_list: List[str] = CONFIGS['exchange'][exchange_symbol]
        for product_symbol in product_symbol_list:
            self._ui.tableProduct.insertRow(row)

            item = QtWidgets.QTableWidgetItem('')
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self._ui.tableProduct.setItem(row, 0, item)

            item = QtWidgets.QTableWidgetItem(get_product_name_by_symbol(product_symbol))
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self._ui.tableProduct.setItem(row, 1, item)

            item = QtWidgets.QTableWidgetItem(product_symbol)
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self._ui.tableProduct.setItem(row, 2, item)

            row += 1

    def on_buttonBox_accepted(self) -> None:
        self.save_check_status()

        for k, v in self.product_check_dict.items():
            print(k, v)
            if v:
                self.result.append(k)
        self.accept()
