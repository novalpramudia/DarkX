# Contributing to DarkX

Terima kasih sudah tertarik berkontribusi ke **DarkX** 🎉 — bahasa
pemrograman esoterik-simbolik dengan interpreter Python dan syntax
highlighting VS Code.

Dokumen ini menjelaskan cara setup environment, menjalankan test, dan
alur menambah fitur baru **tanpa merusak konsistensi grammar** yang
sudah ada.

## Daftar Isi

- [Kode Etik](#kode-etik)
- [Setup Environment](#setup-environment)
- [Menjalankan Test & Example](#menjalankan-test--example)
- [Struktur Proyek](#struktur-proyek)
- [Cara Melaporkan Bug](#cara-melaporkan-bug)
- [Cara Mengusulkan Fitur / Operator Baru](#cara-mengusulkan-fitur--operator-baru)
- [Alur Menambah Fitur ke Bahasa](#alur-menambah-fitur-ke-bahasa)
- [Menambah/Mengubah Contoh `.dx`](#menambahmengubah-contoh-dx)
- [Berkontribusi ke VS Code Extension](#berkontribusi-ke-vs-code-extension)
- [Gaya Commit & Pull Request](#gaya-commit--pull-request)

## Kode Etik

Bersikaplah sopan dan konstruktif. Proyek ini masih tahap awal
(pre-1.0), jadi diskusi terbuka soal desain grammar sangat disambut —
tapi perubahan yang mengubah *filosofi inti* DarkX (syntax berbasis
simbol ASCII, bukan keyword huruf) sebaiknya didiskusikan lewat Issue
dulu sebelum membuat PR besar.

## Setup Environment

Prasyarat: **Python 3.8+**. Interpreter DarkX tidak punya dependency
eksternal; hanya `pytest` yang dibutuhkan untuk testing.

```bash
git clone https://github.com/novalpramudia/DarkX.git
cd DarkX
pip install pytest
```

Tidak perlu virtual environment khusus, tapi disarankan:

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install pytest
```

## Menjalankan Test & Example

Sebelum membuka PR, pastikan semua test dan example tetap lulus:

```bash
# Jalankan seluruh test suite
python -m pytest tests/ -v

# Jalankan setiap contoh .dx secara manual
python -m src.main examples/hello.dx
python -m src.main examples/variables.dx
python -m src.main examples/conditional.dx
python -m src.main examples/loop.dx
python -m src.main examples/function.dx
python -m src.main examples/error_handling.dx
```

Semua harus keluar dengan **exit code 0** dan tanpa traceback yang tidak
disengaja.

## Struktur Proyek

```
darkx/
├── src/
│   ├── lexer.py         # source .dx -> token
│   ├── parser.py        # token -> AST (recursive descent)
│   ├── ast.py            # definisi node AST
│   ├── interpreter.py   # tree-walking interpreter
│   └── main.py            # CLI entry point
├── examples/              # contoh program .dx
├── tests/                 # test lexer/parser/interpreter (pytest)
└── editors/vscode-darkx/  # VS Code extension (syntax highlighting)
```

## Cara Melaporkan Bug

Saat membuka Issue untuk bug pada lexer/parser/interpreter, sertakan:

1. **Potongan kode `.dx`** yang memicu bug (sekecil mungkin, reproducible)
2. **Output/error yang didapat** (termasuk pesan `[Lexer Error]`,
   `[Parser Error]`, atau `[Runtime Error]` lengkap dengan nomor baris)
3. **Output yang diharapkan**
4. Versi Python yang dipakai (`python --version`)

Untuk bug pada VS Code extension (highlighting salah warna/scope),
sertakan screenshot atau cuplikan `.dx` yang bermasalah.

## Cara Mengusulkan Fitur / Operator Baru

DarkX sengaja dirancang **hanya menggunakan simbol ASCII**, bukan
keyword huruf (`if`, `print`, `function`, dst). Sebelum mengusulkan
fitur baru:

1. Cek dulu apakah simbol yang ingin dipakai **belum bentrok** dengan
   simbol lain di tabel `SYMBOL_TABLE` (`src/lexer.py`) atau README.
2. Buka Issue dulu untuk diskusi desain sebelum menulis kode — terutama
   kalau fitur tersebut menambah simbol baru ke grammar inti.
3. Fitur yang **tidak** butuh diskusi desain besar (aman untuk langsung
   PR): builtin function baru (mis. fungsi Python yang di-`env.define`),
   perbaikan pesan error, penambahan test, contoh `.dx` baru.

## Alur Menambah Fitur ke Bahasa

Grammar DarkX dirancang supaya mudah dikembangkan secara konsisten:

1. **Operator baru** → tambah entry di `SYMBOL_TABLE` (`src/lexer.py`).
   Ingat: **urutan penting** — simbol yang lebih panjang harus dicek
   lebih dulu supaya tidak bentrok dengan prefix simbol lain (contoh:
   `:::` harus dicek sebelum `::`, `<=?` sebelum `<=`).
2. **Statement baru** → tambah method `xxx_stmt()` di `Parser`
   (`src/parser.py`) + node baru di `src/ast.py` + handler
   `exec_XxxStmt` di `Interpreter` (`src/interpreter.py`).
3. **Fungsi bawaan (builtin)** → cukup
   `env.define("nama", fungsi_python)` — `eval_Call` di interpreter
   sudah mendukung pemanggilan objek Python `callable` secara langsung.
4. **Tambahkan test** di `tests/test_lexer.py`, `test_parser.py`, dan/atau
   `test_interpreter.py` yang mencakup fitur baru tersebut — termasuk
   test negatif (kasus error) kalau relevan.
5. **Update README.md** — tabel simbol dan grammar EBNF harus tetap
   sinkron dengan implementasi.
6. Jika fitur menambah simbol yang bisa dipakai di editor, pertimbangkan
   apakah `editors/vscode-darkx/syntaxes/darkx.tmLanguage.json` perlu
   diperbarui juga (lihat bagian di bawah).

## Menambah/Mengubah Contoh `.dx`

Contoh di `examples/` sebaiknya:

- Berjalan tanpa error (`python -m src.main examples/nama.dx` exit code 0)
- Mendemonstrasikan satu konsep dengan jelas (jangan mencampur terlalu
  banyak fitur dalam satu file, kecuali memang file "showcase")
- Diberi komentar (`##`) yang menjelaskan apa yang didemonstrasikan

## Berkontribusi ke VS Code Extension

Kode extension ada di `editors/vscode-darkx/`. Untuk development lokal:

```bash
cd editors/vscode-darkx
code .
# tekan F5 di VS Code untuk membuka Extension Development Host
```

Kalau mengubah `syntaxes/darkx.tmLanguage.json`, validasi dulu bahwa
file tetap JSON valid:

```bash
python -c "import json; json.load(open('syntaxes/darkx.tmLanguage.json'))"
```

Perhatikan **urutan pattern** di `tmLanguage.json` — sama seperti lexer,
pattern untuk token yang lebih panjang/spesifik (mis. `:::`) harus
diletakkan sebelum pattern yang lebih pendek/umum (mis. `::`) supaya
highlighting tidak salah.

## Gaya Commit & Pull Request

- Pesan commit singkat dan deskriptif, contoh:
  `fix(lexer): urutan token <=? sebelum <=`,
  `feat(interpreter): tambah builtin function len()`,
  `docs(readme): perbarui tabel simbol`
- Satu PR sebaiknya fokus pada satu perubahan logis
- Sertakan hasil `python -m pytest tests/ -v` di deskripsi PR (atau
  biarkan GitHub Actions CI yang memverifikasi otomatis)
- Untuk perubahan pada grammar/syntax inti, jelaskan alasan desainnya
  di deskripsi PR, bukan hanya "apa" yang berubah

Terima kasih sudah membantu mengembangkan DarkX! 🚀
