"""
DarkX Interpreter
================
Tree-walking interpreter untuk AST DarkX.

Berisi:
  - Environment       : scope variabel (chain ke parent, mendukung closure)
  - DarkXFunction     : representasi fungsi user-defined
  - DarkXRuntimeError : exception untuk semua error saat eksekusi
  - ReturnSignal       : exception internal untuk mengangkat nilai '<='
  - Interpreter        : eval/exec seluruh node AST
"""

from . import ast as A


class DarkXRuntimeError(Exception):
    def __init__(self, message, line=None):
        loc = f"Baris {line}: " if line is not None else ""
        super().__init__(f"[Runtime Error] {loc}{message}")
        self.line = line


class ReturnSignal(Exception):
    """Dipakai secara internal untuk membawa nilai '<=' keluar dari fungsi."""
    def __init__(self, value):
        self.value = value


class DarkXFunction:
    def __init__(self, name, params, body, closure_env):
        self.name = name
        self.params = params
        self.body = body
        self.closure_env = closure_env

    def __repr__(self):
        return f"<fungsi {self.name}/{len(self.params)}>"


class Environment:
    """Scope variabel. Setiap blok {{ }} baru punya Environment sendiri
    yang mengarah (chain) ke parent-nya, sehingga closure & shadowing
    bekerja secara alami."""

    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def define(self, name, value):
        self.vars[name] = value

    def get(self, name, line=None):
        env = self
        while env is not None:
            if name in env.vars:
                return env.vars[name]
            env = env.parent
        raise DarkXRuntimeError(f"Variabel tidak dikenal: '{name}'", line)

    def set(self, name, value, line=None):
        env = self
        while env is not None:
            if name in env.vars:
                env.vars[name] = value
                return
            env = env.parent
        raise DarkXRuntimeError(
            f"Tidak bisa assign ke '{name}' yang belum dideklarasikan "
            f"(gunakan ':::' terlebih dahulu)",
            line,
        )


class Interpreter:
    def __init__(self, output=None, input_func=None):
        self.global_env = Environment()
        self._output = output if output is not None else print
        self._input = input_func if input_func is not None else input

    def run(self, program):
        self.exec_block(program.statements, self.global_env)

    # ---------------- statement execution ----------------
    def exec_block(self, statements, env):
        for stmt in statements:
            self.exec_stmt(stmt, env)

    def exec_stmt(self, node, env):
        method = getattr(self, f"exec_{type(node).__name__}", None)
        if method is None:
            raise DarkXRuntimeError(f"Statement tidak dikenal: {type(node).__name__}")
        return method(node, env)

    def exec_LetStmt(self, node, env):
        value = self.eval_expr(node.expr, env)
        env.define(node.name, value)

    def exec_AssignStmt(self, node, env):
        value = self.eval_expr(node.expr, env)
        env.set(node.name, value, node.line)

    def exec_InputStmt(self, node, env):
        prompt = ""
        if node.prompt_expr is not None:
            prompt = self.stringify(self.eval_expr(node.prompt_expr, env))
        try:
            raw = self._input(prompt)
        except EOFError:
            raw = ""
        env.define(node.name, self._coerce_input(raw))

    @staticmethod
    def _coerce_input(raw):
        try:
            if '.' in raw:
                return float(raw)
            return int(raw)
        except ValueError:
            return raw

    def exec_PrintStmt(self, node, env):
        parts = [self.stringify(self.eval_expr(e, env)) for e in node.exprs]
        self._output(" ".join(parts))

    def exec_ExprStmt(self, node, env):
        self.eval_expr(node.expr, env)

    def exec_IfStmt(self, node, env):
        cond = self.eval_expr(node.cond, env)
        if self.truthy(cond):
            self.exec_block(node.then_body, Environment(env))
        elif node.else_body is not None:
            self.exec_block(node.else_body, Environment(env))

    def exec_WhileStmt(self, node, env):
        while self.truthy(self.eval_expr(node.cond, env)):
            self.exec_block(node.body, Environment(env))

    def exec_FuncDef(self, node, env):
        env.define(node.name, DarkXFunction(node.name, node.params, node.body, env))

    def exec_ReturnStmt(self, node, env):
        value = self.eval_expr(node.expr, env) if node.expr is not None else None
        raise ReturnSignal(value)

    # ---------------- expression evaluation ----------------
    def eval_expr(self, node, env):
        method = getattr(self, f"eval_{type(node).__name__}", None)
        if method is None:
            raise DarkXRuntimeError(f"Ekspresi tidak dikenal: {type(node).__name__}")
        return method(node, env)

    def eval_NumberLiteral(self, node, env):
        return node.value

    def eval_StringLiteral(self, node, env):
        return node.value

    def eval_Identifier(self, node, env):
        return env.get(node.name)

    def eval_UnaryOp(self, node, env):
        val = self.eval_expr(node.operand, env)
        if node.op == "MINUS":
            self._check_number(val, "---")
            return -val
        if node.op == "NOT":
            return not self.truthy(val)
        raise DarkXRuntimeError(f"Operator unary tidak dikenal: {node.op}")

    def eval_BinOp(self, node, env):
        op = node.op
        left = self.eval_expr(node.left, env)
        right = self.eval_expr(node.right, env)

        if op == "PLUS":
            if isinstance(left, str) or isinstance(right, str):
                return self.stringify(left) + self.stringify(right)
            self._check_numbers(left, right, "+++")
            return left + right
        if op == "MINUS":
            self._check_numbers(left, right, "---")
            return left - right
        if op == "MUL":
            self._check_numbers(left, right, "**")
            return left * right
        if op == "DIV":
            self._check_numbers(left, right, "//")
            if right == 0:
                raise DarkXRuntimeError("Pembagian dengan nol")
            result = left / right
            if isinstance(left, int) and isinstance(right, int) and left % right == 0:
                return int(result)
            return result
        if op == "MOD":
            self._check_numbers(left, right, "%%")
            if right == 0:
                raise DarkXRuntimeError("Modulo dengan nol")
            return left % right
        if op == "EQ":
            return left == right
        if op == "NEQ":
            return left != right
        if op == "GT":
            self._check_numbers(left, right, ">?")
            return left > right
        if op == "LT":
            self._check_numbers(left, right, "<?")
            return left < right
        if op == "GE":
            self._check_numbers(left, right, ">=?")
            return left >= right
        if op == "LE":
            self._check_numbers(left, right, "<=?")
            return left <= right
        if op == "AND":
            return self.truthy(left) and self.truthy(right)
        if op == "OR":
            return self.truthy(left) or self.truthy(right)
        raise DarkXRuntimeError(f"Operator biner tidak dikenal: {op}")

    def eval_Call(self, node, env):
        func = env.get(node.callee, node.line)
        args = [self.eval_expr(a, env) for a in node.args]

        if isinstance(func, DarkXFunction):
            if len(args) != len(func.params):
                raise DarkXRuntimeError(
                    f"Fungsi '{func.name}' butuh {len(func.params)} argumen, "
                    f"tetapi diberi {len(args)}",
                    node.line,
                )
            call_env = Environment(func.closure_env)
            for pname, pval in zip(func.params, args):
                call_env.define(pname, pval)
            try:
                self.exec_block(func.body, call_env)
            except ReturnSignal as ret:
                return ret.value
            return None

        if callable(func):
            return func(*args)

        raise DarkXRuntimeError(f"'{node.callee}' bukan fungsi", node.line)

    # ---------------- helpers ----------------
    def truthy(self, value):
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return len(value) > 0
        return True

    def stringify(self, value):
        if value is None:
            return "null"
        if isinstance(value, bool):
            return "benar" if value else "salah"
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)

    def _check_number(self, val, op):
        if not isinstance(val, (int, float)) or isinstance(val, bool):
            raise DarkXRuntimeError(
                f"Operator '{op}' butuh tipe angka, tetapi mendapat {type(val).__name__}"
            )

    def _check_numbers(self, left, right, op):
        self._check_number(left, op)
        self._check_number(right, op)


def interpret(program, output=None, input_func=None):
    interp = Interpreter(output=output, input_func=input_func)
    interp.run(program)
    return interp
