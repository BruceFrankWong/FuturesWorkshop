# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'

from typing import Any, Dict, List
import csv
from pathlib import Path
import copy


# The path of the packages <FuturesWorkshop>
PACKAGE_PATH: Path = Path(__file__).parent


def load_csv(csv_file: Path) -> List[Dict[str, Any]]:
    result: List[Dict[str, Any]] = []
    temp: Dict[str, Any] = {}
    with open(csv_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            for k, v in row.items():
                if '.' in v:
                    x = float(v)
                    temp[k] = x
                else:
                    try:
                        x = int(v)
                        temp[k] = x
                    except ValueError:
                        temp[k] = v
            result.append(copy.deepcopy(temp))
    return result


def save_csv(csv_file: Path, header: List[str], data: List[Dict[str, Any]]) -> None:
    with open(csv_file, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, header)
        writer.writeheader()
        for item in data:
            writer.writerow(item)


def load_config() -> Dict[str, Any]:
    """
    Load the settings csv files, including <exchange.csv>, <product.csv> and <stop.csv>.
    The csv files exists in <App path>/settings directory.
    :return: a dict which key is str and value is list.
    """
    setting_exchange: Path = PACKAGE_PATH.joinpath('settings', 'exchange.csv')
    setting_product: Path = PACKAGE_PATH.joinpath('settings', 'product.csv')
    setting_stop: Path = PACKAGE_PATH.joinpath('settings', 'stop.csv')

    result: Dict[str, Any] = {'exchange': []}

    for item in load_csv(setting_exchange):
        result['exchange'].append(item['symbol'])
        result[item['symbol']] = {'name': item['name'], 'product': []}

    for item in load_csv(setting_product):
        result[item['exchange']]['product'].append(item['symbol'])
        result[item['exchange']][item['symbol']] = {
            'name': item['name'],
            'fluctuation': item['fluctuation'],
            'multiplier': item['multiplier']
        }
    for item in load_csv(setting_stop):
        result[item['exchange']][item['symbol']]['long'] = item['long']
        result[item['exchange']][item['symbol']]['short'] = item['short']
    return result


def get_custom_data(config: Dict[str, Any]) -> List[Dict[str, str]]:
    result: List[Dict[str, str]] = []
    temp: Dict[str, str] = {}
    for exchange in config['exchange']:
        for product in config[exchange]['product']:
            temp['exchange'] = exchange
            temp['symbol'] = product
            temp['long'] = config[exchange][product]['long']
            temp['short'] = config[exchange][product]['short']
            result.append(copy.deepcopy(temp))
    return result


def save_config(config: Dict[str, Any]) -> None:
    """
    Save the stop settings into the <stop.csv>.
    The csv file exists in <App path>/settings directory.
    """
    setting_stop: Path = PACKAGE_PATH.joinpath('settings', 'stop.csv')
    header: List[str] = ['exchange', 'symbol', 'long', 'short']
    data: List[Dict[str, str]] = get_custom_data(config)
    save_csv(csv_file=setting_stop, header=header, data=data)


def get_exchange_symbol_by_name(name: str) -> str:
    for item in CONFIGS['exchange']:
        if CONFIGS[item]['name'] == name:
            return item


# The config variable.
CONFIGS: Dict[str, Any] = load_config()
