# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


"""
FuturesWorkshop - config module

The CONFIGS variable contains the information which application needed when running.
It comprises two parts, one is depended on exchanges (for example, products and their 
symbols) or market, such as the quote. The other is user preferences, which means
the value is controlled by users, as their wills.

The CONFIGS variable is a dict instance:
{
    'index': {
        # The following coming from <exchange.csv>
        'exchange': {
            <exchange_symbol>: <exchange_name>,
        },
        # The following coming from <product.csv>
        'product': {
            <product_symbol>: <product_name>,
        },
        # The following coming from <stop_loss.csv>
        'stop_loss': {
            <product_symbol>: {,
                'long': int,
                'short': int,
            },
        },
    },
    <exchange_symbol>: {
        # The following coming from <product.csv>
        <product_symbol>: {
            'fluctuation': float,
            'multiplier': int,
            'trading_section': int,
            'optional_section': int,
            'trading_time': [
                <time>,
            ],
            'stop_loss_long': int,
            'stop_loss_short': int,
        },
    },
    'tq_account': { 
        'account': str,
        'password': str,
    },
    'trading_account': {
        'broker': str,
        'account': str,
        'password': str,
    },
}
"""


from typing import Any, Dict, List
from pathlib import Path
import csv
import json
from datetime import time
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


def load_json(json_file: Path) -> Dict[str, Any]:
    result: Dict[str, Any]
    with open(json_file, mode='r', encoding='utf-8') as f:
        result = json.load(f)
    return result


def get_config_file_path(config_type: str) -> Path:
    config_file_path: Dict[str, Path] = {
        'exchange': PACKAGE_PATH.joinpath('settings', 'exchange.csv'),
        'product': PACKAGE_PATH.joinpath('settings', 'product.csv'),
        'stop_loss': PACKAGE_PATH.joinpath('settings', 'stop_loss.csv'),
        'user': PACKAGE_PATH.joinpath('settings', 'user.json')
    }
    return config_file_path[config_type]


def load_config() -> Dict[str, Any]:
    """
    Load the config files, including:
        <exchange.csv>,
        <product.csv>,
        <stop_loss.csv>
        <user.json>.
    The config files exists in <App path>/settings directory.
    :return: a dict which key is str and value is list.
    """
    result: Dict[str, Any] = {
        'index': {
            'exchange': {},
            'product': {},
            'stop_loss': {},
        },
        'tq_account': {
            'account': '',
            'password': '',
        },
        'trading_account': {
            'broker': '',
            'account': '',
            'password': '',
        }
    }

    # exchange.csv
    for item in load_csv(get_config_file_path('exchange')):
        result['index']['exchange'][item['symbol']] = item['name']
        result[item['symbol']] = {}

    # product.csv
    for item in load_csv(get_config_file_path('product')):
        result['index']['product'][item['symbol']] = item['name']
        result[item['exchange']][item['symbol']] = {
            'fluctuation': item['fluctuation'],
            'multiplier': item['multiplier'],
            'trading_section': item['trading_section'],
            'optional_section': item['optional_section'],
            'trading_time': [
                time(
                    hour=int(t.split(':')[0]),
                    minute=int(t.split(':')[1])
                ) for t in item['trading_time'].split(';')
            ],
        }

    # stop_loss.csv
    for item in load_csv(get_config_file_path('stop_loss')):
        result['index']['stop_loss'][item['product']] = {
            'long': item['long'],
            'short': item['short'],
        }
        result[item['exchange']][item['product']]['long'] = item['long']
        result[item['exchange']][item['product']]['short'] = item['short']

    # user.json
    result.update(load_json(get_config_file_path('user')))
    return result


def save_config() -> None:
    """
    Save the stop settings into the <stop_loss.csv>.
    The csv file exists in <App path>/settings directory.
    """
    header: List[str] = ['exchange', 'symbol', 'long', 'short']
    data: List[Dict[str, str]] = CONFIGS['stop_loss']
    save_csv(
        csv_file=get_config_file_path('stop_loss'),
        header=header,
        data=data
    )


# The config variable.
CONFIGS: Dict[str, Any] = load_config()
