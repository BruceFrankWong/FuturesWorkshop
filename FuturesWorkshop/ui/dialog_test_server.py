# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Any, Dict, List, Tuple
from enum import Enum
import csv

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread

from .dialog_test_server_ui import Ui_DialogTestServer


class ServerStatusEnum(Enum):
    Unload = 'Unload'
    Loading = 'Loading'
    Loaded = 'Loaded'
    Started = 'Started'
    Paused = 'Paused'
    Stopped = 'Stopped'


class LoadingThread(QThread):
    line_loaded = pyqtSignal(int, dict)
    all_lines_loaded = pyqtSignal(str, int)

    def __init__(self, csv_file: str):
        super().__init__()
        self.csv_file = csv_file

    def run(self):
        with open(self.csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            row: int = 0
            for line in reader:
                self.line_loaded.emit(row, line)
                # self.sleep(1)
                row += 1
        self.all_lines_loaded.emit(self.csv_file, row)


class DialogTestServer(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.loading_thread = None
        self._ui = Ui_DialogTestServer()
        self._ui.setupUi(self)
        self.status = ServerStatusEnum.Unload
        self.set_widget_enabled()

        column_width_of_table_position: List[int] = [
            155, 60, 60, 60, 60, 50, 60, 50, 50, 70, 80
        ]
        for i in range(len(column_width_of_table_position)):
            self._ui.tablePrice.setColumnWidth(i, column_width_of_table_position[i])

    def set_widget_enabled(self):
        """
        Change widgets enable followed by self.status
        :return: None
        """
        if self.status == ServerStatusEnum.Unload:
            self._ui.buttonLoad.setEnabled(True)
            self._ui.buttonRun.setEnabled(False)
            self._ui.buttonPause.setEnabled(False)
            self._ui.buttonStop.setEnabled(False)
            self._ui.labelDateStart.setEnabled(False)
            self._ui.dateStart.setEnabled(False)
            self._ui.labelTimeStart.setEnabled(False)
            self._ui.timeStart.setEnabled(False)
            self._ui.labelDateEnd.setEnabled(False)
            self._ui.dateEnd.setEnabled(False)
            self._ui.labelTimeEnd.setEnabled(False)
            self._ui.timeEnd.setEnabled(False)
        elif self.status == ServerStatusEnum.Loading:
            self._ui.buttonLoad.setEnabled(False)
            self._ui.buttonRun.setEnabled(False)
            self._ui.buttonPause.setEnabled(False)
            self._ui.buttonStop.setEnabled(False)
            self._ui.labelDateStart.setEnabled(False)
            self._ui.dateStart.setEnabled(False)
            self._ui.labelTimeStart.setEnabled(False)
            self._ui.timeStart.setEnabled(False)
            self._ui.labelDateEnd.setEnabled(False)
            self._ui.dateEnd.setEnabled(False)
            self._ui.labelTimeEnd.setEnabled(False)
            self._ui.timeEnd.setEnabled(False)
        elif self.status == ServerStatusEnum.Loaded:
            self._ui.buttonLoad.setEnabled(True)
            self._ui.buttonRun.setEnabled(True)
            self._ui.buttonPause.setEnabled(False)
            self._ui.buttonStop.setEnabled(False)
            self._ui.labelDateStart.setEnabled(True)
            self._ui.dateStart.setEnabled(True)
            self._ui.labelTimeStart.setEnabled(True)
            self._ui.timeStart.setEnabled(True)
            self._ui.labelDateEnd.setEnabled(True)
            self._ui.dateEnd.setEnabled(True)
            self._ui.labelTimeEnd.setEnabled(True)
            self._ui.timeEnd.setEnabled(True)
        elif self.status == ServerStatusEnum.Started:
            self._ui.buttonLoad.setEnabled(False)
            self._ui.buttonRun.setEnabled(False)
            self._ui.buttonPause.setEnabled(True)
            self._ui.buttonStop.setEnabled(True)
            self._ui.labelDateStart.setEnabled(False)
            self._ui.dateStart.setEnabled(False)
            self._ui.labelTimeStart.setEnabled(False)
            self._ui.timeStart.setEnabled(False)
            self._ui.labelDateEnd.setEnabled(False)
            self._ui.dateEnd.setEnabled(False)
            self._ui.labelTimeEnd.setEnabled(False)
            self._ui.timeEnd.setEnabled(False)
        elif self.status == ServerStatusEnum.Paused:
            self._ui.buttonLoad.setEnabled(False)
            self._ui.buttonRun.setEnabled(True)
            self._ui.buttonPause.setEnabled(False)
            self._ui.buttonStop.setEnabled(True)
            self._ui.labelDateStart.setEnabled(False)
            self._ui.dateStart.setEnabled(False)
            self._ui.labelTimeStart.setEnabled(False)
            self._ui.timeStart.setEnabled(False)
            self._ui.labelDateEnd.setEnabled(False)
            self._ui.dateEnd.setEnabled(False)
            self._ui.labelTimeEnd.setEnabled(False)
            self._ui.timeEnd.setEnabled(False)
        elif self.status == ServerStatusEnum.Stopped:
            self._ui.buttonLoad.setEnabled(True)
            self._ui.buttonRun.setEnabled(True)
            self._ui.buttonPause.setEnabled(False)
            self._ui.buttonStop.setEnabled(False)
            self._ui.labelDateStart.setEnabled(True)
            self._ui.dateStart.setEnabled(True)
            self._ui.labelTimeStart.setEnabled(True)
            self._ui.timeStart.setEnabled(True)
            self._ui.labelDateEnd.setEnabled(True)
            self._ui.dateEnd.setEnabled(True)
            self._ui.labelTimeEnd.setEnabled(True)
            self._ui.timeEnd.setEnabled(True)

    @pyqtSlot()
    def on_buttonLoad_clicked(self):
        str_csv_file, filter_type = QtWidgets.QFileDialog.getOpenFileName(
            self, '选择一个文件', QtCore.QDir.currentPath(), 'csv文件(*.csv)'
        )

        # Change widgets status.
        self.status = ServerStatusEnum.Loading
        self.set_widget_enabled()

        # Clear contents of QTableWidget.
        self._ui.tablePrice.clearContents()

        # Run the loading thread.
        self.loading_thread = LoadingThread(str_csv_file)
        self.loading_thread.line_loaded.connect(self.on_line_loaded)
        self.loading_thread.all_lines_loaded.connect(self.on_all_lines_loaded)
        self.loading_thread.start()

    @pyqtSlot(int, dict)
    def on_line_loaded(self, row: int, data: dict):
        # print('on_line_read: ', row, data)
        # Variable declear
        item: QtWidgets.QTableWidgetItem

        # Update progress label.
        self._ui.labelProgress.setText(f'正在加载第 {row} 行数据...')

        # Insert row in QTableWidget.
        self._ui.tablePrice.insertRow(row)

        item = QtWidgets.QTableWidgetItem(data['datetime'][:23])
        item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self._ui.tablePrice.setItem(row, 0, item)

        item = QtWidgets.QTableWidgetItem(data['last_price'])
        item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self._ui.tablePrice.setItem(row, 1, item)

        item = QtWidgets.QTableWidgetItem(data['highest'])
        item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self._ui.tablePrice.setItem(row, 2, item)

        item = QtWidgets.QTableWidgetItem(data['lowest'])
        item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self._ui.tablePrice.setItem(row, 3, item)

        item = QtWidgets.QTableWidgetItem(data['bid_price1'])
        item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self._ui.tablePrice.setItem(row, 4, item)

        item = QtWidgets.QTableWidgetItem(data['bid_volume1'])
        item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self._ui.tablePrice.setItem(row, 5, item)

        item = QtWidgets.QTableWidgetItem(data['ask_price1'])
        item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self._ui.tablePrice.setItem(row, 6, item)

        item = QtWidgets.QTableWidgetItem(data['ask_volume1'])
        item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self._ui.tablePrice.setItem(row, 7, item)

        item = QtWidgets.QTableWidgetItem(data['open_interest'])
        item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self._ui.tablePrice.setItem(row, 8, item)

        item = QtWidgets.QTableWidgetItem(data['volume'])
        item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self._ui.tablePrice.setItem(row, 9, item)

        item = QtWidgets.QTableWidgetItem(data['amount'])
        item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self._ui.tablePrice.setItem(row, 10, item)


    @pyqtSlot(str, int)
    def on_all_lines_loaded(self, file_name: str, row: int):
        self._ui.labelProgress.setText(f'加载完成，共 {row} 行。')
        self._ui.labelFile.setText(file_name)

        # Update progress label.
        self.status = ServerStatusEnum.Loaded
        self.set_widget_enabled()

    @pyqtSlot()
    def on_buttonRun_clicked(self):
        self.status = ServerStatusEnum.Started
        self.set_widget_enabled()

        # for i in range(self._ui.tablePrice.horizontalHeader().count()):
        #     print(i, self._ui.tablePrice.horizontalHeader().sectionSize(i))
        # print(self.width())

    @pyqtSlot()
    def on_buttonPause_clicked(self):
        self.status = ServerStatusEnum.Paused
        self.set_widget_enabled()

    @pyqtSlot()
    def on_buttonStop_clicked(self):
        self.status = ServerStatusEnum.Stopped
        self.set_widget_enabled()
