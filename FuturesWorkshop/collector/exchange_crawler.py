# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


"""
Crawl quote daily data from exchanges, saved in csv format.
The csv file format:
    filename: symbol
    column:
        date
        delivery
        open
        high
        low
        close
        settlement
        volume
        open_interest

The csv files saved in <Package path>\\data\\<exchange symbol>\\<product symbol>.csv
"""


from typing import Any, Dict, List, Optional
from datetime import date, timedelta
import json
from pathlib import Path
import csv

import requests

from ..config import PACKAGE_PATH, CONFIGS
from ..utility import make_path_existed, is_holiday
from ..definition import FuturesDailyData


csv_header: List[str] = [
    'date',
    'delivery',
    'open',
    'high',
    'low',
    'close'
    'settlement',
    'volume',
    'open_interest'
]


def save_as_csv(data: Dict[str, List[FuturesDailyData]], csv_path: Path) -> None:
    for product, quote in data.items():
        csv_file = csv_path.joinpath(f'{product}.csv')
        if csv_file.exists():
            mode = 'a+'
        else:
            mode = 'w'
        with open(csv_file, mode=mode, encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, FuturesDailyData.fields())
            if mode == 'w':
                writer.writeheader()
            for item in quote:
                writer.writerow(item.to_dict())


def _crawl_shfe_futures_data(day: date) -> Dict[str, List[FuturesDailyData]]:
    url: str = 'http://www.shfe.com.cn/data/dailydata/kx/kx{day}.dat'
    result: Dict[str, List] = {}
    response = requests.get(url.format(day=day.strftime('%Y%m%d')))
    if response.status_code == 200:
        data = json.loads(response.text)
        for i in range(len(data['o_curinstrument'])):
            info = data['o_curinstrument'][i]
            if info['DELIVERYMONTH'] == '小计' or \
                    info['DELIVERYMONTH'] == 'efp' or \
                    info['PRODUCTID'] == '总计' or \
                    info['PRODUCTID'] == '总计1' or \
                    info['PRODUCTID'] == '总计2':
                continue
            symbol = info['PRODUCTID'].split('_', 1)[0]
            if symbol not in result.keys():
                result[symbol] = []
            result[symbol].append(
                FuturesDailyData(
                    product=symbol,
                    delivery=info['DELIVERYMONTH'],
                    date=day,
                    open=info['OPENPRICE'],
                    high=info['HIGHESTPRICE'],
                    low=info['LOWESTPRICE'],
                    close=info['CLOSEPRICE'],
                    settlement=info['SETTLEMENTPRICE'],
                    volume=info['VOLUME'],
                    open_interest=info['OPENINTEREST']
                )
            )
    else:
        print(response.status_code)
    return result


def crawl_shfe_futures_daily_data(
        begin: date,
        end: Optional[date] = None
) -> Optional[Dict[str, List[FuturesDailyData]]]:
    """
    Crawl daily quote data of futures from SHFE site.
    :param begin:
    :param end:
    :return:
    """
    first_date: date = date(2002, 1, 7)

    if end is not None and end < begin:
        return None
    date_end: date = date.today() if end is None else end
    date_begin: date = first_date if begin < first_date else begin

    data_path: Path = PACKAGE_PATH.joinpath('data', 'SHFE', 'daily')
    make_path_existed(data_path)
    for i in range((date_end - date_begin).days + 1):
        day = date_begin + timedelta(days=i)
        if is_holiday(day):
            continue
        print(f'Crawl {day}')
        result = _crawl_shfe_futures_data(day)
        save_as_csv(result, data_path)
        yield result


def save_shfe_futures_daily_data_to_csv(data: Dict[str, List[FuturesDailyData]]):
    pass
