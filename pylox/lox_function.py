from LoxCallable import LoxCallable
from lox_instance import LoxInstance
from Stmt import Function
from Environment import Environment
from lox_return import ReturnException


class LoxFunction(LoxCallable):
    def __init__(
        self, declaration: Function, closure: Environment, is_init: bool = False
    ) -> None:
        self.declaration = declaration
        self.closure = closure
        self.is_init = is_init

    def bind(self, instance: LoxInstance):
        env = Environment(self.closure)
        env.define("this", instance)
        return LoxFunction(self.declaration, env, self.is_init)

    def call(self, interpreter, arguments: list):
        environment = Environment(self.closure)
        for arg, param in zip(arguments, self.declaration.params):
            environment.define(param.lexeme, arg)

        try:
            interpreter.exec_block(self.declaration.body, environment)
        except ReturnException as e:
            if self.is_init:
                return self.closure.getAt(0, "this")
            return e.value

        if self.is_init:
            return self.closure.getAt(0, "this")
        return None

    def arity(self) -> int:
        return len(self.declaration.params)

    def __repr__(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"
