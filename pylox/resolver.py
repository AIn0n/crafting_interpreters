from Stmt import VisitorStmt, Stmt
from Expr import VisitorExpr, Expr
from interpreter import Interpreter
from typing import Mapping


class Resolver(VisitorExpr, VisitorStmt):
    def __init__(self, interpreter: Interpreter) -> None:
        self.interpreter = interpreter
        self.scopes: list[Mapping] = []

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
