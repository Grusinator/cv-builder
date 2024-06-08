import json
from datetime import datetime, date
from functools import wraps
from typing import Callable

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


def to_string_if_class_or_instance(obj):
    if isinstance(obj, (dict, tuple, list, float, int, str, bool, datetime, date)):
        return obj
    elif hasattr(obj, "__name__"):
        return obj.__name__
    elif hasattr(obj, "__class__"):
        return obj.__class__.__name__
    else:
        return obj


def cache(func: Callable) -> Callable:
    _cache = Cache()

    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        _args = [to_string_if_class_or_instance(arg) for arg in args]
        key = f"{func_name}__{json.dumps((_args, kwargs))}"
        result = _cache.get(key)
        if result is not None:
            return result
        else:
            result = func(*args, **kwargs)
            _cache.set(key, result)
            return result

    return wrapper
