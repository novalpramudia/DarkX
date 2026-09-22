import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.lexer import tokenize
from src.parser import Parser
from src.interpreter import Interpreter, DarkXRuntimeError


def run(source, feed_input=None):
    """Jalankan source DarkX, kembalikan list baris output."""
    output = []
    input_queue = list(feed_input) if feed_input else []

    def fake_input(prompt=""):
        return input_queue.pop(0) if input_queue else ""

    program = Parser(tokenize(source)).parse()
    interp = Interpreter(output=output.append, input_func=fake_input)
    interp.run(program)
    return output


def test_hello_world():
    out = run('>>> "Hello World" ;;')
    assert out == ["Hello World"]


def test_variables_and_arithmetic():
    out = run('''
        ::: a === 10 ;;
        ::: b === 3 ;;
        >>> a +++ b ;;
        >>> a --- b ;;
        >>> a ** b ;;
        >>> a %% b ;;
    ''')
    assert out == ["13", "7", "30", "1"]


def test_string_concat():
    out = run('''
        ::: nama === "Dunia" ;;
        >>> "Halo, " +++ nama +++ "!" ;;
    ''')
    assert out == ["Halo, Dunia!"]


def test_if_else():
    out = run('''
        ::: umur === 15 ;;
        :: ((umur >=? 18)) {{
            >>> "dewasa" ;;
        }} ?? {{
            >>> "anak" ;;
        }}
    ''')
    assert out == ["anak"]


def test_while_loop_sum():
    out = run('''
        ::: total === 0 ;;
        ::: n === 1 ;;
        ~~ ((n <=? 5)) {{
            total === total +++ n ;;
            n === n +++ 1 ;;
        }}
        >>> total ;;
    ''')
    assert out == ["15"]


def test_function_recursive_fibonacci():
    out = run('''
        => fib((n)) {{
            :: ((n <=? 1)) {{
                <= n ;;
            }}
            <= fib((n --- 1)) +++ fib((n --- 2)) ;;
        }}
        >>> fib((10)) ;;
    ''')
    assert out == ["55"]


def test_function_closure_and_scope():
    out = run('''
        => makeAdder((x)) {{
            <= x ;;
        }}
        ::: hasil === makeAdder((7)) ;;
        >>> hasil +++ 1 ;;
    ''')
    assert out == ["8"]


def test_input_statement():
    out = run('''
        ::: nama === <<< ;;
        >>> "Halo, " +++ nama ;;
    ''', feed_input=["Budi"])
    assert out == ["Halo, Budi"]


def test_division_by_zero_raises():
    try:
        run('>>> 10 // 0 ;;')
        assert False, "seharusnya raise DarkXRuntimeError"
    except DarkXRuntimeError as e:
        assert "nol" in str(e)


def test_undeclared_variable_raises():
    try:
        run('>>> tidakAda ;;')
        assert False, "seharusnya raise DarkXRuntimeError"
    except DarkXRuntimeError as e:
        assert "tidakAda" in str(e)


def test_reassign_without_let_raises():
    try:
        run('x === 5 ;;')
        assert False, "seharusnya raise DarkXRuntimeError"
    except DarkXRuntimeError:
        pass


def test_logic_operators():
    out = run('''
        :: ((1 <? 2 && 3 >? 2)) {{
            >>> "keduanya benar" ;;
        }}
        :: ((1 >? 2 || 3 >? 2)) {{
            >>> "salah satu benar" ;;
        }}
        :: ((!! ((1 >? 2)))) {{
            >>> "negasi benar" ;;
        }}
    ''')
    assert out == ["keduanya benar", "salah satu benar", "negasi benar"]
