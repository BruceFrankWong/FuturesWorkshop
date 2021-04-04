# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from PyQt5 import QtCore
import pandas as pd


class ThreadLoadingCsv(QtCore.QThread):
    loading_started = QtCore.pyqtSignal(str)
    loading_progress = QtCore.pyqtSignal(str, int)
    loading_finished = QtCore.pyqtSignal(str, int)
    df: pd.DataFrame

    def __init__(self, file_name: str, parent=None):
        super().__init__(parent)
        self.file_name = file_name

    def run(self) -> None:
        chunk_size = 5000
        chunk_list = []

        self.loading_started.emit(self.file_name)

        count: int = 0
        with pd.read_csv(self.file_name, chunksize=chunk_size, parse_dates=['datetime']) as reader:
            for chunk in reader:
                chunk_list.append(chunk)
                count += len(chunk)
                self.loading_progress.emit(self.file_name, count)

        self.df = pd.concat(chunk_list)
        self.loading_finished.emit(self.file_name, self.df.shape[0])
