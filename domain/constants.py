from enum import Enum


class DayOfWeek(Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"

    @classmethod
    def all(cls):
        return (
            cls.MONDAY.value,
            cls.TUESDAY.value,
            cls.WEDNESDAY.value,
            cls.THURSDAY.value,
            cls.FRIDAY.value,
            cls.SATURDAY.value,
            cls.SUNDAY.value,
        )

    @classmethod
    def weekdays(cls):
        return (
            cls.MONDAY.value,
            cls.TUESDAY.value,
            cls.WEDNESDAY.value,
            cls.THURSDAY.value,
            cls.FRIDAY.value,
        )

    @classmethod
    def weekends(cls):
        return (
            cls.SATURDAY.value,
            cls.SUNDAY.value,
        )
