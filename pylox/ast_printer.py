from Expr import *
from token import Token
from tokenTypes import Token_type


class Ast_printer(Visitor):
    def parenthasize(self, name, *args: Expr):
        res = f"({name}"
        for expr in args:
            res += f" {expr.accept(self)}"

        return res + ")"

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
        Unary(Token(Token_type.MINUS, "-", None, 1), Literal(123)),
        Token(Token_type.STAR, "*", None, 1),
        Grouping(Literal(45.67)),
    )
    print(Ast_printer().print(expression))


if __name__ == "__main__":
    main()
