# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Any, Dict, List
import copy

import pandas as pd
from PyQt5.QtCore import (
    Qt,
    pyqtSlot,
    QDir,
    QFileInfo,
    QDateTime,
    QDate,
    QPoint,
    QPointF,
    QRectF
)
from PyQt5.QtGui import (
    QPen,
    QPainter,
    QPicture,
    QBrush,
    QStandardItemModel,
    QStandardItem,
    QMouseEvent,
    QPaintEvent
)
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QSplitter
import pyqtgraph as pg

from .dialog_candlestick_chart_ui import Ui_DialogCandlestickChart
from ..config import PACKAGE_PATH


class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data: pd.DataFrame):
        super().__init__()
        self.data: pd.DataFrame = data
        print(self.data)
        print(self.data.info())
        self.picture = QPicture()
        self.generate()

    def generate(self):
        painter = QPainter(self.picture)
        painter.setPen(pg.mkPen('w'))
        w = 1.0 / 3.0
        for i in range(self.data.shape[0]):
            if self.data.at[i, 'close'] > self.data.at[i, 'open']:
                painter.setPen(pg.mkPen('g'))
                painter.setBrush(pg.mkBrush('g'))
            elif self.data.at[i, 'close'] < self.data.at[i, 'open']:
                painter.setPen(pg.mkPen('r'))
                painter.setBrush(pg.mkBrush('r'))
            else:
                painter.setPen(pg.mkPen('w'))
                painter.setBrush(pg.mkBrush('w'))
            painter.drawLine(
                QPointF(i, self.data.at[i, 'low']), QPointF(i, self.data.at[i, 'high'])
            )
            painter.drawRect(
                QRectF(i - w, self.data.at[i, 'open'], w * 2, self.data.at[i, 'close'] - self.data.at[i, 'open'])
            )
        painter.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QRectF(self.picture.boundingRect())


class BarGraph(pg.BarGraphItem):
    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self.df = df

    def mouseClickEvent(self, event):
        print("clicked")


class DialogCandlestickChart(QDialog):
    candlestick_item: CandlestickItem

    def __init__(self, parent=None):
        super().__init__(parent)
        self._ui = Ui_DialogCandlestickChart()
        self._ui.setupUi(self)

        self._init_chart()

        self._ui.buttonDraw.setEnabled(False)

        self.cursor_position: QPoint = QPoint(0, 0)

        # Max stick width
        self.width_max = 39
        self.space_max = 4
        self.width_min = 3
        self.space_min = 1

        # self._init_chart()

        # self._ui.chartCandlestick.mouseMoveEvent.connect(self.on_chartCandlestick_mouseMoveEvent)
        # self._ui.chartCandlestick.paintEvent.connect(self._ui.chartCandlestick.on_paintEvent)

        self._ui.buttonLoad.clicked.connect(self.load_data)
        self._ui.buttonDraw.clicked.connect(self._draw)

    def _init_chart(self):
        # WidgetCanvas and its layout.
        self._ui.layout_canvas = QVBoxLayout(self._ui.widgetCanvas)
        self._ui.layout_canvas.setObjectName('chart_layout')
        self._ui.layout_canvas.setContentsMargins(0, 0, 0, 0)
        self._ui.layout_canvas.setSpacing(0)
        self._ui.widgetCanvas.setLayout(self._ui.layout_canvas)

        # Main Splitter
        self._ui.splitter_main = QSplitter(self._ui.widgetCanvas)
        self._ui.splitter_main.setObjectName('splitter_main')
        self._ui.splitter_main.setOrientation(Qt.Vertical)
        self._ui.splitter_main.setHandleWidth(0)

        # Add MainSplitter into layout_canvas.
        self._ui.layout_canvas.addWidget(self._ui.splitter_main)

        # MainCanvas, and its layouts.
        self._ui.widget_main_canvas = QWidget(self._ui.splitter_main)
        self._ui.widget_main_canvas.setObjectName('widget_main_canvas')

        self._ui.layout_main_canvas = QVBoxLayout(self._ui.widget_main_canvas)
        self._ui.layout_main_canvas.setObjectName('layout_main_canvas')
        self._ui.layout_main_canvas.setContentsMargins(0, 0, 0, 0)
        self._ui.layout_main_canvas.setSpacing(0)

        self._ui.widget_main_canvas.setLayout(self._ui.layout_main_canvas)

        # AttachedCanvas, and its layouts.
        self._ui.widget_attached_canvas = QWidget(self._ui.splitter_main)
        self._ui.widget_attached_canvas.setObjectName('widget_attached_canvas')

        self._ui.layout_attached_canvas = QVBoxLayout(self._ui.widget_attached_canvas)
        self._ui.layout_attached_canvas.setObjectName('layout_attached_canvas')
        self._ui.layout_attached_canvas.setContentsMargins(0, 0, 0, 0)
        self._ui.layout_attached_canvas.setSpacing(0)

        self._ui.widget_attached_canvas.setLayout(self._ui.layout_attached_canvas)

        # Add widget_main_canvas and widget_attached_canvas into splitter_main.
        self._ui.splitter_main.addWidget(self._ui.widget_main_canvas)
        self._ui.splitter_main.addWidget(self._ui.widget_attached_canvas)
        self._ui.splitter_main.setSizes([3, 2])

        # Attached Splitter.
        self._ui.splitter_attached = QSplitter(self._ui.widget_attached_canvas)
        self._ui.splitter_attached.setObjectName('splitter_attached_1')
        self._ui.splitter_attached.setOrientation(Qt.Vertical)
        self._ui.splitter_attached.setHandleWidth(0)
        self._ui.layout_attached_canvas.addWidget(self._ui.splitter_attached)

        # Main Chart.
        self.chart_main = pg.PlotWidget(
            parent=self._ui.widget_main_canvas,
            name='ChartMain',
            title='<span style="font-size: 10pt" justify="left">SHFE, ag 2101'
        )
        self.chart_main.setAntialiasing(True)
        self._ui.layout_main_canvas.addWidget(self.chart_main)

        # Attached Chart.
        self.chart_volume = pg.PlotWidget(
            parent=self._ui.splitter_attached,
            name='ChartVolume',
            title='<span style="font-size: 10pt" justify="left">volume'
        )

        self.chart_macd = pg.PlotWidget(
            parent=self._ui.splitter_attached,
            name='ChartMACD',
            title='<span style="font-size: 10pt" justify="left">MACD'
        )

        # Add attached charts into splitter_attached.
        self._ui.splitter_attached.addWidget(self.chart_volume)
        self._ui.splitter_attached.addWidget(self.chart_macd)
        self._ui.splitter_attached.setSizes([1, 1])

    def load_data(self):
        self.setCursor(Qt.WaitCursor)
        self._ui.buttonLoad.setEnabled(False)
        self.candlestick_item = CandlestickItem(pd.read_csv(PACKAGE_PATH.parent.joinpath('temp', 'test.csv')))
        self.setCursor(Qt.ArrowCursor)
        self._ui.buttonDraw.setEnabled(True)

    def _draw(self):
        self.chart_main.addItem(self.candlestick_item)

    # def draw(self):
    #     self.chart.removeAllSeries()  # 删除所有序列
    #     # self.chart.setTitle("股票日线图--" + self.ui.tabWidget.tabText(0))
    #
    #     # 1. 创建蜡烛图
    #     candlestick_series = QCandlestickSeries()
    #     candlestick_series.setName("蜡烛图")
    #     candlestick_series.setIncreasingColor(Qt.red)        # 暴涨
    #     candlestick_series.setDecreasingColor(Qt.darkGreen)  # 暴跌
    #
    #     # visible = self.ui.chkBox_Outline.isChecked()
    #     # candle_series.setBodyOutlineVisible(visible)
    #     # candle_series.setCapsVisible(self.ui.chkBox_Caps.isChecked())
    #
    #     self.chart.addSeries(candlestick_series)
    #     candlestick_series.attachAxis(self.__axisX)
    #     candlestick_series.attachAxis(self.__axisY)
    #
    #     # candlestick_series.clicked.connect(self.do_candleClicked)
    #     # candlestick_series.hovered.connect(self.do_candleHovered)
    #
    #     print('Step 1')
    #
    #     # 2. 创建MA曲线
    #     pen = QPen()
    #     pen.setWidth(2)
    #
    #     ma_series_1 = QLineSeries()  # 不能使用QSplineSeries
    #     ma_series_1.setName("MA5")
    #     pen.setColor(Qt.magenta)
    #     ma_series_1.setPen(pen)
    #     self.chart.addSeries(ma_series_1)
    #     ma_series_1.attachAxis(self.__axisX)
    #     ma_series_1.attachAxis(self.__axisY)
    #
    #     ma_series_2 = QLineSeries()
    #     ma_series_2.setName("MA10")
    #     pen.setColor(Qt.yellow)
    #     ma_series_2.setPen(pen)
    #     self.chart.addSeries(ma_series_2)
    #     ma_series_2.attachAxis(self.__axisX)
    #     ma_series_2.attachAxis(self.__axisY)
    #
    #     ma_series_3 = QLineSeries()
    #     ma_series_3.setName("MA20")
    #     pen.setColor(Qt.cyan)
    #     ma_series_3.setPen(pen)
    #     self.chart.addSeries(ma_series_3)
    #     ma_series_3.attachAxis(self.__axisX)
    #     ma_series_3.attachAxis(self.__axisY)
    #
    #     ma_series_4 = QLineSeries()
    #     ma_series_4.setName("MA60")
    #     pen.setColor(Qt.green)  # green
    #     ma_series_4.setPen(pen)
    #     self.chart.addSeries(ma_series_4)
    #     ma_series_4.attachAxis(self.__axisX)
    #     ma_series_4.attachAxis(self.__axisY)
    #
    #     print('Step 2')
    #
    #     # 3. 填充数据到序列
    #     data_row_count = self.df.size  # 数据点个数
    #     for i in range(data_row_count):
    #         dateStr = self.df.iloc[i]['datetime']  # 日期字符串，如"2017/02/03"
    #         dateValue = QDate.fromString(dateStr, "yyyy/MM/dd")  # QDate
    #         dtValue = QDateTime(dateValue)  # 日期时间 QDateTime
    #         timeStamp = dtValue.toMSecsSinceEpoch()  # 毫秒数
    #
    #         single_candlestick = QCandlestickSet()  # QCandlestickSet
    #         single_candlestick.setOpen(self.df.iloc[i]['open'])  # 开盘
    #         single_candlestick.setHigh(self.df.iloc[i]['high'])  # 最高
    #         single_candlestick.setLow(self.df.iloc[i]['low'])  # 最低
    #         single_candlestick.setClose(self.df.iloc[i]['close'])  # 收盘
    #         single_candlestick.setTimestamp(timeStamp)  # 时间戳
    #         candlestick_series.append(single_candlestick)  # 添加到序列

            # M1 = float(self.itemModel.item(i, 5).text())
            # M2 = float(self.itemModel.item(i, 6).text())
            # M3 = float(self.itemModel.item(i, 7).text())
            # M4 = float(self.itemModel.item(i, 8).text())
            #
            # ma_series_1.append(timeStamp, M1)
            # ma_series_2.append(timeStamp, M2)
            # ma_series_3.append(timeStamp, M3)
            # ma_series_4.append(timeStamp, M4)

        # 4. 设置坐标轴范围
        # minDateStr = self.itemModel.item(0, 0).text()  # 日期字符串，如"2017/02/03"
        # minDate = QDate.fromString(minDateStr, "yyyy/MM/dd")  # QDate
        # minDateTime = QDateTime(minDate)  # 最小日期时间,QDateTime
        #
        # maxDateStr = self.itemModel.item(data_row_count - 1, 0).text()  # 日期字符串，如"2017/05/03"
        # maxDate = QDate.fromString(maxDateStr, "yyyy/MM/dd")
        # maxDateTime = QDateTime(maxDate)  # 最大日期时间
        #
        # self.__axisX.setRange(minDateTime, maxDateTime)  # 日期时间范围
        # dateFormat = self.ui.comboDateFormat.currentText()  # 格式，如"MM-dd"
        # self.__axisX.setFormat(dateFormat)  # 标签格式
        #
        # self.__axisY.applyNiceNumbers()  # 自动
        #
        # for marker in self.chart.legend().markers():  # QLegendMarker类型列表
        #     marker.clicked.connect(self.do_LegendMarkerClicked)
