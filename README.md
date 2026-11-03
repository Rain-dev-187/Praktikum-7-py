# Praktikum Pemrograman Python - Pertemuan 7

## Exception Handling, Debugging, Logging, Unit Testing, Clean Code, dan Code Review

- **Nama:** Ahmad Sahrul F 
- **NIM:** 20241320031
- **Kelas:** A1
- **Mata Kuliah:** Pemrograman Python
- **Program Studi:** Sistem Informasi

---

# A. Jawaban Soal Teori

## 1. Perbedaan Syntax Error dan Exception

**Syntax error** adalah kesalahan penulisan kode yang dideteksi oleh
parser Python **sebelum program dijalankan**. Jika ada syntax error,
program tidak dapat berjalan sama sekali dan harus diperbaiki dulu.

Contoh syntax error:

- Kurung tutup hilang: `print("Halo"` akan memunculkan
  `SyntaxError: '(' was never closed`.
- Indentasi salah: baris di dalam blok `if` yang tidak menjorok
  dengan benar memunculkan `IndentationError`.

**Exception** adalah kesalahan yang terjadi **saat program berjalan
(runtime)**, padahal sintaks kode sudah benar. Program berhenti di
tengah jalan kecuali exception-nya ditangani dengan `try-except`.

Contoh exception:

- `hasil = 10 / 0` memunculkan `ZeroDivisionError`.
- `nilai = int("abc")` memunculkan `ValueError`.

## 2. Perbedaan Blok else dan Blok finally

- **Blok else** dijalankan **hanya jika blok try selesai tanpa
  exception**. Blok ini cocok untuk kode yang hanya boleh berjalan
  jika operasi berhasil, misalnya menampilkan ringkasan data setelah
  file berhasil dibaca seluruhnya.
- **Blok finally** dijalankan **selalu**, baik terjadi exception
  maupun tidak, bahkan jika ada `return` di dalam blok try/except.
  Blok ini cocok untuk pembersihan sumber daya (resource cleanup),
  misalnya menutup file atau koneksi database agar tidak bocor.

Singkatnya: else = "jika sukses", finally = "apa pun yang terjadi".

## 3. Mengapa Urutan Blok except Penting

Python memeriksa blok `except` dari atas ke bawah, dan blok pertama
yang cocok dengan exception yang terjadi akan dijalankan. Karena
exception membentuk hierarki, menangkap kelas induk (superclass)
otomatis menangkap semua kelas anaknya (subclass).

Jika exception yang lebih umum ditulis lebih dulu, misalnya
`except Exception` sebelum `except ValueError`, maka blok
`ValueError` **tidak akan pernah dijalankan** karena semua
`ValueError` sudah tertangkap oleh `Exception`. Akibatnya penanganan
khusus yang sudah disiapkan menjadi kode mati, dan semua error
diperlakukan sama secara umum. Aturannya: tulis exception yang
**paling spesifik dulu**, yang paling umum terakhir sebagai jaring
pengaman.

## 4. Keuntungan Hierarki Custom Exception

Keuntungan dibanding memakai exception bawaan secara langsung:

1. **Nama bermakna sesuai domain bisnis.** `NIMFormatError` jauh
   lebih jelas daripada `ValueError` yang bisa berarti apa saja.
2. **Pesan dan data konteks lebih kaya.** Custom exception dapat
   membawa atribut tambahan, misalnya NIM yang bermasalah atau sisa
   saldo, sehingga diagnosis lebih cepat.
3. **Penanganan berlapis.** Lapisan bisnis dapat menangkap exception
   yang spesifik, sedangkan lapisan presentasi cukup menangkap kelas
   dasarnya untuk menampilkan pesan umum.
4. **Stabil mengikuti bisnis, bukan teknologi.** Hierarki domain
   tidak berubah meskipun implementasi teknis (misalnya database)
   berganti.

Contoh pada Sistem Informasi Akademik:

```
SIAkademikError            (dasar semua error SI Akademik)
|-- MahasiswaError
|   |-- NIMFormatError     (format NIM tidak sesuai)
|   |-- NIMDuplikatError   (NIM sudah terdaftar)
|-- MatakuliahError
    |-- SKSMelebihiError   (pengambilan SKS melewati batas)
```

## 5. Debugging dengan Print Statement vs pdb

**Print statement** menampilkan nilai variabel dengan `print()`
pada titik tertentu.

- Kelebihan: sangat sederhana, tanpa alat tambahan, cepat untuk
  memeriksa satu-dua nilai.
- Kekurangan: kode harus diubah dan program dijalankan ulang dari
  awal setiap kali ingin memeriksa titik lain; print sisa debug
  harus dibersihkan setelah selesai.
- Tepat digunakan: program kecil dan bug sederhana yang lokasinya
  sudah kira-kira diketahui.

**pdb (Python Debugger)** adalah debugger interaktif bawaan Python.

- Kelebihan: eksekusi dapat dihentikan di breakpoint, diperiksa
  variabelnya, dijalankan baris demi baris (step over/into), dan
  dilihat call stack-nya tanpa mengubah logika program.
- Kekurangan: lebih lambat dipelajari dan berlebihan untuk bug
  sepele; tidak boleh tertinggal di kode produksi.
- Tepat digunakan: bug kompleks, bug yang muncul sesekali, atau
  program besar yang alur eksekusinya sulit diikuti hanya dengan
  membaca kode.

## 6. Lima Level Logging Standar Python

| Level | Nilai | Kegunaan | Contoh pada Sistem Informasi |
|---|---|---|---|
| DEBUG | 10 | Informasi diagnostik paling detail untuk pengembang | `Query SQL: SELECT * FROM mahasiswa WHERE nim='2024132001'` |
| INFO | 20 | Konfirmasi bahwa operasi normal berjalan baik | `User admin berhasil login dari 192.168.1.10` |
| WARNING | 30 | Belum error, tetapi berpotensi menjadi masalah | `Penggunaan disk server mencapai 85%` |
| ERROR | 40 | Terjadi error, fitur gagal, tetapi sistem masih berjalan | `Gagal mengirim notifikasi email ke dosen@univ.ac.id` |
| CRITICAL | 50 | Error fatal, sistem tidak dapat melanjutkan operasi | `Koneksi database utama terputus!` |

Hanya pesan dengan level sama atau lebih tinggi dari level yang
diatur pada logger/handler yang akan dicatat.

## 7. Perbedaan setUp dan setUpClass pada unittest

- **`setUp()`** dijalankan **sebelum setiap method test** dalam
  kelas. Cocok untuk menyiapkan data atau kondisi awal yang dipakai
  satu test dan mungkin diubah oleh test tersebut, misalnya
  menyisipkan satu baris data contoh ke database uji. Pasangannya
  `tearDown()` dijalankan setelah setiap test.
- **`setUpClass()`** adalah classmethod yang dijalankan **sekali
  saja sebelum seluruh test dalam kelas**. Cocok untuk persiapan
  mahal yang dipakai bersama dan tidak berubah antar test, misalnya
  membuat file database uji dan tabelnya. Pasangannya
  `tearDownClass()` dijalankan sekali setelah semua test selesai,
  misalnya untuk menutup koneksi dan menghapus file database uji.

Aturan praktisnya: persiapan murah dan berubah-ubah per test pakai
`setUp`; persiapan mahal dan dipakai bersama pakai `setUpClass`.

## 8. Prinsip DRY dan Contoh Refactoring-nya

DRY (*Don't Repeat Yourself*) berarti setiap pengetahuan atau logika
dalam sistem harus memiliki **satu representasi tunggal**. Kode yang
disalin-tempel di banyak tempat adalah pelanggaran DRY: jika aturan
berubah, semua salinan harus diubah, dan satu salinan yang terlewat
membuat perilaku program tidak konsisten.

Contoh pelanggaran: logika validasi NIM yang sama ditulis di dua
fungsi.

```python
def proses_pendaftaran(data):
    if not data['nim'].isdigit() or len(data['nim']) != 10:
        raise ValueError("NIM tidak valid")   # salinan 1
    # ... proses pendaftaran

def update_mahasiswa(data):
    if not data['nim'].isdigit() or len(data['nim']) != 10:
        raise ValueError("NIM tidak valid")   # salinan 2 (duplikasi)
    # ... proses update
```

Refactoring yang tepat (*Extract Method*): pusatkan validasi dalam
satu fungsi, lalu panggil dari kedua tempat.

```python
def validasi_nim(nim):
    if not nim.isdigit() or len(nim) != 10:
        raise ValueError(f"NIM '{nim}' tidak valid")

def proses_pendaftaran(data):
    validasi_nim(data['nim'])
    # ... proses pendaftaran

def update_mahasiswa(data):
    validasi_nim(data['nim'])
    # ... proses update
```

## 9. Empat Code Smell Umum dan Refactoring-nya

| Code Smell | Gejala | Teknik Refactoring |
|---|---|---|
| Long Method | Satu fungsi sangat panjang (> 20-30 baris) dan mengerjakan banyak hal | *Extract Method*: pecah menjadi fungsi-fungsi kecil satu tugas |
| Duplicate Code | Blok kode yang sama/sangat mirip muncul di beberapa tempat | *Extract Method/Class*: pusatkan menjadi satu, panggil dari semua tempat |
| Magic Number | Angka atau kode tanpa nama yang menjelaskan artinya, misalnya `if status == 3` | *Replace Magic Number with Symbolic Constant*: ganti dengan konstanta bernama, misalnya `STATUS_LULUS = 3` |
| Deep Nesting | `if` bersarang lebih dari 3 tingkat sehingga alur sulit diikuti | *Guard Clause*: periksa kondisi gagal dan `return` lebih awal agar alur utama datar |
| Dead Code | Fungsi/variabel tidak terpakai atau kode setelah `return` | *Remove Dead Code*: hapus seluruhnya |

## 10. Peran Static Analysis Tools dalam Code Review

Static analysis memeriksa kode **tanpa menjalankannya**:

- **pylint**: linting komprehensif (style, potensi error, desain)
  lengkap dengan skor kualitas kode.
- **flake8**: memeriksa kesesuaian PEP 8, error logika sederhana
  (misalnya variabel tidak terpakai), dan kompleksitas.
- **black**: auto-formatter yang memformat kode secara otomatis dan
  konsisten, sehingga perdebatan soal gaya berhenti.
- **mypy**: memeriksa kesesuaian tipe data secara statis berdasarkan
  type hints, menangkap error tipe sebelum program dijalankan.

Perannya dalam code review: masalah mekanis (format, style, error
sederhana, tipe) ditangkap **mesin** lebih dulu, sehingga reviewer
manusia dapat fokus pada hal yang membutuhkan pertimbangan manusia:
kebenaran logika bisnis, arsitektur, dan keamanan.

Integrasi ke CI/CD meningkatkan efektivitas review karena:

1. Pemeriksaan berjalan **otomatis pada setiap pull request**,
   tidak bergantung pada ketelitian reviewer.
2. Standar yang sama berlaku untuk semua anggota tim dan semua
   perubahan (*quality gate*: merge ditolak jika pemeriksaan gagal).
3. Umpan balik diterima penulis **lebih awal**, sebelum review
   manusia dimulai, sehingga siklus revisi lebih singkat.
4. Alat yang sama dapat dijalankan lokal lewat pre-commit hook
   (lihat Soal Praktik 6), sehingga kode yang masuk ke CI sudah
   bersih sejak dari komputer pengembang.

---

# B. Penjelasan Soal Praktik

## Soal 1 - Baca CSV dengan Exception Lengkap
File: `soal_1_baca_csv.py`, `data_mahasiswa.csv`, `data_rusak.csv`

Program membaca data mahasiswa dari CSV dengan tiga lapis penanganan:
`FileNotFoundError` untuk file yang tidak ada, `csv.Error` untuk
format CSV rusak (mode `strict=True`), dan `ValueError` per baris
untuk kolom angka yang tidak dapat dikonversi. Blok `else`
menampilkan ringkasan (jumlah valid, baris dilewati, rata-rata umur,
daftar jurusan) hanya jika pembacaan berhasil, dan blok `finally`
selalu menutup file. Program mendemonstrasikan tiga skenario
sekaligus: file hilang, file rusak, dan file valid dengan 2 baris
tidak valid. Hasil: **6 data valid terbaca, 2 baris dilewati**.

Jalankan: `python soal_1_baca_csv.py`

## Soal 2 - Hierarki Custom Exception Perpustakaan
File: `soal_2_perpustakaan.py`

Hierarki: `PerpustakaanError` sebagai kelas dasar, dengan turunan
`BukuNotFoundError`, `BukuTidakTersediaError`, dan
`AnggotaNotFoundError` yang masing-masing membawa atribut konteks
(judul buku / ID anggota). Fungsi `pinjam_buku()` melempar exception
sesuai kondisi, dan program utama mendemonstrasikan peminjaman
berhasil, ketiga jenis exception secara spesifik, serta penangkapan
melalui kelas dasar `PerpustakaanError`.

Jalankan: `python soal_2_perpustakaan.py`

## Soal 3 - Konfigurasi Logging
File: `soal_3_logging.py` (menghasilkan `aplikasi_si.log`)

Logger `si_akademik` dikonfigurasi dengan dua handler dan satu
formatter (`timestamp | nama logger | level | pesan`):

- `RotatingFileHandler` ke `aplikasi_si.log` (rotasi 10 KB, 3 berkas
  cadangan) untuk level **DEBUG ke atas**,
- `StreamHandler` konsol untuk level **WARNING ke atas**.

Hasil verifikasi terprogram di dalam file: file log berisi **6
baris** (semua level termasuk DEBUG dan INFO), sedangkan konsol
hanya menampilkan WARNING, ERROR, dan CRITICAL.

Jalankan: `python soal_3_logging.py`

## Soal 4 - Unit Test dengan unittest
File: `fungsi_akademik.py`, `soal_4_test_fungsi_akademik.py`

Fungsi yang diuji berada di `fungsi_akademik.py`: `hitung_ipk()`
(IPK berbobot SKS), `validasi_nim()` (tepat 10 digit angka), dan
`konversi_nilai_huruf()` (skala A s.d. E dengan B+, C+, D+). File
test berisi 3 kelas test (memakai `setUp` untuk data bersama) dengan
total **19 test** yang mencakup happy path, edge case (nilai batas
skala 85/80/55/0/100, NIM semua nol, daftar satu mata kuliah), dan
input tidak valid (`assertRaises` untuk `ValueError`/`TypeError`).
Hasil: **19 test OK**.

Jalankan: `python -m unittest soal_4_test_fungsi_akademik -v`

## Soal 5 - Identifikasi dan Refactoring Code Smell
File: `soal_5_sebelum_refactoring.py`, `soal_5_sesudah_refactoring.py`,
`soal_5_analisis.md`

Kode awal perhitungan pembayaran UKT sengaja mengandung lima code
smell: magic number, duplikasi (rumus diulang 6 kali), long method
(+- 60 baris), deep nesting (4 tingkat), dan dead code. Versi sesudah
memperbaikinya dengan konstanta bernama, Extract Method, guard
clause, dan penghapusan dead code, lengkap dengan docstring dan type
hints sesuai PEP 8. Penjelasan lengkap per smell ada di
`soal_5_analisis.md`. Bukti perilaku tidak berubah: kedua versi
menghasilkan total identik (Rp5.497.000 dan Rp893.000).

Jalankan: `python soal_5_sebelum_refactoring.py` lalu
`python soal_5_sesudah_refactoring.py`

## Soal 6 - Pre-commit Hooks (black, flake8, isort)
File: `.pre-commit-config.yaml`, `soal_6_contoh_kotor.py`,
`soal_6_contoh_bersih.py`

File `.pre-commit-config.yaml` memasang tiga hook yang berjalan
otomatis pada setiap `git commit`: isort (mengurutkan import,
profile black), black (auto-format, line length 79), dan flake8
(linting, max line length 79). Cara memasang: `pip install
pre-commit` lalu `pre-commit install` di root repository.

**Demonstrasi yang telah dilakukan** pada repository uji dengan file
`soal_6_contoh_kotor.py` (import tidak urut, format berantakan, ada
import `os` yang tidak terpakai):

1. Commit pertama **gagal/dibatalkan** (exit code 1): isort dan
   black mengubah file secara otomatis, dan flake8 melaporkan
   `F401 'os' imported but unused`. Kode yang tidak memenuhi standar
   tidak dapat masuk ke repository.
2. Setelah import `os` dihapus manual, commit kedua berhasil:
   ketiga hook **Passed** dan commit tercatat.

Isi file hasil perbaikan otomatis + perbaikan manual tersebut
tersimpan sebagai `soal_6_contoh_bersih.py`.

---

# Bukti Hasil Run

## Soal Praktik 1
   <img width="1120" height="752" alt="bukti_praktikum_soal1" src="https://github.com/user-attachments/assets/7fe6f240-73e8-4f56-b9bb-f0b1a94d3d82" />


## Soal Praktik 2
<img width="1120" height="584" alt="bukti_praktikum_soal2" src="https://github.com/user-attachments/assets/3f26521f-94fb-4de3-be69-992b879e9dd1" />

## Soal Praktik 3
<img width="1120" height="608" alt="bukti_praktikum_soal3" src="https://github.com/user-attachments/assets/b119177d-5dd8-4057-883f-9b2180303d5a" />


## Soal Praktik 4
<img width="1120" height="680" alt="bukti_praktikum_soal4" src="https://github.com/user-attachments/assets/13991a1e-a57f-433c-aad9-ba4a2c314edd" />

## Soal Praktik 5
<img width="1120" height="968" alt="bukti_praktikum_soal5" src="https://github.com/user-attachments/assets/50951ad9-acff-412a-859f-e362393a60af" />

## Soal Praktik 6
<img width="1120" height="608" alt="bukti_praktikum_soal6" src="https://github.com/user-attachments/assets/e0c929a2-022e-46aa-84ff-1c94cb3ed7bc" />
