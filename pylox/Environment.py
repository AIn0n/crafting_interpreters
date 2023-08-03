from typing import Any, MutableMapping
from errors import Runtime_lox_error


class Environment:
    def __init__(self) -> None:
        self.values: MutableMapping[str, Any] = {}

    def assign(self, name, value) -> None:
        if name.lexeme not in self.values:
            raise Runtime_lox_error(name, f"Undefined variable '{name.lexeme}'.")
        self.values[name.lexeme] = value

    def define(self, name: str, value) -> None:
        self.values[name] = value

    def get(self, name):
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        raise Runtime_lox_error(name, f"Undefined variable '{name.lexeme}'.")
