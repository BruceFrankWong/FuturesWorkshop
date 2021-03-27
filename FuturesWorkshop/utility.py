# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


"""
FuturesWorkshop - Utility module
"""


from typing import Dict, List
from datetime import time

from .config import CONFIGS


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


def get_stop_loss_settings() -> Dict[str, Dict[str, int]]:
    return CONFIGS['stop_loss']
