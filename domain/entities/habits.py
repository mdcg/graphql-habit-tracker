from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Dict, List, Optional, Self

from domain.entities.rules import (
    AvailableRules,
    CustomDaysRule,
    DateIntervalsRule,
    EveryDayRule,
    Rule,
    WeekdaysRule,
    WeekendsRule,
)
from domain.exceptions.habits_exceptions import InvalidHabitRuleError


@dataclass
class HabitRule:
    rule_name: str
    days: Optional[List] = None
    date_interval: Optional[int] = None

    def __post_init__(self):
        rule = self._get_rule()
        rule_data = rule.parse(asdict(self))

        try:
            self.days = rule_data["days"]
            self.date_interval = rule_data["date_interval"]
        except KeyError:
            raise InvalidHabitRuleError(
                "Implementação da regra não possui os campos corretos."
            )

    def _get_rule(self) -> Rule:
        available_rules = {
            AvailableRules.EVERY_DAY: EveryDayRule,
            AvailableRules.WEEKDAYS: WeekdaysRule,
            AvailableRules.WEEKENDS: WeekendsRule,
            AvailableRules.CUSTOM_DAYS: CustomDaysRule,
            AvailableRules.DATE_INTERVALS: DateIntervalsRule,
        }

        try:
            rule = available_rules[self.rule_name]
        except KeyError:
            raise InvalidHabitRuleError(
                f"Regra inválida. Regras disponível: {AvailableRules.all()}"
            )

        return rule

    @classmethod
    def from_dict(cls, _dict: Dict) -> Self:
        return cls(
            rule_name=_dict["rule_name"],
            days=_dict["days"],
            date_interval=_dict["date_interval"],
        )


@dataclass
class Habit:
    id: str
    name: str
    rule: HabitRule
    created_at: datetime
    description: Optional[str] = None

    @classmethod
    def from_dict(cls, _dict: Dict) -> Self:
        return cls(
            id=_dict["id"],
            description=_dict["description"],
            name=_dict["name"],
            created_at=_dict["created_at"],
            rule=HabitRule.from_dict(_dict["rule"]),
        )

    def to_dict(self) -> Dict:
        return asdict(self)
