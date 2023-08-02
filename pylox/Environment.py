from typing import Any, MutableMapping
from errors import Runtime_lox_error


class Environment:
    def __init__(self) -> None:
        self.values: MutableMapping[str, Any] = {}

    def define(self, name: str, value) -> None:
        self.values[name] = value

    def get(self, name):
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        raise Runtime_lox_error(name, f"Undefined variable '{name.lexeme}'.")
