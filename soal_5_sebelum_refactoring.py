"""Soal Praktik 5 - Kode SEBELUM refactoring (mengandung code smell).

Kode ini sengaja ditulis buruk untuk latihan. Terdapat lima code
smell yang ditandai komentar [SMELL 1] s.d. [SMELL 5]:

1. Magic number   : angka 1000000, 0.1, 0.11, 2500/5000/7500, dan
                    kode status 1/2 tanpa nama yang menjelaskan arti.
2. Duplikasi      : rumus diskon + pajak + admin ditulis ulang pada
                    setiap cabang metode pembayaran (6 kali).
3. Long method    : satu fungsi mengerjakan validasi, perhitungan,
                    dan pencetakan struk sekaligus (+- 60 baris).
4. Deep nesting   : if bersarang sampai 4 tingkat.
5. Dead code      : variabel, fungsi, dan baris yang tidak terpakai.

Versi bersihnya ada di soal_5_sesudah_refactoring.py dan
penjelasannya di soal_5_analisis.md.
"""


# [SMELL 5 - dead code] Fungsi ini tidak pernah dipanggil di mana pun.
def hitung_pajak_lama(subtotal):
    return subtotal * 0.1


# [SMELL 3 - long method] Semua pekerjaan menumpuk di satu fungsi.
def proses_pembayaran_ukt(nama, nim, ukt, metode, semester, status):
    keterangan = "sedang diproses"  # [SMELL 5] variabel tak terpakai
    total = 0
    # [SMELL 4 - deep nesting] if bersarang 4 tingkat.
    if status == 1:  # [SMELL 1] angka 1 = status aktif?
        if semester <= 8:  # [SMELL 1] angka 8 tanpa penjelasan
            if ukt > 1000000:  # [SMELL 1] batas diskon tanpa nama
                # [SMELL 2 - duplikasi] blok hitung diulang 3x di sini
                # dan 3x lagi pada cabang else di bawah.
                if metode == "tunai":
                    diskon = ukt * 0.1
                    subtotal = ukt - diskon
                    pajak = subtotal * 0.11
                    total = subtotal + pajak + 2500
                elif metode == "transfer":
                    diskon = ukt * 0.1
                    subtotal = ukt - diskon
                    pajak = subtotal * 0.11
                    total = subtotal + pajak + 5000
                elif metode == "ewallet":
                    diskon = ukt * 0.1
                    subtotal = ukt - diskon
                    pajak = subtotal * 0.11
                    total = subtotal + pajak + 7500
            else:
                if metode == "tunai":
                    diskon = 0
                    subtotal = ukt - diskon
                    pajak = subtotal * 0.11
                    total = subtotal + pajak + 2500
                elif metode == "transfer":
                    diskon = 0
                    subtotal = ukt - diskon
                    pajak = subtotal * 0.11
                    total = subtotal + pajak + 5000
                elif metode == "ewallet":
                    diskon = 0
                    subtotal = ukt - diskon
                    pajak = subtotal * 0.11
                    total = subtotal + pajak + 7500
            print("STRUK PEMBAYARAN UKT (versi sebelum)")
            print("Nama     :", nama)
            print("NIM      :", nim)
            print("Semester :", semester)
            print("Metode   :", metode)
            print("Total    : Rp", format(int(total), ",").replace(
                ",", "."))
            return total
            print("Baris ini tidak akan pernah dijalankan")  # [SMELL 5]
        else:
            print("Mahasiswa melewati batas semester")
            return 0
    elif status == 2:  # [SMELL 1] angka 2 = cuti?
        print("Mahasiswa sedang cuti, tidak ada tagihan")
        return 0
    else:
        print("Status mahasiswa tidak dikenal")
        return 0


def main():
    """Dua contoh pembayaran yang juga dipakai versi sesudah."""
    print("=== Contoh 1: UKT besar, tunai ===")
    total1 = proses_pembayaran_ukt(
        "Andi Pratama", "2024132001", 5500000, "tunai", 5, 1)
    print("Total dikembalikan:", int(total1))

    print("\n=== Contoh 2: UKT kecil, transfer ===")
    total2 = proses_pembayaran_ukt(
        "Dewi Anggraini", "2024132004", 800000, "transfer", 3, 1)
    print("Total dikembalikan:", int(total2))


if __name__ == "__main__":
    main()
