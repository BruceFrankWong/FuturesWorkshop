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


def save_csv(csv_file: Path, data: List[Dict[str, Any]], header: List[str]) -> None:
    with open(csv_file, mode='w', encoding='utf-8') as f:
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

    result: Dict[str, Any] = {
        'exchange': load_csv(setting_exchange),
        'product': load_csv(setting_product),
        'stop': load_csv(setting_stop)
    }
    return result


def save_config() -> None:
    """
    Save the stop settings into the <stop.csv>.
    The csv file exists in <App path>/settings directory.
    """
    global CONFIGS
    setting_stop: Path = PACKAGE_PATH.joinpath('settings', 'stop.csv')
    header: List[str] = ['symbol', 'long', 'short']
    save_csv(csv_file=setting_stop, data=CONFIGS['stop'], header=header)


# The config variable.
CONFIGS: Dict[str, Any] = load_config()
