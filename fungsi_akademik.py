"""Fungsi-fungsi akademik yang diuji pada Soal Praktik 4.

Berisi tiga fungsi:

- hitung_ipk()           : IPK dari daftar nilai berbobot SKS.
- validasi_nim()         : validasi format NIM 10 digit angka.
- konversi_nilai_huruf() : konversi nilai angka ke nilai huruf.
"""

BOBOT_NILAI = {
    "A": 4.0,
    "B+": 3.5,
    "B": 3.0,
    "C+": 2.5,
    "C": 2.0,
    "D+": 1.5,
    "D": 1.0,
    "E": 0.0,
}


def konversi_nilai_huruf(angka):
    """Konversi nilai angka (0-100) menjadi nilai huruf.

    Skala yang digunakan:
        A  : 85 - 100      C  : 65 - 69
        B+ : 80 - 84       D+ : 60 - 64
        B  : 75 - 79       D  : 55 - 59
        C+ : 70 - 74       E  : di bawah 55

    Raises:
        TypeError: jika angka bukan int/float.
        ValueError: jika angka di luar rentang 0-100.
    """
    if isinstance(angka, bool) or not isinstance(angka, (int, float)):
        raise TypeError("Nilai harus berupa angka (int/float)")
    if angka < 0 or angka > 100:
        raise ValueError("Nilai harus berada pada rentang 0-100")
    if angka >= 85:
        return "A"
    if angka >= 80:
        return "B+"
    if angka >= 75:
        return "B"
    if angka >= 70:
        return "C+"
    if angka >= 65:
        return "C"
    if angka >= 60:
        return "D+"
    if angka >= 55:
        return "D"
    return "E"


def validasi_nim(nim):
    """Validasi format NIM: string berisi tepat 10 digit angka.

    Returns:
        True jika format NIM valid.

    Raises:
        TypeError: jika nim bukan string.
        ValueError: jika panjang bukan 10 atau mengandung non-digit.
    """
    if not isinstance(nim, str):
        raise TypeError("NIM harus berupa string")
    if len(nim) != 10 or not nim.isdigit():
        raise ValueError(f"NIM '{nim}' tidak valid: harus 10 digit angka")
    return True


def hitung_ipk(daftar_nilai):
    """Hitung IPK dari daftar nilai mata kuliah.

    Args:
        daftar_nilai: list of dict dengan kunci "nilai_huruf"
            (misalnya "A") dan "sks" (bilangan bulat positif).

    Returns:
        IPK sebagai float yang dibulatkan ke 2 angka desimal.

    Raises:
        ValueError: jika daftar kosong, nilai huruf tidak dikenal,
            atau SKS tidak positif.
    """
    if not daftar_nilai:
        raise ValueError("Daftar nilai tidak boleh kosong")
    total_bobot = 0.0
    total_sks = 0
    for item in daftar_nilai:
        huruf = item["nilai_huruf"]
        sks = item["sks"]
        if huruf not in BOBOT_NILAI:
            raise ValueError(f"Nilai huruf '{huruf}' tidak dikenal")
        if not isinstance(sks, int) or sks <= 0:
            raise ValueError("SKS harus bilangan bulat positif")
        total_bobot += BOBOT_NILAI[huruf] * sks
        total_sks += sks
    return round(total_bobot / total_sks, 2)
