"""
DarkX Lexer
================
Mengubah source code .dx (teks mentah) menjadi deretan Token.

DarkX tidak memakai keyword berbasis huruf (print, if, while, dst).
Semua "kata kunci" adalah kombinasi simbol ASCII. Tabel lengkap ada
di README.md, ringkasannya:

    :::   LET        deklarasi variabel
    ===   ASSIGN      operator "="
    >>>   PRINT       cetak ke layar
    <<<   INPUT       baca dari input
    +++   PLUS
    ---   MINUS
    **    MUL
    //    DIV
    %%    MOD
    ::    IF
    ??    ELSE
    ~~    WHILE
    =>    FUNC        definisi fungsi
    <=    RETURN
    {{ }} LBRACE/RBRACE  blok kode
    (( )) LPAREN/RPAREN  grup ekspresi / parameter / argumen
    ,,    COMMA
    ;;    SEMI        akhir statement (opsional)
    ##    COMMENT     komentar sampai akhir baris
    =?    EQ          perbandingan sama dengan
    !?    NEQ         tidak sama dengan
    >?    GT
    <?    LT
    >=?   GE
    <=?   LE
    &&    AND
    ||    OR
    !!    NOT
"""

import re


class Token:
    __slots__ = ("type", "value", "line", "col")

    def __init__(self, type_, value, line, col):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, L{self.line}:C{self.col})"


class LexerError(Exception):
    def __init__(self, message, line, col):
        super().__init__(f"[Lexer Error] Baris {line}, Kolom {col}: {message}")
        self.line = line
        self.col = col


# Urutan SANGAT penting: simbol yang lebih panjang harus dicek lebih dulu,
# supaya ':::' tidak salah dibaca sebagai '::' + ':' dan '<=?' tidak salah
# dibaca sebagai '<=' + '?'.
SYMBOL_TABLE = [
    # --- 3 karakter ---
    (":::", "LET"),
    ("===", "ASSIGN"),
    (">>>", "PRINT"),
    ("<<<", "INPUT"),
    ("+++", "PLUS"),
    ("---", "MINUS"),
    ("<=?", "LE"),
    (">=?", "GE"),
    # --- 2 karakter ---
    ("=>", "FUNC"),
    ("<=", "RETURN"),
    ("::", "IF"),
    ("??", "ELSE"),
    ("~~", "WHILE"),
    ("{{", "LBRACE"),
    ("}}", "RBRACE"),
    ("((", "LPAREN"),
    ("))", "RPAREN"),
    (",,", "COMMA"),
    (";;", "SEMI"),
    ("**", "MUL"),
    ("//", "DIV"),
    ("%%", "MOD"),
    ("=?", "EQ"),
    ("!?", "NEQ"),
    (">?", "GT"),
    ("<?", "LT"),
    ("&&", "AND"),
    ("||", "OR"),
    ("!!", "NOT"),
]
# Jaga-jaga: pastikan urutan selalu panjang -> pendek.
SYMBOL_TABLE.sort(key=lambda pair: -len(pair[0]))

STRING_RE = re.compile(r'"(?:[^"\\]|\\.)*"')
NUMBER_RE = re.compile(r'\d+(\.\d+)?')
IDENT_RE = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')
COMMENT_RE = re.compile(r'##[^\n]*')
WHITESPACE_RE = re.compile(r'[ \t\r]+')


def decode_string(raw_inner):
    return (
        raw_inner.replace('\\n', '\n')
                 .replace('\\t', '\t')
                 .replace('\\"', '"')
                 .replace('\\\\', '\\')
    )


def tokenize(source):
    """Ubah source code DarkX menjadi list of Token, diakhiri EOF."""
    tokens = []
    line = 1
    col = 1
    i = 0
    n = len(source)

    while i < n:
        ch = source[i]

        if ch == '\n':
            tokens.append(Token("NEWLINE", "\\n", line, col))
            i += 1
            line += 1
            col = 1
            continue

        m = WHITESPACE_RE.match(source, i)
        if m:
            length = len(m.group())
            i += length
            col += length
            continue

        m = COMMENT_RE.match(source, i)
        if m:
            length = len(m.group())
            i += length
            col += length
            continue

        m = STRING_RE.match(source, i)
        if m:
            raw = m.group()
            value = decode_string(raw[1:-1])
            tokens.append(Token("STRING", value, line, col))
            length = len(raw)
            i += length
            col += length
            continue

        m = NUMBER_RE.match(source, i)
        if m:
            raw = m.group()
            value = float(raw) if '.' in raw else int(raw)
            tokens.append(Token("NUMBER", value, line, col))
            length = len(raw)
            i += length
            col += length
            continue

        matched_symbol = False
        for symbol, ttype in SYMBOL_TABLE:
            slen = len(symbol)
            if source[i:i + slen] == symbol:
                tokens.append(Token(ttype, symbol, line, col))
                i += slen
                col += slen
                matched_symbol = True
                break
        if matched_symbol:
            continue

        m = IDENT_RE.match(source, i)
        if m:
            raw = m.group()
            tokens.append(Token("IDENT", raw, line, col))
            length = len(raw)
            i += length
            col += length
            continue

        raise LexerError(f"Karakter tidak dikenal: {ch!r}", line, col)

    tokens.append(Token("EOF", None, line, col))
    return tokens
