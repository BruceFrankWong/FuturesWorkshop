# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


import sys

from PyQt5 import QtWidgets

from FuturesWorkshop.ui.dialog_candlestick_chart import DialogCandlestickChart


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = DialogCandlestickChart()
    main_window.show()
    sys.exit(app.exec_())
