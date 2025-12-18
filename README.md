# [INF2143] Proyek SOLID OOP Python
## Pertemuan 12: Dokumentasi dan Version Control

### Deskripsi Proyek
Proyek ini mendemonstrasikan implementasi prinsip SOLID (SRP, OCP, DIP) pada **Sistem Validasi Registrasi Mahasiswa**. Sistem ini dirancang untuk memvalidasi rencana studi mahasiswa (FRS/KRS) menggunakan pendekatan *Abstraction* (Interface) dan *Dependency Injection*, serta dilengkapi dengan dokumentasi (Docstrings) dan pencatatan sistem (Logging).

### Struktur File
- `registration_solid.py`: Kode utama sistem registrasi yang mencakup Model, Interface Rule, Implementasi Validasi (SKS, Prasyarat, Jadwal), dan Service Koordinator. File ini sudah dilengkapi Logging dan Docstrings.
- `README.md`: Dokumen penjelasan proyek ini.

### Cara Menjalankan
1. Pastikan Python 3.x terinstal.
2. Jalankan file utama dari terminal:
   ```bash
   python refactor_solid.py
   
### Penjelasan Sistem Validasi Mahasiswa
Sistem ini menggunakan pola desain yang fleksibel di mana `RegistrationService` tidak memvalidasi aturan secara langsung, melainkan mendelegasikannya ke daftar aturan yang mengikuti kontrak `IValidationRule`.

Fitur validasi mencakup:
1.  **Validasi Batas SKS (`SksLimitRule`)**: Memastikan total SKS yang diambil mahasiswa tidak melebihi batas (misal: 24 SKS).
2.  **Validasi Prasyarat (`PrerequisiteRule`)**: Memastikan mahasiswa sudah lulus mata kuliah prasyarat sebelum mengambil mata kuliah lanjut.
3.  **Validasi Jadwal (`JadwalBentrokRule`)**: Mendeteksi secara otomatis jika ada dua mata kuliah yang memiliki irisan waktu (bentrok) pada hari yang sama.

Semua proses validasi kini tercatat melalui **Logging** (bukan print biasa), sehingga level urgensi (INFO, WARNING, ERROR) dan waktu kejadian dapat terpantau dengan jelas di terminal.

### Cara Menjalankan
1. Pastikan Python 3.x terinstal.
2. Jalankan file utama dari terminal:
   ```bash
   python Sistem_Validasi_Registrasi_Mahasiswa.py
   