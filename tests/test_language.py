import pytest

from nyx import run
from nyx.errors import LexError, ParseError, RuntimeNyxError
from nyx.lexer import Lexer
from nyx.tokens import TokenType


def execute(source):
    output = []
    run(source, output=output.append)
    return output


def test_lexer_recognizes_keywords_and_numbers():
    tokens = Lexer('let value = 12.5; print(value);').scan_tokens()
    assert [t.type for t in tokens[:4]] == [
        TokenType.LET, TokenType.IDENTIFIER, TokenType.EQUAL, TokenType.FLOAT
    ]


def test_declaration_arithmetic_and_print():
    assert execute('let x = 2 + 3 * 4; print(x);') == [14]


def test_operator_precedence_and_grouping():
    assert execute('print((2 + 3) * 4);') == [20]


def test_boolean_logic_and_comparison():
    assert execute('print(10 > 3 and not false);') == [True]


def test_string_and_null_literals():
    assert execute('let message = "hello\\nworld"; print(message); print(null);') == [
        "hello\nworld", None
    ]


def test_comments_are_ignored():
    assert execute('# comment\nprint(7); # trailing comment') == [7]


def test_undefined_variable_is_reported():
    with pytest.raises(RuntimeNyxError, match="Undefined variable"):
        execute('print(missing);')


def test_duplicate_declaration_is_rejected():
    with pytest.raises(RuntimeNyxError, match="already declared"):
        execute('let x = 1; let x = 2;')


def test_division_by_zero_is_reported():
    with pytest.raises(RuntimeNyxError, match="Division by zero"):
        execute('print(1 / 0);')


def test_strict_boolean_types():
    with pytest.raises(RuntimeNyxError, match="boolean operands"):
        execute('print(1 and true);')


def test_invalid_character_is_reported():
    with pytest.raises(LexError, match="NYX:L1:C1"):
        Lexer("@").scan_tokens()


def test_missing_semicolon_is_reported():
    with pytest.raises(ParseError, match="Expected ';'"):
        execute('print(1)')
