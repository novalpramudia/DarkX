# DarkX Language Support (VS Code)

Extension ini memberi **syntax highlighting** untuk file `.dx` (bahasa DarkX).

## Fitur

- Highlight untuk seluruh simbol DarkX: `:::` `===` `>>>` `<<<` `+++` `---`
  `**` `//` `%%` `::` `??` `~~` `=>` `<=` `{{ }}` `(( ))` `,,` `;;` `##`
  `=?` `!?` `>?` `<?` `>=?` `<=?` `&&` `||` `!!`
- Highlight literal string (dengan escape) dan angka
- Highlight komentar `## ...`
- Highlight nama fungsi saat dipanggil (`namaFungsi((...))`)
- Auto-closing pairs untuk `{{ }}`, `(( ))`, dan `"`
- Comment toggle (`Ctrl+/`) memakai `##`

## Instalasi Lokal

```bash
npm install -g @vscode/vsce
vsce package
code --install-extension darkx-lang-0.1.0.vsix
```

## Development

Buka folder ini di VS Code, tekan `F5` untuk membuka jendela
**Extension Development Host**, lalu buka file `.dx` apa saja (misalnya
`examples/hello.dx` dari proyek DarkX utama) untuk melihat hasilnya.
