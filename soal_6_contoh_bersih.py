import json
import sys


def hitung_total(harga, qty):
    return harga * qty


data = {"nama": "Buku Tulis", "harga": 5000}
total = hitung_total(data["harga"], 3)
print("Total belanja:", total)
print(json.dumps(data))
print(sys.version_info.major)
