from token import Token
from Expr import *
from tokenTypes import Token_type
from typing import Callable, Sequence
from errors import report


class Parser_error(RuntimeError):
    pass


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.current = 0
        self.had_error = False

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def isAtEnd(self) -> bool:
        return self.peek().ttype == Token_type.EOF

    def advance(self) -> Token:
        if not self.isAtEnd():
            self.current += 1
        return self.previous()

    def check(self, type_: Token_type) -> bool:
        if self.isAtEnd():
            return False
        return self.peek().ttype == type_

    def match(self, *types: Token_type) -> bool:
        for type_ in types:
            if self.check(type_):
                self.advance()
                return True

        return False

    def expression(self) -> Expr:
        return self.equality()

    def collect_right_recursion(self, func: Callable, types: Sequence) -> Expr:
        expr = func()
        # as long as matched thing is comparison operator
        while self.match(*types):
            operator = self.previous()
            right = func()
            expr = Binary(expr, operator, right)
        return expr

    def equality(self) -> Expr:
        return self.collect_right_recursion(
            self.comparison, [Token_type.BANG_EQUAL, Token_type.EQUAL_EQUAL]
        )

    def comparison(self) -> Expr:
        return self.collect_right_recursion(
            self.term,
            [
                Token_type.GREATER,
                Token_type.GREATER_EQUAL,
                Token_type.LESS,
                Token_type.LESS_EQUAL,
            ],
        )

    def term(self) -> Expr:
        return self.collect_right_recursion(
            self.factor, [Token_type.MINUS, Token_type.PLUS]
        )

    def factor(self) -> Expr:
        return self.collect_right_recursion(
            self.unary, [Token_type.SLASH, Token_type.STAR]
        )

    def unary(self) -> Expr:
        if self.match(Token_type.BANG, Token_type.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self):
        if self.match(Token_type.FALSE):
            return Literal(False)
        if self.match(Token_type.TRUE):
            return Literal(True)
        if self.match(Token_type.NIL):
            return Literal(None)

        if self.match(Token_type.NUMBER, Token_type.STRING):
            return Literal(self.previous().literal)

        if self.match(Token_type.LEFT_PAREN):
            expr = self.expression()
            self.consume(Token_type.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise self.error(self.peek(), "Expect expression.")

    def consume(self, type_: Token_type, msg: str) -> Token:
        if self.check(type_):
            return self.advance()
        raise self.error(self.peek(), msg)

    def error(self, token: Token, msg: str):
        if token.ttype == Token_type.EOF:
            report(token.line, " at end", msg)
        else:
            report(token.line, f" at '{token.lexeme}'", msg)
        self.had_error = True
        return Parser_error()

    def synchronize(self):
        self.advance()

        while not self.isAtEnd():
            if self.previous().ttype == Token_type.SEMICOLON:
                return

            match self.peek().ttype:
                case (
                    Token_type.CLASS
                    | Token_type.FUN
                    | Token_type.VAR
                    | Token_type.FOR
                    | Token_type.IF
                    | Token_type.WHILE
                    | Token_type.PRINT
                    | Token_type.RETURN
                ):
                    return

            self.advance()

    def parse(self):
        try:
            return self.expression()
        except Parser_error:
            return None
