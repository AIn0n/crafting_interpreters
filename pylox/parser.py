from token import Token
from Expr import *
from tokenTypes import Token_type
from typing import Optional


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.current = 0

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

    def equality(self) -> Expr:
        expr = self.comparison()

        # as long as matched thing is comparison operator
        while self.match(Token_type.BANG_EQUAL, Token_type.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expr:
        expr = self.term()

        while self.match(
            Token_type.GREATER,
            Token_type.GREATER_EQUAL,
            Token_type.LESS,
            Token_type.LESS_EQUAL,
        ):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self) -> Expr:
        expr = self.factor()

        while self.match(Token_type.MINUS, Token_type.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while self.match(Token_type.SLASH, Token_type.STAR):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

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
            return Expr(self.previous().literal)

        if self.match(Token_type.LEFT_PAREN):
            expr = self.expression()
            self.consume(Token_type.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        
        return None