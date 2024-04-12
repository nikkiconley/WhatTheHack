import redis
import json
import os


class RedisUtil:
    """Utility class to handle interacting with Redis to store and retrieve cached data"""

    def __init__(self):
        """Initialize RedisUtil object"""
        redis_host = os.environ.get('REDIS_HOST')
        redis_port = int(os.environ.get('REDIS_PORT', "6380"))
        redis_password = os.environ.get('REDIS_PASSWORD')

        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, ssl=True)

    def set(self, key, value):
        """Sets a value in the redis for the specified key"""
        self.redis_client.set(key, value)
        return self

    def set_json(self, key, value):
        """Sets a value in the redis for the specified key after the item is JSON serialized"""
        value_to_serialize = json.dumps(value)
        return self.set(key, value_to_serialize)

    def get(self, key):
        """Gets a value from the redis for the specified key"""
        return self.redis_client.get(key)

    def get_json(self, key):
        """Gets a deserialized value from the redis for the specified key"""
        serialized_value = self.get(key)
        de_serialized_value = json.loads(serialized_value)
        return de_serialized_value

    def delete(self, key):
        """Deletes a value from the redis for the specified key"""
        self.redis_client.delete(key)

    def l_push(self, key, values):
        """Appends a value to the head of the list for the specified key to the head of the list"""
        self.redis_client.lpush(key, values)
        return self

    def l_range(self, key, start, end):
        """Retrieves the items in the list for the specified key"""
        return self.redis_client.lrange(key, start, end)

    def r_push(self, key, values):
        """Appends a value to the tail of the list for the specified key to the head of the list"""
        self.redis_client.lpush(key, values)
        return self

    def r_push_json(self, key, values):
        """Appends a value to the tail of the list for the specified key to the head of the list"""
        value_to_serialize = json.dumps(values)
        return self.r_push(key, value_to_serialize)

    def l_push_json(self, key, values):
        value_to_serialize = json.dumps(values)
        return self.l_push(key, value_to_serialize)

    def l_range_json(self, key, start, end):
        serialized_values = self.l_range(key, start, end)
        deserialized_values: list = []
        for serialized_value in serialized_values:
            deserialized_value = json.loads(serialized_value)
            deserialized_values.append(deserialized_value)
        return deserialized_values

    def increment(self, key, increment: int = 1):
        return self.redis_client.incrby(key, increment)

    def increment_float(self, key, increment: float = 1.0):
        return self.redis_client.incrbyfloat(key, increment)

    def decrement(self, key, decrement: int = 1):
        return self.redis_client.decrby(key, decrement)

    def decrement_float(self, key, decrement: float = 1.0):
        return self.redis_client.incrbyfloat(key, (decrement * -1.0))

    def exists(self, key):
        return self.redis_client.exists(key)

    def expire(self, key: str, time: int):
        return self.redis_client.expire(key, time)

    def set_expire(self, key, value, time: int):
        return self.redis_client.setex(key, value, time)
