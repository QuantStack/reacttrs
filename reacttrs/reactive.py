from __future__ import annotations

from copy import copy
from typing import Any, TYPE_CHECKING, Generic, Type, TypeVar, cast, overload

if TYPE_CHECKING:
    from collections.abc import Callable

    from typing_extensions import TypeAlias


ObjectType = TypeVar("ObjectType")
ValueType = TypeVar("ValueType")

Validator: TypeAlias = "Callable[[ObjectType, ValueType], ValueType]"
Watcher: TypeAlias = "Callable[[ObjectType, ValueType | None, ValueType], None]"

ValidateMethodType = TypeVar("ValidateMethodType", bound=Validator)
WatchMethodType = TypeVar("WatchMethodType", bound=Watcher)


class NoValue:
    """Sentinel type."""


_NO_VALUE = NoValue()


class ReactiveError(Exception):
    """Raised when a Reactive related error occurs"""


class ValidateDecorator(Generic[ValidateMethodType]):
    """Validate decorator.

    Decorate a Widget method to make it a validator for the attribute.
    """

    def __init__(self, reactive: Reactive | None = None) -> None:
        self._reactive = reactive
        self._validator: ValidateMethodType | None = None

    @overload
    def __call__(self) -> ValidateDecorator[ValidateMethodType]: ...

    @overload
    def __call__(self, method: ValidateMethodType) -> ValidateMethodType: ...

    def __call__(
        self, method: ValidateMethodType | None = None
    ) -> ValidateMethodType | ValidateDecorator[ValidateMethodType]:
        if method is None:
            return self
        assert self._reactive is not None

        if self._reactive._validator is not None:
            raise ReactiveError(f"A validator has already been set on {self._reactive!r}")
        self._reactive._validator = method
        return method


class WatchDecorator(Generic[WatchMethodType]):
    """Validate decorator.

    Decorate a Widget method to make it a validator for the attribute.
    """

    def __init__(self, reactive: Reactive | None = None) -> None:
        self._reactive = reactive

    @overload
    def __call__(self) -> WatchDecorator[WatchMethodType]: ...

    @overload
    def __call__(self, method: WatchMethodType) -> WatchMethodType: ...

    def __call__(
        self, method: WatchMethodType | None = None
    ) -> WatchMethodType | WatchDecorator[WatchMethodType]:
        if method is None:
            return self
        assert self._reactive is not None

        self._reactive._watchers.add(method)
        return method


class Reactive(Generic[ValueType]):
    """A descriptor to create reactive attributes."""

    def __init__(
        self,
        default: ValueType,
        *,
        validate: Validator | None = None,
        watchers: set[Watcher] | None = None,
    ) -> None:
        self._name = ""
        self._private_name = ""
        self._default = default
        self._validator = validate
        self._watchers = set(watchers) if watchers is not None else set()
        self._copy_default = not isinstance(default, (int, float, bool, str, complex))

    def copy(self) -> Reactive[ValueType]:
        """Return a copy of the Reactive descriptor.

        Returns:
            A Reactive descriptor.
        """
        reactive = Reactive(
            self._default,
            validate=self._validator,
            watchers=set(self._watchers),
        )
        return reactive

    def __call__(
        self,
        default: ValueType | NoValue = _NO_VALUE,
        *,
        validate: Validator | None = None,
        watchers: set[Watcher] | None = None,
    ) -> Reactive[ValueType]:
        """Update the declaration.

        Args:
            default: New default.
            validate: A validator function.
            watchers: A set of watch functions.

        Returns:
            A new Reactive.
        """
        reactive = self.copy()
        if not isinstance(default, NoValue):
            reactive._default = default
        if validate is not None:
            reactive._validator = validate
        if watchers is not None:
            reactive._watchers = set(watchers)
        return reactive

    def __set_name__(self, owner: Type, name: str) -> None:
        self._owner = owner
        self._name = name
        self._private_name = f"__reactive_private_{name}"

    @overload
    def __get__(
        self: Reactive[ValueType], obj: None, obj_type: type[ObjectType]
    ) -> Reactive[ValueType]: ...

    @overload
    def __get__(
        self: Reactive[ValueType], obj: ObjectType, obj_type: type[ObjectType]
    ) -> ValueType: ...

    def __get__(
        self: Reactive[ValueType], obj: ObjectType | None, obj_type: type[ObjectType]
    ) -> Reactive[ValueType] | ValueType:
        if obj is None:
            return self
        if isinstance((value := getattr(obj, self._private_name, _NO_VALUE)), NoValue):
            value = copy(self._default) if self._copy_default else self._default
            setattr(obj, self._private_name, value)
            return value
        else:
            return value

    def __set__(self, obj: object, value: ValueType) -> None:
        if self._watchers:
            current_value = getattr(obj, self._name, None)
            new_value = (
                value if self._validator is None else self._validator(obj, value)
            )
            setattr(obj, self._private_name, new_value)
            if current_value != new_value:
                for watcher in self._watchers:
                    watcher(obj, current_value, new_value)

        else:
            setattr(
                obj,
                self._private_name,
                value if self._validator is None else self._validator(obj, value),
            )

    @property
    def optional(self) -> Reactive[ValueType | None]:
        """Make the type optional."""
        # We're just changing the type, so this doesn't do anything at runtime.
        return cast("Reactive[ValueType | None]", self)

    @property
    def validate(self) -> ValidateDecorator:
        """Decorator to define a validator."""
        return ValidateDecorator(self)

    @property
    def watch(self) -> WatchDecorator:
        """Decorator to create a watcher."""
        return WatchDecorator(self)


def watch(
    obj: ObjectType,
    attribute_name: str,
    callback: Watcher,
):
    reactive: Reactive = getattr(obj.__class__, attribute_name)

    def _callback(_obj: ObjectType, old: Any, new: Any):
        if _obj != obj:
            return

        callback(obj, old, new)

    reactive._watchers.add(_callback)
