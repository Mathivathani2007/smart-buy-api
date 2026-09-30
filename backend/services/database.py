import os
from typing import Any, Optional

try:
    from pymongo import MongoClient
except ImportError:
    MongoClient = None

_client: Optional[Any] = None


def get_database():
    global _client
    url = os.getenv("MONGODB_URL")
    if not url or MongoClient is None:
        return None
    if _client is None:
        _client = MongoClient(url, serverSelectionTimeoutMS=1500)
    return _client.get_default_database()


def save_history(record: dict):
    database = get_database()
    if database is not None:
        database.analysis_history.insert_one(record)
