from dotenv import dotenv_values
from pymongo import MongoClient

mongo_config = dotenv_values('.env_mongo')


class DatabaseManager:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DatabaseManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.client = MongoClient(mongo_config['MONGO_URI'])
        self.db = self.client[mongo_config['MONGO_DB_NAME']]
        self.collection = self.db[mongo_config['MONGO_COLLECTION_NAME']]

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def close_db(self):
        self.client.close()
