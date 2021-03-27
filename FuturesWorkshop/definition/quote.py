# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Any, Dict, List, Union
import datetime


class FuturesDailyData(object):
    def __init__(self,
                 product: str,
                 delivery: str,
                 date: Union[str, datetime.date],   # Date, %Y-%m-%d
                 open: float,
                 high: float,
                 low: float,
                 close: float,
                 settlement: float,
                 volume: int,
                 open_interest: int
                 ):
        if isinstance(date, str):
            self.date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        else:
            self.date = date
        self.product = product
        self.delivery = delivery
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.settlement = settlement
        self.volume = volume
        self.open_interest = open_interest

    def __repr__(self) -> str:
        return f'<FuturesDailyData(' \
               f'product={self.product}, ' \
               f'delivery={self.delivery}, ' \
               f'date={self.date.strftime("%Y-%m-%d")}' \
               f')>'

    def to_dict(self) -> Dict[str, Any]:
        return {
            'product': self.product,
            'delivery': self.delivery,
            'date': self.date,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'settlement': self.settlement,
            'volume': self.volume,
            'open_interest': self.open_interest
        }

    @classmethod
    def fields(cls) -> List[str]:
        return [
            'product',
            'delivery',
            'date',
            'open',
            'high',
            'low',
            'close',
            'settlement',
            'volume',
            'open_interest'
        ]
