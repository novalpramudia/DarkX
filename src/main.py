#!/usr/bin/env python3
"""
DarkX CLI
================
Entry point untuk menjalankan file .dx.

Pemakaian (dijalankan dari root folder darkx/):

    python -m src.main examples/hello.dx

atau, setelah darkx.py di-set executable:

    ./darkx.py examples/hello.dx
"""

import sys
import os

from .lexer import tokenize, LexerError
from .parser import Parser, ParserError
from .interpreter import Interpreter, DarkXRuntimeError


def run_source(source, filename="<script>"):
    tokens = tokenize(source)
    program = Parser(tokens).parse()
    interp = Interpreter()
    interp.run(program)
    return interp


def run_file(path):
    if not path.endswith(".dx"):
        print(f"[DarkX] Peringatan: file '{path}' tidak berekstensi .dx", file=sys.stderr)

    if not os.path.isfile(path):
        print(f"[DarkX] Error: file tidak ditemukan: {path}", file=sys.stderr)
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        run_source(source, filename=path)
    except LexerError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    except ParserError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    except DarkXRuntimeError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Pemakaian: python -m src.main <file.dx>", file=sys.stderr)
        sys.exit(1)
    run_file(sys.argv[1])


if __name__ == "__main__":
    main()
