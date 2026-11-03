# Soal Praktik 5 - Analisis Code Smell dan Refactoring

File yang dianalisis: `soal_5_sebelum_refactoring.py`
Hasil refactoring: `soal_5_sesudah_refactoring.py`

Program contoh: perhitungan total pembayaran UKT mahasiswa
(UKT - diskon + pajak + biaya admin, lalu mencetak struk).

## Daftar Code Smell yang Ditemukan

### 1. Magic Number
- **Bukti:** angka `1000000`, `0.1`, `0.11`, `2500`, `5000`, `7500`,
  `8`, dan kode status `1` / `2` tersebar di dalam fungsi tanpa
  penjelasan artinya.
- **Masalah:** pembaca harus menebak arti setiap angka; jika tarif
  berubah, semua kemunculan angka harus diburu satu per satu dan
  rawan ada yang terlewat.
- **Refactoring:** *Replace Magic Number with Symbolic Constant* -
  semua angka diganti konstanta bernama di awal modul:
  `BATAS_UKT_DISKON`, `PERSEN_DISKON`, `TARIF_PAJAK`,
  `SEMESTER_MAKSIMUM`, `STATUS_AKTIF`, `STATUS_CUTI`, dan
  `BIAYA_ADMIN` dalam bentuk dictionary.

### 2. Duplikasi Kode (Duplicate Code)
- **Bukti:** blok rumus `diskon -> subtotal -> pajak -> total`
  ditulis ulang 6 kali (3 metode pembayaran x 2 cabang besaran UKT).
- **Masalah:** melanggar prinsip DRY; perubahan rumus harus dilakukan
  di 6 tempat, dan satu tempat yang terlewat membuat hasil antar
  metode pembayaran tidak konsisten.
- **Refactoring:** *Extract Method* - rumus dipusatkan satu kali di
  `hitung_diskon()`, `hitung_pajak()`, `biaya_admin()`, dan
  `hitung_total_pembayaran()`.

### 3. Long Method
- **Bukti:** `proses_pembayaran_ukt()` versi sebelum berisi sekitar
  60 baris yang mengerjakan validasi status, validasi semester,
  perhitungan, dan pencetakan struk sekaligus.
- **Masalah:** fungsi yang terlalu panjang sulit dibaca, sulit diuji
  per bagian, dan perubahan kecil berisiko merusak bagian lain.
- **Refactoring:** *Extract Method* - fungsi dipecah menjadi
  fungsi-fungsi kecil satu tugas: `hitung_diskon()`,
  `hitung_pajak()`, `biaya_admin()`, `hitung_total_pembayaran()`,
  `buat_struk()`, dan `format_rupiah()`. Fungsi utama tinggal
  mengorkestrasi.

### 4. Deep Nesting
- **Bukti:** `if status` > `if semester` > `if ukt` > `if metode`,
  bersarang sampai 4 tingkat sebelum logika utama tercapai.
- **Masalah:** semakin dalam sarang, semakin sulit mengikuti alur;
  kondisi gagal justru terkubur paling dalam.
- **Refactoring:** *Guard Clause* - kondisi gagal (status cuti,
  status tidak dikenal, semester berlebih) diperiksa dan
  di-`return` lebih awal, sehingga alur utama berjalan datar tanpa
  sarang.

### 5. Dead Code
- **Bukti:** fungsi `hitung_pajak_lama()` tidak pernah dipanggil,
  variabel `keterangan` tidak pernah dipakai, dan `print()` setelah
  `return` tidak akan pernah dijalankan.
- **Masalah:** kode mati membingungkan pembaca, memberi kesan masih
  dipakai, dan membebani pemeliharaan.
- **Refactoring:** *Remove Dead Code* - ketiganya dihapus seluruhnya.

## Penyesuaian Standar PEP 8 pada Versi Sesudah

- Setiap fungsi memiliki **docstring** yang menjelaskan tugas,
  parameter penting, dan exception yang mungkin muncul.
- Setiap fungsi memiliki **type hints** pada parameter dan nilai
  kembali, misalnya `def hitung_diskon(ukt: int) -> int:`.
- Konstanta ditulis `UPPER_SNAKE_CASE`, fungsi `snake_case`, dan
  panjang baris dijaga maksimal 79 karakter.

## Bukti Perilaku Tidak Berubah

Kedua versi dijalankan dengan data contoh yang sama dan menghasilkan
total yang identik:

| Contoh | Versi sebelum | Versi sesudah |
|---|---|---|
| UKT Rp5.500.000, tunai | Rp5.497.000 | Rp5.497.000 |
| UKT Rp800.000, transfer | Rp893.000 | Rp893.000 |

Artinya refactoring hanya mengubah struktur dan keterbacaan kode,
bukan hasil perhitungannya.
