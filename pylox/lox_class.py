from LoxCallable import LoxCallable
from lox_instance import LoxInstance


class LoxClass(LoxCallable):
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def arity(self) -> int:
        return 0

    def call(self, interpreter, arguments: list):
        return LoxInstance(self)
