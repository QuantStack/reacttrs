from typing import List, Tuple

import reacttrs
from reacttrs import Reactive, watch


def test_predefined():
    class Foo:
        my_int = reacttrs.Int(1)
        my_float = reacttrs.Float(3.14)
        my_bool = reacttrs.Bool(True)
        my_str = reacttrs.Str("Foo")
        my_bytes = reacttrs.Bytes(b"bar")

    foo = Foo()
    assert foo.my_int == 1
    assert foo.my_float == 3.14
    assert foo.my_bool == True
    assert foo.my_str == "Foo"
    assert foo.my_bytes == b"bar"


def test_validate():
    class Foo:
        positive = reacttrs.Int(0)

        @positive.validate
        def _validate_positive(self, value: int) -> int:
            return max(0, value)

    foo = Foo()
    foo.positive = -1
    assert foo.positive == 0
    foo.positive = 1
    assert foo.positive == 1


def test_watch() -> None:
    changes0: List[Tuple[int, int]] = []
    changes1: List[Tuple[int, int]] = []
    changes2: List[Tuple[int, int]] = []
    changes3: List[Tuple[int, int]] = []

    class Foo:
        value0 = reacttrs.Int(0)
        value1 = reacttrs.Int(0)

        @value0.watch
        def _watch_value0(self, old: int, new: int) -> None:
            changes0.append((old, new))

        @value0.watch
        def _watch_value1(self, old: int, new: int) -> None:
            changes1.append((old, new))

    foo0 = Foo()
    foo0.value0 = 1
    assert changes0 == [(0, 1)]
    assert changes1 == [(0, 1)]
    foo0.value0 = 2
    assert changes0 == [(0, 1), (1, 2)]
    assert changes1 == [(0, 1), (1, 2)]

    def callback(obj: Foo, old: int, new: int) -> None:
        changes3.append((old, new))

    foo1 = Foo()
    watch(foo0, "value1", callback)  # type: ignore[arg-type]
    foo0.value1 = 3
    foo1.value1 = 4
    assert changes0 == [(0, 1), (1, 2)]
    assert changes1 == [(0, 1), (1, 2)]
    assert changes3 == [(0, 3)]


def test_custom():
    class Foo:
        things = Reactive[List[str]](["foo", "bar"])

    foo = Foo()
    assert foo.things == ["foo", "bar"]
