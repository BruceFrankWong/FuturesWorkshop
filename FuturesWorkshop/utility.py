# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


"""
FuturesWorkshop - Utility module
"""


from typing import Any, Dict, List
from datetime import date, time
from pathlib import Path
import csv

from .config import CONFIGS, PACKAGE_PATH


def make_path_existed(path: Path):
    if not path.exists():
        path.mkdir(parents=True)


def is_holiday(day: date) -> bool:
    if day in CONFIGS['holiday']['expanded'] or day.isoweekday() == 6 or day.isoweekday() == 7:
        return True
    else:
        return False


def get_exchange_symbol_list() -> List[str]:
    return [exchange['symbol'] for exchange in CONFIGS['exchange']['info']]


def get_exchange_name_list() -> List[str]:
    return [exchange['name'] for exchange in CONFIGS['exchange']['info']]


def get_exchange_symbol_by_name(exchange_name: str) -> str:
    for item in CONFIGS['exchange']['info']:
        if item['name'] == exchange_name:
            return item['symbol']


def get_product_symbol_list() -> List[str]:
    return [product['symbol'] for product in CONFIGS['product']['info']]


def get_product_name_list() -> List[str]:
    return [product['name'] for product in CONFIGS['product']['info']]


def get_product_symbol_by_name(product_name: str) -> str:
    for item in CONFIGS['product']['info']:
        if item['name'] == product_name:
            return item['symbol']


def get_product_symbol_list_by_exchange(exchange: str) -> List[str]:
    return CONFIGS['exchange'][exchange]


def get_product_trading_time(product_symbol: str) -> List[Dict[str, time]]:
    return CONFIGS['product'][product_symbol]['trading_time']


def get_exchange_symbol_by_product_symbol(product_symbol: str) -> str:
    for item in CONFIGS['product']['info']:
        if item['symbol'] == product_symbol:
            return item['exchange']


def get_main_contract(day: date, product_symbol: str = None) -> str:
    exchange_symbol: str = get_exchange_symbol_by_product_symbol(product_symbol)
    csv_file: Path = PACKAGE_PATH.joinpath('data', exchange_symbol, 'daily', f'{product_symbol}.csv')
    result: List[Dict[str, Any]] = []
    with open(csv_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if date.fromisoformat(row['date']) == day:
                result.append(
                    {
                        'delivery': row['delivery'],
                        'open_interest': int(row['open_interest']),
                        'volume': int(row['volume']),
                    }
                )
    result.sort(key=lambda oi: oi['open_interest'], reverse=True)
    if result[1]['open_interest'] == result[0]['open_interest'] and \
            result[1]['volume'] > result[0]['volume']:
        return result[1]['delivery']
    else:
        return result[0]['delivery']


def get_stop_loss_settings() -> Dict[str, Dict[str, int]]:
    return CONFIGS['stop_loss']
