# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from pathlib import Path

from FuturesWorkshop.config import PACKAGE_PATH, CONFIGS, load_csv, save_csv, load_config, save_config


def test_package_path():
    package_path: Path = PACKAGE_PATH
    assert package_path == Path(r'D:\Development\Python\FuturesWorkshop/FuturesWorkshop')


def test_configs():
    configs: dict = CONFIGS
    assert len(configs.keys()) == 3
    assert 'exchange' in configs.keys()
    assert 'product' in configs.keys()
    assert 'stop' in configs.keys()

    assert isinstance(configs['exchange'], list) is True
    for item in configs['exchange']:
        assert isinstance(item, dict) is True
        for k, v in item.items():
            assert isinstance(k, str) is True
            assert (k == 'symbol' or k == 'name') is True
            assert isinstance(v, str) is True

    assert isinstance(configs['product'], list) is True
    for item in configs['product']:
        assert isinstance(item, dict) is True
        for k, v in item.items():
            assert isinstance(k, str) is True
            assert (k == 'exchange' or k == 'symbol' or k == 'name' or k == 'fluctuation' or k == 'multiplier') is True
            if k in ['exchange', 'symbol', 'name']:
                assert isinstance(v, str) is True
            elif k == 'fluctuation':
                assert (isinstance(v, float) or isinstance(v, int)) is True
            elif k == 'multiplier':
                assert isinstance(v, int) is True

    assert isinstance(configs['stop'], list) is True
    for item in configs['stop']:
        assert isinstance(item, dict) is True
        for k, v in item.items():
            assert isinstance(k, str) is True
            assert (k == 'symbol' or k == 'long' or k == 'short') is True
            if k == 'symbol':
                assert isinstance(v, str) is True
            else:
                assert isinstance(v, int) is True
