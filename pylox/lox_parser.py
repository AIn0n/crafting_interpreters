from token import Token
from Expr import *
from tokenTypes import Token_type as TT
from typing import Callable, Sequence
from errors import report
from Stmt import Stmt, Print, Expression, Var, Block


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
        return self.peek().ttype == TT.EOF

    def advance(self) -> Token:
        if not self.isAtEnd():
            self.current += 1
        return self.previous()

    def check(self, type_: TT) -> bool:
        if self.isAtEnd():
            return False
        return self.peek().ttype == type_

    def match(self, *types: TT) -> bool:
        for type_ in types:
            if self.check(type_):
                self.advance()
                return True

        return False

    def assignment(self) -> Expr:
        expr = self.equality()

        if self.match(TT.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)

            self.error(equals, "Invalid assignment target")

        return expr

    def expression(self) -> Expr:
        return self.assignment()

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
            self.comparison, [TT.BANG_EQUAL, TT.EQUAL_EQUAL]
        )

    def comparison(self) -> Expr:
        return self.collect_right_recursion(
            self.term,
            [
                TT.GREATER,
                TT.GREATER_EQUAL,
                TT.LESS,
                TT.LESS_EQUAL,
            ],
        )

    def term(self) -> Expr:
        return self.collect_right_recursion(self.factor, [TT.MINUS, TT.PLUS])

    def factor(self) -> Expr:
        return self.collect_right_recursion(self.unary, [TT.SLASH, TT.STAR])

    def unary(self) -> Expr:
        if self.match(TT.BANG, TT.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self):
        if self.match(TT.FALSE):
            return Literal(False)
        if self.match(TT.TRUE):
            return Literal(True)
        if self.match(TT.NIL):
            return Literal(None)

        if self.match(TT.NUMBER, TT.STRING):
            return Literal(self.previous().literal)

        if self.match(TT.LEFT_PAREN):
            expr = self.expression()
            self.consume(TT.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        if self.match(TT.IDENTIFIER):
            return Variable(self.previous())

        raise self.error(self.peek(), "Expect expression.")

    def consume(self, type_: TT, msg: str) -> Token:
        if self.check(type_):
            return self.advance()
        raise self.error(self.peek(), msg)

    def error(self, token: Token, msg: str):
        if token.ttype == TT.EOF:
            report(token.line, " at end", msg)
        else:
            report(token.line, f" at '{token.lexeme}'", msg)
        self.had_error = True
        return Parser_error()

    def synchronize(self):
        self.advance()

        while not self.isAtEnd():
            if self.previous().ttype == TT.SEMICOLON:
                return

            match self.peek().ttype:
                case (
                    TT.CLASS
                    | TT.FUN
                    | TT.VAR
                    | TT.FOR
                    | TT.IF
                    | TT.WHILE
                    | TT.PRINT
                    | TT.RETURN
                ):
                    return

            self.advance()

    def print_statement(self):
        value = self.expression()
        self.consume(TT.SEMICOLON, "Expected ; after the value")
        return Print(value)

    def expression_statement(self):
        expr = self.expression()
        self.consume(TT.SEMICOLON, "Exprected ; after expression")
        return Expression(expr)

    def block(self) -> Sequence[Stmt]:
        statements = []
        while not self.check(TT.RIGHT_BRACE) and not self.isAtEnd():
            statements.append(self.declaration())

        self.consume(TT.RIGHT_BRACE, "Expect } after block")
        return statements

    def statement(self) -> Stmt:
        if self.match(TT.PRINT):
            return self.print_statement()
        if self.match(TT.LEFT_BRACE):
            return Block(self.block())
        return self.expression_statement()

    def var_declaration(self):
        name = self.consume(TT.IDENTIFIER, "Expected variable name")
        initializer = None
        if self.match(TT.EQUAL):
            initializer = self.expression()

        self.consume(TT.SEMICOLON, "Expected ; after variable declaration")
        return Var(name, initializer)

    def declaration(self):
        try:
            if self.match(TT.VAR):
                return self.var_declaration()

            return self.statement()
        except Parser_error as e:
            self.synchronize()
            return None

    def parse(self):
        statements: list[Stmt] = []
        while not self.isAtEnd():
            statements.append(self.declaration())
        return statements
