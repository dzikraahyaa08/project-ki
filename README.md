# Tugas Besar Keamanan Informasi (UTS & UAS)
## Sistem: E-Commerce "Luxury Store" (Penerapan Konsep Keamanan 5A)

Repositori ini memuat berkas lengkap untuk pemenuhan **Tugas Besar Mata Kuliah Keamanan Informasi**, yang mencakup implementasi nyata kerangka kerja **5A (Authentication, Authorization, Accounting, Auditing, Availability & Assurance)** pada sistem e-commerce barang mewah (*Luxury Store*).

---

### Struktur Berkas & Dokumen

```text
├── DOKUMENTASI_TUGAS_BESAR_KEAMANAN_INFORMASI.docx  # Laporan Utama Sistem & Analisis 5A (Word)
├── DOKUMENTASI_LENGKAP_DAN_KEAMANAN_A5.md           # Laporan Utama Sistem & Analisis 5A (Markdown)
├── FORM_PEMBAGIAN_TUGAS.docx                        # Form Pembagian Tugas Kelompok (Word)
├── FORM_PEMBAGIAN_TUGAS.md                          # Form Pembagian Tugas Kelompok (Markdown)
├── FORM_ANGGOTA_TIDAK_BEKERJA.docx                  # Form Evaluasi Anggota / Kontribusi Tim (Word)
├── FORM_ANGGOTA_TIDAK_BEKERJA.md                    # Form Evaluasi Anggota / Kontribusi Tim (Markdown)
├── database.sql                                     # Skema Basis Data Relasional 3NF + Tabel Keamanan 5A
├── generate_docx.py                                 # Generator Pembuat File Word Otomatis
└── apk belanja/                                     # Source Code Frontend Web Aplikasi (Vue 3 + Vuetify)
    ├── src/
    │   ├── services/
    │   │   ├── security.js                          # Modul Keamanan 5A (Brute-Force Lockout, Logger, Anti-XSS)
    │   │   └── api.js                               # Abstraksi REST API & Auto Bearer Token Injection
    │   ├── views/
    │   │   ├── Login.vue                            # Form Login Admin + Brute-Force Lockout Countdown Timer
    │   │   ├── AuditLogs.vue                        # Halaman Pusat Audit Keamanan (Filter Severity, Export CSV)
    │   │   ├── Dashboard.vue                        # Dashboard Admin + Widget Status Integritas 5A
    │   │   ├── Storefront.vue                       # Katalog Belanja Pelanggan & Cart Checkout
    │   │   ├── Products.vue                         # Manajemen Produk + Event Logging
    │   │   ├── Brands.vue                           # Manajemen Brand Kategori
    │   │   ├── Orders.vue                           # Manajemen Pesanan Pelanggan
    │   │   └── Users.vue                            # Manajemen Pengguna & Tingkat Membership
    │   └── router/
    │       └── index.js                             # Vue Router Guard (RBAC Protection)
    └── package.json
```

---

### Pemetaan Konsep 5A pada Sistem

1. **Authentication (Autentikasi)**:
   * Verifikasi kredensial pengguna (Username & Password hash salted BCrypt).
   * Proteksi **Brute-Force Rate Limiting**: Jika login gagal 3 kali, akun dikunci sementara selama 60 detik dengan hitung mundur (*countdown timer*) visual.
2. **Authorization (Otorisasi)**:
   * Penegakan *Role-Based Access Control* (RBAC) pada rute internal admin menggunakan *Navigation Guard* (`router.beforeEach`).
   * Pencegahan akses tidak sah ke URL `/admin/*` tanpa token otentikasi.
3. **Accounting (Pencatatan Aktivitas)**:
   * Perekaman otomatis seluruh peristiwa sistem ke dalam rekam jejak (*log*): `AUTH_LOGIN_SUCCESS`, `AUTH_LOGIN_FAILED`, `AUTH_BRUTE_FORCE_LOCKOUT`, `PRODUCT_CREATE`, `USER_UPDATE`, `USER_DELETE`, dan `ORDER_STATUS_UPDATE`.
4. **Auditing (Pemeriksaan & Evaluasi Keamanan)**:
   * Konsol interaktif **Audit Keamanan (A5)** di panel admin.
   * Filter tingkat keparahan (*Severity*: Info, Success, Warning, Danger) dan kategori 5A.
   * Tombol **Export CSV** untuk menghasilkan berkas audit resmi bagi kebutuhan kepatuhan (*compliance*).
5. **Availability & Assurance (Ketersediaan Layanan & Jaminan Integritas)**:
   * Sanitasi karakter masukan (`sanitizeInput`) untuk mencegah celah *Cross-Site Scripting* (XSS).
   * Penanganan galat terstandar tanpa mengekspos informasi sensitif server (*Anti-Information Disclosure*).

---

### Cara Menjalankan Aplikasi Web

1. **Prasyarat**: Node.js v18+ terpasang di komputer.
2. Masuk ke direktori web:
   ```bash
   cd "apk belanja"
   ```
3. Install dependensi (jika belum terpasang):
   ```bash
   npm install
   # atau
   pnpm install
   ```
4. Jalankan server lokal:
   ```bash
   npm run dev
   ```
5. Buka peramban di: `http://localhost:5173`

---

### Cara Import Database

1. Buka MySQL Client / phpMyAdmin / DBeaver / Navicat.
2. Buat database baru bernama `luxury_store_db` atau langsung jalankan script:
   ```bash
   mysql -u root -p < database.sql
   ```
3. Seluruh tabel relasional (`users`, `brands`, `products`, `orders`, `order_items`, `audit_logs`, `login_attempts`) beserta data awal (*seed data*) akan otomatis terpasang.
