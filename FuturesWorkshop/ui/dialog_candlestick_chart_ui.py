# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_candlestick_chart.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogCandlestickChart(object):
    def setupUi(self, DialogCandlestickChart):
        DialogCandlestickChart.setObjectName("DialogCandlestickChart")
        DialogCandlestickChart.resize(800, 600)
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogCandlestickChart)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelCsvFile = QtWidgets.QLabel(DialogCandlestickChart)
        self.labelCsvFile.setObjectName("labelCsvFile")
        self.horizontalLayout.addWidget(self.labelCsvFile)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonLoad = QtWidgets.QPushButton(DialogCandlestickChart)
        self.buttonLoad.setObjectName("buttonLoad")
        self.horizontalLayout.addWidget(self.buttonLoad)
        self.buttonDraw = QtWidgets.QPushButton(DialogCandlestickChart)
        self.buttonDraw.setObjectName("buttonDraw")
        self.horizontalLayout.addWidget(self.buttonDraw)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.widgetCanvas = QtWidgets.QWidget(DialogCandlestickChart)
        self.widgetCanvas.setObjectName("widgetCanvas")
        self.verticalLayout.addWidget(self.widgetCanvas)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(DialogCandlestickChart)
        QtCore.QMetaObject.connectSlotsByName(DialogCandlestickChart)

    def retranslateUi(self, DialogCandlestickChart):
        _translate = QtCore.QCoreApplication.translate
        DialogCandlestickChart.setWindowTitle(_translate("DialogCandlestickChart", "CandlestickChart"))
        self.labelCsvFile.setText(_translate("DialogCandlestickChart", "<Package Path>\\temp\\SHFE.ag2102_Tick.csv"))
        self.buttonLoad.setText(_translate("DialogCandlestickChart", "Load"))
        self.buttonDraw.setText(_translate("DialogCandlestickChart", "Draw"))
