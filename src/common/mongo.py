import pymongo
from src.config import MONGO_URI, MONGO_DB_NAME, MONGO_TASK_1_COLLECTION, MONGO_MAINTAINFEE_SERVICE_COLLECTION,\
    MONGO_MAINTAINFEE_RESOURCE_COLLECTION,MONGO_MAINTAINHOUR_RESOURCE_COLLECTION, MONGO_MAINTAINHOUR_SERVICE_COLLECTION, \
    MONGO_MAINTAIN_SERVICE, MONGO_MAINTAIN_PLAN


class MongoDB:
    def __init__(self):
        self.__client = pymongo.MongoClient(MONGO_URI)
        self.db = self.__client[MONGO_DB_NAME]
        self.maintain_hours = self.db[MONGO_TASK_1_COLLECTION]
        self.maintain_fee_service = self.db[MONGO_MAINTAINFEE_SERVICE_COLLECTION]
        self.maintain_fee_resource = self.db[MONGO_MAINTAINFEE_RESOURCE_COLLECTION]
        self.maintain_hour_resource = self.db[MONGO_MAINTAINHOUR_RESOURCE_COLLECTION]
        self.maintain_hour_service = self.db[MONGO_MAINTAINHOUR_SERVICE_COLLECTION]
        self.maintain_service = self.db[MONGO_MAINTAIN_SERVICE]
        self.maintain_plan = self.db[MONGO_MAINTAIN_PLAN]