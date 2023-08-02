from token import Token


def report(line: int, where: str, msg: str) -> None:
    print(f"[line {line}] Error {where}: {msg}")


def error(line: int, msg: str) -> None:
    report(line, "", msg)


class Runtime_lox_error(Exception):
    def __init__(self, token: Token, msg: str) -> None:
        super().__init__(msg)
        self.msg = msg
        self.token = token
        self.had_error = False
