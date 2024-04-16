import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')
MONGO_TASK_1_COLLECTION = os.getenv('MONGO_TASK_1_COLLECTION')
