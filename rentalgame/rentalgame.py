import mysql.connector
import pyfiglet
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from colorama import Fore, Style, init
import time
from time import sleep

# Inisialisasi colorama
init(autoreset=True)

# Koneksi ke MySQL
Connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",  # Ganti dengan password MySQL Anda jika diperlukan
    port="3306",
    database="rental_game"
)
cursor = Connection.cursor()

# Gambar ASCII untuk tampilan awal

# Fungsi untuk banner bergerak horizontal tanpa menghapus layar dan kembali terlihat setelah animasi
def display_banner():
    banner = '''
  _____     __  __ __  ____   _____  ______  ______________________________
        |  __ \ / ____|/ ____/ |   ___|
        | |__) | (___ | (___   |  |____
        |  ___/ \___ \ \___ \  |  _____|
        | |     ____) |____) | | |
        |_|    |_____/|_____/  |_| 
         
        ____  _____     ____   _____                            
 / ___/____/ /_/ // ____/ / ___/____/ __ \ / ___/      
/ /__/ __  / __  // /__    \__ \/ __  / /_/ // /__  
\___/ \__/  \__,_/ \___/   ___/ \__/  \____/ \___/  
                                                     
         ____   _____  ______  ________
        |  __ \ / ____|/ ____/ |   ___|
        | |__) | (___ | (___   |  |____
        |  ___/ \___ \ \___ \  |  _____|
        | |     ____) |____) | | |
        |_|    |_____/|_____/  |_| 
 ______________________________________________________________________       
    '''

    console = Console()
    lines = banner.splitlines()  # Split banner into lines
    width = console.size.width   # Get console width

    # Animasi pergerakan horizontal
    for offset in range(width):
        console.clear()
        for line in lines:
            console.print(" " * offset + line, style="bold green")  # Geser teks dengan spasi
        time.sleep(0.01)  # Waktu jeda animasi

    # Menampilkan kembali banner setelah animasi selesai
    console.clear()
    console.print(Panel(Text(banner, style="bold green"), expand=False))
# Menjalankan fungsi untuk melihat hasilnya
display_banner()




# Fungsi untuk banner "Terima Kasih"
def banner_terima_kasih():
    banner = '''
  _______              _     _                _                 
|__   __|            | |   (_)              | |                
    | | ___  ___ _ __| |__  _ _ __   __ _ ___| |_ ___ _ __ ___  
    | |/ _ \/ __| '_ \| '_ \| | '_ \ / _` / __| __/ _ \ '__/ __| 
    | |  __/\__ \ | | | | | | | | | (_| \__ \ ||  __/ |  \__ \ 
    |_|\___||___/_| |_|_|_| |_|\__, |___/\__\___|_|  |___/ 
                               __/ |                       
                              |___/                        
4
                                                            
    '''
    console = Console()
    lines = banner.splitlines()  # Split banner into lines
    width = console.size.width   # Get console width

    # Animasi pergerakan horizontal
    for offset in range(width):
        console.clear()
        for line in lines:
            console.print(" " * offset + line, style="bold green")  # Geser teks dengan spasi
        time.sleep(0.01) 
    
    console.clear()
    console.print(Panel(Text(banner, style="bold magenta"), expand=False))


# Fungsi untuk animasi loading
def loading():
    console = Console()
    for _ in range(3):
        console.print(Fore.YELLOW + "Mempersiapkan aplikasi...", end="\r")
        time.sleep(1)
        console.print("                         ", end="\r")
        time.sleep(1)

# Fungsi animasi untuk proses penambahan data
def animate_adding():
    console = Console()
    for i in range(3):
        console.print(Fore.CYAN + "Menambahkan data", end="\r")
        time.sleep(0.5)
        console.print("                 ", end="\r")
        time.sleep(0.5)

# Fungsi animasi untuk keberhasilan
def success_animation(message):
    console = Console()
    for _ in range(3):
        console.print(Fore.GREEN + message, end="\r")
        time.sleep(0.5)
        console.print("                         ", end="\r")
        time.sleep(0.5)

# Fungsi animasi untuk kegagalan
def error_animation(message):
    console = Console()
    for _ in range(3):
        console.print(Fore.RED + message, end="\r")
        time.sleep(0.5)
        console.print("                         ", end="\r")
        time.sleep(0.5)

# Fungsi untuk menambahkan pelanggan
def tambah_pelanggan():
    nama = input(Fore.CYAN + "Nama Pelanggan: ")
    kontak = input(Fore.CYAN + "Kontak Pelanggan: ")
    if nama and kontak:
        try:
            animate_adding()
            cursor.execute("INSERT INTO pelanggan (nama, kontak) VALUES (%s, %s)", (nama, kontak))
            Connection.commit()
            success_animation(f"Pelanggan '{nama}' berhasil ditambahkan.")
        except mysql.connector.Error as err:
            error_animation(f"Error: {err}")
    else:
        error_animation("Nama dan Kontak harus diisi!")

def lihat_pelanggan():
    
    cursor.execute("SELECT * FROM pelanggan")
    pelanggan = cursor.fetchall()
    
    console = Console()
    console.print(Fore.YELLOW + "lihat pelanggan...", end="\r")
    time.sleep(2)
   

    # Membuat dan menampilkan tabel
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("ID", justify="center")
    table.add_column("Nama Pelanggan", justify="center")
    table.add_column("Kontak Pelanggan", justify="center")

    for p in pelanggan:
        table.add_row(str(p[0]), str(p[1]), str(p[2]))

    console.print(table)
    
def hapus_pelanggan():
    try:
        lihat_pelanggan()  # Tampilkan pelanggan untuk referensi ID
        pelanggan_id = input(Fore.CYAN + "Masukkan ID Pelanggan yang akan dihapus: ")
        
        if pelanggan_id:
            cursor.execute("DELETE FROM pelanggan WHERE id = %s", (pelanggan_id,))
            Connection.commit()
            if cursor.rowcount > 0:
                success_animation(f"Pelanggan dengan ID {pelanggan_id} berhasil dihapus.")
            else:
                error_animation(f"Pelanggan dengan ID {pelanggan_id} tidak ditemukan.")
        else:
            error_animation("ID tidak boleh kosong!")
    except mysql.connector.Error as err:
        error_animation(f"Error: {err}")
        
# Fungsi untuk menambahkan transaksi
def tambah_transaksi():
    kontak_pelanggan = input(Fore.CYAN + "kontak pelanggan: ")
    game_konsol = input(Fore.CYAN + "Nama Game/Konsol: ")
    tanggal_sewa = input(Fore.CYAN + "Tanggal Sewa (YYYY-MM-DD): ")
    tanggal_kembali = input(Fore.CYAN + "Tanggal Kembali (YYYY-MM-DD): ")

    if kontak_pelanggan and game_konsol and tanggal_sewa and tanggal_kembali:
        try:
            animate_adding()
            tanggal_sewa = datetime.strptime(tanggal_sewa, "%Y-%m-%d")
            tanggal_kembali = datetime.strptime(tanggal_kembali, "%Y-%m-%d")
            denda = 0
            if tanggal_kembali > datetime.now():
                denda = (tanggal_kembali - datetime.now()).days * 500

            cursor.execute("""
                INSERT INTO transaksi (pelanggan_id, game_konsol, tanggal_sewa, tanggal_kembali, denda)
                VALUES (%s, %s, %s, %s, %s)
            """, (kontak_pelanggan, game_konsol, tanggal_sewa, tanggal_kembali, denda))
            Connection.commit()
            success_animation(f"Transaksi untuk pelanggan ID {kontak_pelanggan} berhasil ditambahkan.")
        except mysql.connector.Error as err:
            error_animation(f"Error: {err}")
        except ValueError:
            error_animation("Format tanggal salah. Gunakan format YYYY-MM-DD.")
    else:
        error_animation("Semua data transaksi harus diisi!")

# Fungsi untuk menampilkan transaksi dalam format tabel dengan animasi
def tampilkan_transaksi():
    cursor.execute("SELECT * FROM transaksi")
    transaksi = cursor.fetchall()

    # Animasi untuk proses menampilkan data
    console = Console()
    console.print(Fore.YELLOW + "Menampilkan transaksi...", end="\r")
    time.sleep(2)

    # Membuat dan menampilkan tabel
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("ID", justify="center")
    table.add_column("Kontak pelanggan", justify="center")
    table.add_column("Game/Konsol", justify="center")
    table.add_column("Tanggal Sewa", justify="center")
    table.add_column("Tanggal Kembali", justify="center")
    table.add_column("Denda", justify="center")

    for t in transaksi:
        table.add_row(str(t[0]), str(t[1]), t[2], str(t[3]), str(t[4]), f"Rp {t[5]}")

    console.print(table)
    
# Fungsi untuk menampilkan halaman utama yang keren
def tampilkan_halaman_utama():
    console = Console()
    panel_header = Panel(
        Text("Aplikasi Rental Game & Konsol", style="bold white on blue"), 
        title="Selamat datang", 
        subtitle="Sistem Manajemen Rental Game", 
        expand=False
    )
    console.print(panel_header)
    console.print(Fore.YELLOW + "\n--- Pilih Menu ---", style="bold white on blue")
    console.print(Fore.CYAN + "1. Tambah Pelanggan")
    console.print(Fore.CYAN + "2. Lihat Pelanggan")
    console.print(Fore.CYAN + "3. Tambah Transaksi")
    console.print(Fore.CYAN + "4. Tampilkan Transaksi")
    console.print(Fore.CYAN + "5. Hapus Pelanggan")
    console.print(Fore.CYAN + "6. Keluar")

# Perbarui menu() untuk menangani opsi hapus
def menu():
    while True:
        tampilkan_halaman_utama()

        pilihan = input(Fore.YELLOW + "Pilih menu (1/2/3/4/5/6/): ")

        if pilihan == '1':
            tambah_pelanggan()
        elif pilihan == '2':
            lihat_pelanggan()
        elif pilihan == '3':
            tambah_transaksi()
        elif pilihan == '4':
            tampilkan_transaksi()
        elif pilihan == '5':
            hapus_pelanggan()
        elif pilihan == '6':
            banner_terima_kasih()
            break
        else:
            error_animation("Pilihan tidak valid! Silakan pilih menu yang benar.")
# Menjalankan aplikasi
display_banner()
loading()  # Menambahkan animasi loading
menu()

# Menutup koneksi
cursor.close()
Connection.close()








