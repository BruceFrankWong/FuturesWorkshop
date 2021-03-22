# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Any, Dict, List
from pathlib import Path
import os

from FuturesWorkshop.config import (
    PACKAGE_PATH,
    CONFIGS,
    load_csv,
    save_csv,
    load_config,
    get_custom_data,
    get_exchange_symbol_by_name
)


def test_package_path():
    package_path: Path = PACKAGE_PATH
    assert package_path == Path(r'D:\Development\Python\FuturesWorkshop/FuturesWorkshop')


def test_load_csv():
    file_list: List[Path] = [
        PACKAGE_PATH.joinpath('settings', 'exchange.csv'),
        PACKAGE_PATH.joinpath('settings', 'product.csv'),
        PACKAGE_PATH.joinpath('settings', 'stop.csv'),
    ]
    for file in file_list:
        result = load_csv(file)
        assert isinstance(result, list) is True
        for item in result:
            assert isinstance(item, dict) is True
            for k, v in item.items():
                assert isinstance(k, str) is True
                assert (isinstance(v, str) or isinstance(v, int) or isinstance(v, float)) is True


def test_save_csv():
    file: Path = Path.cwd().joinpath('test_save_csv.csv')
    assert file.exists() is False
    header: List[str] = ['exchange', 'symbol', 'long', 'short']
    data: List[Dict[str, Any]] = [
        {
            'exchange': 'SHFE',
            'symbol': 'rb',
            'long': -3,
            'short': 3,
        },
        {
            'exchange': 'SHFE',
            'symbol': 'hc',
            'long': -5,
            'short': 3,
        },
        {
            'exchange': 'DCE',
            'symbol': 'c',
            'long': -3,
            'short': 3,
        },
        {
            'exchange': 'CZCE',
            'symbol': 'ZC',
            'long': -10,
            'short': 3,
        },
    ]
    save_csv(file, header, data)

    assert file.exists() is True
    row: int = 0
    with open(file, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if row == 0:
                assert line.strip() == ''.join([x + ',' for x in header])[:-1]
            else:
                assert line.strip() == ''.join([str(data[row-1][x]) + ',' for x in header])[:-1]
            row += 1
    os.remove(file)


def test_load_config():
    configs: dict = load_config()

    # Level 1, exchanges.
    assert 'exchange' in configs.keys()
    assert len(configs.keys()) == len(configs['exchange']) + 1
    for key_exchange, value_exchange in configs.items():
        if key_exchange == 'exchange':
            assert isinstance(value_exchange, list) is True
        else:
            assert key_exchange in configs['exchange']
            assert isinstance(value_exchange, dict) is True

            assert 'name' in configs[key_exchange].keys()
            assert 'product' in configs[key_exchange].keys()

            # Level 2, products.
            assert len(configs[key_exchange].keys()) == len(configs[key_exchange]['product']) + 2
            for key_product, value_product in configs[key_exchange].items():
                if key_product == 'name':
                    assert isinstance(value_product, str) is True
                elif key_product == 'product':
                    assert isinstance(value_product, list) is True
                else:
                    assert key_product in configs[key_exchange]['product']
                    assert isinstance(value_product, dict) is True

                    # Level 3, product details.
                    for key_detail, value_detail in configs[key_exchange][key_product].items():
                        assert isinstance(key_detail, str) is True
                        assert key_detail in ['name', 'fluctuation', 'multiplier', 'long', 'short']
                        if key_detail == 'name':
                            assert isinstance(value_detail, str) is True
                        elif key_detail == 'long' or key_detail == 'short':
                            assert isinstance(value_detail, int) is True
                        else:
                            assert (isinstance(value_detail, int) or isinstance(value_detail, float)) is True


def test_get_custom_data():
    result = get_custom_data(CONFIGS)
    assert isinstance(result, list) is True
    assert len(result) == 70
    for item in result:
        assert isinstance(item, dict) is True
        for key in item.keys():
            assert isinstance(key, str) is True


def test_get_exchange_symbol_by_name():
    name_dict: Dict[str, str] = {
        '上海期货交易所': 'SHFE',
        '大连商品交易所': 'DCE',
        '郑州商品交易所': 'CZCE',
        '中国金融期货交易所': 'CFFEX',
        '上海国际能源交易中心': 'INE'
    }
    for k, v in name_dict.items():
        assert get_exchange_symbol_by_name(k) == v
