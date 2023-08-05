from typing import Any, MutableMapping
from errors import Runtime_lox_error


class Environment:
    def __init__(self, enclosing=None) -> None:
        self.values: MutableMapping[str, Any] = {}
        self.enclosing: Environment = enclosing

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
            res = self.values[name.lexeme]
            if res is None:
                raise Runtime_lox_error(name, f"variable {name.lexeme} not initalized")
            return res

        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise Runtime_lox_error(name, f"Undefined variable '{name.lexeme}'.")
