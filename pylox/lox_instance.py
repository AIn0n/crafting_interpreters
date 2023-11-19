class LoxInstance:
    def __init__(self, _class) -> None:
        self._class = _class

    def __repr__(self) -> str:
        return f"{self._class.name} instance"
