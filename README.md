# Otomasi Absen ESS Mastersystem

Script ini digunakan untuk melakukan pengisian roster kehadiran secara otomatis pada portal ESS Mastersystem. Script ini menggunakan Selenium untuk mengotomasi interaksi browser.

## Fitur
- Login otomatis ke portal ESS.
- Navigasi otomatis ke halaman Roster.
- Pengisian rentang tanggal (From - To).
- Pengisian detail kehadiran ("Hadir") secara otomatis untuk baris yang memiliki jam kerja standar (08:00 - 17:00).
- Penanganan sinkronisasi postback web ASP.NET.

## Prasyarat (Requirements)

Sebelum menjalankan script, pastikan Anda sudah menginstal:
1. **Python 3.x**
2. **Google Chrome** (Browser yang didukung)
3. **Library Python**:
   - `selenium`
   - `webdriver-manager`

Anda bisa menginstal library yang dibutuhkan dengan menjalankan perintah berikut di terminal:
```bash
pip install selenium webdriver-manager
```

## Cara Menjalankan

1. Buka file `absen.py` menggunakan text editor (VS Code, Notepad++, dll).
2. Sesuaikan konfigurasi pada bagian `--- CONFIG ---` (lihat bagian [Yang Perlu Diganti](#yang-perlu-diganti)).
3. Buka terminal atau command prompt di folder tempat file `absen.py` berada.
4. Jalankan script dengan perintah:
   ```bash
   python absen.py
   ```

## Yang Perlu Diganti

Cari baris-baris berikut di dalam file `absen.py` dan ganti nilainya sesuai dengan data Anda:

| Variabel | Keterangan | Contoh Nilai |
| :--- | :--- | :--- |
| `USERNAME` | Username login ESS Anda | `"nama.user"` |
| `PASSWORD` | Password login ESS Anda | `"password123"` |
| `TGL_FROM` | Tanggal mulai roster (Format: MM/DD/YYYY) | `"05/01/2026"` |
| `TGL_TO` | Tanggal akhir roster (Format: MM/DD/YYYY) | `"05/31/2026"` |

## Catatan Penting
- **Chrome Profile**: Script ini akan membuat folder `selenium_profile` di direktori yang sama. Folder ini digunakan untuk menyimpan session agar Anda tidak perlu login ulang setiap kali script dijalankan.
- **Waktu Tunggu**: Script ini menggunakan banyak jeda waktu (`time.sleep`) untuk memastikan sistem ESS (yang berbasis ASP.NET) selesai memproses data. Jangan menutup browser atau menekan tombol apapun saat script sedang berjalan kecuali jika terjadi error.
- **Jam Kerja**: Script secara otomatis melewati (skip) baris yang jam kerjanya **bukan** 08:00 - 17:00 (misalnya hari libur atau shift berbeda).
