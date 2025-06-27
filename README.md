# 💸 Sepolia ETH Sender GUI

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Aplikasi GUI sederhana yang dibuat dengan Python dan Tkinter untuk mengirim ETH di jaringan **Sepolia Testnet** secara massal. Ditenagai oleh Alchemy dan Web3.py, aplikasi ini memudahkan developer dan tester untuk mendistribusikan ETH ke banyak alamat sekaligus.


---

## 🚀 Fitur Utama

- ✅ **Import Wallet Fleksibel**: Langsung impor wallet Anda menggunakan *mnemonic phrase* (BIP-39).
- ✅ **Daftar Alamat Massal**: Impor ratusan alamat tujuan dari file `.txt` dengan mudah.
- ✅ **Pengiriman Multi-Alamat**: Kirim ETH ke semua alamat dalam daftar dengan satu kali klik.
- ✅ **Estimasi Gas Cerdas**: Pilih prioritas transaksi (Rendah, Pasar, Agresif) dan biarkan aplikasi mengurus gasnya.
- ✅ **Monitoring Real-time**: Lacak status transaksi dan buka detailnya di Etherscan langsung dari aplikasi.
- ✅ **Pencatatan Otomatis**: Semua aktivitas transaksi dicatat secara otomatis ke dalam file `log.csv`.
- ✅ **Antarmuka Intuitif**: GUI yang bersih dan sederhana dibangun menggunakan Tkinter.

---

## 🔧 Persiapan Awal

Sebelum memulai, pastikan Anda memiliki:
- Python 3.7 atau versi yang lebih baru
- `pip` untuk instalasi paket

### ⚙️ Instalasi

1.  Clone repositori ini:
    ```bash
    git clone https://github.com/blockscrew/Sepolia-ETH-Sender-GUI.git
    cd sepolia-eth-sender-gui
    ```

2.  Instal semua dependensi yang diperlukan:
    ```bash
    pip install -r requirements.txt
    ```

### 🔑 Konfigurasi Alchemy API Key

Aplikasi ini memerlukan API Key dari [Alchemy](https://alchemy.com) untuk terhubung ke jaringan Sepolia.

1.  Daftar atau Login ke akun [Alchemy](https://alchemy.com).
2.  Klik **"Create App"** dan isi detail berikut:
    -   **Name**: `Sepolia Sender` (atau nama lain)
    -   **Chain**: `Ethereum`
    -   **Network**: `Sepolia`
3.  Setelah aplikasi dibuat, klik **"View Key"** dan salin **HTTPS API Key**.
4.  Buka file `main.py` dan ganti `YOUR_API_KEY` dengan kunci yang baru Anda salin.
    ```python
    # Ganti bagian ini di dalam file main.py
    ALCHEMY_URL = "https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY"
    ```

---

## ▶️ Cara Menjalankan

1.  **Siapkan Wallet**: Buat file `wallet.txt` dan isi dengan 12 kata *mnemonic phrase* Anda.
    *Contoh `wallet.txt`:*
    ```
    word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12
    ```

2.  **Siapkan Alamat Tujuan**: Buat file `addresses.txt` dan isi dengan semua alamat penerima (satu alamat per baris).
    *Contoh `addresses.txt`:*
    ```
    0x1111111111111111111111111111111111111111
    0x2222222222222222222222222222222222222222
    ```

3.  **Jalankan Aplikasi**:
    ```bash
    python main.py
    ```

---

## 🪟 Panduan Penggunaan GUI

Berikut adalah panduan singkat untuk setiap tombol pada antarmuka aplikasi.

| Tombol / Fitur | Fungsi |
| :--- | :--- |
| 📂 **Import Wallet** | Memuat *mnemonic phrase* dari `wallet.txt` dan menampilkan alamat wallet. |
| ⟳ **Refresh Saldo** | Memperbarui dan menampilkan saldo ETH terkini dari jaringan Sepolia. |
| 📂 **Import Addresses** | Memuat daftar alamat tujuan dari `addresses.txt`. |
| 🗑️ **Hapus Address** | Menghapus daftar alamat yang sudah di-load dari memori. |
| 💸 **Kirim ETH** | Memulai proses pengiriman ETH ke semua alamat yang terdaftar. |
| 🔗 **TX Explorer Terakhir** | Membuka link Etherscan untuk transaksi terakhir yang dikirim. |
| 📋 **Status Transaksi** | Menampilkan log dan status dari setiap transaksi yang diproses. |

---

## 📜 File Output: `log.csv`

Setiap kali Anda mengirim transaksi, sebuah catatan akan otomatis ditambahkan ke `log.csv`. File ini berguna untuk melacak riwayat pengiriman.

**Format Log:**
- **Nomor**: Urutan transaksi.
- **Alamat Tujuan**: Alamat penerima ETH.
- **Jumlah ETH**: Total ETH yang dikirim.
- **Status**: ✅ Berhasil / ⏳ Pending / ❌ Gagal.
- **URL Explorer**: Link Etherscan untuk verifikasi.

---

## ⚠️ Peringatan Penting

-   **Hanya Untuk Tujuan Edukasi & Testing**: Skrip ini dirancang untuk tujuan pembelajaran dan pengujian.
-   **Gunakan Jaringan Testnet**: Selalu gunakan di jaringan **Sepolia**. Dapatkan ETH gratis dari faucet seperti [sepoliafaucet.com](https://sepoliafaucet.com).
-   **JANGAN GUNAKAN WALLET UTAMA**: Untuk keamanan, selalu gunakan wallet baru yang dibuat khusus untuk development atau testing. Jangan pernah menggunakan *seed phrase* dari wallet utama Anda.
