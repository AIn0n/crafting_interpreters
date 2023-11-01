from Stmt import VisitorStmt, Stmt, Var
from Expr import VisitorExpr, Expr, Variable, Assign
from interpreter import Interpreter
from typing import Mapping
from errors import Runtime_lox_error


class Resolver(VisitorExpr, VisitorStmt):
    def __init__(self, interpreter: Interpreter) -> None:
        self.interpreter = interpreter
        self.scopes: list[Mapping[str, bool]] = []

    def visitAssign(self, expr: Assign) -> None:
        self.resolve_expr(expr.value)
        self.resolve_local(expr, expr.name)

    def define(self, name) -> None:
        if not self.scopes_empty():
            self.scopes[len(self.scopes) - 1][name.lexeme] = True

    def declare(self, name) -> None:
        if not self.scopes_empty():
            self.scopes[len(self.scopes) - 1][name.lexeme] = False

    def resolve_local(self, expr: Expr, name) -> None:
        for idx, scope in enumerate(reversed(self.scopes)):
            if name.lexeme in scope:
                self.interpreter.resolve(expr, idx)
                break

    def visitVariable(self, expr: Variable) -> None:
        if not self.scopes_empty() and not self.scope_peek()[expr.name.lexeme]:
            raise Runtime_lox_error(
                expr.name, "Can't read local variable in it's own initializer"
            )
        self.resolve_local(expr, expr.name)

    def scopes_empty(self) -> bool:
        return len(self.scopes) == 0

    def scope_peek(self) -> Mapping[str, bool]:
        return self.scopes[len(self.scopes) - 1]

    def visitVar(self, stmt: Var) -> None:
        self.declare(stmt.name)
        if stmt.initializer is None:
            self.resolve_expr(stmt.initializer)
        self.define(stmt.name)

    def beginScope(self) -> None:
        self.scopes.append({})

    def endScope(self) -> None:
        self.scopes.pop()

    def resolve_expr(self, expr: Expr):
        expr.accept(self)

    def resolve_stmt(self, stmt: Stmt):
        stmt.accept(self)

    def resolve_statements(self, statements):
        for stmt in statements:
            self.resolve_stmt(stmt)

    def visitBlock(self, stmt) -> None:
        self.beginScope()
        self.resolve_statements(stmt.statements)
        self.endScope()
