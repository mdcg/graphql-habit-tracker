from datetime import datetime, timezone
from typing import List

from bson import ObjectId
from bson.errors import InvalidId
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from domain.entities.habits import Habit
from domain.entities.users import User
from domain.exceptions.habits_exceptions import HabitNotFoundError
from domain.exceptions.users_exceptions import (
    UserAlreadyRegisteredError,
    UserNotFoundError,
)
from domain.repositories.habit_tracker_repository import HabitTrackerRepository
from infrastructure.settings import settings


class MongoHabitTrackerRepository(HabitTrackerRepository):
    def __init__(self, client: MongoClient = None):
        self.MAX_LIMIT = 100

        self.client = client or MongoClient(settings.MONGODB_URL)
        db = self.client.habit_tracker

        self.collection = db.users
        self.collection.create_index("email", unique=True)

    def create_user(self, user: User) -> User:
        user.created_at = datetime.now(timezone.utc)
        try:
            result = self.collection.insert_one(user.to_dict())
        except DuplicateKeyError:
            raise UserAlreadyRegisteredError("E-mail já cadastrado.")

        user.id = result.inserted_id
        return user

    def get_user_by_id(self, _id: str) -> User:
        try:
            doc = self.collection.find_one({"_id": ObjectId(_id)})
        except InvalidId:
            raise UserNotFoundError("ID inválido.")

        if not doc:
            raise UserNotFoundError("Usuário não encontrado.")

        return User.from_dict(doc)

    def get_user_by_email(self, email: str) -> User:
        doc = self.collection.find_one({"email": email})
        if not doc:
            raise UserNotFoundError("Usuário não encontrado.")

        return User.from_dict(doc)

    def list_users(self, limit: int = 20, offset: int = 0) -> List[User]:
        limit = max(1, min(int(limit), self.MAX_LIMIT))
        offset = max(0, int(offset))

        cursor = (
            self.collection.find({}, {"habits": {"$slice": 5}})
            .sort([("_id", 1)])
            .skip(offset)
            .limit(limit)
        )

        return [User.from_dict(doc) for doc in cursor]

    def create_habit(self, user_id: str, habit: Habit) -> User:
        user = self.get_user_by_id(user_id)
        habit.id = ObjectId()
        habit.created_at = datetime.now(timezone.utc)
        self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$push": {"habits": habit.to_dict()}},
        )
        user.habits.append(habit)
        return user

    def delete_habit(self, user_id: str, habit_id: str) -> User:
        user = self.get_user_by_id(user_id)
        result = self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$pull": {"habits": {"id": ObjectId(habit_id)}}},
        )

        if result.modified_count == 0:
            raise HabitNotFoundError("Hábito não encontrado para o usuário.")

        user.habits = [habit for habit in user.habits if str(habit.id) != habit_id]
        return user
