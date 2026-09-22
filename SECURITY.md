# Security Policy

## Cakupan

DarkX adalah **interpreter bahasa pemrograman yang berjalan lokal**
(tidak ada komponen jaringan, server, atau eksekusi kode jarak jauh).
Permukaan risiko keamanannya jauh lebih kecil dibanding aplikasi
web/server pada umumnya, tapi tetap ada beberapa hal yang relevan:

- **Interpreter** (`src/`) — mengeksekusi file `.dx` yang diberikan
  pengguna. Interpreter dijalankan dengan privilege proses Python biasa
  (tidak ada sandboxing bawaan), jadi menjalankan file `.dx` dari sumber
  yang tidak dipercaya punya risiko yang sama seperti menjalankan skrip
  apa pun yang tidak dipercaya — perlakukan file `.dx` seperti Anda
  memperlakukan skrip Python asing.
- **VS Code extension** (`editors/vscode-darkx/`) — hanya melakukan
  syntax highlighting statis (TextMate grammar), tidak menjalankan
  kode `.dx` apa pun.

## Versi yang Didukung

| Versi | Didukung |
|---|---|
| `0.1.x` (terbaru) | ✅ |
| < `0.1.0` | ❌ (belum ada rilis sebelumnya) |

Selama DarkX masih pre-1.0, hanya rilis terbaru yang menerima
perbaikan keamanan.

## Melaporkan Kerentanan

Jika Anda menemukan masalah keamanan pada DarkX — misalnya:

- Input `.dx` tertentu yang menyebabkan interpreter melakukan sesuatu
  di luar dugaan (mis. infinite loop yang menghabiskan resource,
  crash yang tidak terduga di luar `DarkXRuntimeError` yang terkontrol)
- Kerentanan pada VS Code extension

**Mohon jangan buka Issue publik untuk kerentanan keamanan.** Sebagai
gantinya:

1. Gunakan fitur **[GitHub Security Advisories](https://github.com/novalpramudia/DarkX/security/advisories/new)**
   pada repository ini untuk melaporkan secara privat, **atau**
2. Hubungi maintainer langsung melalui profil GitHub
   [@novalpramudia](https://github.com/novalpramudia)

Sertakan sebanyak mungkin detail: langkah reproduksi, potongan kode
`.dx` yang memicu masalah, versi Python, dan dampak yang Anda amati.

## Ekspektasi Respons

Karena ini proyek open-source yang dikelola secara personal/komunitas
(bukan tim keamanan berdedikasi), tidak ada SLA formal. Laporan akan
ditinjau sesegera mungkin, dan perbaikan akan dirilis lewat versi patch
begitu tervalidasi.

## Bukan Kerentanan Keamanan

Untuk kejelasan, hal-hal berikut **diharapkan/by design**, bukan bug
keamanan:

- Kode `.dx` yang error menghasilkan `[Lexer Error]` / `[Parser Error]` /
  `[Runtime Error]` dengan pesan jelas — ini perilaku normal
  (lihat bagian *Error Handling* di `README.md`)
- Interpreter tidak melakukan sandboxing terhadap file `.dx` yang
  dijalankan — sama seperti menjalankan skrip Python biasa, tanggung
  jawab ada pada pengguna untuk hanya menjalankan file dari sumber
  yang dipercaya
