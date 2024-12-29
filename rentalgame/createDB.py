import mysql.connector

# Membuat koneksi ke MySQL
Connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",  # Ganti dengan password MySQL Anda jika diperlukan
    port="3306"
)

cursor = Connection.cursor()

# Mengecek apakah koneksi berhasil
if Connection:
    print("Berhasil terhubung ke Database")

    # Membuat database jika belum ada
    cursor.execute("CREATE DATABASE IF NOT EXISTS rental_game")
    print('Database "rental_game" berhasil dibuat atau sudah ada')

    # Menggunakan database yang baru dibuat
    cursor.execute("USE rental_game")
    
 # Membuat tabel pelanggan
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pelanggan (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nama VARCHAR(255),
            kontak VARCHAR(50)
        )
    ''')
    print('Tabel "pelanggan" berhasil dibuat')

    # Membuat tabel transaksi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transaksi (
            id INT AUTO_INCREMENT PRIMARY KEY,
            pelanggan_id INT,
            game_konsol VARCHAR(255),
            tanggal_sewa DATE,
            tanggal_kembali DATE,
            denda INT DEFAULT 0,
            FOREIGN KEY (pelanggan_id) REFERENCES pelanggan(id)
        )
    ''')
    print('Tabel "transaksi" berhasil dibuat')

# Menampilkan daftar database
cursor.execute("SHOW DATABASES")
databases = cursor.fetchall()
print("\nDaftar Databases:")
for db in databases:
    print(db)

# Menutup koneksi
cursor.close()
Connection.close()
