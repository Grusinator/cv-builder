import json
from typing import Callable
from functools import wraps

from loguru import logger


class Cache:
    _instance = None
    cache_file = "cache.json"

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Cache, cls).__new__(cls, *args, **kwargs)
            cls._instance.load()
        return cls._instance

    def load(self):
        try:
            with open(self.cache_file, "r") as f:
                self.cache_dict = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logger.error("Cache file not found or invalid, creating new cache")
            self.cache_dict = {}

    def save(self):
        with open(self.cache_file, "w+") as f:
            json.dump(self.cache_dict, f, indent=2)

    def get(self, key):
        return self.cache_dict.get(key)

    def set(self, key, value):
        self.cache_dict[key] = value
        self.save()


def cache(func: Callable) -> Callable:
    _cache = Cache()

    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        if args:
            # Handle the case when the first argument is not a native type
            first_arg = args[0]
            try:
                first_arg_json = json.dumps(first_arg)
            except TypeError:
                first_arg_json = str(first_arg)
            key = func_name + first_arg_json + json.dumps((args[1:], kwargs))
        else:
            key = func_name + json.dumps((args, kwargs))

        result = _cache.get(key)
        if result is not None:
            return result
        else:
            result = func(*args, **kwargs)
            _cache.set(key, result)
            return result

    return wrapper
