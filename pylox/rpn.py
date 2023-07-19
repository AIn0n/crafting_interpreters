from Expr import *
from token import Token
from tokenTypes import Token_type


class RPN(Visitor):
    def parenthasize(self, name, *args: Expr):
        res = ""
        for expr in args:
            res += f" {expr.accept(self)}"

        return res + f" {name}"

    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def visitBinary(self, expr: Binary) -> str:
        return self.parenthasize(expr.operator.lexeme, expr.left, expr.right)

    def visitGrouping(self, expr: Grouping) -> str:
        return self.parenthasize("group", expr.expression)

    def visitLiteral(self, expr: Literal) -> str:
        if expr.value == None:
            return "nil"
        return str(expr.value)

    def visitUnary(self, expr: Unary) -> str:
        return self.parenthasize(expr.operator.lexeme, expr.right)


def main() -> None:
    expression = Binary(
        Binary(
            Literal(1), Token(Token_type.PLUS, "+", None, 1), Literal(2)
        ),
        Token(Token_type.STAR, "*", None, 1),
        Binary(
            Literal(4), Token(Token_type.MINUS, "-", None, 1), Literal(3)
        )
    )
    print(RPN().print(expression))


if __name__ == "__main__":
    main()
