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


from typing import Any, Callable, Dict, List, Tuple, Optional, NoReturn
from datetime import date, timedelta
import json
from pathlib import Path
import csv
import sqlite3
from lxml import etree

import requests

from ..config import PACKAGE_PATH, CONFIGS
from ..utility import make_path_existed, is_holiday
from ..definition import FuturesDailyData


def save_as_csv(data: Dict[str, List[FuturesDailyData]], csv_path: Path) -> NoReturn:
    """
    Save the crawled data into csv files.
    :param data:
    :param csv_path:
    :return:
    """
    make_path_existed(csv_path)
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


def crawl_shfe_futures_daily_data(day: date) -> Dict[str, List[FuturesDailyData]]:
    """
    Crawl futures daily quote data from SHFE site, for a single day.
    :param day: <datetime.date>.
    :return: <dict>. key is the product symbol, and value is a list of <FuturesDailyData> object.
    """
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
            # Skip INE product.
            if symbol in ['sc', 'nr', 'lu', 'bc']:
                continue

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


def crawl_cffex_futures_daily_data(day: date) -> Dict[str, List[FuturesDailyData]]:
    """
    Crawl futures daily quote data from CFFEX site, for a single day.
    :param day: <datetime.date>.
    :return: <dict>. key is the product symbol, and value is a list of <FuturesDailyData> object.
    """
    url: str = 'http://www.cffex.com.cn/sj/hqsj/rtj/{day}/index.xml'
    result: Dict[str, List[FuturesDailyData]] = {}
    data: Dict[str, Any] = {}
    response = requests.get(url.format(day=day.strftime('%Y%m/%d')))
    if response.status_code == 200:
        xml = response.text.encode('utf-8')
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        root = etree.fromstring(xml, parser=parser)
        for element in root:
            for attribute in element:
                if attribute.text is not None:
                    data[attribute.tag] = attribute.text.strip()
                else:
                    data[attribute.tag] = None
            if '-' in data['instrumentid']:
                continue
            else:
                symbol = data['productid']
                if symbol not in result.keys():
                    result[symbol] = []
                result[symbol].append(
                    FuturesDailyData(
                        product=symbol,
                        delivery=data['expiredate'][2:6],
                        date=day,
                        open=data['openprice'],
                        high=data['highestprice'],
                        low=data['lowestprice'],
                        close=data['closeprice'],
                        settlement=data['settlementprice'],
                        volume=data['volume'],
                        open_interest=data['openinterest']
                    )
                )
        return result


def crawl_ine_futures_daily_data(day: date) -> Dict[str, List[FuturesDailyData]]:
    """
    Crawl futures daily quote data from INE site, for a single day.
    :param day: <datetime.date>.
    :return: <dict>. key is the product symbol, and value is a list of <FuturesDailyData> object.
    """
    url: str = 'http://www.ine.cn/data/dailydata/kx/kx{day}.dat'
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


def crawl_dce_futures_daily_data(day: date) -> Dict[str, List[FuturesDailyData]]:
    """
    Crawl futures daily quote data from DCE site, for a single day.
    :param day:
    :return:
    """
    # The site used JavaScript confuse. Find the way out.
    pass


def crawl_czce_futures_daily_data(day: date) -> Dict[str, List[FuturesDailyData]]:
    """
    Crawl futures daily quote data from CZCE site, for a single day..
    :param day:
    :return:
    """
    # The site used JavaScript confuse. Find the way out.
    pass


def check_date(exchange: str, begin: date = None, end: date = None) -> Tuple[date, date]:
    """
    Check the parameters date begin and date end. Raise error if parameters not valid.
    :param exchange:
    :param begin:
    :param end:
    :return:
    """
    date_begin: date
    date_end: date
    first_date: Dict[str, date] = {
        'SHFE': date(2002, 1, 7),
        'DCE': date(2007, 1, 4),
        'CZCE': date(2005, 4, 29),
        'CFFEX': date(2010, 4, 16),
        'INE': date(2018, 3, 26),
    }

    if begin is not None and end is not None and end < begin:
        raise ValueError(
            f'Parameter <end> is earlier than parameter <begin>.'
        )
    elif begin is not None:
        if begin < first_date[exchange]:
            raise ValueError(
                f'Parameter <begin> should not be earlier than {first_date[exchange].strftime("%Y-%m-%d")}, '
                f'cause of exchange <{exchange}> no earlier data provided.'
            )
        elif begin > date.today():
            raise ValueError(
                f'Parameter <begin> should not be later than today ({date.today()}).'
            )
    elif end is not None:
        if end < first_date[exchange]:
            raise ValueError(
                f'Parameter <end> should not be earlier than {first_date[exchange].strftime("%Y-%m-%d")}, '
                f'cause of exchange <{exchange}> no earlier data provided.'
            )
        elif end > date.today():
            raise ValueError(
                f'Parameter <end> should not be later than today ({date.today()}).'
            )
    if begin is None:
        date_begin = first_date[exchange]
    else:
        date_begin = begin
    if end is None:
        date_end = date.today()
    else:
        date_end = end
    return date_begin, date_end


def crawl_futures_daily_data(
        exchange: str,
        begin: Optional[date] = None,
        end: Optional[date] = None,
) -> NoReturn:
    """
    Crawl futures daily data from a single exchange.
    :param exchange:
    :param begin:
    :param end:
    :return:
    """
    crawler: Dict[str, Callable] = {
        'SHFE': crawl_shfe_futures_daily_data,
        'DCE': crawl_dce_futures_daily_data,
        'CZCE': crawl_czce_futures_daily_data,
        'CFFEX': crawl_cffex_futures_daily_data,
        'INE': crawl_ine_futures_daily_data,
    }

    exchange_symbol: str = exchange.upper()
    if exchange_symbol not in ['SHFE', 'DCE', 'CZCE', 'CFFEX', 'INE']:
        raise ValueError(f"<exchange> should be in ['SHFE', 'DCE', 'CZCE', 'CFFEX', 'INE']")

    date_begin: date
    date_end: date
    date_begin, date_end = check_date(exchange_symbol, begin, end)

    downloaded_path: Path = PACKAGE_PATH.joinpath('data', exchange_symbol, 'daily')
    make_path_existed(downloaded_path)

    n: int
    day: date
    for n in range((date_end - date_begin).days + 1):
        day = begin + timedelta(days=n)
        if is_holiday(day):
            continue
        crawled_data = crawler[exchange_symbol](day)
        save_as_csv(crawled_data, downloaded_path)
