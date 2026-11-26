import os
import csv
from datetime import datetime
import pandas as pd


FILE_MENU = "menu.csv"
FILE_VOUCHER = "Voucher.csv"
FILE_TRANSAKSI = "Transaksi.csv"

# Perisapan/Inisialisasi file
try:
    df = pd.read_csv('users.csv', dtype=str)
    if 'ceo' not in df['Nama'].values:
        df.loc[len(df)] = ['ceo', 'ceo123', 'ceo']
        df.to_csv('users.csv', index=False)
except FileNotFoundError:
    df = pd.DataFrame({'Nama': [], 'Password': [], 'Sebagai': []})
    df.loc[len(df)] = ['ceo', 'ceo123', 'ceo']
    df.to_csv('users.csv', index=False)

# Inisialisasi file Transaksi.csv kalau belum ada
try:
    pd.read_csv(FILE_TRANSAKSI)
except FileNotFoundError:
    df_trx = pd.DataFrame(columns=['ID', 'Waktu', 'Item_Pesanan', 'Jumlah', 'Harga'])
    df_trx.to_csv(FILE_TRANSAKSI, index=False)

nama_akun = ''

# keranjang pesanan
keranjang = []


# Beranda, registrasi, login
def df_beranda():
    while True:
        os.system('cls')
        print('======================================================')
        print('|     SELAMAT DATANG DI CAFE DAPOER DIGITAL          |')
        print('======================================================')
        print()
        print('==================== MENU MASUK ======================')
        print()
        print('(1) Login sebagai admin/ceo')
        print('(2) Login customer')
        print('(3) Registrasi')
        print('(0) Keluar')
        print()

        pilih = input("Masukkan nomer pilihan (1),(2),(3),(0): ")
        if pilih in ['1', '2']:
            df_login()
        elif pilih == '3':
            df_registrasi()
        elif pilih == '0':
            print('Terima kasih telah berkunjung, sampai jumpa lagi!! ')
            break
        else:
            print('pilihan tidak valid!!')
            input('Tekan enter...')


def df_registrasi():
    while True:
        os.system('cls')
        print('======================================================')
        print('|               REGISTRASI AKUN BARU                 |')
        print('======================================================')
        print()
        dfuser = pd.read_csv('users.csv', dtype=str)
        print('ketik (404) untuk kembali ke beranda')
        nama = input("Masukkan nama/username anda : ").strip()

        if nama == '':
            print('Nama tidak boleh kosong!!')
            input("Tekan enter...")
            continue

        if nama == '404':
            return df_beranda()

        if nama in dfuser['Nama'].values:
            print('Nama sudah digunakan!!')
            input("Tekan enter...")
            continue

        kembali_ke_nama = False
        while True:
            print('ketik (kembali) untuk mengubah nama')
            password = input('Masukkan password anda (minimal 8 karakter, mengandung huruf besar dan angka): ')
            
            if password.strip().lower() == 'kembali':
                kembali_ke_nama = True
                break

            if len(password) < 8:
                print('Password minimal memiliki 8 karakter!!')
                continue

            ada_huruf_besar = False
            ada_huruf_kecil = False
            ada_angka = False

            for char in password:
                if char.isupper():
                    ada_huruf_besar = True
                if char.islower():
                    ada_huruf_kecil = True
                if char.isdigit():
                    ada_angka = True

            if not (ada_huruf_besar and ada_huruf_kecil and ada_angka):
                print('Password harus mengandung huruf besar, huruf kecil, dan angka!!')
                continue

            else:
                print('Password sudah valid')
                break

        if kembali_ke_nama:
            continue

        while True:
            cek = input('Apakah Nama dan Password sudah benar? (y/t) : ')
            if cek == 'y':
                dfuser.loc[len(dfuser)] = [nama, password, 'customer']
                dfuser.to_csv('users.csv', index=False)
                input('Registrasi sudah berhasil!! Tekan enter.....')
                return
            elif cek == 't':
                input('Silahkan registrasi ulang dengan menekan enter...')
                return df_registrasi()
            else:
                print('tidak valid!! silahkan ulangi!!')


def df_login():
    global nama_akun
    while True:
        os.system('cls')
        print('======================================================')
        print('|          SUDAH PUNYA AKUN? SILAHKAN LOGIN          |')
        print('======================================================')
        print('(ketik 0 pada nama untuk kembali)')
        print()

        nama = input('Masukkan nama/username akun : ').strip()
        if nama == '0':
            return
        password = input('Masukkan password : ')

        loginberhasil = False
        sebagai = ''

        with open('users.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if str(row.get('Nama', '')).strip() == nama and str(row.get('Password', '')).strip() == password:
                    nama_akun = row.get('Nama').strip()
                    sebagai = row.get('Sebagai').strip().lower()
                    loginberhasil = True
                    break

        if loginberhasil:
            print(f'Login berhasil!!! Halo, {nama_akun}, sebagai {sebagai}!')
            input('\nTekan enter....')
            if sebagai == 'customer':
                df_menucustomer()
            elif sebagai == 'ceo':
                df_menuceo()
            else:
                print('siapa anda??, kembali ke halaman utama....')
                input('\nTekan enter........')
            return
        else:
            print('Nama atau password salah!!')
            input('Tekan enter untuk coba lagi...')


# Menu Ceo
def df_menuceo():
    while True:
        os.system('cls')
        print('======================================================')
        print(f'|           MENU CEO - {nama_akun}                  |')
        print('======================================================')
        print('(1) Lihat daftar akun')
        print('(2) Kelola daftar menu')
        print('(3) Rekap transaksi (Struk & Arsip)')
        print('(0) Logout')
        pilih = input('Masukkan pilihan (angka) : ')
        if pilih == '1':
            os.system('cls')
            dfuser = pd.read_csv('users.csv', dtype=str)
            print()
            print(dfuser[['Nama', 'Sebagai']])
            input('\nTekan enter untuk kembali...')
        elif pilih == '2':
            df_kelola_daftar_menu()
        elif pilih == '3':
            rekap_transaksi()
        elif pilih == '0':
            return
        else:
            print('Pilihan tidak valid!!')
            input('Tekan enter...')


def rekap_transaksi():
    while True:
        os.system('cls')
        print("======================================================")
        print("|          REKAP TRANSAKSI (STRUK & ARSIP)           |")
        print("======================================================")
        print("(1) Lihat arsip transaksi & total pemasukan")
        print("(2) Cari & cetak ulang struk")
        print("(0) Kembali")
        pilih = input("Pilih menu (angka): ").strip()

        df_trx = pd.read_csv(FILE_TRANSAKSI)

        if pilih == '1':
            os.system('cls')
            print("======================================================")
            print("|               ARSIP TRANSAKSI PENJUALAN            |")
            print("======================================================")
            if df_trx.empty:
                print("\nBelum ada data transaksi.")
            else:
                for i, row in df_trx.iterrows():
                    print(f"[{row['ID']}] {row['Waktu']} | {row['Item_Pesanan']} ({row['Jumlah']}x) = Rp {int(row['Harga']):,}")
                print("-" * 54)
                total_pemasukan = int(df_trx['Harga'].sum())
                print(f"Total Item Terjual : {int(df_trx['Jumlah'].sum())} porsi")
                print(f"TOTAL PEMASUKAN    : Rp {total_pemasukan:,}")
            input("\nTekan enter untuk kembali...")

        elif pilih == '2':
            os.system('cls')
            print("======================================================")
            print("|              CARI & CETAK ULANG STRUK              |")
            print("======================================================")
            if df_trx.empty:
                print("\nBelum ada data transaksi.")
                input("\nTekan enter untuk kembali...")
            else:
                print("\nDaftar ID Transaksi:")
                for id_unik in df_trx['ID'].unique():
                    print(f"- {id_unik}")

                while True:
                    cari_id = input("\nMasukkan ID Transaksi (contoh TRX-001, ketik 0 untuk kembali): ").strip().upper()
                    if cari_id == '0':
                        break

                    hasil = df_trx[df_trx['ID'].astype(str).str.upper() == cari_id]

                    if hasil.empty:
                        print("[!] ID Transaksi tidak ditemukan! Silakan input ulang.")
                    else:
                        waktu_trx = hasil['Waktu'].values[0]
                        total_struk = int(hasil['Harga'].sum())
                        print("\n" + "=" * 38)
                        print("         CAFE DAPOER DIGITAL          ")
                        print("            STRUK PESANAN             ")
                        print("=" * 38)
                        print(f"ID Transaksi : {cari_id}")
                        print(f"Waktu        : {waktu_trx}")
                        print("-" * 38)
                        for i, row in hasil.iterrows():
                            print(f"{row['Jumlah']}x {row['Item_Pesanan']} = Rp {int(row['Harga']):,}")
                        print("-" * 38)
                        print(f"TOTAL        : Rp {total_struk:,}")
                        print("=" * 38)
                        input("\nTekan enter untuk kembali...")
                        break

        elif pilih == '0':
            return
        else:
            print("Pilihan tidak valid!!")
            input("Tekan enter...")

#sub menu daftar menu
def tampilkan_menu():
    df = pd.read_csv(FILE_MENU)
    kategori_list = ["Makanan", "Minuman", "Dessert"]

    for kat in kategori_list:
        print(f"\n--- [ {kat.upper()} ] ---")
        menu_kat = df[df['Kategori'].str.lower() == kat.lower()]
        for i, row in menu_kat.iterrows():
            print(f"{row['No']} - {row['Menu']} : Rp {int(row['Harga']):,}")


def baca_menu():
    tampilkan_menu()


def tambah_menu():
    tampilkan_menu()
    print("\nTambahkan menu baru:")
    print("(Enter / Ketik 'batal' pada nomor, kategori, atau menu untuk membatalkan)")
    print("(Kosongkan harga/Enter kolom harga untuk membatalkan)")
    
    nama_raw = input('Masukkan nama menu baru: ').strip()
    if nama_raw == '' or nama_raw.lower() == 'batal':
        print('Penambahan menu dibatalkan.')
        input('\ntekan enter untuk kembali')
        return

    nama_raw = nama_raw.title()

    kategori = input('Masukkan kategori: ').strip().lower()
    if kategori == '' or kategori == 'batal':
        print('Penambahan menu dibatalkan.')
        input('\ntekan enter untuk kembali')
        return

    no_raw = input('Masukkan nomor menu baru: ').strip()
    if no_raw == '' or no_raw == 'batal':
        print('Penambahan menu dibatalkan.')
        input('\ntekan enter untuk kembali')
        return
    
    harga_raw = input('Masukkan harga menu: ').strip()
    if harga_raw == '' or harga_raw.lower() == 'batal':
        print('Penambahan menu dibatalkan.')
        input('\ntekan enter untuk kembali')
        return

    try:
        harga = int(harga_raw)
    except ValueError:
        print('[!] Harga barang berupa angka bulat!')
        input('tekan enter untuk kembali ke kelola menu...')
        return

    df = pd.read_csv(FILE_MENU)

    try:
        harga = int(harga_raw)
    except ValueError:
        print("\n[!] Harga menu harus berupa angka!")
        input("Tekan enter untuk kembali...")
        return

    data_baru = pd.DataFrame([{'No': no_raw, 'Kategori': kategori, 'Menu': nama_raw, 'Harga': harga_raw}])
    df = pd.concat([df, data_baru], ignore_index=True)
    df.to_csv(FILE_MENU, index=False)
    print("\n[✓] Menu berhasil ditambahkan!")
    input("Tekan enter untuk kembali...")

def ubah_menu():
    tampilkan_menu()
    print("\nUbah menu yang sudah ada:")
    print("(Ketik 'batal' pada nomor, kategori, atau menu untuk membatalkan)")
    print("(Kosongkan harga/Enter kolom harga untuk membatalkan)")

    no_raw = input('Masukkan nomor menu yang ingin diubah: ').strip().lower()
    if no_raw == '' or no_raw == 'batal':
        print('pengubahan menu dibatalkan.')
        input('\ntekan enter untuk kembali')
        return

    kategori = input('Masukkan kategori yang ingin diubah: ').strip().lower()
    if kategori == '' or kategori == 'batal':
        print('pengubahan menu dibatalkan.')
        input('\ntekan enter untuk kembali')
        return

    nama_raw = input('Masukkan nama menu yang ingin diubah: ').strip().lower()
    if nama_raw == '' or nama_raw.lower() == 'batal':
        print('Pengubahan menu dibatalkan.')
        input('\ntekan enter untuk kembali')
        return

    nama_baru = input('Masukkan nama baru: ').strip().lower()
    if nama_baru == '' or nama_baru == 'batal':
        print('pengubahan menu dibatalkan.')
        input('\ntekan enter untuk kembali')
        return

    nama_baru = nama_baru.title()

    harga_raw = input('Masukkan harga baru: ').strip()
    if harga_raw == '' or harga_raw.lower() == 'batal':
        print('Pengubahan menu dibatalkan.')
        input('\ntekan enter untuk kembali')
        return

    try:
        harga = int(harga_raw)
    except ValueError:
        print('[!] Harga barang berupa angka bulat!')
        input('tekan enter untuk kembali ke kelola menu...')
        return

    df = pd.read_csv(FILE_MENU)

    mask = (df['No'].astype(str).str.strip() == no_raw) & (df['Kategori'].astype(str).str.strip().str.lower() == kategori.lower()) & (df['Menu'].astype(str).str.strip().str.lower() == nama_raw.lower())

    if df[mask].empty:
        print('\n[!] Menu atau kategori tidak ditemukan. Tidak ada perubahan!!')
    else:
        df.loc[mask, 'Menu'] = nama_baru
        df.loc[mask, 'Harga'] = harga
        df.to_csv(FILE_MENU, index=False)
        print('\nMenu berhasil diubah!')

    input('tekan enter untuk kembali..')


def hapus_menu():
    df = pd.read_csv(FILE_MENU, dtype=str)
    tampilkan_menu()
    
    nama_raw = input('Masukkan nama menu: ').strip()
    if nama_raw == '' or nama_raw.lower() == 'batal':
        print('Penghapusan menu dibatalkan.')
        input('\ntekan enter untuk kembali')
        return

    nama_raw = nama_raw.title()

    harga_raw = input('Masukkan harga menu: ').strip()
    if harga_raw == '' or harga_raw.lower() == 'batal':
        print('Penghapusan menu dibatalkan.')
        input('\ntekan enter untuk kembali')
        return

    try:
        harga = int(harga_raw)
    except ValueError:
        print('[!] Harga barang berupa angka bulat!')
        input('tekan enter untuk kembali ke kelola menu...')
        return

    no_hapus = input("\nMasukkan nomor menu yang ingin dihapus: ").strip()

    if (df['No'] == no_hapus).any():
        df = df[df['No'] != no_hapus]
        df.to_csv(FILE_MENU, index=False)
        print("\nMenu berhasil dihapus!")
    else:
        print("\n[!] Nomor menu tidak ditemukan!")

    input("Tekan enter untuk kembali...")


def df_kelola_daftar_menu():
    os.system('cls')
    print("=========================================")
    print("|          KELOLA DAFTAR MENU           |")
    print("=========================================")
    print()
    print('(1) tampilkan daftar menu')
    print('(2) tambah menu')
    print('(3) ubah menu')
    print('(4) hapus menu')
    print('(0) kembali')

    pilih = input('pilih menu (angka): ')
    if pilih == '1':
        os.system('cls')
        print("==============================")
        print("|        DAFTAR MENU         |")
        print("==============================")
        baca_menu()
        print()
        input('tekan enter untuk kembali')
        return df_kelola_daftar_menu()
    elif pilih == '2':
        os.system('cls')
        print("==============================")
        print("|         TAMBAH MENU        |")
        print("==============================")
        tambah_menu()
        print()
        return df_kelola_daftar_menu()
    elif pilih == '3':
        os.system('cls')
        print("==============================")
        print("|         UBAH MENU          |")
        print("==============================")
        print()
        ubah_menu()
        return df_kelola_daftar_menu()
    elif pilih == '4':
        os.system('cls')
        print("==============================")
        print("|       HAPUS MENU         |")
        print("==============================")
        print()
        hapus_menu()
        return df_kelola_daftar_menu()
    elif pilih == '0':
        os.system('cls')
        return
    else:
        print('input tidak sesuai!!!')
        input('tekan enter untuk kembali')
        return df_kelola_daftar_menu()


# crud keranjang belanja
def tampilkan_keranjang():
    if not keranjang:
        print("Keranjang belanja masih kosong!")
        return False
    else:
        total_bayar = 0
        for i, item in enumerate(keranjang, 1):
            print(f"{i}. {item['menu']} | {item['jumlah']} porsi | @Rp {item['harga_satuan']:,} | Subtotal: Rp {item['total']:,}")
            total_bayar += item['total']
        print("-" * 45)
        print(f"Total Bayar: Rp {total_bayar:,}")
        return True

def liat_keranjang():
    os.system('cls')
    print("==============================")
    print("|     ISI KERANJANG ANDA     |")
    print("==============================")
    tampilkan_keranjang()
    print()
    input('Tekan enter untuk kembali..')

def pesan_menu():
    while True:
        os.system('cls')
        print("==============================")
        print("|        PESAN MENU          |")
        print("==============================")
        baca_menu()
        print()
        
        pesanan = input('\nMasukkan nomor menu pesanan (Klik Enter untuk batal) : ').strip()
        df = pd.read_csv(FILE_MENU)
        menu_ditemukan = df[df['No'].astype(str).str.strip() == pesanan]
        
        if not menu_ditemukan.empty:
            nama_menu = menu_ditemukan['Menu'].values[0]
            harga_satuan = int(menu_ditemukan['Harga'].values[0])
            try:
                jumlah_pesanan = int(input('Untuk berapa porsi : '))
                if jumlah_pesanan <= 0:
                    print('\nJumlah porsi harus lebih dari 0!')
                    input('Tekan enter untuk coba lagi..')
                    continue
            except ValueError:
                print('\nMasukkan jumlah porsi berupa angka!')
                input('Tekan enter untuk coba lagi..')
                continue
            total_harga = harga_satuan * jumlah_pesanan
            keranjang.append({
                'menu': nama_menu,
                'harga_satuan': harga_satuan,
                'jumlah': jumlah_pesanan,
                'total': total_harga
            })
            print(f'\n Berhasil menambahkan {jumlah_pesanan} {nama_menu} ke keranjang!')
        elif pesanan == '':
            print('\nPemesanan dibatalkan!')
            input('Tekan enter untuk kembali..')
            break
        else:
            print('\nMenu tidak ditemukan di daftar menu!')
        
        tambah_lagi = input('\nMau tambah menu lagi? (y/t) : ').strip().lower()
        if tambah_lagi != 'y':
            print('\nPemesanan selesai! Kembali ke menu...')
            input('Tekan enter..')
            break

def ubah_keranjang():
    os.system('cls')
    print("==============================")
    print("|    UBAH PESANAN KERANJANG  |")
    print("==============================")
    print()
    if not tampilkan_keranjang():
        input('\nTekan enter untuk kembali..')
        return
    try:
        nomor = int(input('\nMasukkan nomor urut item yang ingin diubah (ketik 0 untuk kembali): '))
        if nomor == 0:
            return
        if 1 <= nomor <= len(keranjang):
            item = keranjang[nomor - 1]
            print(f"Mengubah pesanan: {item['menu']} (Jumlah sekarang: {item['jumlah']} porsi)")
            jumlah_baru = int(input('Masukkan jumlah porsi yang baru: '))
            
            if jumlah_baru > 0:
                item['jumlah'] = jumlah_baru
                item['total'] = item['harga_satuan'] * jumlah_baru
                print('\n Jumlah porsi pesanan berhasil diperbarui!')
            else:
                print('\nJumlah porsi harus lebih dari 0!')
        else:
            print('\nNomor item tidak valid!')
    except ValueError:
        print('\nMasukkan input angka yang benar!')
    input('\nTekan enter untuk kembali..')

def hapus_keranjang():
    os.system('cls')
    print("==============================")
    print("|   HAPUS PESANAN KERANJANG  |")
    print("==============================")
    print()
    if not tampilkan_keranjang():
        input('\nTekan enter untuk kembali..')
        return
    try:
        nomor = int(input('\nMasukkan nomor urut item yang ingin dihapus (0 untuk batal): '))
        if nomor == 0:
            return
        if 1 <= nomor <= len(keranjang):
            item_dihapus = keranjang.pop(nomor - 1)
            print(f"\n Berhasil menghapus '{item_dihapus['menu']}' dari keranjang!")
        else:
            print('\n[!] Nomor item tidak valid!')
    except ValueError:
        print('\n[!] Masukkan input angka yang benar!')
    input('\nTekan enter untuk kembali..')

def df_kelola_keranjang():
    while True:
        os.system('cls')
        print("=========================================")
        print("|          KELOLA KERANJANG             |")
        print("=========================================")
        print()
        print('(1) Lihat keranjang belanja ')
        print('(2) Tambah menu ke keranjang ')
        print('(3) Ubah jumlah pesanan ')
        print('(4) Hapus pesanan dari keranjang ')
        print('(0) Kembali')
        print()

        pilih = input('Pilih menu (angka): ').strip()
        if pilih == '1':
            liat_keranjang()
        elif pilih == '2':
            pesan_menu()
        elif pilih == '3':
            ubah_keranjang()
        elif pilih == '4':
            hapus_keranjang()
        elif pilih == '0':
            return
        else:
            print('Pilihan tidak valid!!')
            input('Tekan enter...')

def checkout():
    os.system('cls')
    print("==============================")
    print("|         CHECKOUT           |")
    print("==============================")
    print()
    if len(keranjang) == 0:
        print("Keranjang masih kosong!")
        input("Tekan enter...")
        return

    total = 0
    for item in keranjang:
        nama = item['menu']
        jumlah = item['jumlah']
        subtotal = item['total']
        print(f"{jumlah}x {nama} = Rp {subtotal:,}")
        total += subtotal
    print("-" * 30)
    print(f"TOTAL BAYAR : Rp {total:,}")

    pakai_voucher = input('\nPunya voucher ga? (y/t) : ').strip().lower()
    potongan = 0

    if pakai_voucher == 'y':
        df_voucher = pd.read_csv(FILE_VOUCHER)
        while True:
            kode_input = input("Masukkan kode voucher: ").strip().upper()
            voucher_cocok = df_voucher[df_voucher['Kode'].astype(str).str.strip().str.upper() == kode_input]

            if not voucher_cocok.empty:
                potongan = int(voucher_cocok['Potongan'].values[0])
                total = max(0, total - potongan)
                print(f'Voucher {kode_input} berlaku!! Potongan : Rp {potongan:,}')
                break
            else:
                print('Voucher tidak ditemukan!')
                coba_lagi = input('Mau coba masukkan kode voucher lagi? (y/t) : ').strip().lower()
                if coba_lagi != 'y':
                    break

        print(f'TOTAL BAYAR : Rp {total:,}')
        print('-' * 30)

    konfirmasi = input("\nLanjut bayar? (y/t) : ").lower()
    if konfirmasi == 'y':
        total_akhir = total
        while True:
            try:
                bayar = int(input(f"Masukkan uang pembayaran (Rp {total_akhir:,}): Rp "))
                if bayar < total_akhir:
                    print(f"Uang kurang Rp {total_akhir - bayar:,}. Silakan bayar dengan nominal yang cukup.")
                else:
                    kembalian = bayar - total_akhir

                    df_trx = pd.read_csv(FILE_TRANSAKSI)
                    nomor_urut = df_trx['ID'].nunique() + 1
                    id_trx = f"TRX-{nomor_urut:03d}"
                    waktu = datetime.now().strftime("%Y-%m-%d %H:%M")

                    for item in keranjang:
                        baris_baru = pd.DataFrame([{
                            'ID': id_trx,
                            'Waktu': waktu,
                            'Item_Pesanan': item['menu'],
                            'Jumlah': item['jumlah'],
                            'Harga': item['total']
                        }])
                        df_trx = pd.concat([df_trx, baris_baru], ignore_index=True)
                    df_trx.to_csv(FILE_TRANSAKSI, index=False)

                    print("\n" + "=" * 38)
                    print("         CAFE DAPOER DIGITAL          ")
                    print("            STRUK PESANAN             ")
                    print("=" * 38)
                    print(f"ID Transaksi  : {id_trx}")
                    print(f"Waktu         : {waktu}")
                    print("-" * 38)
                    for item in keranjang:
                        print(f"{item['jumlah']}x {item['menu']} = Rp {item['total']:,}")
                    print("-" * 38)
                    print(f"Total Akhir   : Rp {total_akhir:,}")
                    print(f"Uang Diterima : Rp {bayar:,}")
                    print(f"Kembalian     : Rp {kembalian:,}")
                    print("=" * 38)
                    print("Pembayaran berhasil! Terima kasih telah berkunjung!")
                    keranjang.clear()
                    break
            except ValueError:
                print("Masukkan nominal uang berupa angka!")
    else:
        print("Pesanan tetap disimpan di keranjang.")
    input("Tekan enter...")

def df_menucustomer():
    while True:
        os.system('cls')
        print('======================================================')
        print(f'|           MENU CUSTOMER - {nama_akun}             |')
        print('======================================================')
        print('(1) Pesan menu (Tambah ke Keranjang)')
        print('(2) Kelola keranjang belanja (Lihat / Ubah / Hapus)')
        print('(3) Checkout / Pembayaran')
        print('(0) Logout')
        pilih = input('Masukkan pilihan : ').strip()

        if pilih == '1':
            pesan_menu()
        elif pilih == '2':
            df_kelola_keranjang()
        elif pilih == '3':
            checkout()
        elif pilih == '0':
            keranjang.clear()
            return
        else:
            print('Pilihan tidak valid!!')
            input('Tekan enter...')

# Mulai Program
df_beranda()