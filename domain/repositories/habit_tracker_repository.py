from abc import ABC, abstractmethod
from typing import List

from domain.entities.users import User


class HabitTrackerRepository(ABC):
    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_user_by_id(self, id: str) -> User:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def list_users(self, limit: int, offset: int) -> List[User]:
        pass

    @abstractmethod
    def create_habit(self) -> User:
        pass

    @abstractmethod
    def delete_habit(self, user_id: str, habit_id: str) -> User:
        pass

    # @abstractmethod
    # def get_habit_by_id(self):
    #     pass

    # @abstractmethod
    # def list_user_habits(self):
    #     pass

    # @abstractmethod
    # def update_habit(self):
    #     pass

    # @abstractmethod
    # def delete_habit(self):
    #     pass

    # @abstractmethod
    # def record_habit_progress(self):
    #     pass

    # @abstractmethod
    # def list_habit_logs(self):
    #     pass
