#!/usr/bin/env python3
"""0x02-redis_basic"""
import redis
import uuid
from typing import Union
from typing import Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """decorator that takes a single method
    Callable argument and returns a Callable"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """this is theclass Cache"""
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """this is store method that
        that takes a data argument and returns a string"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self,
        key: str,
        fn: Callable = None
    ) -> Union[str, bytes, int, None]:
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
    cache = Cache()
    cache.store(b"first")
    print(cache.get(cache.store.__qualname__))
    cache.store(b"second")
    cache.store(b"third")
    print(cache.get(cache.store.__qualname__))
