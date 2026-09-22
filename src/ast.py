"""
DarkX AST
================
Definisi node-node Abstract Syntax Tree untuk DarkX.
Setiap node adalah kelas Python sederhana (bukan tuple), supaya
Interpreter bisa melakukan dispatch lewat nama kelas (lihat interpreter.py).

Catatan: file ini bernama ast.py di dalam package 'src'. Ia TIDAK
bentrok dengan modul standar Python 'ast' karena selalu diimpor secara
relatif (from . import ast) di dalam package, sehingga nama lengkapnya
adalah 'src.ast', bukan 'ast'.
"""


class Node:
    """Base class untuk semua node AST."""
    pass


# ---------- Program ----------

class Program(Node):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Program({len(self.statements)} statements)"


# ---------- Ekspresi ----------

class NumberLiteral(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"NumberLiteral({self.value})"


class StringLiteral(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"StringLiteral({self.value!r})"


class Identifier(Node):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"


class BinOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BinOp({self.op}, {self.left!r}, {self.right!r})"


class UnaryOp(Node):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

    def __repr__(self):
        return f"UnaryOp({self.op}, {self.operand!r})"


class Call(Node):
    def __init__(self, callee, args, line=None):
        self.callee = callee
        self.args = args
        self.line = line

    def __repr__(self):
        return f"Call({self.callee}, {self.args!r})"


# ---------- Statement ----------

class LetStmt(Node):
    def __init__(self, name, expr, line=None):
        self.name = name
        self.expr = expr
        self.line = line

    def __repr__(self):
        return f"LetStmt({self.name} === {self.expr!r})"


class AssignStmt(Node):
    def __init__(self, name, expr, line=None):
        self.name = name
        self.expr = expr
        self.line = line

    def __repr__(self):
        return f"AssignStmt({self.name} === {self.expr!r})"


class PrintStmt(Node):
    def __init__(self, exprs, line=None):
        self.exprs = exprs
        self.line = line

    def __repr__(self):
        return f"PrintStmt({self.exprs!r})"


class InputStmt(Node):
    def __init__(self, name, prompt_expr, line=None):
        self.name = name
        self.prompt_expr = prompt_expr
        self.line = line

    def __repr__(self):
        return f"InputStmt({self.name})"


class IfStmt(Node):
    def __init__(self, cond, then_body, else_body, line=None):
        self.cond = cond
        self.then_body = then_body
        self.else_body = else_body
        self.line = line

    def __repr__(self):
        return f"IfStmt({self.cond!r})"


class WhileStmt(Node):
    def __init__(self, cond, body, line=None):
        self.cond = cond
        self.body = body
        self.line = line

    def __repr__(self):
        return f"WhileStmt({self.cond!r})"


class FuncDef(Node):
    def __init__(self, name, params, body, line=None):
        self.name = name
        self.params = params
        self.body = body
        self.line = line

    def __repr__(self):
        return f"FuncDef({self.name}/{len(self.params)})"


class ReturnStmt(Node):
    def __init__(self, expr, line=None):
        self.expr = expr
        self.line = line

    def __repr__(self):
        return f"ReturnStmt({self.expr!r})"


class ExprStmt(Node):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"ExprStmt({self.expr!r})"
