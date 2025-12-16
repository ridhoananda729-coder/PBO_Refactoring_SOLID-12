# PBO_Refactoring_SOLID-12
## Studi Kasus: Refactoring Sistem Validasi Registrasi Mahasiswa
repositori ini berisi perbandingan kode sebelum (registration_bad.py) dan sesudah (registration_solid.py`) refactoring untuk studi kasus Validasi Registrasi Mahasiswa
### analisis pelanggaran prinsip SOLID (Kode: registration_bad.py)
[cite_start]Kelas registrationValidator pada kode awal adalah contoh dari "God Class" [cite: 17] karena menangani berbagai tanggung jawab dalam satu method, menyebabkan pelanggaran prinsip SOLID.

#### 1. pelanggaran single responsibility principle (SRP)
* [cite_start]**definisi SRP:** sebuah class harus memiliki satu, dan hanya satu, alasan untuk berubah.
* **Pelanggaran:** Kelas `registrationValidator` bertanggung jawab atas validasi batas SKS dan validasi prasyarat.

#### 2. pelanggaran open/closed principle (OCP)
* [cite_start]**Definisi OCP:** class harus terbuka untuk ekstensi, tetapi tertutup untuk modifikasi[cite: 25].
* **Pelanggaran:** penambahan aturan validasi baru (misalnya, validasi Pembayaran SPP) akan memaksa pengembang untuk memodifikasi method `validate_registration()` dan menambahkan blok elif baru

#### 3. pelanggaran Dependency Inversion Principle (DIP)
* [cite_start]**definisi DIP:** modul high-level harus bergantung pada abstraksi (Kontrak), bukan pada Implementasi konkret (detail low-level).
* **Pelanggaran:** kelas *high-level* (`RegistrationValidator`) bergantung langsung pada detail implementasi yang spesifik, yaitu *string* `rule_type` dan logika $if/else$ di dalamnya
  
### 🚀 hasil refactoring (kode: `registration_solid.py`)
Kode registration_solid.py berhasil menerapkan:
**SRP:** tanggung jawab dipisahkan menjadi sksLimitrule, PrerequisiteRule, dan registrationService
[cite_start]**DIP/OCP:** Menggunakan Abstraksi (IValidationRule) [cite: 26] [cite_start]dan **dependency injection**.penambahan TuitionPaymentRule dapat dilakukan tanpa mengubah kode pada kelas RegistrationService (Pembuktian OCP)
