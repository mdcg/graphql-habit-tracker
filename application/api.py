from datetime import datetime
from typing import List, Optional, Self

import strawberry
import uvicorn
from fastapi import FastAPI
from graphql import GraphQLError
from strawberry.asgi import GraphQL

from domain.entities.habits import Habit, HabitRule
from domain.entities.users import User
from domain.exceptions.users_exceptions import (
    UserAlreadyRegisteredError,
    UserNotFoundError,
)
from infrastructure.mongo.mongo_habit_tracker_repository import (
    MongoHabitTrackerRepository,
)


@strawberry.type
class HabitRuleGraphQL:
    user_id: strawberry.ID
    rule_name: str
    days: Optional[List[str]] = None
    date_interval: Optional[int] = None

    def to_domain(self):
        return HabitRule(
            rule_name=self.rule_name,
            days=self.days,
            date_interval=self.date_interval,
        )


@strawberry.type
class HabitGraphQL:
    id: strawberry.ID
    name: str
    rule: HabitRuleGraphQL
    description: Optional[str] = None
    created_at: datetime

    @classmethod
    def from_domain(cls, habit: Habit) -> Self:
        return cls(
            id=habit.id,
            name=habit.name,
            rule=habit.rule,
            description=habit.description,
            created_at=habit.created_at,
        )


@strawberry.input
class HabitRuleInputGraphQL:
    rule_name: str
    days: Optional[List[str]] = None
    date_interval: Optional[int] = None

    def to_domain(self):
        return HabitRule(
            rule_name=self.rule_name,
            days=self.days,
            date_interval=self.date_interval,
        )


@strawberry.input
class HabitInputGraphQL:
    user_id: strawberry.ID
    name: str
    rule: HabitRuleInputGraphQL
    description: Optional[str] = None

    def to_domain(self):
        return Habit(
            id=None,
            created_at=None,
            name=self.name,
            rule=self.rule.to_domain(),
            description=self.description,
        )


@strawberry.type
class UserGraphQL:
    id: strawberry.ID
    name: str
    email: str
    created_at: datetime
    habits: Optional[List[HabitGraphQL]]

    @classmethod
    def from_domain(cls, user: User) -> Self:
        return cls(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at,
            habits=[HabitGraphQL.from_domain(h) for h in user.habits],
        )


@strawberry.input
class UserInputGraphQL:
    name: str
    email: str

    def to_domain(self):
        return User(
            name=self.name,
            email=self.email,
            created_at=None,
            id=None,
            habits=[],
        )


@strawberry.type
class Query:
    @strawberry.field
    def get_user_by_id(self, id: str) -> UserGraphQL:
        repository = MongoHabitTrackerRepository()
        try:
            user = repository.get_user_by_id(id)
        except UserNotFoundError as err:
            raise GraphQLError(str(err))

        return UserGraphQL.from_domain(user)

    @strawberry.field
    def get_user_by_email(self, email: str) -> UserGraphQL:
        repository = MongoHabitTrackerRepository()
        try:
            user = repository.get_user_by_email(email)
        except UserNotFoundError as err:
            raise GraphQLError(str(err))

        return UserGraphQL.from_domain(user)

    @strawberry.field
    def list_users(self, limit: int = 20, offset: int = 0) -> List[UserGraphQL]:
        repository = MongoHabitTrackerRepository()
        users = repository.list_users(limit, offset)
        return [UserGraphQL.from_domain(user) for user in users]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, user: UserInputGraphQL) -> UserGraphQL:
        repository = MongoHabitTrackerRepository()
        try:
            user = repository.create_user(user.to_domain())
        except UserAlreadyRegisteredError as err:
            raise GraphQLError(str(err))

        return UserGraphQL.from_domain(user)

    @strawberry.mutation
    def create_habit(self, habit: HabitInputGraphQL) -> UserGraphQL:
        repository = MongoHabitTrackerRepository()
        user_id = habit.user_id
        try:
            user = repository.create_habit(user_id, habit.to_domain())
        except Exception as err:
            raise GraphQLError(str(err))

        return UserGraphQL.from_domain(user)

    @strawberry.mutation
    def delete_habit(
        self, user_id: strawberry.ID, habit_id: strawberry.ID
    ) -> UserGraphQL:
        repository = MongoHabitTrackerRepository()
        try:
            user = repository.delete_habit(user_id, habit_id)
        except Exception as err:
            raise GraphQLError(str(err))

        return UserGraphQL.from_domain(user)


schema = strawberry.Schema(query=Query, mutation=Mutation)

app = FastAPI()


@app.get("/")
def index():
    return {"Hello": "World"}


app.add_route("/graphql", GraphQL(schema))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
