import json
from typing import Callable
from functools import wraps

def cache(func: Callable) -> Callable:
    cache_file = "cache.json"
    try:
        with open(cache_file, "r") as f:
            cache_dict = json.load(f)
    except FileNotFoundError:
        cache_dict = {}

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

        if key in cache_dict:
            return cache_dict[key]
        else:
            result = func(*args, **kwargs)
            cache_dict[key] = result
            with open(cache_file, "w") as f:
                json.dump(cache_dict, f)
            return result

    return wrapper