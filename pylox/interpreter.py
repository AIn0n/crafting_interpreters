from Expr import *
from tokenTypes import Token_type as TT


class Interpreter(Visitor):
    def visitBinary(self, expr):
        pass

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def visitGrouping(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def visitLiteral(self, expr: Literal):
        return expr.value

    def visitUnary(self, expr: Unary):
        right = self.evaluate(expr.right)

        match expr.operator.ttype:
            case TT.MINUS:
                return -float(right)
            case TT.BANG:
                return self.isTruthy(right)
