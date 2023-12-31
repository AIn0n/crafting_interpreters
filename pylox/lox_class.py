from LoxCallable import LoxCallable
from lox_instance import LoxInstance
from lox_function import LoxFunction

from typing import MutableMapping, Optional, Iterable


class LoxClass(LoxCallable):
    def __init__(
        self,
        name: str,
        superclass: Optional["LoxClass"],
        methods: MutableMapping[str, LoxFunction],
    ) -> None:
        self.name = name
        self.methods = methods
        self.superclass = superclass

    def __repr__(self) -> str:
        return self.name

    def find_method(self, name: str) -> Optional[LoxFunction]:
        if name in self.methods:
            return self.methods[name]

        if self.superclass is not None:
            return self.superclass.find_method(name)

        return None

    def arity(self) -> int:
        initializer = self.find_method("init")
        if initializer is None:
            return 0

        return initializer.arity()

    def call(self, interpreter, arguments: Iterable) -> LoxInstance:
        instance = LoxInstance(self)
        initalizer = self.find_method("init")
        if initalizer is not None:
            initalizer.bind(instance).call(interpreter, arguments)
        return instance
