#!/usr/bin/env python3
"""0x02-redis_basic"""
import redis
import uuid
from typing import Union
from typing import Callable


class Cache:
    """this is theclass Cache"""
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """this is store method that
        that takes a data argument and returns a string"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, None]:
        """this is get method that take a key string
        argument and an optional Callable argument named fn"""
        data = self._redis.get(key)
        if data is None:
            return None

        return fn(data) if fn else data

    def get_str(self, key: str) -> str:
        """get_str method"""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """get_int method"""
        return self.get(key, fn=int)


if __name__ == "__main__":
"""    
    cache = Cache()

    data = b"hello"
    key = cache.store(data)
    print(key)

    local_redis = redis.Redis()
    print(local_redis.get(key))
"""
    cache = Cache()

    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value
