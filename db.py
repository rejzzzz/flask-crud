# database.py
from pymongo import MongoClient
from config import Config
import logging

_client = None
_db = None


def get_db():
    """
    Singleton pattern to ensure only one MongoDB connection client
    is created per application instance.
    Returns the 'users' collection.
    """
    global _client, _db

    if _client is None:
        try:
            _client = MongoClient(
                Config.MONGO_URI,
                serverSelectionTimeoutMS=5000,# 5s
                maxPoolSize=50,
                socketTimeoutMS=30000
            )
            # Test the connection
            _client.admin.command('ping')
            _db = _client.get_default_database()  # Uses DB from MONGO_URI (e.g., ?authSource=admin)
            logging.info("Connected to MongoDB successfully.")
        except Exception as e:
            logging.critical(f"Failed to connect to MongoDB: {e}")
            raise RuntimeError("Unable to connect to the database") from e

    return _db['users']