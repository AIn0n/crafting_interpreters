from Stmt import *
from Expr import *

from errors import Runtime_lox_error
from interpreter import Interpreter

from typing import MutableMapping, Sequence
from enum import Enum, auto


class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()


class Resolver(VisitorExpr, VisitorStmt):
    def __init__(self, interpreter: Interpreter) -> None:
        self.interpreter = interpreter
        self.scopes: list[MutableMapping[str, bool]] = [{}]
        self.current_function = FunctionType.NONE

    def visitGet(self, expr: Get):
        self.resolve(expr.object)

    def visitExpression(self, stmt: Expression) -> None:
        self.resolve(stmt.expression)

    def visitIf(self, stmt: If) -> None:
        self.resolve(stmt.condition)
        self.resolve(stmt.then_branch)
        if stmt.else_branch is not None:
            self.resolve(stmt.else_branch)

    def visitPrint(self, stmt: Print) -> None:
        self.resolve(stmt.expression)

    def visitReturn(self, stmt: Return) -> None:
        if self.current_function == FunctionType.NONE:
            raise Runtime_lox_error(stmt.keyword, "Can't return from top-level code")

        if stmt.value is not None:
            self.resolve(stmt.value)

    def visitWhile(self, stmt: While) -> None:
        self.resolve(stmt.condition)
        self.resolve(stmt.body)

    def visitBinary(self, expr: Binary) -> None:
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visitCall(self, expr: Call) -> None:
        self.resolve(expr.callee)

        for arg in expr.arguments:
            self.resolve(arg)

    def visitGrouping(self, expr: Grouping) -> None:
        self.resolve(expr.expression)

    def visitLiteral(self, expr) -> None:
        return None

    def visitLogical(self, expr: Logical) -> None:
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visitUnary(self, expr: Unary) -> None:
        self.resolve(expr.right)

    def resolve_function(self, stmt: Function, _type: FunctionType) -> None:
        enclosing_function = self.current_function
        self.current_function = _type

        self.beginScope()
        for param in stmt.params:
            self.declare(param)
            self.define(param)

        self.resolve(stmt.body)
        self.endScope()
        self.current_function = enclosing_function

    def visitFunction(self, stmt: Function) -> None:
        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolve_function(stmt, FunctionType.FUNCTION)

    def visitClass(self, stmt):
        self.declare(stmt.name)
        self.define(stmt.name)

    def visitAssign(self, expr: Assign) -> None:
        self.resolve(expr.value)
        self.resolve_local(expr, expr.name)

    def define(self, name) -> None:
        if not self.scopes_empty():
            self.scopes[-1][name.lexeme] = True

    def declare(self, name) -> None:
        if not self.scopes_empty():
            if name.lexeme in self.scope_peek():
                raise Runtime_lox_error(
                    name, "Already a variable with this name in this scope"
                )
            self.scopes[-1][name.lexeme] = False

    def resolve_local(self, expr: Expr, name) -> None:
        for idx, scope in enumerate(reversed(self.scopes)):
            if name.lexeme in scope:
                self.interpreter.resolve(expr, idx)
                break

    def visitVariable(self, expr: Variable) -> None:
        peek = self.scope_peek()
        if (
            not self.scopes_empty()
            and expr.name.lexeme in peek
            and not peek[expr.name.lexeme]
        ):
            raise Runtime_lox_error(
                expr.name, "Can't read local variable in it's own initializer"
            )
        self.resolve_local(expr, expr.name)

    def scopes_empty(self) -> bool:
        return len(self.scopes) == 0

    def scope_peek(self) -> MutableMapping[str, bool]:
        return self.scopes[-1]

    def visitVar(self, stmt: Var) -> None:
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve(stmt.initializer)
        self.define(stmt.name)

    def beginScope(self) -> None:
        self.scopes.append({})

    def endScope(self) -> None:
        self.scopes.pop()

    def resolve(self, obj):
        if isinstance(obj, Sequence):
            for stmt in obj:
                self.resolve(stmt)
        else:
            obj.accept(self)

    def visitBlock(self, stmt) -> None:
        self.beginScope()
        self.resolve(stmt.statements)
        self.endScope()
