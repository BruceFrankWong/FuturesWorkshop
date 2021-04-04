# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Callable

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread
import pyqtgraph as pg
import pandas as pd
import numpy as np


# appropriate types
ColorMap = pg.ColorMap

# module definitions, mostly colors
legend_border_color = '#000000dd'
legend_fill_color   = '#00000055'
legend_text_color   = '#dddddd66'
soft_colors = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
]
hard_colors = [
    '#000000', '#772211', '#000066', '#555555', '#0022cc', '#ffcc00'
]
colmap_clash = ColorMap(
    [0.0, 0.2, 0.6, 1.0],
    [[127, 127, 255, 51], [0, 0, 127, 51], [255, 51, 102, 51], [255, 178, 76, 51]]
)
foreground = '#000000'
background = '#ffffff'
odd_plot_background = '#f0f0f0'
candle_bull_color = '#26a69a'
candle_bear_color = '#ef5350'
candle_bull_body_color = background
volume_bull_color = '#92d2cc'
volume_bear_color = '#f7a9a7'
volume_bull_body_color = volume_bull_color
volume_neutral_color = '#b0b0b0'
poc_color = '#000060'
band_color = '#d2dfe6'
cross_hair_color = '#00000077'
draw_line_color = '#000000'
draw_done_color = '#555555'
significant_decimals = 8
significant_eps = 1e-8
max_zoom_points = 20        # number of visible candles when maximum zoomed in
top_graph_scale = 2
clamp_grid = True
right_margin_candles = 5    # whitespace at the right-hand side
side_margin = 0.5
lod_candles = 3000
lod_labels = 700
cache_candle_factor = 3     # factor extra candles rendered to buffer
y_label_width = 65
long_time = 2*365*24*60*60*1e9
display_timezone = None  # default to local
winx, winy, winw, winh = 400, 300, 800, 400

app = None
windows = []    # no gc
timers = []     # no gc
sounds = {}     # no gc
epoch_period = 1e30
last_ax = None      # always assume we want to plot in the last axis, unless explicitly specified
overlay_axs = []    # for keeping track of candlesticks in overlays
viewrestore = False
master_data = {}


class FinPlotItem(pg.GraphicsObject):
    def __init__(self, ax, data_source, lod):
        super().__init__()
        self.ax = ax
        self.data_source = data_source
        self.picture = QtGui.QPicture()
        self.painter = QtGui.QPainter()
        self.dirty = True
        self.lod = lod
        self.cachedRect = None

    def repaint(self):
        self.dirty = True
        self.paint(self.painter)

    def paint(self, p, *args):
        if self.datasrc.is_sparse:
            self.dirty = True
        self.update_dirty_picture(self.viewRect())
        p.drawPicture(0, 0, self.picture)

    def update_dirty_picture(self, visible_rect):
        if self.dirty or \
            (self.lod and   # regenerate when zoom changes?
                (visible_rect.left() < self.cachedRect.left() or
                 visible_rect.right() > self.cachedRect.right() or
                 visible_rect.width() < self.cachedRect.width() / cache_candle_factor)):     # optimize when zooming in
            self._generate_picture(visible_rect)

    def _generate_picture(self, boundingRect):
        w = boundingRect.width()
        self.cachedRect = QtCore.QRectF(boundingRect.left()-(cache_candle_factor-1)*0.5*w, 0, cache_candle_factor*w, 0)
        self.painter.begin(self.picture)
        self._generate_dummy_picture(self.viewRect())
        self.generate_picture(self.cachedRect)
        self.painter.end()
        self.dirty = False

    def _generate_dummy_picture(self, boundingRect):
        if self.datasrc.is_sparse:
            # just draw something to ensure PyQt will paint us again
            self.painter.setPen(pg.mkPen(background))
            self.painter.setBrush(pg.mkBrush(background))
            l, r = boundingRect.left(), boundingRect.right()
            self.painter.drawRect(QtCore.QRectF(l, boundingRect.top(), 1e-3, boundingRect.height()*1e-5))
            self.painter.drawRect(QtCore.QRectF(r, boundingRect.bottom(), -1e-3, -boundingRect.height()*1e-5))

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())


class CandlestickItem(FinPlotItem):
    def __init__(self, ax, data_source, draw_body, draw_shadow, candle_width, color_func):
        self.colors = dict(
            bull_shadow      =candle_bull_color,
            bull_frame       =candle_bull_color,
            bull_body        =candle_bull_body_color,
            bear_shadow      =candle_bear_color,
            bear_frame       =candle_bear_color,
            bear_body        =candle_bear_color,
            weak_bull_shadow =brighten(candle_bull_color, 1.2),
            weak_bull_frame  =brighten(candle_bull_color, 1.2),
            weak_bull_body   =brighten(candle_bull_color, 1.2),
            weak_bear_shadow =brighten(candle_bear_color, 1.5),
            weak_bear_frame  =brighten(candle_bear_color, 1.5),
            weak_bear_body   =brighten(candle_bear_color, 1.5)
        )
        self.draw_body = draw_body
        self.draw_shadow = draw_shadow
        self.candle_width = candle_width
        self.shadow_width = 1
        self.color_func = color_func
        self.x_offset = 0
        super().__init__(ax, data_source, lod=True)

    def generate_picture(self, boundingRect):
        w = self.candle_width
        w2 = w * 0.5
        left, right = boundingRect.left(), boundingRect.right()
        p = self.painter
        df, origlen = self.datasrc.rows(5, left, right, yscale=self.ax.vb.yscale)
        drawing_many_shadows = self.draw_shadow and origlen > lod_candles*2//3
        for shadow, frame, body, df_rows in self.colorfunc(self, self.datasrc, df):
            idxs = df_rows.index
            rows = df_rows.values
            if self.x_offset:
                idxs += self.x_offset
            if self.draw_shadow:
                p.setPen(pg.mkPen(shadow, width=self.shadow_width))
                for x, (t, open, close, high, low) in zip(idxs, rows):
                    if high > low:
                        p.drawLine(QtCore.QPointF(x, low), QtCore.QPointF(x, high))
            if self.draw_body and not drawing_many_shadows:     # settle with only drawing shadows if too much detail
                p.setPen(pg.mkPen(frame))
                p.setBrush(pg.mkBrush(body))
                for x, (t, open, close, high, low) in zip(idxs, rows):
                    p.drawRect(QtCore.QRectF(x-w2, open, w, close-open))

    def rowcolors(self, prefix):
        return [self.colors[prefix+'_shadow'], self.colors[prefix+'_frame'], self.colors[prefix+'_body']]


def brighten(color, f):
    if not color:
        return color
    return pg.mkColor(color).lighter(int(f*100))


def price_color_filter(item, data_source, df):
    column_open = df.columns['open']
    column_close = df.columns['close']
    is_up = df[column_open] <= df[column_close]     # open lower than close = goes up
    yield item.rowcolors('bull') + [df.loc[is_up, :]]
    yield item.rowcolors('bear') + [df.loc[~is_up, :]]


def _create_datasrc(ax, *args):
    def do_create(argument):
        if len(argument) == 1:
            if type(argument[0]) == PandasDataSource:
                return argument[0]
            elif type(argument[0]) in (list, tuple):
                argument = [np.array(argument[0])]
            elif type(argument[0]) == np.ndarray:
                argument = [pd.DataFrame(argument[0].T)]
            elif type(argument[0]) == pd.DataFrame:
                return PandasDataSource(argument[0])
        argument = [_create_series(a) for a in argument]
        return PandasDataSource(pd.concat(argument, axis=1))

    iargs = [a for a in args if a is not None]
    data_source = do_create(iargs)
    # check if time column missing
    if len(data_source.df.columns) == 1:
        # assume time data has already been added before
        for a in ax.vb.win.axs:
            if a.vb.datasrc and len(a.vb.datasrc.df.columns) >= 2:
                data_source.df.columns = a.vb.datasrc.df.columns[1:len(data_source.df.columns)+1]
                col = a.vb.datasrc.df.columns[0]
                data_source.df.insert(0, col, a.vb.datasrc.df[col])
                data_source = PandasDataSource(data_source.df)
                break
    elif len(iargs) >= 2 and len(data_source.df.columns) == len(iargs)+1 and len(iargs) == len(args):
        try:
            if '.Int' in str(type(iargs[0].index)):
                print('WARNING: performance penalty and crash may occur when using int64 instead of range indices.')
                if (iargs[0].index == range(len(iargs[0]))).all():
                    print(' - Fix by .reset_index(drop=True)')
                    return _create_datasrc(ax, data_source.df[data_source.df.columns[1:]])
        except:
            print('WARNING: input data source may cause performance penalty and crash.')

    # FIX: stupid QT bug causes rectangles larger than 2G to flicker, so scale rendering down some
    if data_source.df.iloc[:, 1:].max(numeric_only=True).max() > 1e8:   # too close to 2G for comfort
        ax.vb.yscale.set_scale(int(1e8))
    return data_source


def _create_plot(ax=None, **kwargs):
    if ax:
        return ax
    if last_ax:
        return last_ax
    return create_plot(**kwargs)


def create_plot(title='Finance Plot', rows=1, init_zoom_periods=1e10, maximize=True, yscale='linear'):
    pg.setConfigOptions(foreground=foreground, background=background)
    win = FinWindow(title)
    # normally first graph is of higher significance, so enlarge
    win.ci.layout.setRowStretchFactor(0, top_graph_scale)
    win.show_maximized = maximize
    ax0 = axs = create_plot_widget(master=win, rows=rows, init_zoom_periods=init_zoom_periods, yscale=yscale)
    axs = axs if type(axs) in (tuple,list) else [axs]
    for ax in axs:
        win.addItem(ax)
        win.nextRow()
    return ax0


def create_plot_widget(master, rows=1, init_zoom_periods=1e10, yscale='linear'):
    pg.setConfigOptions(foreground=foreground, background=background)
    global last_ax
    if master not in windows:
        windows.append(master)
    axs = []
    prev_ax = None
    for n in range(rows):
        ysc = yscale[n] if type(yscale) in (list,tuple) else yscale
        ysc = YScale(ysc, 1)
        v_zoom_scale = 0.97
        viewbox = FinViewBox(master, init_steps=init_zoom_periods, yscale=ysc, v_zoom_scale=v_zoom_scale, enableMenu=False)
        ax = prev_ax = _add_timestamp_plot(master=master, prev_ax=prev_ax, viewbox=viewbox, index=n, yscale=ysc)
        if axs:
            ax.setXLink(axs[0].vb)
        else:
            viewbox.setFocus()
        axs += [ax]
    if isinstance(master, pg.GraphicsLayoutWidget):
        proxy = pg.SignalProxy(master.scene().sigMouseMoved, rateLimit=144, slot=partial(_mouse_moved, master))
    else:
        proxy = []
        for ax in axs:
            proxy += [pg.SignalProxy(ax.ax_widget.scene().sigMouseMoved, rateLimit=144, slot=partial(_mouse_moved, master))]
    master_data[master] = dict(proxymm=proxy, last_mouse_evs=None, last_mouse_y=0)
    last_ax = axs[0]
    return axs[0] if len(axs) == 1 else axs


def candlestick_ochl(
        data_source,
        draw_body: bool = True,
        draw_shadow: bool = True,
        candle_width: float = 0.6,
        ax=None,
        color_func: Callable = price_color_filter):
    ax = _create_plot(ax=ax, maximize=False)
    data_source = _create_datasrc(ax, data_source)
    data_source.scale_cols = [3, 4]     # only hi+lo scales
    _set_datasrc(ax, data_source)
    item = CandlestickItem(
        ax=ax,
        data_source=data_source,
        draw_body=draw_body,
        draw_shadow=draw_shadow,
        candle_width=candle_width,
        color_func=color_func
    )
    _update_significants(ax, data_source, force=True)
    item.update_data = partial(_update_data, None, None, item)
    item.update_gfx = partial(_update_gfx, item)
    ax.addItem(item)
    return item


class CandlestickItem2(pg.GraphicsObject):
    def __init__(self, data: pd.DataFrame):
        super().__init__(self)
        self.data: pd.DataFrame = data
        self.generatePicture()

    def generatePicture(self):
        self.picture = QtGui.QPicture()
        painter = QtGui.QPainter(self.picture)
        painter.setPen(pg.mkPen('w'))
        w = (self.data[1][0] - self.data[0][0]) / 3.
        for (t, open, close, min, max) in self.data:
            print(open, close, type(open))
            if open > close:
                painter.setPen(pg.mkPen('g'))
                painter.setBrush(pg.mkBrush('g'))
            else:
                painter.setPen(pg.mkPen('r'))
                painter.setBrush(pg.mkBrush('r'))
            painter.drawLine(QtCore.QPointF(t, min), QtCore.QPointF(t, max))
            painter.drawRect(QtCore.QRectF(t - w, open, w * 2, close - open))
        painter.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())


class WidgetChart(QtWidgets.QGraphicsView):
    def __init__(self,
                 parent: QtWidgets.QWidget = None,
                 size: QtCore.QSize = None,
                 title: str = None,
                 show: bool = False,
                 **kargs
                 ):
        super().__init__(parent)
        self.plot = pg.GraphicsLayoutWidget(parent=self)

        self.chart_candlestick = self.plot.addPlot(
            row=0,
            col=0,
            title='<span style="font-size: 10pt">SHFE, ag 2101'
        )
        self.chart_candlestick.titleLabel.setAttr('justify', 'left')
        self.chart_attached: dict = {}
        self.chart_volume = self.plot.addPlot(row=1, col=0)
        self.chart_macd = self.plot.addPlot(row=2, col=0)

        if size is not None:
            self.plot.resize(size)

        if title is not None:
            self.plot.setWindowTitle(title)

        if show is True:
            self.plot.show()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.plot.resize(event.size())
