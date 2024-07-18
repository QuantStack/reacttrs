# reacttrs

Reactive attributes, initially extracted out from [Textual](https://textual.textualize.io/guide/reactivity), now a fork of [Declare](https://github.com/willmcgugan/declare).

```py
from reacttrs import Int, Str


class Foo:

    name = Str("Paul")
    age = Int(34)
    birth = Int(1990)

    @name.watch
    def _watch_name(self, old: str, new: str):
        print(f"{old=}, {new=}")

    @age.validate
    def _validate_age(self, value: int) -> int:
        return 2024 - self.birth

foo = Foo()
foo.name = "John"  # old='Paul', new='John'
foo.name = "Steve"  # old='John', new='Steve'

print(foo.age)  # 34
foo.birth = 1991
foo.age = 34
print(foo.age)  # 33
```
