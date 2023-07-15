def report(line: int, where: str, msg: str) -> None:
    print(f"[line {line}] Error {where}: {msg}")


def error(line: int, msg: str) -> None:
    report(line, "", msg)
