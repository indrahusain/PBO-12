# Tugas Praktikum 11: Refactoring Code with SOLID Principles
**Mata Kuliah:** Pemrograman Berorientasi Objek - Praktikum (INF2143)  
**Universitas:** Universitas Muhammadiyah Kalimantan Timur

---

## 👤 Identitas Mahasiswa
* **Nama** : Rohmi ihsan
* **NIM** : 2411102441244
* **Kelas** : B

---

##  Deskripsi Tugas
Proyek ini adalah hasil refactoring dari sistem pendaftaran KRS (Kartu Rencana Studi) sederhana. Tujuan utama refactoring ini adalah mengubah kode yang kaku (rigid) menjadi fleksibel menggunakan prinsip **SOLID**, khususnya:
1.  **SRP (Single Responsibility Principle)**
2.  **OCP (Open/Closed Principle)**
3.  **DIP (Dependency Inversion Principle)**

### Skenario Refactoring
Sistem awal (hipotetis) menggunakan logika validasi yang menumpuk di dalam satu fungsi besar menggunakan banyak `if-else`. Sistem yang baru memecah validasi menjadi kelas-kelas terpisah yang independen.

---

## 🛠️ Analisis Penerapan SOLID
Berikut adalah penjelasan bagaimana prinsip SOLID diterapkan dalam kode ini:

### 1. Single Responsibility Principle (SRP)
* **Masalah:** Sebelumnya, logika validasi (cek SKS, cek Prasyarat) bercampur dengan logika pendaftaran.
* **Solusi:** Memisahkan setiap aturan validasi menjadi kelas tersendiri (`SksLimitRule`, `PrerequisiteRule`). Kelas `RegistrationService` sekarang hanya bertanggung jawab untuk mengelola alur pendaftaran, bukan memvalidasi detail aturannya.

### 2. Open/Closed Principle (OCP)
* **Masalah:** Menambah aturan baru biasanya mengharuskan kita mengedit kode lama (memodifikasi `if` statement), yang berisiko merusak fitur lain.
* **Solusi:** Dengan pola ini, jika ingin menambah aturan baru (misalnya Cek Jadwal Bentrok), kita cukup membuat class baru (`JadwalBentrokRule`) tanpa menyentuh/mengubah satu baris pun kode di dalam `RegistrationService`.

### 3. Dependency Inversion Principle (DIP)
* **Masalah:** Kelas tingkat tinggi (`RegistrationService`) bergantung pada kelas tingkat rendah yang konkret.
* **Solusi:** `RegistrationService` kini bergantung pada abstraksi (Interface) bernama `IValidationRule`. Ia tidak peduli aturan apa yang dijalankan, selama aturan tersebut mematuhi kontrak `validate()`.

---

## 🚀 Cara Menjalankan Program
Pastikan Python sudah terinstal, lalu jalankan perintah berikut di terminal:

```bash
python sistem_krs.py