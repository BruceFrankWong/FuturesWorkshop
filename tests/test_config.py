# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


"""
Unit test from FuturesWorkshop.config module, with PyTest.

The variable CONFIGS, or the return of load_config(), is an instance of dict.
See <config.py> for more details.
"""


from typing import Any, Dict, List
from pathlib import Path
import os
from datetime import time

from FuturesWorkshop.config import (
    PACKAGE_PATH,
    CONFIGS,
    load_csv,
    save_csv,
    load_config
)


def test_package_path():
    package_path: Path = PACKAGE_PATH
    assert package_path == Path(r'D:\Development\Python\FuturesWorkshop/FuturesWorkshop')


def test_load_csv():
    file_list: List[Path] = [
        PACKAGE_PATH.joinpath('settings', 'exchange.csv'),
        PACKAGE_PATH.joinpath('settings', 'product.csv'),
        PACKAGE_PATH.joinpath('settings', 'stop_loss.csv'),
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

    # Level 1.
    key_level_1: List[str] = ['exchange', 'product', 'stop_loss', 'tq_account', 'trading_account']
    assert len(configs.keys()) == len(key_level_1)
    for key in configs.keys():
        assert key in key_level_1

    # CONFIGS['exchange']
    assert isinstance(configs['exchange'], dict) is True
    assert len(configs['exchange']) == len(configs['exchange']['info']) + 1
    for item in configs['exchange']['info']:
        assert item['symbol'] in ['SHFE', 'DCE', 'CZCE', 'CFFEX', 'INE']
        assert item['name'] in ['上海期货交易所', '大连商品交易所', '郑州商品交易所', '中国金融期货交易所', '上海国际能源交易中心']
    exchange_symbol_list: List[str] = [item['symbol'] for item in configs['exchange']['info']]
    for k, v in configs['exchange'].items():
        assert isinstance(v, list)
        if k != 'info':
            assert k in exchange_symbol_list
            for item in v:
                assert isinstance(item, str)

    # CONFIGS['product']
    assert isinstance(configs['product'], dict) is True
    assert len(configs['product']) == len(configs['product']['info']) + 1
    product_symbol_list: List[str] = [item['symbol'] for item in configs['product']['info']]
    for k, v in configs['product'].items():
        if k == 'info':
            assert isinstance(v, list)
        else:
            assert isinstance(k, str)
            assert k in product_symbol_list
            assert isinstance(v, dict)
            for v_k, v_v in v.items():
                assert isinstance(v_k, str)
                assert v_k in ['fluctuation', 'multiplier', 'trading_section', 'optional_section', 'trading_time']
                assert (isinstance(v['fluctuation'], int) or isinstance(v['fluctuation'], float)) is True
                assert isinstance(v['multiplier'], int) is True
                assert isinstance(v['trading_section'], int) is True
                assert (2 <= v['trading_section'] <= 4) is True
                assert isinstance(v['optional_section'], int) is True
                assert (v['optional_section'] == 0 or v['optional_section'] == 1 or v['optional_section'] == 2) is True
                assert isinstance(v['trading_time'], list) is True
                assert len(v['trading_time']) == v['trading_section']

    # CONFIGS['stop_loss']
    assert isinstance(configs['stop_loss'], dict) is True
    assert len(configs['stop_loss']) == len(product_symbol_list)
    for k, v in configs['stop_loss'].items():
        assert isinstance(k, str)
        assert k in product_symbol_list
        assert isinstance(v, dict)
        assert 'long' in v.keys()
        assert isinstance(v['long'], int)
        assert 'short' in v.keys()
        assert isinstance(v['short'], int)

    # CONFIGS['tq_account']
    assert isinstance(configs['tq_account'], dict) is True
    assert len(configs['tq_account']) == 2
    for k, v in configs['tq_account'].items():
        assert isinstance(k, str) is True
        assert isinstance(v, str) is True
        assert k in ['account', 'password']

    # CONFIGS['trading_account']
    assert isinstance(configs['trading_account'], dict) is True
    for k, v in configs['tq_account'].items():
        assert isinstance(k, str) is True
        assert isinstance(v, str) is True
        assert k in ['broker', 'account', 'password']


def test_trading_time():
    for product in CONFIGS['product']['info']:
        product_symbol = product['symbol']
        trading_section = CONFIGS['product'][product_symbol]['trading_section']
        optional_section = CONFIGS['product'][product_symbol]['optional_section']
        trading_time_list = CONFIGS['product'][product_symbol]['trading_time']
        assert len(trading_time_list) == trading_section
        if trading_section == 2:        # 金融期货
            if optional_section == 0:
                assert product_symbol in ['IF', 'IC', 'IH']
                assert trading_time_list[0]['open'] == time(hour=9, minute=30)
                assert trading_time_list[0]['close'] == time(hour=11, minute=30)
                assert trading_time_list[1]['open'] == time(hour=13, minute=00)
                assert trading_time_list[1]['close'] == time(hour=15, minute=00)
            else:
                assert product_symbol in ['TS', 'TF', 'T']
                assert trading_time_list[0]['open'] == time(hour=9, minute=30)
                assert trading_time_list[0]['close'] == time(hour=11, minute=30)
                assert trading_time_list[1]['open'] == time(hour=13, minute=00)
                assert trading_time_list[1]['close'] == time(hour=15, minute=15)
        elif trading_section == 3:      # 商品期货，无夜盘
            assert optional_section == 0
            assert product_symbol in [
                # 上期所
                'wr',
                # 大商所
                'fb', 'bb', 'jd', 'lh',
                # 郑商所
                'WH', 'PM', 'RI', 'JR', 'LR', 'RS', 'AP', 'CJ', 'PK', 'SF', 'SM', 'UR',
            ]
            assert trading_time_list[0]['open'] == time(hour=9, minute=0)
            assert trading_time_list[0]['close'] == time(hour=10, minute=15)
            assert trading_time_list[1]['open'] == time(hour=10, minute=30)
            assert trading_time_list[1]['close'] == time(hour=11, minute=30)
            assert trading_time_list[2]['open'] == time(hour=13, minute=30)
            assert trading_time_list[2]['close'] == time(hour=15, minute=0)
        elif trading_section == 4:      # 商品期货，有夜盘
            assert optional_section == 1
            assert product_symbol in [
                # 上期所
                'au', 'ag', 'cu', 'al', 'zn', 'pb', 'ni', 'sn', 'ss', 'rb', 'hc', 'fu', 'bu', 'ru', 'sp',
                # 大商所
                'c', 'cs', 'a', 'b', 'm', 'y', 'p', 'rr', 'l', 'v', 'pp', 'eg', 'eb', 'pg', 'j', 'jm', 'i',
                # 郑商所
                'OI', 'RM', 'CF', 'CY', 'SR', 'ZC', 'TA', 'MA', 'SA', 'FG', 'PF',
                # 能源所
                'sc', 'nr', 'lu', 'bc'
            ]
            if product_symbol in ['au', 'ag', 'sc']:
                try:
                    assert trading_time_list[0]['open'] == time(hour=21, minute=0)
                    assert trading_time_list[0]['close'] == time(hour=2, minute=30)
                except AssertionError:
                    print(product_symbol)
                    raise
            elif product_symbol in ['cu', 'al', 'zn', 'pb', 'ni', 'sn', 'ss', 'bc']:
                try:
                    assert trading_time_list[0]['open'] == time(hour=21, minute=0)
                    assert trading_time_list[0]['close'] == time(hour=1, minute=0)
                except AssertionError:
                    print(product_symbol)
                    raise
            else:
                try:
                    assert trading_time_list[0]['open'] == time(hour=21, minute=0)
                    assert trading_time_list[0]['close'] == time(hour=23, minute=0)
                except AssertionError:
                    print(product_symbol)
                    raise
            assert trading_time_list[1]['open'] == time(hour=9, minute=0)
            assert trading_time_list[1]['close'] == time(hour=10, minute=15)
            assert trading_time_list[2]['open'] == time(hour=10, minute=30)
            assert trading_time_list[2]['close'] == time(hour=11, minute=30)
            assert trading_time_list[3]['open'] == time(hour=13, minute=30)
            assert trading_time_list[3]['close'] == time(hour=15, minute=0)
