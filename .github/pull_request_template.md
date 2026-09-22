<!--
Terima kasih sudah berkontribusi ke DarkX! Mohon isi template ini
sebelum meminta review. Lihat CONTRIBUTING.md untuk panduan lengkap.
-->

## Deskripsi Perubahan

<!-- Jelaskan apa yang diubah dan kenapa -->

## Jenis Perubahan

- [ ] Bug fix (perubahan non-breaking yang memperbaiki masalah)
- [ ] Fitur baru (perubahan non-breaking yang menambah fungsionalitas)
- [ ] Breaking change (fix/fitur yang mengubah perilaku yang sudah ada)
- [ ] Perubahan dokumentasi
- [ ] Perubahan VS Code extension
- [ ] Lainnya: <!-- jelaskan -->

## Area yang Terdampak

- [ ] Lexer (`src/lexer.py`)
- [ ] Parser (`src/parser.py`)
- [ ] AST (`src/ast.py`)
- [ ] Interpreter (`src/interpreter.py`)
- [ ] CLI (`src/main.py` / `darkx.py`)
- [ ] Tests (`tests/`)
- [ ] Examples (`examples/`)
- [ ] VS Code extension (`editors/vscode-darkx/`)
- [ ] Dokumentasi (`README.md`, `CONTRIBUTING.md`, dll)

## Checklist Sebelum Meminta Review

- [ ] `python -m pytest tests/ -v` — semua test **pass**
- [ ] Semua file di `examples/*.dx` masih berjalan tanpa error
      (`python -m src.main examples/<file>.dx`)
- [ ] Saya sudah menambahkan/memperbarui test untuk perubahan ini
      (jika relevan)
- [ ] Saya sudah memperbarui `README.md` (tabel simbol/grammar EBNF)
      jika perubahan ini menambah/mengubah sintaks
- [ ] Saya sudah memperbarui `editors/vscode-darkx/syntaxes/darkx.tmLanguage.json`
      jika perubahan ini menambah simbol baru ke grammar
- [ ] Saya sudah menambah entry di `CHANGELOG.md` (di bawah `[Unreleased]`)
- [ ] Perubahan ini **tidak** mengubah filosofi inti DarkX (syntax
      berbasis simbol ASCII, bukan keyword huruf) tanpa diskusi Issue
      terlebih dahulu

## Bukti Pengujian

<!-- Tempel output `pytest` atau contoh input/output .dx yang relevan -->

```

```

## Issue Terkait

<!-- mis. Closes #12, Relates to #7 -->
