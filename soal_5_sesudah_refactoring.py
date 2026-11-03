"""Soal Praktik 5 - Kode SESUDAH refactoring (clean code).

Hasil refactoring dari soal_5_sebelum_refactoring.py:

1. Magic number   -> diganti konstanta bernama (Replace Magic Number
                     with Symbolic Constant).
2. Duplikasi      -> rumus hitung dipusatkan di fungsi kecil
                     (Extract Method, prinsip DRY).
3. Long method    -> dipecah menjadi fungsi-fungsi satu tugas.
4. Deep nesting   -> diratakan dengan guard clause.
5. Dead code      -> dihapus seluruhnya (Remove Dead Code).

Seluruh fungsi dilengkapi docstring dan type hints sesuai PEP 8.
Perilaku program tidak berubah: total kedua contoh pembayaran sama
persis dengan versi sebelum refactoring.
"""

BATAS_UKT_DISKON = 1_000_000
PERSEN_DISKON = 0.10
TARIF_PAJAK = 0.11
SEMESTER_MAKSIMUM = 8
STATUS_AKTIF = 1
STATUS_CUTI = 2
BIAYA_ADMIN = {"tunai": 2_500, "transfer": 5_000, "ewallet": 7_500}


def format_rupiah(nilai: int) -> str:
    """Format bilangan bulat menjadi string Rupiah, mis. Rp5.497.000."""
    return "Rp" + format(nilai, ",").replace(",", ".")


def hitung_diskon(ukt: int) -> int:
    """Hitung diskon: 10% jika UKT melewati batas, selain itu 0."""
    if ukt > BATAS_UKT_DISKON:
        return round(ukt * PERSEN_DISKON)
    return 0


def hitung_pajak(subtotal: int) -> int:
    """Hitung pajak 11% dari subtotal pembayaran."""
    return round(subtotal * TARIF_PAJAK)


def biaya_admin(metode: str) -> int:
    """Ambil biaya admin berdasarkan metode pembayaran.

    Raises:
        ValueError: jika metode pembayaran tidak dikenal.
    """
    if metode not in BIAYA_ADMIN:
        raise ValueError(f"Metode pembayaran '{metode}' tidak dikenal")
    return BIAYA_ADMIN[metode]


def hitung_total_pembayaran(ukt: int, metode: str) -> int:
    """Hitung total bayar: UKT - diskon + pajak + biaya admin."""
    diskon = hitung_diskon(ukt)
    subtotal = ukt - diskon
    return subtotal + hitung_pajak(subtotal) + biaya_admin(metode)


def buat_struk(nama: str, nim: str, semester: int, metode: str,
               total: int) -> str:
    """Susun teks struk pembayaran UKT."""
    baris = [
        "STRUK PEMBAYARAN UKT (versi sesudah)",
        f"Nama     : {nama}",
        f"NIM      : {nim}",
        f"Semester : {semester}",
        f"Metode   : {metode}",
        f"Total    : {format_rupiah(total)}",
    ]
    return "\n".join(baris)


def proses_pembayaran_ukt(nama: str, nim: str, ukt: int, metode: str,
                          semester: int, status: int) -> int:
    """Proses satu pembayaran UKT dan cetak struknya.

    Guard clause menangani status tidak aktif dan semester berlebih
    di awal, sehingga alur utama tidak bersarang dalam.
    """
    if status == STATUS_CUTI:
        print("Mahasiswa sedang cuti, tidak ada tagihan")
        return 0
    if status != STATUS_AKTIF:
        print("Status mahasiswa tidak dikenal")
        return 0
    if semester > SEMESTER_MAKSIMUM:
        print("Mahasiswa melewati batas semester")
        return 0
    total = hitung_total_pembayaran(ukt, metode)
    print(buat_struk(nama, nim, semester, metode, total))
    return total


def main() -> None:
    """Dua contoh pembayaran yang sama dengan versi sebelum."""
    print("=== Contoh 1: UKT besar, tunai ===")
    total1 = proses_pembayaran_ukt(
        "Andi Pratama", "2024132001", 5_500_000, "tunai", 5, STATUS_AKTIF
    )
    print("Total dikembalikan:", total1)

    print("\n=== Contoh 2: UKT kecil, transfer ===")
    total2 = proses_pembayaran_ukt(
        "Dewi Anggraini", "2024132004", 800_000, "transfer", 3,
        STATUS_AKTIF,
    )
    print("Total dikembalikan:", total2)


if __name__ == "__main__":
    main()
