# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from enum import Enum


__all__ = ['PeriodUnitEnum', 'Period', 'PeriodEnum']


class PeriodUnitEnum(Enum):
    Tick = 'Tick'
    Second = 'Second'
    Minute = 'Minute'
    Hour = 'Hour'
    Day = 'Day'
    Week = 'Week'
    Month = 'Month'
    Year = 'Year'

    def to_second(self) -> int:
        if self.value == 'Tick':
            return 0
        elif self.value == 'Second':
            return 1
        elif self.value == 'Minute':
            return 60
        elif self.value == 'Hour':
            return 60 * 60
        elif self.value == 'Day':
            return 60 * 60 * 24
        elif self.value == 'Week':
            return 60 * 60 * 24 * 5
        elif self.value == 'Month':
            return 60 * 60 * 24 * 5 * 4
        elif self.value == 'Year':
            return 60 * 60 * 24 * 5 * 4 * 12

    def to_chinese(self) -> str:
        if self.value == 'Tick':
            return 'Tick'
        elif self.value == 'Second':
            return '秒'
        elif self.value == 'Minute':
            return '分钟'
        elif self.value == 'Hour':
            return '小时'
        elif self.value == 'Day':
            return '日'
        elif self.value == 'Week':
            return '周'
        elif self.value == 'Month':
            return '月'
        elif self.value == 'Year':
            return '年'


class Period(object):
    unit: PeriodUnitEnum
    frequency: int

    def __init__(self, frequency: int, unit: PeriodUnitEnum):
        self.unit = unit
        if frequency < 1:
            raise ValueError('parameter <frequency> should be a positive integer.')
        else:
            self.frequency = frequency

    def to_second(self) -> int:
        return self.frequency * self.unit.to_second()

    def to_english(self) -> str:
        return f'{str(self.frequency) if self.frequency > 1 else ""}{self.unit.value}'

    def to_chinese(self) -> str:
        return f'{str(self.frequency) if self.frequency > 1 else ""}{self.unit.to_chinese()}'

    def __repr__(self) -> str:
        return f'<QWPeriod(frequency={self.frequency}), unit={self.unit.value}>'

    def __str__(self) -> str:
        result: str = ''
        if self.frequency > 1:
            result += str(self.frequency)
        result += self.unit.value
        return result


class PeriodEnum(Enum):
    Tick = Period(1, PeriodUnitEnum.Tick)
    Minute_1 = Period(1, PeriodUnitEnum.Minute)
    Minute_5 = Period(5, PeriodUnitEnum.Minute)
    Minute_15 = Period(15, PeriodUnitEnum.Minute)
    Hour = Period(1, PeriodUnitEnum.Hour)
    Day = Period(1, PeriodUnitEnum.Day)
