from textwrap import dedent

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


def test(capfd):
    foo = Foo()

    foo.name = "John"
    out, err = capfd.readouterr()
    # watch_name is called first time unless `init=False`
    assert out == dedent("""\
        old='Paul', new='Paul'
        Hey John!
        old='Paul', new='John'
    """)

    foo.name = "Steve"
    out, err = capfd.readouterr()
    assert out == dedent("""\
        old='John', new='Steve'
    """)

    foo.age
    out, err = capfd.readouterr()
    # compute_age is called first time unless `init=False`
    assert out == dedent("""\
        age=33
        age=33
    """)

    foo.birth = 1991
    foo.age
    out, err = capfd.readouterr()
    assert out == dedent("""\
        age=32
    """)
