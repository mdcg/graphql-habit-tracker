from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Optional

from domain.constants import DayOfWeek
from domain.exceptions.habits_exceptions import InvalidDateError


class AvailableRules(str, Enum):
    EVERY_DAY = "EVERY_DAY"
    WEEKDAYS = "WEEKDAYS"
    WEEKENDS = "WEEKENDS"
    CUSTOM_DAYS = "CUSTOM_DAYS"
    DATE_INTERVALS = "DATE_INTERVALS"

    @classmethod
    def all(cls):
        return (
            cls.EVERY_DAY.value,
            cls.WEEKDAYS.value,
            cls.WEEKENDS.value,
            cls.CUSTOM_DAYS.value,
            cls.DATE_INTERVALS.value,
        )


class Rule(ABC):
    @abstractmethod
    def check(cls, input: Optional[Dict] = None) -> bool:
        pass

    @abstractmethod
    def parse(cls, input: Optional[Dict] = None) -> Dict:
        pass


class EveryDayRule(Rule):
    @classmethod
    def check(cls, input: Optional[Dict] = None) -> bool:
        return True

    @classmethod
    def parse(cls, input: Optional[Dict] = None) -> Dict:
        return {
            "days": DayOfWeek.all(),
            "date_interval": None,
        }


class WeekdaysRule(Rule):
    @classmethod
    def check(cls, input: Optional[Dict] = None) -> bool:
        return True

    @classmethod
    def parse(cls, input: Optional[Dict] = None) -> Dict:
        return {
            "days": DayOfWeek.weekdays(),
            "date_interval": None,
        }


class WeekendsRule(Rule):
    @classmethod
    def check(cls, input: Optional[Dict] = None) -> bool:
        return True

    @classmethod
    def parse(cls, input: Optional[Dict] = None) -> Dict:
        return {
            "days": DayOfWeek.weekends(),
            "date_interval": None,
        }


class CustomDaysRule(Rule):
    @classmethod
    def check(cls, input: Optional[Dict] = None) -> bool:
        try:
            days_of_week = set(input["days"])
        except Exception:
            return False

        if not len(days_of_week):
            return False

        for day in days_of_week:
            if day not in DayOfWeek.all():
                return False

        return True

    @classmethod
    def parse(cls, input: Optional[Dict] = None) -> Dict:
        if not cls.check(input):
            raise InvalidDateError(
                f"Especificação de datas inválidas. Escolhas possíveis: {DayOfWeek.all()}."
            )

        return {
            "days": list(set(input["days"])),
            "date_interval": None,
        }


class DateIntervalsRule:
    @classmethod
    def check(cls, input: Optional[Dict] = None) -> bool:
        try:
            date_interval = int(input["date_interval"])
        except Exception:
            return False

        return 0 < date_interval <= 7

    @classmethod
    def parse(cls, input: Optional[Dict] = None) -> Dict:
        if not cls.check(input):
            raise InvalidDateError(
                "Intervalo de datas deve ser inteiro e estar entre 1 - 7."
            )

        return {
            "days": None,
            "date_interval": int(input["date_interval"]),
        }
