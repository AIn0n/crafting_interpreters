# code generated by pylox/tools/generate_ast.py
class Stmt:
    def accept(self, visitor):
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

    def accept(self, visitor):
        return visitor.visitBlock(self)


class Expression(Stmt):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitExpression(self)


class If(Stmt):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visitIf(self)


class Print(Stmt):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitPrint(self)


class Var(Stmt):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visitVar(self)


class While(Stmt):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visitWhile(self)
