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


def test_newline_separates_statements_without_semicolons():
    source = 'let nome = "NYX"\nlet versao = 0.1\nprint(nome)\nprint(versao)'
    assert execute(source) == ["NYX", 0.1]


def test_semicolons_remain_valid_and_optional():
    assert execute('let x = 2;\nprint(x)\nprint(x + 1);') == [2, 3]


def test_expression_can_continue_on_next_line():
    source = 'let total = 10 +\n    5 * 2\nprint(total)'
    assert execute(source) == [20]


def test_utf8_bom_is_ignored_at_source_start():
    assert execute('\ufefflet nome = "NYX"\nprint(nome)') == ["NYX"]


def test_operator_precedence_and_grouping():
    assert execute('print((2 + 3) * 4);') == [20]


def test_boolean_logic_and_comparison():
    assert execute('print(10 > 3 and not false);') == [True]


def test_logical_operators_use_short_circuit_evaluation():
    assert execute('print(false and missing)\nprint(true or missing)') == [False, True]


def test_unary_numeric_operators():
    assert execute('print(-5)\nprint(+3.5)') == [-5, 3.5]


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


def test_assignment_updates_nearest_visible_scope():
    source = '''
let value = 1
{
    let value = 2
    value = 3
    print(value)
}
print(value)
'''
    assert execute(source) == [3, 1]


def test_assignment_updates_outer_scope_when_not_shadowed():
    source = '''
let value = 1
{
    value = 8
}
print(value)
'''
    assert execute(source) == [8]


def test_assignment_to_undefined_variable_is_rejected():
    with pytest.raises(RuntimeNyxError, match="undefined variable"):
        execute('missing = 10')


def test_division_by_zero_is_reported():
    with pytest.raises(RuntimeNyxError, match="Division by zero"):
        execute('print(1 / 0);')


def test_modulo_by_zero_is_reported():
    with pytest.raises(RuntimeNyxError, match="Modulo by zero"):
        execute('print(5 % 0)')


def test_strict_boolean_types():
    with pytest.raises(RuntimeNyxError, match="boolean operands"):
        execute('print(1 and true);')


def test_non_boolean_if_condition_is_rejected():
    with pytest.raises(RuntimeNyxError, match="boolean operands"):
        execute('if (1) { print("invalid") }')


def test_non_boolean_while_condition_is_rejected():
    with pytest.raises(RuntimeNyxError, match="boolean operands"):
        execute('while (1) { print("invalid") }')


def test_invalid_character_is_reported():
    with pytest.raises(LexError, match="NYX:L1:C1"):
        Lexer("@").scan_tokens()


def test_missing_statement_separator_is_reported_on_same_line():
    with pytest.raises(ParseError, match="Expected ';' or a line break"):
        execute('print(1) print(2)')


def test_if_true_branch():
    source = 'if (true) {\n print("yes")\n} else {\n print("no")\n}'
    assert execute(source) == ["yes"]


def test_if_else_false_branch():
    source = 'if (false) { print("yes") } else { print("no") }'
    assert execute(source) == ["no"]


def test_if_without_else():
    assert execute('if (2 > 1) { print("ok") }') == ["ok"]


def test_empty_block_is_valid():
    assert execute('if (true) { }\nprint("after")') == ["after"]


def test_while_repeats_until_condition_is_false():
    source = '''
let index = 0
while (index < 4) {
    print(index)
    index = index + 1
}
'''
    assert execute(source) == [0, 1, 2, 3]


def test_nested_control_flow_and_block_scope():
    source = '''
let visible = 7
if (true) {
    let hidden = 9
    if (hidden > visible) { print(hidden) }
}
'''
    assert execute(source) == [9]
    with pytest.raises(RuntimeNyxError, match="Undefined variable"):
        execute(source + '\nprint(hidden)')
