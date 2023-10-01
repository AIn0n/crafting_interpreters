class ReturnException(RuntimeError):
    def __init__(self, val, *args: object) -> None:
        super().__init__(*args)
        self.value = val
