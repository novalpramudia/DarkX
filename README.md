# DarkX
# DarkX

[![VS Code Marketplace](https://img.shields.io/badge/VS%20Code-DarkX%20Support-blue?logo=visualstudiocode)](https://marketplace.visualstudio.com/items?itemName=novalpramudia.darkx-lang)

**Status:** Experimental / Pre-1.0 (active development)
**Version:** `0.1.0`
**License:** [MIT](LICENSE)
**Repository:** [github.com/novalpramudia/DarkX](https://github.com/novalpramudia/DarkX)

**DarkX** adalah bahasa pemrograman esoterik-simbolik: seluruh keyword
(`let`, `if`, `else`, `while`, `function`, `return`, `print`, dst) diganti
dengan kombinasi simbol ASCII. Tidak ada satupun keyword berbasis huruf di
grammar-nya — semuanya `>>>`, `<<<`, `:::`, `===`, `+++`, `::`, `??`, `~~`,
`=>`, `<=`, dan sejenisnya.

File DarkX berekstensi **`.dx`**.

```text
>>> "Hello World" ;;
```

adalah program DarkX yang valid dan bisa langsung dijalankan.

## Kenapa DarkX terlihat begini?

Setiap "kata kunci" sengaja dibuat dari simbol berulang atau berpasangan,
supaya kode DarkX secara visual didominasi simbol, bukan huruf:

```text
::: nama === "DarkX" ;;
>>> "Halo, " +++ nama +++ "!" ;;
```

## Instalasi & Menjalankan

Butuh Python 3.8+, tanpa dependency eksternal untuk interpreter-nya.

```bash
cd darkx
python -m src.main examples/hello.dx
# atau
./darkx.py examples/hello.dx
```

Output:

```text
Hello World
```

## Struktur Proyek

```text
darkx/
├── README.md
├── darkx.py              # runner tingkat atas (opsional, memanggil src.main)
├── examples/              # contoh program .dx
│   ├── hello.dx
│   ├── variables.dx
│   ├── conditional.dx
│   ├── loop.dx
│   ├── function.dx
│   └── error_handling.dx
├── src/
│   ├── __init__.py
│   ├── lexer.py           # source -> token
│   ├── parser.py          # token -> AST
│   ├── ast.py              # definisi node AST
│   ├── interpreter.py     # tree-walking interpreter
│   └── main.py             # CLI entry point
├── tests/
│   ├── test_lexer.py
│   ├── test_parser.py
│   └── test_interpreter.py
└── editors/
    └── vscode-darkx/       # VS Code extension (syntax highlighting)
```

## Tabel Simbol (Grammar Reference)

| Simbol | Nama Token | Arti                                   |
|--------|-----------|-----------------------------------------|
| `:::`  | LET        | Deklarasi variabel                      |
| `===`  | ASSIGN     | Operator penugasan (`=`)                |
| `>>>`  | PRINT      | Cetak ke layar                          |
| `<<<`  | INPUT      | Baca dari input (stdin)                 |
| `+++`  | PLUS       | Penjumlahan / penggabungan string       |
| `---`  | MINUS      | Pengurangan / negasi unary              |
| `**`   | MUL        | Perkalian                               |
| `//`   | DIV        | Pembagian                               |
| `%%`   | MOD        | Modulo (sisa bagi)                      |
| `::`   | IF         | Percabangan `if`                        |
| `??`   | ELSE       | Percabangan `else`                      |
| `~~`   | WHILE      | Perulangan `while`                      |
| `=>`   | FUNC       | Definisi fungsi                         |
| `<=`   | RETURN     | Mengembalikan nilai dari fungsi         |
| `{{` `}}` | LBRACE/RBRACE | Pembuka/penutup blok kode          |
| `((` `))` | LPAREN/RPAREN | Grup ekspresi, parameter, argumen  |
| `,,`   | COMMA      | Pemisah argumen/parameter/nilai print   |
| `;;`   | SEMI       | Akhir statement (opsional)              |
| `##`   | COMMENT    | Komentar satu baris                     |
| `=?`   | EQ         | Sama dengan (perbandingan)              |
| `!?`   | NEQ        | Tidak sama dengan                       |
| `>?`   | GT         | Lebih besar                             |
| `<?`   | LT         | Lebih kecil                             |
| `>=?`  | GE         | Lebih besar atau sama dengan            |
| `<=?`  | LE         | Lebih kecil atau sama dengan            |
| `&&`   | AND        | Logika DAN                              |
| `\|\|` | OR         | Logika ATAU                             |
| `!!`   | NOT        | Negasi logika                           |

> Aturan lexer: simbol yang lebih panjang selalu dicoba lebih dulu, jadi
> `:::` tidak pernah salah dibaca sebagai `::` + `:`, dan `<=?` tidak
> pernah salah dibaca sebagai `<=` + `?`.

## Grammar (EBNF)

```text
program     := statement*
block       := '{{' statement* '}}'

statement   := let_stmt | assign_stmt | print_stmt | if_stmt
             | while_stmt | func_def | return_stmt | expr_stmt

let_stmt    := ':::' IDENT '===' ( '<<<' expression? | expression ) ';;'?
assign_stmt := IDENT '===' ( '<<<' expression? | expression ) ';;'?
print_stmt  := '>>>' expression (',,' expression)* ';;'?
if_stmt     := '::' '((' expression '))' block ('??' block)?
while_stmt  := '~~' '((' expression '))' block
func_def    := '=>' IDENT '((' (IDENT (',,' IDENT)*)? '))' block
return_stmt := '<=' expression? ';;'?
expr_stmt   := expression ';;'?

expression  := logic_or
logic_or    := logic_and ('||' logic_and)*
logic_and   := equality ('&&' equality)*
equality    := comparison (('=?' | '!?') comparison)*
comparison  := term (('>?' | '<?' | '>=?' | '<=?') term)*
term        := factor (('+++' | '---') factor)*
factor      := unary (('**' | '//' | '%%') unary)*
unary       := ('!!' | '---') unary | call
call        := primary ( '((' (expression (',,' expression)*)? '))' )*
primary     := NUMBER | STRING | IDENT | '((' expression '))'
```

Grammar ini sengaja dibuat mudah dikembangkan: menambah operator baru cukup
menambah satu baris di `SYMBOL_TABLE` (lexer.py), satu level presedensi
baru di parser.py, dan satu handler baru di interpreter.py.

## Contoh Program

### Hello World (`examples/hello.dx`)

```text
>>> "Hello World" ;;
```

### Variabel & Operator (`examples/variables.dx`)

```text
::: nama === "DarkX" ;;
::: a === 10 ;;
::: b === 3 ;;
>>> "a +++ b ===" ,, a +++ b ;;
```

### Percabangan (`examples/conditional.dx`)

```text
::: umur === 20 ;;
:: ((umur >=? 18)) {{
    >>> "Status: Dewasa" ;;
}} ?? {{
    >>> "Status: Anak-anak" ;;
}}
```

### Perulangan (`examples/loop.dx`)

```text
::: i === 1 ;;
~~ ((i <=? 5)) {{
    >>> "Hitungan:" ,, i ;;
    i === i +++ 1 ;;
}}
```

### Fungsi & Rekursi (`examples/function.dx`)

```text
=> fib((n)) {{
    :: ((n <=? 1)) {{
        <= n ;;
    }}
    <= fib((n --- 1)) +++ fib((n --- 2)) ;;
}}

>>> fib((10)) ;;
```

### Input dari pengguna

```text
::: nama === <<< "Siapa nama kamu? " ;;
>>> "Halo, " +++ nama ;;
```

### Error Handling

DarkX tidak (belum) punya blok try/catch bawaan. Filosofinya: interpreter
selalu menghentikan eksekusi dengan pesan error yang jelas + nomor baris
begitu terjadi kondisi tidak valid (variabel tak dikenal, pembagian
dengan nol, tipe data tidak cocok, jumlah argumen fungsi salah, dst),
sehingga program yang berjalan tidak pernah diam-diam menghasilkan nilai
yang salah.

```text
::: hasil === 10 // 0 ;;
```

menghasilkan:

```text
[Runtime Error] Pembagian dengan nol
```

Pola yang direkomendasikan untuk error handling "manual" adalah mengecek
kondisi terlebih dahulu (lihat `examples/error_handling.dx`):

```text
=> bagiAman((a,, b)) {{
    :: ((b =? 0)) {{
        >>> "Error: tidak bisa membagi dengan nol!" ;;
        <= 0 ;;
    }}
    <= a // b ;;
}}
```

## Testing

```bash
cd darkx
pip install pytest
python -m pytest tests/ -v
```

28 test mencakup lexer (tokenisasi, ambiguitas simbol, error karakter
tidak dikenal), parser (AST, presedensi operator, error sintaks), dan
interpreter (aritmatika, string, kondisional, loop, fungsi rekursif,
closure, input, dan error runtime).

## Konsep Bahasa

- **Variable**: `:::` untuk deklarasi, `===` untuk assignment/re-assign.
  Re-assign ke variabel yang belum dideklarasikan akan menghasilkan error.
- **String**: literal diapit `"..."`, mendukung escape `\n`, `\t`, `\"`, `\\`.
  `+++` pada string melakukan penggabungan (concatenation).
- **Number**: integer dan float (`10`, `3.14`).
- **Operator**: aritmatika (`+++ --- ** // %%`), perbandingan
  (`=? !? >? <? >=? <=?`), logika (`&& || !!`).
- **Conditional**: `::` (if) / `??` (else), bisa dirangkai (`else if`)
  dengan menulis `::` baru di dalam blok `??`.
- **Loop**: `~~` (while).
- **Function**: `=>` untuk mendefinisikan, mendukung parameter, rekursi,
  dan closure (fungsi meng-capture environment tempat ia didefinisikan).
- **Return**: `<=`, boleh tanpa nilai (mengembalikan `null`).
- **Error handling**: semua error (lexer/parser/runtime) berupa exception
  Python (`LexerError`, `ParserError`, `DarkXRuntimeError`) dengan pesan
  dan nomor baris yang jelas, ditangkap rapi oleh `src/main.py` dan
  ditampilkan ke stderr dengan exit code 1.

## GitHub Linguist Status

`.dx` **belum** merupakan bahasa yang dikenal secara resmi oleh GitHub
Linguist (jadi GitHub.com belum otomatis menampilkan file `.dx` sebagai
"DarkX" di language bar repo manapun).

Yang **sudah** dilakukan/diverifikasi:
- Konfigurasi bahasa (`languages.yml` entry, extension `.dx`, `tm_scope`)
  sudah divalidasi berhasil di-parse oleh `github-linguist` versi lokal
  hasil compile sendiri (`script/update-ids` + `bundle exec rake compile`
  + `github-linguist <file>.dx` → melaporkan `language: DarkX`). Ini
  membuktikan konfigurasi **valid secara teknis**.

Yang **belum** dilakukan:
- Pull request ke [`github-linguist/linguist`](https://github.com/github-linguist/linguist)
  upstream belum diajukan, dan belum akan diajukan sampai syarat
  pemakaian nyata di bawah ini realistis untuk dipenuhi.

Kenapa belum diajukan: berdasarkan `CONTRIBUTING.md` resmi mereka,
Linguist mensyaratkan bukti pemakaian nyata dalam skala besar sebelum
menerima bahasa baru — minimal **≥ 2.000 file** dengan ekstensi terkait
yang terindeks GitHub Search dalam setahun terakhir (di luar fork), dan
tersebar di banyak repository berbeda (bukan didominasi satu repo/user).
Mereka eksplisit menyatakan tidak menerima PR untuk *"very new or hobby
languages"*. Contoh "Hello World"/tutorial juga tidak diterima sebagai
sample resmi di `samples/` mereka.

➡️ **Local override** (opsional, hanya berlaku untuk repo Anda sendiri,
tidak mengubah apa pun secara global di GitHub) bisa ditambahkan lewat
`.gitattributes` di root repo:

```
*.dx linguist-language=Python
```

Status ini akan diperbarui begitu DarkX punya adopsi nyata yang cukup
untuk mengajukan PR resmi ke upstream Linguist.

## VS Code Extension

Lihat `editors/vscode-darkx/` untuk extension syntax highlighting `.dx`.
Cara instal cepat (local):

```bash
cd editors/vscode-darkx
npm install -g @vscode/vsce   # sekali saja
vsce package
code --install-extension darkx-lang-0.1.0.vsix
```

Atau untuk development: buka folder `editors/vscode-darkx` di VS Code lalu
tekan `F5` untuk membuka **Extension Development Host**.

## Repository Information

- **Repository:** [https://github.com/novalpramudia/DarkX](https://github.com/novalpramudia/DarkX)
- **Clone:**
  ```bash
  git clone https://github.com/novalpramudia/DarkX.git
  cd DarkX
  ```
- **Issues / bug report:** [github.com/novalpramudia/DarkX/issues](https://github.com/novalpramudia/DarkX/issues)

## Contribution

Kontribusi (bug report, contoh `.dx` baru, penambahan operator/statement,
perbaikan VS Code extension) sangat diterima. Lihat bagian
[Roadmap / Cara Mengembangkan](#roadmap--cara-mengembangkan) di bawah
untuk pola menambah fitur baru. Panduan kontribusi lebih lengkap akan
ditambahkan di `CONTRIBUTING.md`.

## License

DarkX dilisensikan di bawah **[MIT License](LICENSE)** — bebas dipakai,
dimodifikasi, dan didistribusikan ulang (termasuk untuk proyek
closed-source), selama notice copyright & lisensi disertakan.

Copyright (c) 2026 Noval Pramudia.

## Roadmap / Cara Mengembangkan

Grammar DarkX dirancang supaya mudah ditambah:

1. **Operator baru** → tambah entry di `SYMBOL_TABLE` (`src/lexer.py`).
2. **Statement baru** → tambah method `xxx_stmt()` di `Parser`
   (`src/parser.py`) + node baru di `src/ast.py` + handler
   `exec_XxxStmt` di `Interpreter` (`src/interpreter.py`).
3. **Fungsi bawaan (builtin)** → cukup `env.define("nama", fungsi_python)`
   di `Interpreter.__init__` / `run`, karena `eval_Call` sudah mendukung
   pemanggilan objek Python `callable`.

Ide pengembangan lanjutan: array/list, dictionary, `elif` native,
`break`/`continue`, modul/import antar file `.dx`, try/catch native
(`??:` misalnya), standard library builtin (math, string utils).
