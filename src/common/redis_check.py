from redis import Redis
import json


class RedisCache:

    def __init__(self, payload: dict):
        """payload dataform: {'payload': {"plan_name": "s3:cold",
                                            "category_code": "default",
                                            "quantity": 10}}"""
        self.redis = Redis(host='localhost', port=6379, db=0)
        self._key = False
        self.payload = payload
        self.data = None

    def redis_data_check(self):
        if self.redis.get(json.dumps(self.payload)) is not None:
            self._key = True
            self.data = self.redis.get(json.dumps(self.payload)).decode('utf-8')
        return self._key

    def redis_save(self, response_data: float):
        self.redis.set(json.dumps(self.payload), response_data)


"""payload = {
    'payload': {"plan_name": "s3:cold",
                "category_code": "default",
                "quantity": 10
                }, 'amount': 52}

data = RedisCache(payload)
#data.redis_save(1)
print(data.redis_data_check(), data.data)"""


