from LoxCallable import LoxCallable
from Stmt import Function
from Environment import Environment
from lox_return import ReturnException


class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function) -> None:
        self.declaration = declaration

    def call(self, interpreter, arguments: list):
        environment = Environment(interpreter.globals)
        for arg, param in zip(arguments, self.declaration.params):
            environment.define(param.lexeme, arg)

        try:
            interpreter.exec_block(self.declaration.body, environment)
        except ReturnException as e:
            return e.value

        return None

    def arity(self) -> int:
        return len(self.declaration.params)

    def __repr__(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"
