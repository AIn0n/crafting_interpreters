import argparse
from scanner import Scanner
from lox_parser import Parser
from ast_printer import Ast_printer
from interpreter import Interpreter
from Stmt import Expression


class Lox:
    def __init__(self) -> None:
        self.interpreter = Interpreter()

    def run(self, src: str) -> None:
        scanner = Scanner(src)
        tokens = scanner.scan_tokens()
        if scanner.had_error:
            return

        parser = Parser(tokens)
        statements = parser.parse()

        if parser.had_error:
            return

        self.interpreter.interpret(statements)

        if isinstance(statements[0], Expression):
            print(self.interpreter.evaluate(statements[0].expression))

    def run_file(self, script_path: str):
        with open(script_path, "rt") as f:
            self.run(f.read())

    def run_prompt(self):
        while True:
            try:
                line = input("> ")
                self.run(line)
            except EOFError:
                print("\nsee you later :)")
                break


def main(script_path: str) -> None:
    lox = Lox()
    if len(script_path) > 0:
        lox.run_file(script_path)
    else:
        lox.run_prompt()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="pylox",
        description="lox language interperter",
    )
    parser.add_argument("-s", "--script", required=False, default="")
    args = parser.parse_args()
    main(args.script)
