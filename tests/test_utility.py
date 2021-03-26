# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Dict, List

from FuturesWorkshop.config import CONFIGS
from FuturesWorkshop.utility import (
    get_exchange_symbol_list,
    get_exchange_name_list,
    get_exchange_symbol_by_name,
    get_product_symbol_list,
    get_product_name_list,
    get_product_symbol_by_name,
    get_stop_loss_settings,
)


def test_get_exchange_symbol_list():
    exchange_symbol_list: List[str] = [
        'SHFE', 'DCE', 'CZCE', 'CFFEX', 'INE',
    ]
    result = get_exchange_symbol_list()
    assert isinstance(result, list)
    assert len(result) == len(exchange_symbol_list)
    for item in result:
        assert item in exchange_symbol_list


def test_get_exchange_name_list():
    exchange_name_list: List[str] = [
        '上海期货交易所', '大连商品交易所', '郑州商品交易所', '中国金融期货交易所', '上海国际能源交易中心',
    ]
    result = get_exchange_name_list()
    assert isinstance(result, list)
    assert len(result) == len(exchange_name_list)
    for item in result:
        assert item in exchange_name_list


def test_get_exchange_symbol_by_name():
    exchange_name_dict: Dict[str, str] = {
        'SHFE': '上海期货交易所',
        'DCE': '大连商品交易所',
        'CZCE': '郑州商品交易所',
        'CFFEX': '中国金融期货交易所',
        'INE': '上海国际能源交易中心',
    }
    for k, v in exchange_name_dict.items():
        assert get_exchange_symbol_by_name(v) == k


def test_get_product_symbol_list():
    product_symbol_list: List[str] = [
        'au', 'ag', 'cu', 'al', 'zn',
        'pb', 'ni', 'sn', 'rb', 'wr',
        'hc', 'ss', 'fu', 'bu', 'ru',
        'sp', 'c', 'cs', 'a', 'b',
        'm', 'y', 'p', 'fb', 'bb',
        'jd', 'rr', 'lh', 'l', 'v',
        'pp', 'eg', 'eb', 'pg', 'j',
        'jm', 'i', 'WH', 'PM', 'RI',
        'JR', 'LR', 'OI', 'RS', 'RM',
        'CF', 'CY', 'SR', 'AP', 'CJ',
        'PK', 'ZC', 'SF', 'SM', 'TA',
        'MA', 'UR', 'SA', 'FG', 'PF',
        'sc', 'lu', 'nr', 'bc', 'IC',
        'IF', 'IH', 'T', 'TF', 'TS',
    ]
    result = get_product_symbol_list()
    assert isinstance(result, list)
    assert len(result) == len(product_symbol_list)
    for item in result:
        assert item in product_symbol_list


def test_get_product_name_list():
    product_name_list: List[str] = [
        '黄金', '白银', '铜', '铝', '锌', '铅', '镍', '锡', '螺纹钢', '线材', '热轧卷板', '不锈钢', '燃料油',
        '石油沥青', '天然橡胶', '纸浆', '玉米', '玉米淀粉', '黄大豆一号', '黄大豆二号', '豆粕', '豆油',
        '棕榈油', '纤维板', '胶合板', '鸡蛋', '粳米', '生猪', '聚乙烯', '聚氯乙烯', '聚丙烯', '乙二醇',
        '苯乙烯', '液化石油气', '焦炭', '焦煤', '铁矿石', '强麦', '普麦', '早籼稻', '粳稻', '晚籼稻',
        '菜籽油', '油菜籽', '菜籽粕', '棉花', '棉纱', '白糖', '苹果', '红枣', '花生', '动力煤', '硅铁', '锰硅',
        'PTA', '甲醇', '尿素', '纯碱', '玻璃', '短纤', '原油', '低硫燃料油', '20号胶', '国际铜',
         '中证500股指期货', '沪深300股指期货', '上证50股指期货', '10年期国债期货', '5年期国债期货', '2年期国债期货',
    ]
    result = get_product_name_list()
    assert isinstance(result, list)
    assert len(result) == len(product_name_list)
    for item in result:
        assert item in product_name_list


def test_get_product_symbol_by_name():
    product_name_dict: Dict[str, str] = {
        'au': '黄金',
        'ag': '白银',
        'cu': '铜',
        'al': '铝',
        'zn': '锌',
        'pb': '铅',
        'ni': '镍',
        'sn': '锡',
        'rb': '螺纹钢',
        'wr': '线材',
        'hc': '热轧卷板',
        'ss': '不锈钢',
        'fu': '燃料油',
        'bu': '石油沥青',
        'ru': '天然橡胶',
        'sp': '纸浆',
        'c': '玉米',
        'cs': '玉米淀粉',
        'a': '黄大豆一号',
        'b': '黄大豆二号',
        'm': '豆粕',
        'y': '豆油',
        'p': '棕榈油',
        'fb': '纤维板',
        'bb': '胶合板',
        'jd': '鸡蛋',
        'rr': '粳米',
        'lh': '生猪',
        'l': '聚乙烯',
        'v': '聚氯乙烯',
        'pp': '聚丙烯',
        'eg': '乙二醇',
        'eb': '苯乙烯',
        'pg': '液化石油气',
        'j': '焦炭',
        'jm': '焦煤',
        'i': '铁矿石',
        'WH': '强麦',
        'PM': '普麦',
        'RI': '早籼稻',
        'JR': '粳稻',
        'LR': '晚籼稻',
        'OI': '菜籽油',
        'RS': '油菜籽',
        'RM': '菜籽粕',
        'CF': '棉花',
        'CY': '棉纱',
        'SR': '白糖',
        'AP': '苹果',
        'CJ': '红枣',
        'PK': '花生',
        'ZC': '动力煤',
        'SF': '硅铁',
        'SM': '锰硅',
        'TA': 'PTA',
        'MA': '甲醇',
        'UR': '尿素',
        'SA': '纯碱',
        'FG': '玻璃',
        'PF': '短纤',
        'sc': '原油',
        'lu': '低硫燃料油',
        'nr': '20号胶',
        'bc': '国际铜',
        'IC': '中证500股指期货',
        'IF': '沪深300股指期货',
        'IH': '上证50股指期货',
        'T': '10年期国债期货',
        'TF': '5年期国债期货',
        'TS': '2年期国债期货',
    }
    for k, v in product_name_dict.items():
        assert get_product_symbol_by_name(v) == k


def test_get_stop_loss_settings():
    result = get_stop_loss_settings()
    assert isinstance(result, dict) is True
    assert len(result) == len(CONFIGS['index']['product'])
    for product_symbol, setting in result.items():
        assert isinstance(setting, dict) is True
        for k, v in setting.items():
            assert isinstance(k, str) is True
            assert isinstance(v, int) is True
