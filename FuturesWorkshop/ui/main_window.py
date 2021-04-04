# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Any, List
from enum import Enum

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
import finplot as fplt
import pandas as pd

from .main_window_ui import Ui_MainWindow
from .dialog_preference import DialogPreference
from .dialog_exchange_selector import DialogExchangeSelector
from .dialog_product_selector import DialogProductSelector
from .thread import ThreadLoadingCsv


class MainWindowStatusEnum(Enum):
    Ready = 'Ready'
    Unload = 'Unload'
    Loading = 'Loading'
    Loaded = 'Loaded'
    Started = 'Started'
    Paused = 'Paused'
    Stopped = 'Stopped'


class MainWindow(QtWidgets.QMainWindow):
    df: pd.DataFrame
    thread_loading: QtCore.QThread

    data_updated: QtCore.pyqtSignal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self.init_chart()

        self.plot_list = []
        self.is_busy: bool = False
        self.status: MainWindowStatusEnum = MainWindowStatusEnum.Unload
        self.on_status_changed()

        self._ui.actionQuit.triggered.connect(QtWidgets.qApp.quit)
        self.data_updated.connect(self.on_data_updated)

    def init_chart(self):
        canvas = QtWidgets.QGraphicsView()
        ax = fplt.create_plot(init_zoom_periods=10)
        print(type(ax))
        canvas.axs = [ax]
        self._ui.centralLayout.addWidget(ax.vb.win, 1, 0, 1, 2)
        canvas.show()

    def on_data_updated(self):
        price = self.df['datetime open close high low'.split()]
        if not self.plot_list:
            self.plot_list.append(fplt.candlestick_ochl(price))
        else:
            self.plot_list[0].update_data(price)

    def on_status_changed(self):
        if not self.is_busy:
            self._ui.statusbar.showMessage('就绪')
        if self.status == MainWindowStatusEnum.Unload:
            self._ui.actionRun.setEnabled(False)
        elif self.status == MainWindowStatusEnum.Loaded:
            self._ui.statusbar.showMessage('加载完成')
            self._ui.actionRun.setEnabled(True)

    @pyqtSlot()
    def on_actionPreference_triggered(self):
        dialog = DialogPreference(self)
        dialog.show()

    @pyqtSlot()
    def on_actionLoad_triggered(self):
        dialog = QtWidgets.QFileDialog(self, '选择一个文件', QtCore.QDir.currentPath(), 'csv文件(*.csv)')
        if dialog.exec_():
            str_csv_file: str = dialog.selectedFiles()[0]

            self.thread_loading = ThreadLoadingCsv(str_csv_file)
            self.thread_loading.loading_started.connect(self.on_loading_started)
            self.thread_loading.loading_progress.connect(self.on_loading_progress)
            self.thread_loading.loading_finished.connect(self.on_loading_finished)
            self.thread_loading.start()

        dialog.destroy()

    @pyqtSlot()
    def on_actionCrawl_triggered(self):
        dialog = DialogExchangeSelector(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            exchange_selected: List[str] = dialog.result
            dialog.destroy()
            print(exchange_selected)

    @pyqtSlot()
    def on_actionDownload_triggered(self):
        dialog = DialogProductSelector(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            product_selected: List[str] = dialog.result
            dialog.destroy()
            print(product_selected)

    @pyqtSlot(str)
    def on_loading_started(self, file_name: str):
        self._ui.statusbar.showMessage(f'{file_name} 加载开始 ...')
        self.setCursor(QtCore.Qt.WaitCursor)
        self.update()

    @pyqtSlot(str, int)
    def on_loading_progress(self, file_name: str, lines_loaded: int):
        self._ui.statusbar.showMessage(f'{file_name} 加载中，已加载 {lines_loaded} 行 ...')
        self.update()

    @pyqtSlot(str, int)
    def on_loading_finished(self, file_name: str, lines_loaded: int):
        self._ui.statusbar.showMessage(f'{file_name} 加载完成，共 {lines_loaded} 行。')
        self.setCursor(QtCore.Qt.ArrowCursor)
        self.update()
        self.df = self.thread_loading.df
        print(self.df.dtypes)
        # self.df['datetime'] = pd.Timestamp(self.df['datetime'])
        self.data_updated.emit()
