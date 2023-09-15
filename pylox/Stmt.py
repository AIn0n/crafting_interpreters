# code generated by pylox/tools/generate_ast.py
from visitor_node import Visitor_node


class Stmt(Visitor_node):
    pass


class Visitor:
    def visitBlock(self, stmt):
        pass

    def visitExpression(self, stmt):
        pass

    def visitIf(self, stmt):
        pass

    def visitPrint(self, stmt):
        pass

    def visitVar(self, stmt):
        pass

    def visitWhile(self, stmt):
        pass


class Block(Stmt):
    def __init__(self, statements):
        self.statements = statements


class Expression(Stmt):
    def __init__(self, expression):
        self.expression = expression


class If(Stmt):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class Print(Stmt):
    def __init__(self, expression):
        self.expression = expression


class Var(Stmt):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer


class While(Stmt):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
