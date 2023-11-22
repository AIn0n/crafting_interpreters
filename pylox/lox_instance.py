from typing import MutableMapping, Any
from token import Token
from errors import Runtime_lox_error


class LoxInstance:
    def __init__(self, _class) -> None:
        self._class = _class
        self.fields: MutableMapping[str, Any] = {}

    def get(self, name: Token) -> Any:
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]

        raise Runtime_lox_error(name, f"Undefined property '{name.lexeme}'.")

    def set(self, name: Token, val: Any) -> None:
        self.fields[name.lexeme] = val

    def __repr__(self) -> str:
        return f"{self._class.name} instance"
