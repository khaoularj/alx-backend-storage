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


def call_history(method: Callable) -> Callable:
    """decorator that takes a single method
    Callable argument and returns a Callable"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_k = f"{method.__qualname__}:inputs"
        output_k = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_k, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(output_k, res)
        return res
    return wrapper


class Cache:
    """this is theclass Cache"""
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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


def replay(method):
    """function to display the history of calls of a particular function"""
    input_k = f"{method.__qualname__}:inputs"
    output_k = f"{method.__qualname__}:outputs"

    inputs = cache._redis.lrange(input_k, 0, -1)
    outputs = cache._redis.lrange(output_k, 0, -1)

    if not inputs:
        print("No history for this method.")
        return

    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for inp, outp in zip(inputs, outputs):
        args = eval(inp.decode())
        print(f"{method.__qualname__}(*{args}) -> {outp.decode()}")


if __name__ == "__main__":
    cache = Cache()

    s1 = cache.store("first")
    print(s1)
    s2 = cache.store("second")
    print(s2)
    s3 = cache.store("third")
    print(s3)

    inputs = cache._redis.lrange(f"{cache.store.__qualname__}:inputs", 0, -1)
    outputs = cache._redis.lrange(f"{cache.store.__qualname__}:outputs", 0, -1)

    print("inputs:", inputs)
    print("outputs:", outputs)
