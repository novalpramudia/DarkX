import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.lexer import tokenize, LexerError


def token_types(source):
    # NEWLINE murni informatif di level lexer (dipakai utk pelacakan baris);
    # parser yang membuang NEWLINE karena statement dipisah oleh ';;'.
    return [t.type for t in tokenize(source) if t.type not in ("EOF", "NEWLINE")]


def test_print_string():
    types = token_types('>>> "Hello World" ;;')
    assert types == ["PRINT", "STRING", "SEMI"]


def test_let_assign_number():
    types = token_types(':::  x === 42 ;;')
    assert types == ["LET", "IDENT", "ASSIGN", "NUMBER", "SEMI"]


def test_does_not_confuse_let_with_if():
    # ':::' harus terbaca sebagai 1 token LET, bukan IF + ASSIGN-partial
    tokens = tokenize(':::')
    assert tokens[0].type == "LET"
    assert tokens[1].type == "EOF"


def test_does_not_confuse_le_with_return():
    tokens = tokenize('<=?')
    assert tokens[0].type == "LE"
    tokens2 = tokenize('<=')
    assert tokens2[0].type == "RETURN"


def test_comment_is_skipped():
    types = token_types('## ini komentar\n>>> 1 ;;')
    assert types == ["PRINT", "NUMBER", "SEMI"]


def test_operators():
    types = token_types('a +++ b --- c ** d // e %% f')
    assert types == [
        "IDENT", "PLUS", "IDENT", "MINUS", "IDENT",
        "MUL", "IDENT", "DIV", "IDENT", "MOD", "IDENT",
    ]


def test_comparisons_and_logic():
    types = token_types('a =? b !? c >? d <? e >=? f <=? g && h || i !! j')
    expected = [
        "IDENT", "EQ", "IDENT", "NEQ", "IDENT", "GT", "IDENT", "LT",
        "IDENT", "GE", "IDENT", "LE", "IDENT", "AND", "IDENT", "OR",
        "IDENT", "NOT", "IDENT",
    ]
    assert types == expected


def test_string_escape():
    tokens = tokenize(r'"baris1\nbaris2\ttab\"kutip\""')
    assert tokens[0].value == 'baris1\nbaris2\ttab"kutip"'


def test_unknown_character_raises():
    try:
        tokenize('@@@')
        assert False, "seharusnya raise LexerError"
    except LexerError as e:
        assert e.line == 1
