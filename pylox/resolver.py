from Stmt import VisitorStmt
from Expr import VisitorExpr
from interpreter import Interpreter


class Resolver(VisitorExpr, VisitorStmt):
    def __init__(self, interpreter: Interpreter) -> None:
        self.interpreter = interpreter
