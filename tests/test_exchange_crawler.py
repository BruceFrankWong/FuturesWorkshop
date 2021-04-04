# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


import pytest

from typing import Dict, List
from datetime import date, timedelta

from FuturesWorkshop.collector.exchange_crawler import (
    check_date,
    crawl_shfe_futures_daily_data,
    crawl_ine_futures_daily_data,
    crawl_cffex_futures_daily_data,
)
from FuturesWorkshop.definition import FuturesDailyData


@pytest.fixture
def exchange_list() -> List[str]:
    return ['SHFE', 'DCE', 'CZCE', 'CFFEX', 'INE']


@pytest.fixture
def earliest_date_dict() -> Dict[str, date]:
    return {
        'SHFE': date(2002, 1, 7),
        'DCE': date(2007, 1, 4),
        'CZCE': date(2005, 4, 29),
        'CFFEX': date(2010, 4, 16),
        'INE': date(2018, 3, 26),
    }


def test_check_date_for_both_none(exchange_list, earliest_date_dict):
    # Variable declaration.
    result_begin: date
    result_end: date
    test_begin: date
    test_end: date

    # Test for begin is None, and end is None
    for exchange in exchange_list:
        result_begin, result_end = check_date(exchange)
        assert result_begin == earliest_date_dict[exchange]
        assert result_end == date.today()

    # Test for end < begin.
    test_begin = date(2021, 4, 4)
    test_end = date(2021, 4, 1)
    for exchange in exchange_list:
        with pytest.raises(ValueError):
            check_date(exchange, test_begin, test_end)

    # Test for <begin> is less than <earliest_date>.
    for exchange in exchange_list:
        test_begin = earliest_date_dict[exchange] - timedelta(days=5)
        with pytest.raises(ValueError):
            check_date(exchange, test_begin, None)

    # Test for <end> is less than <earliest_date>.
    for exchange in exchange_list:
        test_end = earliest_date_dict[exchange] - timedelta(days=5)
        with pytest.raises(ValueError):
            check_date(exchange, None, test_end)

    # Test for <begin> is less than <earliest_date>.
    for exchange in exchange_list:
        test_begin = date.today() + timedelta(days=5)
        with pytest.raises(ValueError):
            check_date(exchange, test_begin, None)

    # Test for <begin> is less than <earliest_date>.
    for exchange in exchange_list:
        test_end = date.today() + timedelta(days=5)
        with pytest.raises(ValueError):
            check_date(exchange, None, test_end)

    # Test for valid value.
    for exchange in exchange_list:
        test_begin = date(2021, 1, 6)
        test_end = date(2021, 3, 31)
        result_begin, result_end = check_date(exchange, test_begin, test_end)
        assert result_begin == test_begin
        assert result_end == test_end


def test_crawl_shfe_futures_daily_data():
    product_shfe: List[str] = [
        'au', 'ag', 'cu', 'al', 'zn', 'pb', 'ni', 'sn', 'rb', 'wr', 'hc', 'ss', 'fu', 'bu', 'ru', 'sp'
    ]
    result = crawl_shfe_futures_daily_data(date(2021, 4, 1))
    assert isinstance(result, dict)
    assert len(result) == len(product_shfe)
    for k, v in result.items():
        assert isinstance(k, str)
        assert k in product_shfe
        assert isinstance(v, list)
        for item in v:
            assert isinstance(item, FuturesDailyData)


def test_crawl_ine_futures_daily_data():
    product_ine: List[str] = [
        'sc', 'lu', 'nr', 'bc'
    ]
    result = crawl_ine_futures_daily_data(date(2021, 4, 1))
    assert isinstance(result, dict)
    assert len(result) == len(product_ine)
    for k, v in result.items():
        assert isinstance(k, str)
        assert k in product_ine
        assert isinstance(v, list)
        for item in v:
            assert isinstance(item, FuturesDailyData)


def test_crawl_cffex_futures_daily_data():
    product_ine: List[str] = [
        'IC', 'IF', 'IH', 'T', 'TS', 'TF'
    ]
    result = crawl_cffex_futures_daily_data(date(2021, 4, 1))
    assert isinstance(result, dict)
    assert len(result) == len(product_ine)
    for k, v in result.items():
        assert isinstance(k, str)
        assert k in product_ine
        assert isinstance(v, list)
        for item in v:
            assert isinstance(item, FuturesDailyData)
