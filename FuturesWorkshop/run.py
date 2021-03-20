# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


import sys

from PyQt5 import QtWidgets

from .ui import MainWindow


def run():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
