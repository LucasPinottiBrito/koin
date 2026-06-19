from pymongo import MongoClient
from pymongo.database import Database

from src.config.settings import get_settings


class MongoAdapter:
    """Initial MongoDB adapter for future audit and processing records."""

    def __init__(self) -> None:
        settings = get_settings()
        self._client: MongoClient = MongoClient(settings.mongo_url, serverSelectionTimeoutMS=1000)
        self._database_name = settings.mongo_database

    @property
    def database(self) -> Database:
        return self._client[self._database_name]

    def ping(self) -> bool:
        self._client.admin.command("ping")
        return True

    def close(self) -> None:
        self._client.close()
