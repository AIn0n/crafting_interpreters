import argparse


def report(line: int, where: str, msg: str) -> None:
    print(f"[line {line}] Error {where}: {msg}")


def error(line: int, msg: str) -> None:
    report(line, "", msg)


def run(src: str) -> None:
    print(src.split(" "))


def run_file(script_path: str):
    with open(script_path, "rt") as f:
        run(f.read())


def run_prompt():
    while True:
        try:
            line = input("> ")
            run(line)
        except EOFError:
            print("\nsee you later :)")
            break


def main(script_path: str) -> None:
    if len(script_path) > 0:
        run_file(script_path)
    else:
        run_prompt()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="pylox",
        description="lox language interperter",
    )
    parser.add_argument("-s", "--script", required=False, default="")
    args = parser.parse_args()
    main(args.script)
