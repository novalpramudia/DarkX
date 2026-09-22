"""
DarkX Parser
================
Recursive-descent parser: token stream -> AST.

Grammar (EBNF) ringkas — lihat README.md untuk versi lengkap:

    program     := statement*
    statement   := let_stmt | assign_stmt | print_stmt | if_stmt
                 | while_stmt | func_def | return_stmt | expr_stmt
    block       := '{{' statement* '}}'

    let_stmt    := ':::' IDENT '===' ( '<<<' expr? | expression ) ';;'?
    assign_stmt := IDENT '===' ( '<<<' expr? | expression ) ';;'?
    print_stmt  := '>>>' expression (',,' expression)* ';;'?
    if_stmt     := '::' '((' expression '))' block ('??' block)?
    while_stmt  := '~~' '((' expression '))' block
    func_def    := '=>' IDENT '((' (IDENT (',,' IDENT)*)? '))' block
    return_stmt := '<=' expression? ';;'?
    expr_stmt   := expression ';;'?

    expression  := logic_or
    logic_or    := logic_and ('||' logic_and)*
    logic_and   := equality ('&&' equality)*
    equality    := comparison (('=?'|'!?') comparison)*
    comparison  := term (('>?'|'<?'|'>=?'|'<=?') term)*
    term        := factor (('+++'|'---') factor)*
    factor      := unary (('**'|'//'|'%%') unary)*
    unary       := ('!!'|'---') unary | call
    call        := primary ( '((' (expression (',,' expression)*)? '))' )*
    primary     := NUMBER | STRING | IDENT | '((' expression '))'
"""

from . import ast as A


class ParserError(Exception):
    def __init__(self, message, line, col):
        super().__init__(f"[Parser Error] Baris {line}, Kolom {col}: {message}")
        self.line = line
        self.col = col


class Parser:
    def __init__(self, tokens):
        # NEWLINE murni kosmetik di DarkX: statement dipisah oleh ';;'
        # (opsional) atau cukup oleh struktur grammar itu sendiri.
        self.tokens = [t for t in tokens if t.type != "NEWLINE"]
        self.pos = 0

    # ---------------- helper dasar ----------------
    def peek(self, offset=0):
        idx = self.pos + offset
        if idx >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[idx]

    def advance(self):
        tok = self.peek()
        if tok.type != "EOF":
            self.pos += 1
        return tok

    def check(self, ttype):
        return self.peek().type == ttype

    def match(self, *ttypes):
        if self.peek().type in ttypes:
            return self.advance()
        return None

    def expect(self, ttype, what=None):
        tok = self.peek()
        if tok.type != ttype:
            expected = what or f"'{ttype}'"
            raise ParserError(
                f"Diharapkan {expected}, tetapi menemukan {tok.type} ({tok.value!r})",
                tok.line, tok.col,
            )
        return self.advance()

    def skip_semi(self):
        while self.match("SEMI"):
            pass

    def is_stmt_start(self):
        return self.peek().type in ("LET", "PRINT", "IF", "WHILE", "FUNC", "RETURN")

    # ---------------- entry point ----------------
    def parse(self):
        statements = []
        self.skip_semi()
        while not self.check("EOF"):
            statements.append(self.statement())
            self.skip_semi()
        return A.Program(statements)

    # ---------------- statements ----------------
    def statement(self):
        tok = self.peek()

        if tok.type == "LET":
            return self.let_stmt()
        if tok.type == "PRINT":
            return self.print_stmt()
        if tok.type == "IF":
            return self.if_stmt()
        if tok.type == "WHILE":
            return self.while_stmt()
        if tok.type == "FUNC":
            return self.func_def()
        if tok.type == "RETURN":
            return self.return_stmt()
        if tok.type == "IDENT" and self.peek(1).type == "ASSIGN":
            return self.assign_stmt()

        expr = self.expression()
        return A.ExprStmt(expr)

    def block(self):
        self.expect("LBRACE", "'{{'")
        statements = []
        self.skip_semi()
        while not self.check("RBRACE") and not self.check("EOF"):
            statements.append(self.statement())
            self.skip_semi()
        self.expect("RBRACE", "'}}'")
        return statements

    def _optional_prompt(self):
        if (self.check("SEMI") or self.check("RBRACE") or self.check("EOF")
                or self.is_stmt_start()):
            return None
        return self.expression()

    def let_stmt(self):
        line = self.peek().line
        self.expect("LET")
        name_tok = self.expect("IDENT", "nama variabel")
        self.expect("ASSIGN", "'==='")
        if self.check("INPUT"):
            self.advance()
            prompt = self._optional_prompt()
            return A.InputStmt(name_tok.value, prompt, line)
        expr = self.expression()
        return A.LetStmt(name_tok.value, expr, line)

    def assign_stmt(self):
        name_tok = self.expect("IDENT")
        line = name_tok.line
        self.expect("ASSIGN", "'==='")
        if self.check("INPUT"):
            self.advance()
            prompt = self._optional_prompt()
            return A.InputStmt(name_tok.value, prompt, line)
        expr = self.expression()
        return A.AssignStmt(name_tok.value, expr, line)

    def print_stmt(self):
        line = self.peek().line
        self.expect("PRINT")
        exprs = [self.expression()]
        while self.match("COMMA"):
            exprs.append(self.expression())
        return A.PrintStmt(exprs, line)

    def if_stmt(self):
        line = self.peek().line
        self.expect("IF")
        self.expect("LPAREN", "'(('")
        cond = self.expression()
        self.expect("RPAREN", "'))'")
        then_body = self.block()
        else_body = None
        if self.match("ELSE"):
            else_body = self.block()
        return A.IfStmt(cond, then_body, else_body, line)

    def while_stmt(self):
        line = self.peek().line
        self.expect("WHILE")
        self.expect("LPAREN", "'(('")
        cond = self.expression()
        self.expect("RPAREN", "'))'")
        body = self.block()
        return A.WhileStmt(cond, body, line)

    def func_def(self):
        line = self.peek().line
        self.expect("FUNC")
        name_tok = self.expect("IDENT", "nama fungsi")
        self.expect("LPAREN", "'(('")
        params = []
        if not self.check("RPAREN"):
            params.append(self.expect("IDENT", "nama parameter").value)
            while self.match("COMMA"):
                params.append(self.expect("IDENT", "nama parameter").value)
        self.expect("RPAREN", "'))'")
        body = self.block()
        return A.FuncDef(name_tok.value, params, body, line)

    def return_stmt(self):
        line = self.peek().line
        self.expect("RETURN")
        expr = None
        if not (self.check("SEMI") or self.check("RBRACE") or self.check("EOF")):
            expr = self.expression()
        return A.ReturnStmt(expr, line)

    # ---------------- expressions ----------------
    def expression(self):
        return self.logic_or()

    def logic_or(self):
        left = self.logic_and()
        while self.check("OR"):
            self.advance()
            right = self.logic_and()
            left = A.BinOp("OR", left, right)
        return left

    def logic_and(self):
        left = self.equality()
        while self.check("AND"):
            self.advance()
            right = self.equality()
            left = A.BinOp("AND", left, right)
        return left

    def equality(self):
        left = self.comparison()
        while self.peek().type in ("EQ", "NEQ"):
            op = self.advance().type
            right = self.comparison()
            left = A.BinOp(op, left, right)
        return left

    def comparison(self):
        left = self.term()
        while self.peek().type in ("GT", "LT", "GE", "LE"):
            op = self.advance().type
            right = self.term()
            left = A.BinOp(op, left, right)
        return left

    def term(self):
        left = self.factor()
        while self.peek().type in ("PLUS", "MINUS"):
            op = self.advance().type
            right = self.factor()
            left = A.BinOp(op, left, right)
        return left

    def factor(self):
        left = self.unary()
        while self.peek().type in ("MUL", "DIV", "MOD"):
            op = self.advance().type
            right = self.unary()
            left = A.BinOp(op, left, right)
        return left

    def unary(self):
        if self.peek().type in ("NOT", "MINUS"):
            op = self.advance().type
            operand = self.unary()
            return A.UnaryOp(op, operand)
        return self.call_expr()

    def call_expr(self):
        expr = self.primary()
        while self.check("LPAREN"):
            line = self.peek().line
            self.advance()
            args = []
            if not self.check("RPAREN"):
                args.append(self.expression())
                while self.match("COMMA"):
                    args.append(self.expression())
            self.expect("RPAREN", "'))'")
            if not isinstance(expr, A.Identifier):
                raise ParserError(
                    "Hanya identifier yang bisa dipanggil sebagai fungsi",
                    line, self.peek().col,
                )
            expr = A.Call(expr.name, args, line)
        return expr

    def primary(self):
        tok = self.peek()
        if tok.type == "NUMBER":
            self.advance()
            return A.NumberLiteral(tok.value)
        if tok.type == "STRING":
            self.advance()
            return A.StringLiteral(tok.value)
        if tok.type == "IDENT":
            self.advance()
            return A.Identifier(tok.value)
        if tok.type == "LPAREN":
            self.advance()
            expr = self.expression()
            self.expect("RPAREN", "'))'")
            return expr
        raise ParserError(
            f"Ekspresi tidak valid, menemukan {tok.type} ({tok.value!r})",
            tok.line, tok.col,
        )


def parse(tokens):
    """Helper: parse list token menjadi Program."""
    return Parser(tokens).parse()
