from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Dict, List, Optional, Self

from domain.entities.habits import Habit


@dataclass
class User:
    id: str
    name: str
    email: str
    created_at: datetime
    habits: Optional[List[Habit]]

    @classmethod
    def from_dict(cls, _dict: Dict) -> Self:
        return cls(
            id=_dict.get("_id"),
            name=_dict.get("name"),
            email=_dict.get("email"),
            created_at=_dict.get("created_at"),
            habits=[Habit.from_dict(h) for h in _dict.get("habits", [])],
        )

    def to_dict(self) -> Dict:
        return asdict(self)
