from typing import Any, MutableMapping
from errors import Runtime_lox_error


class Environment:
    def __init__(self, enclosing=None) -> None:
        self.values: MutableMapping[str, Any] = {}
        self.enclosing: Environment = enclosing

    def getAt(self, dist: int, name: str) -> Any:
        return self.ancestor(dist).values[name]

    def ancestor(self, dist: int) -> Any:
        env = self
        for _ in range(dist):
            env = env.enclosing
        return env

    def assign(self, name, value) -> None:
        if name.lexeme not in self.values:
            if self.enclosing is not None:
                return self.enclosing.assign(name, value)

            raise Runtime_lox_error(name, f"Undefined variable '{name.lexeme}'.")

        self.values[name.lexeme] = value

    def define(self, name: str, value) -> None:
        self.values[name] = value

    def get(self, name):
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise Runtime_lox_error(name, f"Undefined variable '{name.lexeme}'.")
