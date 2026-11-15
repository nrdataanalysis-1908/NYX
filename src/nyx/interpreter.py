"""Tree-walk interpreter for the NYX language MVP."""
from .ast_nodes import Binary, Grouping, LetStatement, Literal, PrintStatement, Unary, Variable
from .errors import RuntimeNyxError
from .tokens import TokenType


class Interpreter:
    def __init__(self, output=print):
        self.environment: dict[str, object] = {}
        self.output = output

    def interpret(self, statements: list[object]) -> None:
        for statement in statements:
            self._execute(statement)

    def _execute(self, statement) -> None:
        if isinstance(statement, LetStatement):
            name = statement.name.lexeme
            if name in self.environment:
                self._runtime_error(statement.name, f"Variable '{name}' is already declared.")
            self.environment[name] = self._evaluate(statement.initializer)
        elif isinstance(statement, PrintStatement):
            self.output(self._evaluate(statement.expression))
        else:
            raise RuntimeNyxError("Unsupported statement node.")

    def _evaluate(self, expression):
        if isinstance(expression, Literal):
            return expression.value
        if isinstance(expression, Grouping):
            return self._evaluate(expression.expression)
        if isinstance(expression, Variable):
            name = expression.name.lexeme
            if name not in self.environment:
                self._runtime_error(expression.name, f"Undefined variable '{name}'.")
            return self.environment[name]
        if isinstance(expression, Unary):
            right = self._evaluate(expression.right)
            if expression.operator.type == TokenType.NOT:
                self._require_bool(right, expression.operator)
                return not right
            self._require_number(right, expression.operator)
            return -right if expression.operator.type == TokenType.MINUS else right
        if isinstance(expression, Binary):
            return self._binary(expression)
        raise RuntimeNyxError("Unsupported expression node.")

    def _binary(self, expression: Binary):
        op = expression.operator
        left = self._evaluate(expression.left)
        if op.type == TokenType.OR:
            self._require_bool(left, op)
            return left or self._logical_right(expression.right, op)
        if op.type == TokenType.AND:
            self._require_bool(left, op)
            return left and self._logical_right(expression.right, op)
        right = self._evaluate(expression.right)
        if op.type in (TokenType.PLUS, TokenType.MINUS, TokenType.STAR,
                       TokenType.SLASH, TokenType.PERCENT):
            self._require_number(left, op)
            self._require_number(right, op)
            if op.type == TokenType.PLUS:
                return left + right
            if op.type == TokenType.MINUS:
                return left - right
            if op.type == TokenType.STAR:
                return left * right
            if op.type == TokenType.SLASH:
                if right == 0:
                    self._runtime_error(op, "Division by zero.")
                return left / right
            if right == 0:
                self._runtime_error(op, "Modulo by zero.")
            return left % right
        if op.type in (TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER,
                       TokenType.GREATER_EQUAL):
            if type(left) not in (int, float) or type(right) not in (int, float):
                self._runtime_error(op, "Comparison operators require numeric operands.")
            return {
                TokenType.LESS: left < right,
                TokenType.LESS_EQUAL: left <= right,
                TokenType.GREATER: left > right,
                TokenType.GREATER_EQUAL: left >= right,
            }[op.type]
        if op.type in (TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            equal = type(left) is type(right) and left == right
            return equal if op.type == TokenType.EQUAL_EQUAL else not equal
        self._runtime_error(op, "Unsupported binary operator.")

    def _logical_right(self, expression, operator):
        value = self._evaluate(expression)
        self._require_bool(value, operator)
        return value

    def _require_number(self, value, token) -> None:
        if type(value) not in (int, float):
            self._runtime_error(token, "Arithmetic operators require numeric operands.")

    def _require_bool(self, value, token) -> None:
        if type(value) is not bool:
            self._runtime_error(token, "Logical operators require boolean operands.")

    def _runtime_error(self, token, message):
        raise RuntimeNyxError(f"[NYX:L{token.line}:C{token.column}] {message}")
