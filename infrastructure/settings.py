from dataclasses import dataclass
from os import environ

dataclass


class Settings:
    MONGODB_URL = environ.get("MONGODB_URL", "mongodb://localhost:27017/")


settings = Settings()
