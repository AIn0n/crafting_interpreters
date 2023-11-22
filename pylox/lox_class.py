from LoxCallable import LoxCallable
from lox_instance import LoxInstance
from lox_function import LoxFunction

from typing import MutableMapping, Optional


class LoxClass(LoxCallable):
    def __init__(self, name: str, methods: MutableMapping[str, LoxFunction]) -> None:
        self.name = name
        self.methods = methods

    def __repr__(self) -> str:
        return self.name

    def find_method(self, name: str) -> Optional[LoxFunction]:
        if name in self.methods:
            return self.methods[name]

        return None

    def arity(self) -> int:
        return 0

    def call(self, interpreter, arguments: list):
        return LoxInstance(self)
