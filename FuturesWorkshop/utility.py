# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


"""
FuturesWorkshop - Utility module
"""


from typing import Dict, List

from .config import CONFIGS


def get_exchange_symbol_list() -> List[str]:
    return [symbol for symbol in CONFIGS['index']['exchange'].keys()]


def get_exchange_name_list() -> List[str]:
    return [name for name in CONFIGS['index']['exchange'].values()]


def get_exchange_symbol_by_name(name: str) -> str:
    for k, v in CONFIGS['index']['exchange'].items():
        if v == name:
            return k


def get_product_symbol_list() -> List[str]:
    return [symbol for symbol in CONFIGS['index']['product'].keys()]


def get_product_name_list() -> List[str]:
    return [name for name in CONFIGS['index']['product'].values()]


def get_product_symbol_by_name(name: str) -> str:
    for k, v in CONFIGS['index']['product'].items():
        if v == name:
            return k


def get_stop_loss_settings() -> Dict[str, Dict[str, int]]:
    return CONFIGS['index']['stop_loss']
