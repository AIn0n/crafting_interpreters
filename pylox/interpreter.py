from Expr import *
from tokenTypes import Token_type as TT
from token import Token


class Runtime_lox_error(Exception):
    def __init__(self, token: Token, msg: str) -> None:
        super().__init__(msg)
        self.msg = msg
        self.token = token
        self.had_error = False


class Interpreter(Visitor):
    def runtime_error(self, err: Runtime_lox_error):
        print(f"{err.msg} [{err.token.line}]")
        self.had_error = True

    def stringify(self, expression) -> str:
        return "nil" if expression is None else str(expression)

    def interpret(self, expression: Expr):
        try:
            value = self.evaluate(expression)
            print(self.stringify(value))
        except RuntimeError:
            pass

    def check_num_operands(self, operator: Token, left, right) -> None:
        if isinstance(float, left) and isinstance(float, right):
            return
        raise Runtime_lox_error(operator, "Operands must be numbers")

    def visitBinary(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.visitUnary(expr.right)

        match expr.operator.ttype:
            case TT.MINUS:
                self.check_num_operands(expr.operator, left, right)
                return left - right
            case TT.SLASH:
                self.check_num_operands(expr.operator, left, right)
                return left / right
            case TT.STAR:
                self.check_num_operands(expr.operator, left, right)
                return left * right
            case TT.PLUS:
                if (isinstance(left, float) and isinstance(right, float)) or (
                    isinstance(left, str) and isinstance(right, str)
                ):
                    return left + right  # type: ignore
                raise Runtime_lox_error(
                    expr.operator, "Operands must be two numbers or two strings"
                )
            case TT.GREATER:
                self.check_num_operands(expr.operator, left, right)
                return left > right
            case TT.GREATER_EQUAL:
                self.check_num_operands(expr.operator, left, right)
                return left >= right
            case TT.LESS:
                self.check_num_operands(expr.operator, left, right)
                return left < right
            case TT.LESS_EQUAL:
                self.check_num_operands(expr.operator, left, right)
                return left <= right
            case TT.EQUAL_EQUAL:
                return left == right
            case TT.BANG_EQUAL:
                return left != right
        return None

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def visitGrouping(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def visitLiteral(self, expr: Literal):
        return expr.value

    def is_truthy(self, obj) -> bool:
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def check_num_operand(self, operator: Token, operand) -> None:
        if isinstance(operand, float):
            return
        raise RuntimeError(f"{operator} operand must be a number")

    def visitUnary(self, expr: Unary):
        right = self.evaluate(expr.right)

        match expr.operator.ttype:
            case TT.MINUS:
                self.check_num_operand(expr.operator, right)
                return -float(right)
            case TT.BANG:
                return self.is_truthy(right)
