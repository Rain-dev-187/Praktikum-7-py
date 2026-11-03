"""Soal Praktik 3 - Konfigurasi logging untuk aplikasi SI.

Konfigurasi yang dibuat:

(a) File handler RotatingFileHandler: mencatat level DEBUG ke atas
    ke berkas aplikasi_si.log (rotasi 10 KB, 3 berkas cadangan).
(b) Console handler: mencatat level WARNING ke atas ke layar.
(c) Formatter untuk kedua handler: timestamp, nama logger, level,
    dan pesan.

Akibatnya pesan DEBUG dan INFO hanya masuk ke file, sedangkan
WARNING, ERROR, dan CRITICAL muncul di file DAN di konsol.
Program menutup bagian dengan verifikasi isi file log.
"""

import logging
from logging.handlers import RotatingFileHandler

NAMA_FILE_LOG = "aplikasi_si.log"


def buat_logger():
    """Buat dan konfigurasi logger aplikasi SI."""
    logger = logging.getLogger("si_akademik")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()

    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # (a) File handler dengan rotasi: DEBUG ke atas.
    file_handler = RotatingFileHandler(
        NAMA_FILE_LOG, maxBytes=10 * 1024, backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # (b) Console handler: WARNING ke atas.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


def main():
    """Tulis log di berbagai level lalu verifikasi hasilnya."""
    logger = buat_logger()

    print("Menulis log (yang tampil di bawah baris ini hanya")
    print("WARNING ke atas, sesuai level console handler):")
    print("-" * 60)
    logger.debug("Query SQL: SELECT * FROM mahasiswa WHERE nim=%s",
                 "2024132001")
    logger.info("User admin berhasil login dari 192.168.1.10")
    logger.info("Pendaftaran mahasiswa baru berhasil: NIM 2024132009")
    logger.warning("Penggunaan disk server mencapai 85%")
    logger.error("Gagal mengirim notifikasi email ke dosen@univ.ac.id")
    logger.critical("Koneksi database utama terputus!")
    print("-" * 60)

    # Pastikan semua pesan sudah ditulis ke file sebelum diverifikasi.
    for handler in logger.handlers:
        handler.flush()

    print("\n=== Verifikasi isi file log (aplikasi_si.log) ===")
    with open(NAMA_FILE_LOG, encoding="utf-8") as f:
        baris_log = [b.rstrip() for b in f if b.strip()]
    for baris in baris_log:
        print(baris)

    jumlah = len(baris_log)
    ada_debug = any("DEBUG" in b for b in baris_log)
    ada_info = any("INFO" in b for b in baris_log)
    print("\n=== Hasil verifikasi ===")
    print(f"  Total baris di file log : {jumlah}")
    print(f"  Ada level DEBUG di file : {ada_debug} "
          "(tidak tampil di konsol)")
    print(f"  Ada level INFO di file  : {ada_info} "
          "(tidak tampil di konsol)")
    print("  WARNING/ERROR/CRITICAL tampil di file DAN konsol.")


if __name__ == "__main__":
    main()
