# GREYPHA ANDER SAKEL
# 24416255201044
# IF24F 

import csv
import os
from collections import deque

# ==== STRUKTUR DATA ====

class RiwayatNode:
    def __init__(self, tanggal, keluhan, diagnosa):
        self.tanggal = tanggal
        self.keluhan = keluhan
        self.diagnosa = diagnosa
        self.next = None

class Pasien:
    def __init__(self, id_pasien, nama):
        self.id_pasien = id_pasien
        self.nama = nama
        self.riwayat = None  # Linked List

# ==== DATABASE ====

antrian = deque()
data_pasien = {}  # id_pasien: Pasien

# ==== FILE PATH ====

FILE_PASIEN = "pasien.csv"
FILE_RIWAYAT = "riwayat.csv"

# ==== INISIALISASI CSV JIKA BELUM ADA ====

def inisialisasi_csv():
    if not os.path.exists(FILE_PASIEN):
        with open(FILE_PASIEN, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["001", "John Doe"])
            writer.writerow(["002", "Jane Smith"])
            writer.writerow(["003", "Ahmad Fauzi"])
    if not os.path.exists(FILE_RIWAYAT):
        with open(FILE_RIWAYAT, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["001", "2025-07-01", "Demam", "Tifus"])
            writer.writerow(["001", "2025-07-05", "Batuk", "Pilek Biasa"])
            writer.writerow(["002", "2025-07-02", "Sakit Kepala", "Migrain"])
            writer.writerow(["003", "2025-07-03", "Sakit Perut", "Maag Akut"])

# ==== BACA DATA DARI CSV ====

def muat_data_pasien():
    if os.path.exists(FILE_PASIEN):
        with open(FILE_PASIEN, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    id_pasien, nama = row
                    data_pasien[id_pasien] = Pasien(id_pasien, nama)

def muat_data_riwayat():
    if os.path.exists(FILE_RIWAYAT):
        with open(FILE_RIWAYAT, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 4:
                    id_pasien, tanggal, keluhan, diagnosa = row
                    if id_pasien in data_pasien:
                        node = RiwayatNode(tanggal, keluhan, diagnosa)
                        pasien = data_pasien[id_pasien]
                        if not pasien.riwayat:
                            pasien.riwayat = node
                        else:
                            current = pasien.riwayat
                            while current.next:
                                current = current.next
                            current.next = node

def simpan_pasien_csv(pasien):
    with open(FILE_PASIEN, "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([pasien.id_pasien, pasien.nama])

def simpan_riwayat_csv(id_pasien, tanggal, keluhan, diagnosa):
    with open(FILE_RIWAYAT, "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([id_pasien, tanggal, keluhan, diagnosa])

# ==== FITUR ====

def tambah_pasien():
    id_pasien = input("ID Pasien: ")
    nama = input("Nama Pasien: ")
    if id_pasien not in data_pasien:
        pasien = Pasien(id_pasien, nama)
        data_pasien[id_pasien] = pasien
        simpan_pasien_csv(pasien)
        print("Pasien baru ditambahkan.")
    else:
        pasien = data_pasien[id_pasien]
        print("Pasien sudah terdaftar.")
    antrian.append(pasien)
    print(f"Pasien {pasien.nama} masuk ke antrian.")

def panggil_pasien():
    if not antrian:
        print("Antrian kosong.")
        return
    pasien = antrian.popleft()
    print(f"Memanggil pasien: {pasien.nama} (ID: {pasien.id_pasien})")

def lihat_antrian():
    if not antrian:
        print("Antrian kosong.")
        return
    print("\nDaftar Antrian:")
    for i, pasien in enumerate(antrian, start=1):
        print(f"{i}. {pasien.nama} (ID: {pasien.id_pasien})")

def tambah_riwayat():
    id_pasien = input("ID Pasien: ")
    pasien = data_pasien.get(id_pasien)
    if not pasien:
        print("Pasien tidak ditemukan.")
        return
    tanggal = input("Tanggal Kunjungan: ")
    keluhan = input("Keluhan: ")
    diagnosa = input("Diagnosa: ")

    node = RiwayatNode(tanggal, keluhan, diagnosa)
    if not pasien.riwayat:
        pasien.riwayat = node
    else:
        current = pasien.riwayat
        while current.next:
            current = current.next
        current.next = node

    simpan_riwayat_csv(id_pasien, tanggal, keluhan, diagnosa)
    print("Riwayat berhasil ditambahkan.")

def lihat_riwayat():
    id_pasien = input("ID Pasien: ")
    pasien = data_pasien.get(id_pasien)
    if not pasien:
        print("Pasien tidak ditemukan.")
        return
    print(f"Riwayat kunjungan {pasien.nama}:")
    current = pasien.riwayat
    if not current:
        print("Belum ada riwayat.")
        return
    while current:
        print(f"- {current.tanggal}: {current.keluhan} ({current.diagnosa})")
        current = current.next

# ==== MENU UTAMA ====

def menu():
    inisialisasi_csv()  # 👈 buat file jika belum ada
    muat_data_pasien()
    muat_data_riwayat()
    while True:
        print("\n=== MENU APLIKASI KLINIK (CSV) ===")
        print("1. Tambah Pasien ke Antrian")
        print("2. Lihat Antrian")
        print("3. Panggil Pasien")
        print("4. Tambah Riwayat Kunjungan")
        print("5. Lihat Riwayat Pasien")
        print("6. Keluar")
        pilih = input("Pilih menu: ")

        if pilih == "1":
            tambah_pasien()
        elif pilih == "2":
            lihat_antrian()
        elif pilih == "3":
            panggil_pasien()
        elif pilih == "4":
            tambah_riwayat()
        elif pilih == "5":
            lihat_riwayat()
        elif pilih == "6":
            print("Terima kasih.")
            break
        else:
            print("Menu tidak valid.")

# ==== JALANKAN PROGRAM ====
menu()
