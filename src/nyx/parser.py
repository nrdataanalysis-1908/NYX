"""Recursive-descent parser for NYX."""
from .ast_nodes import (
    AssignStatement, Binary, BlockStatement, Grouping, IfStatement,
    LetStatement, Literal, PrintStatement, Unary, Variable, WhileStatement,
)
from .errors import ParseError
from .tokens import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> list[object]:
        statements = []
        while not self._check(TokenType.EOF):
            statements.append(self._statement())
        return statements

    def _statement(self):
        if self._match(TokenType.LET):
            name = self._consume(TokenType.IDENTIFIER, "Expected a variable name after 'let'.")
            self._consume(TokenType.EQUAL, "Expected '=' after the variable name.")
            value = self._expression()
            self._consume_terminator("Expected ';' or a line break after the declaration.")
            return LetStatement(name, value)
        if self._match(TokenType.PRINT):
            self._consume(TokenType.LEFT_PAREN, "Expected '(' after 'print'.")
            value = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expected ')' after the value.")
            self._consume_terminator("Expected ';' or a line break after the print statement.")
            return PrintStatement(value)
        if self._check(TokenType.IDENTIFIER) and self._check_next(TokenType.EQUAL):
            name = self._advance()
            self._advance()
            value = self._expression()
            self._consume_terminator("Expected ';' or a line break after the assignment.")
            return AssignStatement(name, value)
        if self._match(TokenType.IF):
            keyword = self._previous()
            self._consume(TokenType.LEFT_PAREN, "Expected '(' after 'if'.")
            condition = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expected ')' after the if condition.")
            then_branch = self._block()
            else_branch = self._block() if self._match(TokenType.ELSE) else None
            return IfStatement(keyword, condition, then_branch, else_branch)
        if self._match(TokenType.WHILE):
            keyword = self._previous()
            self._consume(TokenType.LEFT_PAREN, "Expected '(' after 'while'.")
            condition = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expected ')' after the while condition.")
            return WhileStatement(keyword, condition, self._block())
        if self._match(TokenType.LEFT_BRACE):
            return self._block_body()
        self._error(self._peek(), "Expected a statement: 'let', assignment, 'print', 'if', 'while' or block.")

    def _block(self) -> BlockStatement:
        self._consume(TokenType.LEFT_BRACE, "Expected '{' before block.")
        return self._block_body()

    def _block_body(self) -> BlockStatement:
        statements = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._check(TokenType.EOF):
            statements.append(self._statement())
        self._consume(TokenType.RIGHT_BRACE, "Expected '}' after block.")
        return BlockStatement(statements)

    def _consume_terminator(self, message: str) -> None:
        if self._match(TokenType.SEMICOLON):
            return
        previous = self._previous()
        current = self._peek()
        if current.type in (TokenType.EOF, TokenType.RIGHT_BRACE) or current.line > previous.line:
            return
        self._error(current, message)

    def _expression(self):
        return self._or()

    def _or(self):
        expr = self._and()
        while self._match(TokenType.OR):
            op = self._previous()
            expr = Binary(expr, op, self._and())
        return expr

    def _and(self):
        expr = self._equality()
        while self._match(TokenType.AND):
            op = self._previous()
            expr = Binary(expr, op, self._equality())
        return expr

    def _equality(self):
        expr = self._comparison()
        while self._match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            op = self._previous()
            expr = Binary(expr, op, self._comparison())
        return expr

    def _comparison(self):
        expr = self._term()
        while self._match(TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER,
                          TokenType.GREATER_EQUAL):
            op = self._previous()
            expr = Binary(expr, op, self._term())
        return expr

    def _term(self):
        expr = self._factor()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            op = self._previous()
            expr = Binary(expr, op, self._factor())
        return expr

    def _factor(self):
        expr = self._unary()
        while self._match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op = self._previous()
            expr = Binary(expr, op, self._unary())
        return expr

    def _unary(self):
        if self._match(TokenType.NOT, TokenType.MINUS, TokenType.PLUS):
            op = self._previous()
            return Unary(op, self._unary())
        return self._primary()

    def _primary(self):
        if self._match(TokenType.FALSE):
            return Literal(False)
        if self._match(TokenType.TRUE):
            return Literal(True)
        if self._match(TokenType.NULL):
            return Literal(None)
        if self._match(TokenType.INTEGER, TokenType.FLOAT, TokenType.STRING):
            return Literal(self._previous().literal)
        if self._match(TokenType.IDENTIFIER):
            return Variable(self._previous())
        if self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expected ')' after expression.")
            return Grouping(expr)
        self._error(self._peek(), "Expected a literal, variable or parenthesized expression.")

    def _match(self, *types: TokenType) -> bool:
        if any(self._check(token_type) for token_type in types):
            self._advance()
            return True
        return False

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if self._check(token_type):
            return self._advance()
        self._error(self._peek(), message)

    def _check(self, token_type: TokenType) -> bool:
        return self._peek().type == token_type

    def _check_next(self, token_type: TokenType) -> bool:
        return self.current + 1 < len(self.tokens) and self.tokens[self.current + 1].type == token_type

    def _advance(self) -> Token:
        if not self._check(TokenType.EOF):
            self.current += 1
        return self._previous()

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]

    def _error(self, token: Token, message: str):
        raise ParseError(f"[NYX:L{token.line}:C{token.column}] {message}")
