from __future__ import annotations

from .reactive import Reactive as Reactive
from .reactive import watch as watch

__version__ = "0.2.1"

__all__ = [
    "Reactive",
    "Int",
    "Float",
    "Bool",
    "Str",
    "Bytes",
    "watch",
]

Int: type[Reactive[int]] = Reactive
Float: type[Reactive[float]] = Reactive
Bool: type[Reactive[bool]] = Reactive
Str: type[Reactive[str]] = Reactive
Bytes: type[Reactive[bytes]] = Reactive
