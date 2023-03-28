from functools import lru_cache
from typing import Callable
from inspect import signature


@lru_cache(maxsize=2048)
def count_parameters(func: Callable) -> int:
    """Count the number of parameters in a callable"""
    return len(signature(func).parameters)
