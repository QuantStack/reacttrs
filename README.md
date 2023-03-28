# reacttrs

Reactive attributes extracted out from [Textual](https://textual.textualize.io/guide/reactivity).

```py
from reacttrs import reactive


class Foo:

    name = reactive("Paul")
    age = reactive(33)
    birth = reactive(1990)

    def watch_name(self, old, new):
        print(f"{old=}, {new=}")

    def validate_name(self, name):
        if name == "John":
            print("Hey John!")
        return name

    def compute_age(self) -> int:
        age = 2023 - self.birth
        print(f"{age=}")
        return age

foo = Foo()
foo.name = "John"
foo.name = "Steve"

foo.age
foo.birth = 1991
foo.age
```
