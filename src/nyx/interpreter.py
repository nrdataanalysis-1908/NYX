"""Tree-walk interpreter for the NYX language."""
from dataclasses import dataclass
from .ast_nodes import (
    AssignStatement, Binary, BlockStatement, Call, FunctionStatement, Grouping,
    IfStatement, LetStatement, Literal, PrintStatement, ReturnStatement,
    Unary, Variable, WhileStatement,
)
from .errors import RuntimeNyxError
from .tokens import TokenType


class _ReturnSignal(Exception):
    def __init__(self, value): self.value = value


@dataclass
class _UserFunction:
    declaration: FunctionStatement
    closure: tuple[dict[str, object], ...]

    def __repr__(self): return f"<fn {self.declaration.name.lexeme}>"


class Interpreter:
    def __init__(self, output=print):
        self.scopes: list[dict[str, object]] = [{}]
        self.output = output

    def interpret(self, statements):
        try:
            for statement in statements: self._execute(statement)
        except _ReturnSignal:
            raise RuntimeNyxError("Return statement used outside a function.")

    def _execute(self, statement):
        if isinstance(statement, LetStatement):
            scope, name = self.scopes[-1], statement.name.lexeme
            if name in scope: self._runtime_error(statement.name, f"Variable '{name}' is already declared in this scope.")
            scope[name] = self._evaluate(statement.initializer)
        elif isinstance(statement, FunctionStatement):
            scope, name = self.scopes[-1], statement.name.lexeme
            if name in scope: self._runtime_error(statement.name, f"Name '{name}' is already declared in this scope.")
            scope[name] = _UserFunction(statement, tuple(self.scopes))
        elif isinstance(statement, ReturnStatement):
            if statement.value is None: raise _ReturnSignal(None)
            raise _ReturnSignal(self._evaluate(statement.value))
        elif isinstance(statement, AssignStatement):
            name = statement.name.lexeme
            for scope in reversed(self.scopes):
                if name in scope:
                    scope[name] = self._evaluate(statement.value)
                    break
            else: self._runtime_error(statement.name, f"Cannot assign to undefined variable '{name}'.")
        elif isinstance(statement, PrintStatement): self.output(self._evaluate(statement.expression))
        elif isinstance(statement, BlockStatement):
            self.scopes.append({})
            try:
                for child in statement.statements: self._execute(child)
            finally: self.scopes.pop()
        elif isinstance(statement, IfStatement):
            condition = self._evaluate(statement.condition)
            self._require_bool(condition, statement.keyword)
            if condition: self._execute(statement.then_branch)
            elif statement.else_branch is not None: self._execute(statement.else_branch)
        elif isinstance(statement, WhileStatement):
            while True:
                condition = self._evaluate(statement.condition)
                self._require_bool(condition, statement.keyword)
                if not condition: break
                self._execute(statement.body)
        else: raise RuntimeNyxError("Unsupported statement node.")

    def _evaluate(self, expression):
        if isinstance(expression, Literal): return expression.value
        if isinstance(expression, Grouping): return self._evaluate(expression.expression)
        if isinstance(expression, Variable):
            name = expression.name.lexeme
            for scope in reversed(self.scopes):
                if name in scope: return scope[name]
            self._runtime_error(expression.name, f"Undefined variable '{name}'.")
        if isinstance(expression, Unary):
            right = self._evaluate(expression.right)
            if expression.operator.type == TokenType.NOT:
                self._require_bool(right, expression.operator)
                return not right
            self._require_number(right, expression.operator)
            return -right if expression.operator.type == TokenType.MINUS else right
        if isinstance(expression, Binary): return self._binary(expression)
        if isinstance(expression, Call): return self._call(expression)
        raise RuntimeNyxError("Unsupported expression node.")

    def _call(self, expression):
        callee = self._evaluate(expression.callee)
        if not isinstance(callee, _UserFunction):
            self._runtime_error(expression.paren, "Only user-defined functions can be called.")
        expected = len(callee.declaration.parameters)
        if len(expression.arguments) != expected:
            self._runtime_error(expression.paren, f"Function '{callee.declaration.name.lexeme}' expects {expected} argument(s), got {len(expression.arguments)}.")
        arguments = [self._evaluate(arg) for arg in expression.arguments]
        parameter_scope = {p.lexeme: value for p, value in zip(callee.declaration.parameters, arguments)}
        previous_scopes = self.scopes
        self.scopes = [*callee.closure, parameter_scope]
        try:
            try:
                self._execute(callee.declaration.body)
            except _ReturnSignal as signal:
                return signal.value
            return None
        finally:
            self.scopes = previous_scopes

    def _binary(self, expression):
        op = expression.operator
        left = self._evaluate(expression.left)
        if op.type == TokenType.OR:
            self._require_bool(left, op)
            return left or self._logical_right(expression.right, op)
        if op.type == TokenType.AND:
            self._require_bool(left, op)
            return left and self._logical_right(expression.right, op)
        right = self._evaluate(expression.right)
        if op.type in (TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            self._require_number(left, op)
            self._require_number(right, op)
            if op.type == TokenType.PLUS: return left + right
            if op.type == TokenType.MINUS: return left - right
            if op.type == TokenType.STAR: return left * right
            if op.type == TokenType.SLASH:
                if right == 0: self._runtime_error(op, "Division by zero.")
                return left / right
            if right == 0: self._runtime_error(op, "Modulo by zero.")
            return left % right
        if op.type in (TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL):
            if type(left) not in (int, float) or type(right) not in (int, float):
                self._runtime_error(op, "Comparison operators require numeric operands.")
            return {TokenType.LESS: left < right, TokenType.LESS_EQUAL: left <= right,
                    TokenType.GREATER: left > right, TokenType.GREATER_EQUAL: left >= right}[op.type]
        if op.type in (TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            equal = type(left) is type(right) and left == right
            return equal if op.type == TokenType.EQUAL_EQUAL else not equal
        self._runtime_error(op, "Unsupported binary operator.")

    def _logical_right(self, expression, operator):
        value = self._evaluate(expression)
        self._require_bool(value, operator)
        return value
    def _require_number(self, value, token):
        if type(value) not in (int, float): self._runtime_error(token, "Arithmetic operators require numeric operands.")
    def _require_bool(self, value, token):
        if type(value) is not bool: self._runtime_error(token, "Conditions and logical operators require boolean operands.")
    def _runtime_error(self, token, message):
        raise RuntimeNyxError(f"[NYX:L{token.line}:C{token.column}] {message}")
