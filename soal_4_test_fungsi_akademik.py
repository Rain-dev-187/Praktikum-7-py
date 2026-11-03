"""Soal Praktik 4 - Unit test unittest untuk fungsi akademik.

Menguji tiga fungsi dari modul fungsi_akademik:
(a) hitung_ipk(), (b) validasi_nim(), (c) konversi_nilai_huruf().

Setiap fungsi diuji pada tiga kelompok kasus:
- happy path  : input normal yang valid,
- edge case   : nilai batas (boundary),
- input salah : input tidak valid yang harus memunculkan exception.

Jalankan dengan:  python -m unittest soal_4_test_fungsi_akademik -v
"""

import unittest

from fungsi_akademik import (
    hitung_ipk,
    konversi_nilai_huruf,
    validasi_nim,
)


class TestHitungIPK(unittest.TestCase):
    """Test untuk fungsi hitung_ipk()."""

    def setUp(self):
        """Data contoh dipakai bersama oleh beberapa test."""
        self.nilai_campuran = [
            {"nilai_huruf": "A", "sks": 3},
            {"nilai_huruf": "B+", "sks": 2},
            {"nilai_huruf": "B", "sks": 3},
        ]

    # --- happy path ---
    def test_ipk_nilai_campuran(self):
        # (4.0*3 + 3.5*2 + 3.0*3) / 8 = 28 / 8 = 3.5
        self.assertEqual(hitung_ipk(self.nilai_campuran), 3.5)

    def test_ipk_satu_mata_kuliah(self):
        nilai = [{"nilai_huruf": "C", "sks": 2}]
        self.assertEqual(hitung_ipk(nilai), 2.0)

    # --- edge case ---
    def test_ipk_semua_a(self):
        nilai = [
            {"nilai_huruf": "A", "sks": 3},
            {"nilai_huruf": "A", "sks": 2},
        ]
        self.assertEqual(hitung_ipk(nilai), 4.0)

    def test_ipk_semua_e(self):
        nilai = [{"nilai_huruf": "E", "sks": 3}]
        self.assertEqual(hitung_ipk(nilai), 0.0)

    # --- input tidak valid ---
    def test_ipk_daftar_kosong(self):
        with self.assertRaises(ValueError):
            hitung_ipk([])

    def test_ipk_huruf_tidak_dikenal(self):
        with self.assertRaises(ValueError):
            hitung_ipk([{"nilai_huruf": "F", "sks": 3}])

    def test_ipk_sks_nol(self):
        with self.assertRaises(ValueError):
            hitung_ipk([{"nilai_huruf": "A", "sks": 0}])


class TestValidasiNIM(unittest.TestCase):
    """Test untuk fungsi validasi_nim()."""

    # --- happy path ---
    def test_nim_valid(self):
        self.assertTrue(validasi_nim("2024132031"))

    # --- edge case ---
    def test_nim_semua_nol(self):
        self.assertTrue(validasi_nim("0000000000"))

    # --- input tidak valid ---
    def test_nim_kurang_dari_10_digit(self):
        with self.assertRaises(ValueError):
            validasi_nim("202413203")

    def test_nim_lebih_dari_10_digit(self):
        with self.assertRaises(ValueError):
            validasi_nim("20241320311")

    def test_nim_mengandung_huruf(self):
        with self.assertRaises(ValueError):
            validasi_nim("2024AB2031")

    def test_nim_bukan_string(self):
        with self.assertRaises(TypeError):
            validasi_nim(2024132031)


class TestKonversiNilaiHuruf(unittest.TestCase):
    """Test untuk fungsi konversi_nilai_huruf()."""

    # --- happy path ---
    def test_konversi_nilai_tengah(self):
        self.assertEqual(konversi_nilai_huruf(90), "A")
        self.assertEqual(konversi_nilai_huruf(82), "B+")
        self.assertEqual(konversi_nilai_huruf(77), "B")
        self.assertEqual(konversi_nilai_huruf(72), "C+")
        self.assertEqual(konversi_nilai_huruf(67), "C")
        self.assertEqual(konversi_nilai_huruf(62), "D+")
        self.assertEqual(konversi_nilai_huruf(57), "D")
        self.assertEqual(konversi_nilai_huruf(40), "E")

    # --- edge case: tepat pada batas skala ---
    def test_konversi_batas_atas(self):
        self.assertEqual(konversi_nilai_huruf(100), "A")
        self.assertEqual(konversi_nilai_huruf(85), "A")
        self.assertEqual(konversi_nilai_huruf(80), "B+")

    def test_konversi_batas_bawah(self):
        self.assertEqual(konversi_nilai_huruf(55), "D")
        self.assertEqual(konversi_nilai_huruf(54), "E")
        self.assertEqual(konversi_nilai_huruf(0), "E")

    def test_konversi_desimal(self):
        self.assertEqual(konversi_nilai_huruf(84.9), "B+")
        self.assertEqual(konversi_nilai_huruf(79.5), "B")

    # --- input tidak valid ---
    def test_konversi_di_luar_rentang(self):
        with self.assertRaises(ValueError):
            konversi_nilai_huruf(101)
        with self.assertRaises(ValueError):
            konversi_nilai_huruf(-1)

    def test_konversi_bukan_angka(self):
        with self.assertRaises(TypeError):
            konversi_nilai_huruf("delapan puluh")


if __name__ == "__main__":
    unittest.main()
