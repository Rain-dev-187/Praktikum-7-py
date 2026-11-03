"""Soal Praktik 2 - Hierarki custom exception Sistem Perpustakaan.

Hierarki exception:

    PerpustakaanError            (base)
    |- BukuNotFoundError         (judul tidak ada di katalog)
    |- BukuTidakTersediaError    (buku ada, tetapi stok habis)
    |- AnggotaNotFoundError      (anggota tidak terdaftar)

Fungsi pinjam_buku() melempar exception di atas, dan program utama
mendemonstrasikan penanganan setiap jenis exception, termasuk
penangkapan melalui kelas base PerpustakaanError.
"""


class PerpustakaanError(Exception):
    """Base exception untuk seluruh error Sistem Perpustakaan."""


class BukuNotFoundError(PerpustakaanError):
    """Judul buku tidak ditemukan di katalog."""

    def __init__(self, judul):
        self.judul = judul
        super().__init__(f"Buku '{judul}' tidak ditemukan di katalog")


class BukuTidakTersediaError(PerpustakaanError):
    """Buku ada di katalog, tetapi semua eksemplarnya sedang dipinjam."""

    def __init__(self, judul):
        self.judul = judul
        super().__init__(
            f"Buku '{judul}' sedang tidak tersedia (stok habis)"
        )


class AnggotaNotFoundError(PerpustakaanError):
    """ID anggota tidak terdaftar di perpustakaan."""

    def __init__(self, id_anggota):
        self.id_anggota = id_anggota
        super().__init__(f"Anggota '{id_anggota}' tidak terdaftar")


# Data contoh: katalog judul -> stok, daftar anggota, catatan pinjam.
KATALOG = {
    "Pemrograman Python": 3,
    "Basis Data": 0,
    "Sistem Informasi": 2,
}
ANGGOTA = {"A001": "Andi Pratama", "A002": "Dewi Anggraini"}
PEMINJAMAN = []


def pinjam_buku(id_anggota, judul):
    """Pinjam buku untuk seorang anggota.

    Raises:
        AnggotaNotFoundError: anggota tidak terdaftar.
        BukuNotFoundError: judul tidak ada di katalog.
        BukuTidakTersediaError: stok buku habis.
    """
    if id_anggota not in ANGGOTA:
        raise AnggotaNotFoundError(id_anggota)
    if judul not in KATALOG:
        raise BukuNotFoundError(judul)
    if KATALOG[judul] <= 0:
        raise BukuTidakTersediaError(judul)
    KATALOG[judul] -= 1
    PEMINJAMAN.append((id_anggota, judul))
    return (
        f"{ANGGOTA[id_anggota]} berhasil meminjam '{judul}' "
        f"(sisa stok: {KATALOG[judul]})"
    )


def coba_pinjam(id_anggota, judul):
    """Coba satu peminjaman dan tangani setiap exception-nya."""
    print(f"\n> pinjam_buku('{id_anggota}', '{judul}')")
    try:
        hasil = pinjam_buku(id_anggota, judul)
    except BukuNotFoundError as e:
        print(f"  [BukuNotFoundError] {e}")
    except BukuTidakTersediaError as e:
        print(f"  [BukuTidakTersediaError] {e}")
    except AnggotaNotFoundError as e:
        print(f"  [AnggotaNotFoundError] {e}")
    except PerpustakaanError as e:
        print(f"  [PerpustakaanError lain] {e}")
    else:
        print(f"  [Berhasil] {hasil}")


def main():
    """Demonstrasikan peminjaman berhasil dan ketiga exception."""
    print("=== Demonstrasi Sistem Perpustakaan ===")
    coba_pinjam("A001", "Pemrograman Python")   # berhasil
    coba_pinjam("A002", "Algoritma Modern")     # BukuNotFoundError
    coba_pinjam("A001", "Basis Data")           # BukuTidakTersediaError
    coba_pinjam("A999", "Sistem Informasi")     # AnggotaNotFoundError

    # Menangkap lewat kelas base menangkap semua subclass-nya.
    print("\n> pinjam_buku('A001', 'Jaringan Komputer') "
          "ditangkap sebagai PerpustakaanError")
    try:
        pinjam_buku("A001", "Jaringan Komputer")
    except PerpustakaanError as e:
        print(f"  [PerpustakaanError] {type(e).__name__}: {e}")

    print("\n=== Ringkasan akhir ===")
    print(f"  Daftar peminjaman: {PEMINJAMAN}")
    print(f"  Stok akhir katalog: {KATALOG}")


if __name__ == "__main__":
    main()
