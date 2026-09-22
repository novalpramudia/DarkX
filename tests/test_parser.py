import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.lexer import tokenize
from src.parser import Parser, ParserError
from src import ast as A


def parse_src(source):
    return Parser(tokenize(source)).parse()


def test_parse_print_string():
    program = parse_src('>>> "Hello World" ;;')
    assert len(program.statements) == 1
    stmt = program.statements[0]
    assert isinstance(stmt, A.PrintStmt)
    assert isinstance(stmt.exprs[0], A.StringLiteral)
    assert stmt.exprs[0].value == "Hello World"


def test_parse_let():
    program = parse_src(':::  x === 1 +++ 2 ;;')
    stmt = program.statements[0]
    assert isinstance(stmt, A.LetStmt)
    assert stmt.name == "x"
    assert isinstance(stmt.expr, A.BinOp)
    assert stmt.expr.op == "PLUS"


def test_parse_if_else():
    program = parse_src('''
        :: ((1 >? 0)) {{
            >>> "ya" ;;
        }} ?? {{
            >>> "tidak" ;;
        }}
    ''')
    stmt = program.statements[0]
    assert isinstance(stmt, A.IfStmt)
    assert stmt.else_body is not None


def test_parse_while():
    program = parse_src('~~ ((1 <? 2)) {{ >>> 1 ;; }}')
    stmt = program.statements[0]
    assert isinstance(stmt, A.WhileStmt)


def test_parse_func_and_call():
    program = parse_src('''
        => tambah((a,, b)) {{
            <= a +++ b ;;
        }}
        >>> tambah((1,, 2)) ;;
    ''')
    func_def = program.statements[0]
    assert isinstance(func_def, A.FuncDef)
    assert func_def.name == "tambah"
    assert func_def.params == ["a", "b"]

    print_stmt = program.statements[1]
    call = print_stmt.exprs[0]
    assert isinstance(call, A.Call)
    assert call.callee == "tambah"
    assert len(call.args) == 2


def test_operator_precedence():
    # 1 +++ 2 ** 3  harus jadi 1 +++ (2 ** 3)
    program = parse_src(':::  x === 1 +++ 2 ** 3 ;;')
    expr = program.statements[0].expr
    assert expr.op == "PLUS"
    assert isinstance(expr.right, A.BinOp)
    assert expr.right.op == "MUL"


def test_syntax_error_raises():
    try:
        parse_src(':::  x 1 ;;')  # tidak ada '==='
        assert False, "seharusnya raise ParserError"
    except ParserError:
        pass
