from token import Token
from Expr import *
from tokenTypes import Token_type as TT
from typing import Callable, Sequence
from errors import report
from Stmt import *


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

    def and_expr(self) -> Expr:
        expr = self.equality()

        while self.match(TT.AND):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)

        return expr

    def or_expr(self) -> Expr:
        expr = self.and_expr()

        while self.match(TT.OR):
            operator = self.previous()
            right = self.and_expr()
            expr = Logical(expr, operator, right)

        return expr

    def assignment(self) -> Expr:
        expr = self.or_expr()

        if self.match(TT.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)
            elif isinstance(expr, Get):
                get = expr
                return Set(get.object, get.name, value)

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

    def finish_call(self, callee: Expr) -> Expr:
        arguments: list = []
        if not self.check(TT.RIGHT_PAREN):
            while True:
                if len(arguments) >= 255:
                    self.error(self.peek(), "Function can have more than 255 arguments")
                arguments.append(self.expression())
                if not self.match(TT.COMMA):
                    break
        paren = self.consume(TT.RIGHT_PAREN, "Expected ) after a function arguments")
        return Call(callee, paren, arguments)

    def call(self) -> Expr:
        expr = self.primary()

        while True:
            if self.match(TT.LEFT_PAREN):
                expr = self.finish_call(expr)
            elif self.match(TT.DOT):
                name = self.consume(
                    TT.IDENTIFIER, "Expected property name after the dot."
                )
                expr = Get(expr, name)
            else:
                break

        return expr

    def unary(self) -> Expr:
        if self.match(TT.BANG, TT.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.call()

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

        if self.match(TT.SUPER):
            keyword = self.previous()
            self.consume(TT.DOT, "Expected . after super keyword.")
            method = self.consume(TT.IDENTIFIER, "Expect superclass method name")
            return Super(keyword, method)

        if self.match(TT.THIS):
            return This(self.previous())

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

    def if_statement(self) -> Stmt:
        self.consume(TT.LEFT_PAREN, "expected ( after a if")
        condition = self.expression()
        self.consume(TT.RIGHT_PAREN, "Expected ) after if condition")
        then_branch = self.statement()
        else_branch = None
        if self.match(TT.ELSE):
            else_branch = self.statement()

        return If(condition, then_branch, else_branch)

    def while_statement(self):
        self.consume(TT.LEFT_PAREN, "Expect ( after a while keyword")
        condition = self.expression()
        self.consume(TT.RIGHT_PAREN, "Expect ) after a condition")
        body = self.statement()

        return While(condition, body)

    def for_statement(self):
        self.consume(TT.LEFT_PAREN, "Expected ( after for keyword")
        initializer = None
        if not self.match(TT.SEMICOLON):
            if self.match(TT.VAR):
                initializer = self.var_declaration()
            else:
                initializer = self.expression_statement()

        condition = None
        if not self.check(TT.SEMICOLON):
            condition = self.expression()
        self.consume(TT.SEMICOLON, "Expected ; after loop condition")

        increment = None
        if not self.check(TT.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TT.RIGHT_PAREN, "Expected ) after for clauses")

        body = self.statement()

        if increment is not None:
            body = Block([body, Expression(increment)])

        if condition is None:
            condition = Literal(True)
        body = While(condition, body)

        if initializer is not None:
            body = Block([initializer, body])

        return body

    def return_statement(self):
        keyword = self.previous()
        value = None
        if not self.check(TT.SEMICOLON):
            value = self.expression()

        self.consume(TT.SEMICOLON, "Expect ; after return value.")
        return Return(keyword, value)

    def statement(self) -> Stmt:
        if self.match(TT.FOR):
            return self.for_statement()
        if self.match(TT.IF):
            return self.if_statement()
        if self.match(TT.PRINT):
            return self.print_statement()
        if self.match(TT.RETURN):
            return self.return_statement()
        if self.match(TT.WHILE):
            return self.while_statement()
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

    def function(self, kind: str) -> Function:
        name = self.consume(TT.IDENTIFIER, f"Expected {kind} name.")
        self.consume(TT.LEFT_PAREN, f"Expected ( afte {kind} name")

        # parameters parsing
        parameters: list[Token] = []
        if not self.check(TT.RIGHT_PAREN):
            while True:
                if len(parameters) >= 255:
                    self.error(self.peek(), "Can't have more than 255 parameters")
                parameters.append(
                    self.consume(TT.IDENTIFIER, "Expected parameter name")
                )
                if not self.match(TT.COMMA):
                    break
        self.consume(TT.RIGHT_PAREN, "expected ) after function parameters")

        # parsing the body of the function
        self.consume(TT.LEFT_BRACE, f"Expected left brace before {kind} body")
        body = self.block()
        return Function(name, parameters, body)

    def class_declaration(self):
        name = self.consume(TT.IDENTIFIER, "Expected class name.")

        superclass = None

        if self.match(TT.LESS):
            self.consume(TT.IDENTIFIER, "Expected superclass name.")
            superclass = Variable(self.previous())

        self.consume(TT.LEFT_BRACE, "Expect '{' before class body.")

        methods = []
        while not self.check(TT.RIGHT_BRACE) and not self.isAtEnd():
            methods.append(self.function("method"))

        self.consume(TT.RIGHT_BRACE, "Expected '}' after class body.")

        return Class(name, superclass, methods)

    def declaration(self):
        try:
            if self.match(TT.CLASS):
                return self.class_declaration()
            if self.match(TT.FUN):
                return self.function("function")
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
