"""Soal Praktik 1 - Membaca data mahasiswa dari file CSV.

Program membaca file CSV data mahasiswa dengan penanganan exception
yang lengkap:

- FileNotFoundError : file tidak ditemukan.
- csv.Error         : format CSV rusak (dibaca dengan mode strict).
- ValueError        : isi kolom tidak dapat dikonversi ke angka.

Blok else menampilkan ringkasan hanya jika pembacaan berhasil, dan
blok finally memastikan file selalu ditutup.
"""

import csv


def baca_data_mahasiswa(path):
    """Baca file CSV mahasiswa dan kembalikan list data yang valid.

    Baris yang nilainya tidak valid dilewati (penanganan ValueError
    per baris), sedangkan error pada level file (file tidak ada atau
    format CSV rusak) menghentikan pembacaan file tersebut.
    """
    data_valid = []
    baris_rusak = 0
    berkas = None
    try:
        berkas = open(path, newline="", encoding="utf-8")
        pembaca = csv.reader(berkas, strict=True)
        header = next(pembaca, None)
        print(f"  Header terbaca: {header}")
        for nomor_baris, baris in enumerate(pembaca, start=2):
            try:
                if len(baris) != 5:
                    raise ValueError(
                        f"jumlah kolom {len(baris)}, seharusnya 5"
                    )
                mahasiswa = {
                    "nim": baris[0],
                    "nama": baris[1],
                    "jurusan": baris[2],
                    "umur": int(baris[3]),
                    "semester": int(baris[4]),
                }
            except ValueError as e:
                baris_rusak += 1
                print(f"  [ValueError] Baris {nomor_baris} dilewati: {e}")
            else:
                data_valid.append(mahasiswa)
    except FileNotFoundError:
        print(f"  [FileNotFoundError] File '{path}' tidak ditemukan.")
    except csv.Error as e:
        print(f"  [csv.Error] Format CSV pada '{path}' rusak: {e}")
    else:
        # Blok else: hanya jalan jika TIDAK ada exception level file.
        total = len(data_valid)
        rata_umur = (
            sum(m["umur"] for m in data_valid) / total if total else 0
        )
        jurusan_unik = sorted({m["jurusan"] for m in data_valid})
        print("  --- Ringkasan (blok else) ---")
        print(f"  Data valid terbaca : {total} mahasiswa")
        print(f"  Baris dilewati     : {baris_rusak} baris")
        print(f"  Rata-rata umur     : {rata_umur:.1f} tahun")
        print(f"  Jurusan ditemukan  : {', '.join(jurusan_unik)}")
    finally:
        # Blok finally: selalu jalan, file pasti ditutup.
        if berkas is not None:
            berkas.close()
        print(f"  [finally] File '{path}' ditutup.")
    return data_valid


def main():
    """Demonstrasikan tiga skenario pembacaan file."""
    print("=== Skenario 1: file tidak ditemukan ===")
    baca_data_mahasiswa("data_tidak_ada.csv")

    print("\n=== Skenario 2: format CSV rusak ===")
    baca_data_mahasiswa("data_rusak.csv")

    print("\n=== Skenario 3: file valid (ada 2 baris tidak valid) ===")
    data = baca_data_mahasiswa("data_mahasiswa.csv")

    print(f"\nTotal data valid dari skenario 3: {len(data)} mahasiswa")
    for m in data:
        print(
            f"  - {m['nim']} | {m['nama']} | {m['jurusan']} | "
            f"umur {m['umur']} | semester {m['semester']}"
        )


if __name__ == "__main__":
    main()
