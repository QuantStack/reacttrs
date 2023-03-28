# this is a partial copy/paste from:
# https://github.com/Textualize/textual/blob/ed28a7019c1cb3343c8e8284ff82d984800fb579/src/textual/_callback.py

from functools import lru_cache
from typing import Callable
from inspect import signature


@lru_cache(maxsize=2048)
def count_parameters(func: Callable) -> int:
    """Count the number of parameters in a callable"""
    return len(signature(func).parameters)
