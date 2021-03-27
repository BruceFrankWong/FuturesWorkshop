# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from datetime import date

from FuturesWorkshop.collector.exchange_crawler import crawl_shfe_futures_daily_data


if __name__ == '__main__':
    x = crawl_shfe_futures_daily_data(
        begin=date(2002, 1, 7),
        end=date(2021, 3, 27)
    )
    for item in x:
        print('-'*10)
        print(item)
