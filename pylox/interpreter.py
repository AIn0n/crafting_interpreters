from Expr import *
from Stmt import *
from tokenTypes import Token_type as TT
from token import Token
from errors import Runtime_lox_error
from Environment import Environment
from typing import Sequence, MutableMapping, Any
from LoxCallable import LoxCallable
from lox_function import LoxFunction
from native_extensions import NativeClock
from lox_return import ReturnException
from lox_class import LoxClass
from lox_instance import LoxInstance


class Interpreter(VisitorExpr, VisitorStmt):
    def __init__(self) -> None:
        super().__init__()
        self.globals = Environment()
        self.globals.define("clock", NativeClock())
        self.env = self.globals
        self.local: MutableMapping[Expr, int] = {}

    def visitSuper(self, expr: Super):
        dist = self.local[expr]
        superclass = self.env.getAt(dist, "super")

        obj = self.env.getAt(dist - 1, "this")

        method = superclass.find_method(expr.method.lexeme)

        if method is None:
            Runtime_lox_error(
                expr.method, f"Undefined property '{expr.method.lexeme}'."
            )

        return method.bind(obj)

    def visitThis(self, expr: This):
        return self.lookUpVar(expr.keyword, expr)

    def visitSet(self, expr: Set):
        obj = self.evaluate(expr.obj)

        if not isinstance(obj, LoxInstance):
            raise Runtime_lox_error(expr.name, "Only instances have fields.")

        value = self.evaluate(expr.value)
        obj.set(expr.name, value)
        return value

    def visitGet(self, expr: Get):
        obj = self.evaluate(expr.object)
        if isinstance(obj, LoxInstance):
            return obj.get(expr.name)

        raise Runtime_lox_error(expr.name, "Only instances have property")

    def visitClass(self, stmt: Class):
        superclass = None

        if stmt.superclass is not None:
            superclass = self.evaluate(stmt.superclass)
            if not isinstance(superclass, LoxClass):
                raise Runtime_lox_error(
                    stmt.superclass.name, "Superclass must be a class."
                )

        self.env.define(stmt.name.lexeme, None)

        if stmt.superclass is not None:
            self.env = Environment(self.env)
            self.env.define("super", superclass)

        methods = {}
        for method in stmt.methods:
            func = LoxFunction(method, self.env, method.name.lexeme == "init")
            methods[method.name.lexeme] = func

        _class = LoxClass(stmt.name.lexeme, superclass, methods)

        if stmt.superclass is not None:
            self.env = self.env.enclosing

        self.env.assign(stmt.name, _class)

    def resolve(self, expr: Expr, depth: int):
        self.local[expr] = depth

    def visitReturn(self, stmt: Return):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)

        raise ReturnException(value)

    def visitFunction(self, stmt: Function):
        function = LoxFunction(stmt, self.env)
        self.env.define(stmt.name.lexeme, function)

    def visitCall(self, expr: Call):
        callee = self.evaluate(expr.callee)
        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))

        if not isinstance(callee, LoxCallable):
            raise Runtime_lox_error(expr.paren, "can only call functions and classes.")

        func = callee

        if len(arguments) != func.arity():
            raise Runtime_lox_error(
                expr.paren,
                f"Expected {func.arity()} arguments, but got {len(arguments)} instead.",
            )

        return func.call(self, arguments)

    def exec_block(self, statements: Sequence[Stmt], env: Environment) -> None:
        previous = self.env
        try:
            self.env = env
            for statement in statements:
                self.execute(statement)
        finally:
            self.env = previous

    def visitWhile(self, stmt: While):
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    def visitLogical(self, expr: Logical):
        left = self.evaluate(expr.left)

        if expr.operator == TT.OR:
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left

        return self.evaluate(expr.right)

    def visitIf(self, stmt) -> None:
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

    def visitBlock(self, stmt: Block) -> None:
        self.exec_block(stmt.statements, Environment(self.env))

    def visitAssign(self, expr: Assign):
        value = self.evaluate(expr.value)

        dist: int = self.local[expr]
        if dist is not None:
            self.env.assignAt(dist, expr.name, value)
        else:
            self.globals.assign(expr.name, value)

    def lookUpVar(self, name: Token, expr: Expr) -> Any:
        try:
            dist = self.local[expr]
        except KeyError as e:
            return self.globals.get(name)

        return self.env.getAt(dist, name.lexeme)

    def visitVariable(self, expr: Variable):
        return self.lookUpVar(expr.name, expr)

    def visitVar(self, stmt: Var):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)

        self.env.define(stmt.name.lexeme, value)

    def visitExpression(self, stmt: Expression):
        self.evaluate(stmt.expression)

    def visitPrint(self, stmt: Print):
        print(self.stringify(self.evaluate(stmt.expression)))

    def runtime_error(self, err: Runtime_lox_error):
        print(f"{err.msg} [{err.token.line}]")
        self.had_error = True

    def stringify(self, expression) -> str:
        return "nil" if expression is None else str(expression)

    def execute(self, statement: Stmt):
        statement.accept(self)

    def interpret(self, statements: list[Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except Runtime_lox_error as e:
            self.runtime_error(e)

    def check_num_operands(self, operator: Token, left, right) -> None:
        if isinstance(left, float) and isinstance(right, float):
            return
        raise Runtime_lox_error(operator, "Operands must be numbers")

    def visitBinary(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

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
