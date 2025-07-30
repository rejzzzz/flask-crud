from pymongo import MongoClient
from config import Config
import logging

_client = None
_db = None


def get_db():
    global _client, _db

    if _client is None:
        try:
            # Connect to MongoDB
            _client = MongoClient(
                Config.MONGO_URI,
                serverSelectionTimeoutMS=5000,
                maxPoolSize=50,
                socketTimeoutMS=30000
            )

            # Test connection
            _client.admin.command('ping')

            db_name = Config.MONGO_URI.split('/')[-1].split('?')[0]
            if not db_name:
                raise ValueError("Database name not found in MONGO_URI")

            _db = _client[db_name]  # Use explicit database name
            logging.info(f"Connected to MongoDB database: {db_name}")

        except Exception as e:
            logging.critical(f"Failed to connect to MongoDB: {e}")
            raise RuntimeError("Unable to connect to the database") from e

    return _db['users']