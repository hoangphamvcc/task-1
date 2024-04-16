import pymongo
from src.config import MONGO_URI, MONGO_DB_NAME, MONGO_TASK_1_COLLECTION


class MongoDB:
    def __init__(self):
        self.__client = pymongo.MongoClient(MONGO_URI)
        self.db = self.__client[MONGO_DB_NAME]
        self.news = self.db[MONGO_TASK_1_COLLECTION]