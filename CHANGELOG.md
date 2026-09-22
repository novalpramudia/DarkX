# Changelog

Semua perubahan penting pada proyek DarkX akan dicatat di file ini.

Format mengikuti [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
dan proyek ini mengikuti [Semantic Versioning](https://semver.org/lang/id/)
setelah rilis `1.0.0` (sebelum itu, versi `0.x.y` dapat berisi perubahan
yang belum backward-compatible).

## [Unreleased]

### Added
- `.github/ISSUE_TEMPLATE/bug_report.md` — template laporan bug
- `.github/ISSUE_TEMPLATE/feature_request.md` — template usulan fitur
- `.github/ISSUE_TEMPLATE/config.yml` — konfigurasi issue template chooser
- `.github/pull_request_template.md` — checklist PR (test, example,
  README/grammar, CHANGELOG, konsistensi filosofi simbol ASCII)
- `SECURITY.md` — kebijakan keamanan dan cara melaporkan kerentanan

## [0.1.0] - 2026-09-22

Rilis awal DarkX.

### Added
- **Lexer** (`src/lexer.py`) — tokenizer berbasis simbol ASCII dengan
  aturan longest-match-first untuk menghindari ambiguitas antar simbol
  (mis. `:::` vs `::`, `<=?` vs `<=`)
- **Parser** (`src/parser.py`) — recursive-descent parser dengan
  precedence climbing untuk ekspresi (logic → equality → comparison →
  term → factor → unary → call → primary)
- **AST** (`src/ast.py`) — definisi node: `Program`, `LetStmt`,
  `AssignStmt`, `PrintStmt`, `InputStmt`, `IfStmt`, `WhileStmt`,
  `FuncDef`, `ReturnStmt`, `ExprStmt`, `BinOp`, `UnaryOp`, `Call`,
  `Identifier`, `NumberLiteral`, `StringLiteral`
- **Interpreter** (`src/interpreter.py`) — tree-walking interpreter
  dengan environment ber-scope (mendukung closure), penanganan error
  runtime dengan pesan jelas + nomor baris
- **CLI** (`src/main.py`, `darkx.py`) — menjalankan file `.dx` lewat
  `python -m src.main <file>.dx`
- Dukungan bahasa: variabel (`:::`/`===`), string (dengan escape
  `\n \t \" \\`), number (int & float), operator aritmatika
  (`+++ --- ** // %%`), operator perbandingan (`=? !? >? <? >=? <=?`),
  operator logika (`&& || !!`), percabangan (`::`/`??`), perulangan
  (`~~`), fungsi + rekursi + closure (`=>`/`<=`), input dari stdin (`<<<`)
- 6 contoh program: `hello.dx`, `variables.dx`, `conditional.dx`,
  `loop.dx`, `function.dx`, `error_handling.dx`
- 28 unit test (`tests/test_lexer.py`, `test_parser.py`,
  `test_interpreter.py`) — semua pass
- VS Code extension (`editors/vscode-darkx/`) — syntax highlighting
  `.dx` via TextMate grammar, auto-closing pairs untuk `{{ }}` dan
  `(( ))`, comment toggle `##`
- `README.md` — grammar EBNF lengkap, tabel simbol, contoh program,
  panduan testing dan pengembangan, status project/version/license/
  repository, status GitHub Linguist (jujur — belum resmi didukung)
- `.gitignore` — Python + Node/VS Code extension
- `LICENSE` — MIT License
- `CONTRIBUTING.md` — panduan kontribusi lengkap
- `CHANGELOG.md` — file ini
- `.github/workflows/ci.yml` — GitHub Actions CI (matrix Python
  3.9–3.12: test suite + validasi semua example + validasi grammar JSON)
- Metadata `repository`, `bugs`, `homepage`, `keywords`, `license` di
  `editors/vscode-darkx/package.json`
- CI status badge di `README.md`

### Fixed
- `editors/vscode-darkx/package.json`: menghapus referensi `icon.png`
  yang tidak memiliki file fisik (menyebabkan `vsce package` gagal)

[Unreleased]: https://github.com/novalpramudia/DarkX/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/novalpramudia/DarkX/releases/tag/v0.1.0
