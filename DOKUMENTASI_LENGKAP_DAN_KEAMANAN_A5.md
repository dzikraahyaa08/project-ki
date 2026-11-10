# DOKUMENTASI SISTEM & IMPLEMENTASI KONSEP KEAMANAN 5A
## TUGAS BESAR KEAMANAN INFORMASI (UTS & UAS)
### SISTEM E-COMMERCE: "LUXURY STORE"

---

## DAFTAR ISI
1. [BAB I: GAMBARAN UMUM SISTEM](#bab-i-gambaran-umum-sistem)
   - 1.1 Latar Belakang & Deskripsi Aplikasi
   - 1.2 Tech Stack & Arsitektur Sistem
   - 1.3 Daftar Modul & Fitur Aplikasi
2. [BAB II: PENJELASAN KONSEP 5A PADA SETIAP PROSES APLIKASI](#bab-ii-penjelasan-konsep-5a-pada-setiap-proses-aplikasi)
   - 2.1 Definisi Konsep Keamanan 5A
   - 2.2 Pemetaan 5A pada Proses Login & Autentikasi Pengguna
   - 2.3 Pemetaan 5A pada Proses Otorisasi Akses Panel Admin (RBAC)
   - 2.4 Pemetaan 5A pada Proses Manajemen Data (Produk, Merek, Pengguna)
   - 2.5 Pemetaan 5A pada Proses Transaksi Belanja & Checkout Pelanggan
   - 2.6 Pemetaan 5A pada Modul Pusat Audit Keamanan (Security Audit Trail)
   - 2.7 Matriks Ringkasan Implementasi 5A
3. [BAB III: DOKUMENTASI KEAMANAN SISTEM & MITIGASI KERENTANAN](#bab-iii-dokumentasi-keamanan-sistem--mitigasi-kerentanan)
   - 3.1 Mitigasi OWASP Top 10 Web Vulnerabilities
   - 3.2 Threat Modeling & Strategi Pertahanan
   - 3.3 Mekanisme Kriptografi & Proteksi Token Sesi
4. [BAB IV: SPESIFIKASI DAN SKEMA BASIS DATA](#bab-iv-spesifikasi-dan-skema-basis-data)
   - 4.1 Diagram Hubungan Entitas (ERD)
   - 4.2 Kamus Data (Data Dictionary)
   - 4.3 Kontrol Keamanan pada Level Database
5. [BAB V: PANDUAN DAN SIMULASI WAWANCARA DOSEN (INTERVIEW PREP)](#bab-v-panduan-dan-simulasi-wawancara-dosen-interview-prep)
   - 5.1 Tips Menghadapi Wawancara Individu
   - 5.2 Bank Soal dan Kunci Jawaban Konsep 5A
   - 5.3 Skenario Pertanyaan Pengujian Live Demo Sistem

---

## BAB I: GAMBARAN UMUM SISTEM

### 1.1 Latar Belakang & Deskripsi Aplikasi
**Luxury Store** adalah platform e-commerce berbasis web modern yang dirancang khusus untuk transaksi barang-barang bernilai tinggi (*high-value luxury goods*), seperti jam tangan mewah, tas desainer, perhiasan, dan pakaian premium. Karena menangani produk bernilai jutaan hingga ratusan juta rupiah serta data sensitif identitas pelanggan, aspek **Keamanan Informasi** merupakan prioritas paling fundamental dalam perancangan aplikasi ini.

Aplikasi ini dibangun untuk memenuhi standar tata kelola keamanan informasi dan kontrol akses yang ketat, mengadopsi prinsip **5A (Authentication, Authorization, Accounting, Auditing, Availability/Assurance)** pada setiap siklus transaksi dan pengelolaan data.

### 1.2 Tech Stack & Arsitektur Sistem
Sistem mengadopsi arsitektur *Decoupled Client-Server* (Frontend-Backend Terpisah) dengan standar industri:
* **Frontend Web**: Vue.js 3 (Composition API `<script setup>`), Vite Build Engine, Vuetify 3 (Material Design Component Library), Vue Router 4 (Client-side Routing & Navigation Guards).
* **Komunikasi Data**: RESTful API berbasis JSON over HTTPS/TLS, dengan abstraksi HTTP Client terpusat (`apiClient`) yang mendukung injeksi Bearer Token otomatis dan penanganan galat terstandar.
* **Backend API**: Node.js / Express.js REST API terpusat yang di-host pada infrastruktur cloud (Vercel Serverless Function).
* **Basis Data**: Relational Database Management System (RDBMS MySQL / MariaDB / PostgreSQL Compatible) dengan skema relasional terindeks dan tabel khusus jejak audit (`audit_logs`) dan pembatasan percobaan login (`login_attempts`).
* **Penyimpanan Status Klien**: Browser Storage (`localStorage`) dengan enkapsulasi modul keamanan khusus (`security.js`) untuk proteksi brute force dan caching log audit offline-first.

```
+-------------------------------------------------------------------+
|                        FRONTEND CLIENT                            |
|  [Storefront / Katalog]   [Panel Admin]   [Modul Audit Trail 5A]  |
|         |                        |                    |           |
|         +----------+-------------+--------------------+           |
|                    |                                              |
|            [Router Guard & RBAC]                                  |
|            [Security Module (Rate Limiting, Sanitizer, Logger)]   |
+--------------------+----------------------------------------------+
                     |  HTTPS / JSON (Bearer Token JWT)
                     v
+-------------------------------------------------------------------+
|                        BACKEND API SERVER                         |
|  [Auth Controller]   [Product API]   [Order API]   [Audit API]    |
|  [Token Verifier]    [Role Check]    [BCrypt Salt] [Input Filter] |
+--------------------+----------------------------------------------+
                     |  SQL Queries (Prepared Statements)
                     v
+-------------------------------------------------------------------+
|                       DATABASE RELASIONAL                         |
|  users | brands | products | orders | order_items | audit_logs    |
+-------------------------------------------------------------------+
```

### 1.3 Daftar Modul & Fitur Aplikasi
1. **Modul Storefront (Katalog Publik)**: Menampilkan koleksi barang mewah, filter kategori/merek, rincian detail produk, keranjang belanja interaktif (*Cart Drawer*), serta formulir checkout pesanan dengan validasi input.
2. **Modul Autentikasi Pengguna & Pelanggan**: Login sesi administrator dan pelanggan, form registrasi pelanggan, proteksi brute-force dengan timer penguncian otomatis (lockout), serta validasi format kredensial.
3. **Modul Panel Administrasi (Dashboard)**: Ringkasan statistik inventaris produk, jumlah pelanggan terdaftar, visual status integritas keamanan 5A, dan pemantauan ringkas aktivitas audit terkini.
4. **Modul Manajemen Data (CRUD)**:
   - *Kelola Produk*: Tambah, ubah data, dan hapus inventaris barang.
   - *Kelola Merek*: Pengelompokan brand mewah mitra.
   - *Kelola Pesanan*: Pemantauan invoice, verifikasi pembayaran, dan pembaruan status pengiriman barang.
   - *Kelola Pengguna*: Administrasi akun pelanggan dan tingkat keanggotaan (Silver, Gold, Platinum).
5. **Modul Pusat Audit Keamanan (A5 Audit Trail Console)**: Halaman khusus inspeksi rekam jejak aktivitas, metrik keamanan (Insiden Tinggi, Peringatan, Login Sukses), filter berdasarkan keparahan (Severity) dan kategori 5A, serta ekspor rekaman audit ke format CSV untuk audit kepatuhan resmi.

---

## BAB II: PENJELASAN KONSEP 5A PADA SETIAP PROSES APLIKASI

Konsep 5A merupakan kerangka kerja pengamanan berlapis yang memperluas model klasik AAA (Authentication, Authorization, Accounting) dengan menambahkan fungsi kontrol pengawasan menyeluruh (Auditing) serta jaminan kelangsungan operasional dan integritas data (Availability/Assurance).

### 2.1 Definisi Konsep Keamanan 5A
1. **Authentication (Autentikasi)** — *"Who are you?"*
   Proses verifikasi dan validasi keabsahan identitas subjek (pengguna/sistem) sebelum diizinkan berinteraksi dengan sumber daya terlindungi.
2. **Authorization (Otorisasi)** — *"What are you permitted to do?"*
   Proses penentuan dan penegakan batasan hak akses atau wewenang subjek terhadap objek dan fungsi di dalam sistem berdasarkan peran (*Role-Based Access Control / RBAC*).
3. **Accounting (Akuntansi / Pencatatan Aktivitas)** — *"What did you do and when?"*
   Proses pengumpulan dan pencatatan secara sistematis atas setiap peristiwa, transaksi, konsumsi sumber daya, serta durasi aktivitas pengguna ke dalam rekam jejak (*log*).
4. **Auditing (Pemeriksaan & Evaluasi Keamanan)** — *"Are security rules and integrity preserved?"*
   Proses pengawasan, analisis, investigasi berkala, dan peninjauan retrospektif terhadap catatan log akuntansi untuk menemukan kejanggalan (*anomaly detection*), potensi serangan, atau pelanggaran kebijakan.
5. **Availability & Assurance (Ketersediaan Layanan & Jaminan Integritas)** — *"Is the system reliable, available, and tamper-resistant?"*
   Upaya memastikan sistem tetap dapat diakses oleh pihak yang berwenang kapan pun dibutuhkan, serta memberikan jaminan bahwa data dan kode program bersih dari manipulasi, injeksi berbahaya, maupun gangguan denial-of-service.

---

### 2.2 Pemetaan 5A pada Proses Login & Autentikasi Pengguna
Proses masuk (*Login*) adalah gerbang utama perlindungan sistem:

* **Authentication (Autentikasi)**:
  - Pengguna memasukkan `username` dan `password` pada form login (`src/views/Login.vue`).
  - Sistem frontend memverifikasi kelengkapan form, lalu mengirim request `POST /api/login` ke backend.
  - Backend memverifikasi kecocokan password menggunakan hashing kriptografi satu arah (BCrypt dengan salted string).
  - Jika valid, backend menerbitkan JSON Web Token (JWT) yang disimpan secara aman di `localStorage` sebagai kredensial sesi aktif.
  - **Fitur Khusus Brute-Force Lockout**: Frontend dilengkapi logika proteksi pada `src/services/security.js`. Jika terjadi kesalahan login sebanyak 3 kali berturut-turut, tombol login dinonaktifkan dan akun dikunci sementara selama 60 detik dengan hitung mundur (*countdown*) visual.
* **Authorization (Otorisasi)**:
  - Token JWT memuat payload klaim peran pengguna (`role: 'admin'`).
  - Seseorang yang gagal login tidak akan mendapatkan token dan ditolak dari semua halaman yang membutuhkan hak akses istimewa.
* **Accounting (Pencatatan Aktivitas)**:
  - Setiap percobaan login dicatat seketika oleh fungsi `logSecurityEvent`.
  - Jika login berhasil, event dicatat sebagai `AUTH_LOGIN_SUCCESS` (Severity: SUCCESS).
  - Jika salah password, dicatat sebagai `AUTH_LOGIN_FAILED` dengan jumlah percobaan (Severity: WARNING).
  - Jika mencapai 3x gagal, dicatat event `AUTH_BRUTE_FORCE_LOCKOUT` (Severity: DANGER) lengkap dengan timestamp dan fingerprint peramban.
* **Auditing (Pemeriksaan & Audit)**:
  - Administrator dapat membuka menu *Audit Keamanan (A5)* untuk meninjau log login.
  - Pola serangan tebakan kata sandi berulang dari satu aktor/IP dapat langsung teridentifikasi melalui filter severity "DANGER".
* **Availability & Assurance (Ketersediaan & Jaminan)**:
  - Pembatasan laju (*rate limiting*) mencegah server tumbang akibat kebanjiran ribuan request serangan credential stuffing.
  - Indikator antarmuka interaktif memberikan pesan kesalahan yang jelas tanpa membocorkan informasi internal sistem (*vulnerability information disclosure prevention*).

---

### 2.3 Pemetaan 5A pada Proses Otorisasi Akses Panel Admin (RBAC)
Ketika pengguna mencoba mengakses rute internal `/admin/*`:

* **Authentication (Autentikasi)**:
  - Navigation Guard pada Vue Router (`src/router/index.js`) mengecek keberadaan token:
    ```javascript
    router.beforeEach((to, from, next) => {
      const token = localStorage.getItem('token')
      if (to.meta.requiresAuth && !token) {
        next('/login')
      } else {
        next()
      }
    })
    ```
  - Jika token tidak ditemukan atau telah kedaluwarsa, pengguna secara otomatis dialihkan ke halaman `/login`.
* **Authorization (Otorisasi)**:
  - Seluruh sub-rute admin (`/admin/dashboard`, `/admin/products`, `/admin/brands`, `/admin/orders`, `/admin/users`, `/admin/audit-logs`) diberi tanda `meta: { requiresAuth: true }`.
  - Hanya pengguna dengan peran terotorisasi yang dapat merender komponen layout admin (`AdminLayout.vue`).
  - Request API yang dikirim oleh `apiClient` secara otomatis menyematkan header `Authorization: Bearer <token>`. Jika token dimanipulasi, server mengembalikan respon HTTP 401 Unauthorized dan sesi otomatis dihentikan.
* **Accounting (Pencatatan Aktivitas)**:
  - Saat pengguna menekan tombol Logout, sistem mencatat event `AUTH_LOGOUT` (Severity: INFO).
  - Jika terjadi penolakan akses (HTTP 401), sistem mencatat upaya akses ilegal.
* **Auditing (Pemeriksaan & Audit)**:
  - Log perpindahan rute dan status sesi dapat diaudit melalui daftar riwayat aktivitas di panel admin.
* **Availability & Assurance (Ketersediaan & Jaminan)**:
  - Layout admin menerapkan *Lazy Loading* dan penanganan status pemanggilan API dengan animasi *progress circular* untuk menjamin responsivitas antarmuka jika jaringan melambat.

---

### 2.4 Pemetaan 5A pada Proses Manajemen Data (Produk, Merek, Pengguna)
Aktivitas pengelolaan master data barang mewah dan akun pelanggan:

* **Authentication (Autentikasi)**:
  - Setiap operasi CRUD (Create, Read, Update, Delete) diwajibkan menyertakan token otentikasi aktif pada header request.
* **Authorization (Otorisasi)**:
  - Hak menghapus (*Delete*) dan mengubah (*Update*) data dibatasi secara ketat hanya untuk admin.
  - Dialog konfirmasi (`confirm()`) dipasang untuk mencegah tindakan penghapusan tidak disengaja.
* **Accounting (Pencatatan Aktivitas)**:
  - Setiap kali administrator menambah produk baru, event `PRODUCT_CREATE` dicatat dengan rincian nama dan harga barang.
  - Ketika data pengguna diubah, dicatat event `USER_UPDATE` (misalnya perubahan tingkat membership menjadi Platinum).
  - Ketika pengguna dihapus, dicatat event `USER_DELETE` dengan tingkat keparahan WARNING.
* **Auditing (Pemeriksaan & Audit)**:
  - Tersedia rekaman lengkap mengenai *siapa* administrator yang melakukan modifikasi, *kapan* tanggal dan jam perubahan dilakukan, serta *apa* objek yang diubah. Ini menjamin asas **Non-Repudiation** (tidak dapat menyangkal perbuatan).
* **Availability & Assurance (Ketersediaan & Jaminan)**:
  - Seluruh masukan form (nama barang, email, username) divalidasi dan disanitasi menggunakan fungsi `sanitizeInput()` guna mencegah serangan *Cross-Site Scripting (XSS)* dan *SQL Injection*.
  - Di tingkat basis data, relasi dilindungi dengan constraint `FOREIGN KEY ... ON DELETE CASCADE/SET NULL` untuk menjamin integritas referensial data (*data consistency*).

---

### 2.5 Pemetaan 5A pada Proses Transaksi Belanja & Checkout Pelanggan
Alur pelanggan memilih koleksi barang mewah hingga menyelesaikan pesanan di Storefront:

* **Authentication (Autentikasi)**:
  - Pelanggan dapat berbelanja sebagai tamu terdaftar (*authenticated customer*) dengan login terlebih dahulu, atau melakukan pembelian langsung dengan mengisi identitas pengiriman yang sah.
* **Authorization (Otorisasi)**:
  - Pelanggan hanya diizinkan melihat riwayat belanja miliknya sendiri (`/orders?user_id=X`), dan tidak diperbolehkan mengakses atau memanipulasi pesanan pelanggan lain (*mitigasi Insecure Direct Object References / IDOR*).
* **Accounting (Pencatatan Aktivitas)**:
  - Ketika pelanggan berhasil menekan tombol "Selesaikan Pembelian", sistem membuat entri pesanan baru di tabel `orders` dan `order_items`.
  - Modul keamanan mencatat event `ORDER_CHECKOUT_SUCCESS` berisi nominal total belanja dan ID pesanan.
  - Saat admin mengubah status pesanan (misal dari "Pending" menjadi "Selesai"), sistem mencatat event `ORDER_STATUS_UPDATE`.
* **Auditing (Pemeriksaan & Audit)**:
  - Log transaksi pesanan dapat dicocokkan antara tabel keuangan `orders` dan tabel audit `audit_logs` untuk memastikan tidak ada pesanan siluman atau manipulasi nominal harga oleh pihak tak berwenang.
* **Availability & Assurance (Ketersediaan & Jaminan)**:
  - Kalkulasi total belanja dan validasi stok produk dilakukan secara presisi menggunakan format mata uang terstandar Rupiah (IDR).
  - Penanganan transaksi keranjang belanja menggunakan mekanisme state reaktif yang tidak hilang saat navigasi tab.

---

### 2.6 Pemetaan 5A pada Modul Pusat Audit Keamanan (Security Audit Trail)
Halaman khusus `src/views/AuditLogs.vue` yang didedikasikan untuk mengelola kontrol keamanan tingkat tinggi:

* **Authentication (Autentikasi)**:
  - Hanya dapat diakses setelah melewati verifikasi kredensial login admin.
* **Authorization (Otorisasi)**:
  - Diberikan hak akses eksklusif untuk peran Administrator.
* **Accounting (Pencatatan Aktivitas)**:
  - Menyajikan seluruh data log historis yang dihimpun dari modul `security.js`.
  - Jika log direset, sistem secara otomatis mencatat event meta-audit `AUDIT_LOGS_PURGED` sebagai bukti bahwa reset telah dilakukan oleh admin.
* **Auditing (Pemeriksaan & Audit)**:
  - Menyediakan filter multi-parameter:
    1. Filter Tingkat Keparahan (*Severity*): INFO, SUCCESS, WARNING, DANGER.
    2. Filter Kategori 5A: Authentication, Authorization, Data Management, Auditing, System.
    3. Kotak Pencarian Teks Bebas: Mencari berdasarkan nama aktor atau kata kunci aktivitas.
  - Tombol **Export CSV**: Menghasilkan berkas `.csv` resmi yang dapat dicetak atau diserahkan kepada auditor eksternal / penguji keamanan.
* **Availability & Assurance (Ketersediaan & Jaminan)**:
  - Dilengkapi mekanisme penyimpanan terisolasi yang menjamin data log tetap dapat diakses meskipun koneksi ke server backend utama mengalami gangguan sementara.

---

### 2.7 Matriks Ringkasan Implementasi 5A

| Proses / Modul Sistem | Authentication (Autentikasi) | Authorization (Otorisasi) | Accounting (Pencatatan) | Auditing (Pemeriksaan) | Availability / Assurance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Login Pengguna** | Password hash BCrypt + Brute-force lockout (60s) | Pemberian JWT Token berisi klaim peran | Log `AUTH_LOGIN_SUCCESS`, `AUTH_LOGIN_FAILED`, & `LOCKOUT` | Deteksi anomali tebakan password pada Audit Console | Rate-limiting request mencegah overload server |
| **Akses Panel Admin** | Verifikasi Bearer Token pada route guard | RBAC: Rute terlindungi `meta.requiresAuth` | Log `AUTH_LOGOUT` & sesi terputus | Monitoring durasi sesi aktif administrator | Navigasi SPA cepat dengan transisi fallback |
| **Kelola Produk & Brand** | Header Bearer Token wajib pada setiap API call | Admin only (Akses modifikasi & penghapusan) | Log `PRODUCT_CREATE`, `PRODUCT_UPDATE`, `PRODUCT_DELETE` | Rekam jejak perubahan harga & deskripsi barang | Input sanitization cegah XSS & SQLi |
| **Kelola Pengguna** | Verifikasi sesi admin pengelola | Admin only (Restriksi CRUD akun) | Log `USER_CREATE`, `USER_UPDATE`, `USER_DELETE` | Jejak perubahan hak akses / membership level | Validasi format email & pencegahan duplikasi |
| **Checkout & Pesanan** | Kredensial akun pelanggan / data valid checkout | Pembatasan akses invoice hanya pemilik hak | Log `ORDER_CHECKOUT_SUCCESS` & `ORDER_STATUS_UPDATE` | Rekonsiliasi transaksi penjualan & pembatalan | Perhitungan total belanja presisi & validasi stok |
| **Pusat Audit Keamanan** | Login administrator level tinggi | Khusus Administrator Keamanan | Meta-logging saat ekspor atau reset log | Filter severity, audit anomali, & fitur Ekspor CSV | Caching lokal tahan gangguan jaringan (offline-resilient) |

---

## BAB III: DOKUMENTASI KEAMANAN SISTEM & MITIGASI KERENTANAN

### 3.1 Mitigasi OWASP Top 10 Web Vulnerabilities
Aplikasi dirancang dengan mempertimbangkan 10 kerentanan paling krusial menurut Open Web Application Security Project (OWASP):

1. **A01: Broken Access Control (Pelanggaran Kontrol Akses)**:
   - *Mitigasi*: Penerapan Navigation Guard ketat di sisi klien (`router.beforeEach`) dan verifikasi tanda tangan token JWT di setiap endpoint backend. Pengguna biasa tidak dapat mengakses URL `/admin/*` meskipun mengetahui alamat jalurnya.
2. **A02: Cryptographic Failures (Kegagalan Kriptografi)**:
   - *Mitigasi*: Seluruh transmisi data menggunakan protokol HTTPS/TLS. Password tidak pernah disimpan dalam bentuk plaintext, melainkan di-hash menggunakan algoritma modern dengan salt acak. Data sensitif token sesi dikirim melalui header `Authorization`.
3. **A03: Injection (Injeksi SQL & Cross-Site Scripting)**:
   - *Mitigasi*: Pada sisi frontend, masukan data dibersihkan dengan helper `sanitizeInput()` yang menetralkan karakter berbahaya (`<`, `>`, `"`, `'`, `/`). Pada sisi backend/database, seluruh query dijalankan dengan parameterized queries (Prepared Statements), meniadakan kemungkinan SQL Injection.
4. **A04: Insecure Design (Desain Tidak Aman)**:
   - *Mitigasi*: Mengadopsi prinsip *Defense in Depth* dan *Least Privilege*. Arsitektur dilengkapi modul kontrol audit independen sejak tahap awal perencanaan.
5. **A05: Security Misconfiguration (Salah Konfigurasi Keamanan)**:
   - *Mitigasi*: Pengaturan CORS ketat pada API backend, penonaktifan direktori listing, dan penyeragaman format pesan kesalahan tanpa mengekspos stack trace server.
6. **A06: Vulnerable and Outdated Components (Komponen Rentan & Kedaluwarsa)**:
   - *Mitigasi*: Menggunakan library versi stabil terkini (Vue 3.5, Vite 5.4, Vuetify 3.12) serta manajemen dependensi terisolasi.
7. **A07: Identification and Authentication Failures (Kegagalan Identifikasi & Autentikasi)**:
   - *Mitigasi*: Implementasi proteksi Brute-Force lockout otomatis setelah 3 percobaan gagal, session termination otomatis saat logout, dan pencegahan penggunaan username ganda.
8. **A08: Software and Data Integrity Failures (Kegagalan Integritas Software & Data)**:
   - *Mitigasi*: Validasi integritas paket dependensi melalui `pnpm-lock.yaml` dan verifikasi integritas data transaksi pada tabel `order_items`.
9. **A09: Security Logging and Monitoring Failures (Kegagalan Pencatatan & Pemantauan Keamanan)**:
   - *Mitigasi*: Terpenuhi secara menyeluruh melalui tabel `audit_logs` dan tampilan interaktif `AuditLogs.vue` yang mencatat setiap peristiwa penting secara real-time.
10. **A10: Server-Side Request Forgery (SSRF)**:
    - *Mitigasi*: API backend membatasi request hanya pada rute internal yang telah didaftarkan dan tidak menerima URL eksternal arbitrary dari input pengguna.

### 3.2 Threat Modeling & Strategi Pertahanan
* **Ancaman Credential Stuffing & Brute Force**: Ditangkal melalui timer kunci akun 60 detik di level antarmuka dan pembatasan frekuensi request (Rate Limiting).
* **Ancaman Session Hijacking**: Ditangkal dengan masa kedaluwarsa token JWT yang terbatas, penghapusan token seketika saat logout, dan transmisi terenkripsi.
* **Ancaman Pemalsuan Data Belanja (Price Tampering)**: Harga produk dihitung ulang secara independen di sisi server berdasarkan basis data resmi sebelum invoice pesanan diterbitkan.

---

## BAB IV: SPESIFIKASI DAN SKEMA BASIS DATA

### 4.1 Diagram Hubungan Entitas (ERD)
Hubungan antar tabel dalam sistem dirancang secara normal (3NF) guna menjamin efisiensi dan integritas:

```
+-------------------+       +-----------------------+
|       users       |       |        brands         |
+-------------------+       +-----------------------+
| PK  user_id       |       | PK  brand_id          |
|     username (UQ) |       |     name (UQ)         |
|     email (UQ)    |       |     description       |
|     password_hash |       +-----------+-----------+
|     role          |                   | 1
|     membership    |                   |
+---------+---------+                   | M
          | 1                           v
          |                 +-----------------------+
          |                 |       products        |
          |                 +-----------------------+
          |                 | PK  product_id        |
          |                 | FK  brand_id          |
          |                 |     name              |
          |                 |     price             |
          |                 |     stock             |
          |                 +-----------+-----------+
          | M                           | 1
          v                             |
+-------------------+                   |
|      orders       |                   | M
+-------------------+                   v
| PK  order_id      |       +-----------------------+
| FK  user_id       |<----->|      order_items      |
|     customer_name | 1   M +-----------------------+
|     total_amount  |       | PK  item_id           |
|     status        |       | FK  order_id          |
+-------------------+       | FK  product_id        |
                            |     quantity          |
                            |     subtotal          |
                            +-----------------------+

+---------------------------------------------------+
|               TABEL KEAMANAN KHUSUS               |
+---------------------------------------------------+
| audit_logs        : log_id (PK), actor, role,     |
|                     category, action, details,    |
|                     severity, status, created_at  |
|                                                   |
| login_attempts    : attempt_id (PK), ip_address,  |
|                     username, attempts_count,     |
|                     locked_until                  |
+---------------------------------------------------+
```

### 4.2 Kamus Data (Data Dictionary Ringkas)
1. **users**: Menyimpan akun pengguna, sandi terenkripsi, hak peran (admin/customer/staff), dan status akun.
2. **brands**: Menyimpan katalog nama produsen barang mewah.
3. **products**: Menyimpan detail barang, keterkaitan merek (`brand_id`), harga satuan, dan kuantitas persediaan.
4. **orders**: Menyimpan data faktur pemesanan, pembeli, alamat ekspedisi, total pembayaran, dan status transaksi.
5. **order_items**: Menyimpan data barang individual dalam pesanan untuk menjamin jejak audit harga saat transaksi terjadi.
6. **audit_logs**: Menyimpan rekam jejak peristiwa keamanan, keparahan insiden, dan identitas pelaku aksi.
7. **login_attempts**: Menyimpan penghitung percobaan login gagal per kombinasi IP dan username guna menegakkan kebijakan lockout.

---

## BAB V: PANDUAN DAN SIMULASI WAWANCARA DOSEN (INTERVIEW PREP)

> **PERINGATAN PENTING**: Dosen menetapkan aturan bahwa apabila satu anggota kelompok gagal menjawab saat wawancara individu, nilai kelompok dapat digugurkan menjadi 0. Seluruh anggota WAJIB mempelajari dan menguasai bank tanya-jawab di bawah ini!

### 5.1 Tips Menghadapi Wawancara Individu
1. **Pahami Peran Anda**: Jelaskan peran spesifik Anda sesuai dengan lembar pembagian tugas, namun pahami gambaran besar alur kerja 5A sistem.
2. **Jawab Menggunakan Terminologi Resmi**: Selalu sebutkan istilah bahasa Inggrisnya terlebih dahulu (*Authentication, Authorization, Accounting, Auditing, Availability/Assurance*) lalu jelaskan penerapannya di web Luxury Store.
3. **Bisa Menunjukkan Bukti di Aplikasi**: Tahu letak fitur di aplikasi (Menu Audit Keamanan, pesan kunci akun di Login, tombol Export CSV, dan rute guard di kode program).

---

### 5.2 Bank Soal dan Kunci Jawaban Konsep 5A

#### Pertanyaan 1: "Coba jelaskan apa itu konsep 5A dan bagaimana kelompok Anda menerapkannya pada aplikasi ini?"
* **Kunci Jawaban**:
  > "Konsep 5A adalah kerangka kerja komprehensif dalam keamanan informasi yang terdiri dari:
  > 1. **Authentication**: Verifikasi keabsahan identitas pengguna. Di aplikasi kami, ini diterapkan pada form login dengan verifikasi username-password, hashing password, serta proteksi Brute-Force lockout selama 60 detik jika 3x salah password.
  > 2. **Authorization**: Penentuan hak akses pengguna berdasarkan peran. Diterapkan melalui Vue Router Navigation Guard yang membatasi menu admin hanya untuk akun berstatus Administrator, serta proteksi Bearer Token pada setiap panggilan API.
  > 3. **Accounting**: Pencatatan aktivitas pengguna ke dalam rekaman log. Diterapkan melalui modul `security.js` yang mencatat setiap peristiwa login, logout, penambahan/penghapusan produk, dan perubahan status pesanan secara real-time.
  > 4. **Auditing**: Pemeriksaan dan peninjauan berkala terhadap rekaman log. Kami menyediakan halaman khusus 'Audit Keamanan (A5)' di dashboard admin yang menampilkan grafik keparahan (Severity), filter kategori, dan tombol ekspor rekaman ke berkas CSV.
  > 5. **Availability / Assurance**: Memastikan sistem selalu siap melayani pengguna dengan integritas data yang terjamin. Kami menerapkan pembersihan input (input sanitization) untuk menangkal serangan XSS, serta validasi data sebelum dikirim ke backend."

#### Pertanyaan 2: "Bagaimana proses Authentication bekerja saat pengguna memasukkan password yang salah berkali-kali?"
* **Kunci Jawaban**:
  > "Pada aplikasi Luxury Store kami, kami menerapkan mekanisme mitigasi Brute-Force Attack. Di dalam file `src/views/Login.vue` dan `src/services/security.js`, setiap kegagalan login dihitung. Jika pengguna salah memasukkan password sebanyak 3 kali:
  > 1. Tombol 'Masuk' dinonaktifkan secara otomatis.
  > 2. Muncul kotak peringatan darurat dengan hitung mundur (*countdown timer*) 60 detik.
  > 3. Sistem mencatat event `AUTH_BRUTE_FORCE_LOCKOUT` dengan tingkat keparahan 'DANGER' ke dalam tabel log audit.
  > Hal ini mencegah penyerang membobol akun menggunakan teknik serangan tebakan kata sandi otomatis (dictionary attack)."

#### Pertanyaan 3: "Apa perbedaan mendasar antara Accounting dan Auditing di sistem Anda?"
* **Kunci Jawaban**:
  > "Perbedaan mendasarnya terletak pada fungsi pasif dan aktifnya:
  > - **Accounting** adalah proses *pencatatan data mentah* (logging). Tugasnya mencatat 'Siapa yang melakukan, Apa yang dilakukan, Kapan, dan Bagaimana hasilnya'. Di sistem kami, ini terjadi di belakang layar setiap kali ada operasi CRUD atau login.
  > - **Auditing** adalah proses *analisis, evaluasi, dan pemeriksaan* terhadap data yang telah dicatat tadi. Auditing dilakukan oleh admin/auditor melalui menu Audit Keamanan untuk mendeteksi apakah ada pola mencurigakan (seperti percobaan login gagal beruntun) serta menghasilkan laporan kepatuhan dalam bentuk berkas CSV."

#### Pertanyaan 4: "Bagaimana jika ada pengguna yang sengaja mengetik alamat URL `/admin/products` langsung di browser tanpa login terlebih dahulu?"
* **Kunci Jawaban**:
  > "Aksi tersebut akan digagalkan oleh mekanisme **Authorization** melalui Navigation Guard di file `src/router/index.js`.
  > Sebelum halaman ditampilkan, fungsi `router.beforeEach` memeriksa apakah terdapat token valid di penyimpanan browser. Karena pengguna belum login dan tidak memiliki token, rute dicegat dan pengguna langsung dialihkan paksa (*redirect*) kembali ke halaman `/login`. Selain itu, panggilan API ke server juga akan ditolak dengan kode status HTTP 401 Unauthorized."

#### Pertanyaan 5: "Di mana letak penerapan Availability dan Assurance pada aplikasi web Anda?"
* **Kunci Jawaban**:
  > "Penerapannya mencakup dua aspek penting:
  > 1. **Assurance (Jaminan Integritas)**: Kami menggunakan fungsi `sanitizeInput()` untuk membersihkan karakter kode berbahaya sebelum data produk atau pengguna diproses, sehingga aplikasi terbebas dari ancaman Cross-Site Scripting (XSS).
  > 2. **Availability (Ketersediaan Layanan)**: Proteksi rate-limiting pada percobaan login menjaga agar server tidak mengalami kelebihan beban (*denial of service*). Di sisi antarmuka, penanganan error terpusat dan indikator loading memastikan pengguna selalu mendapatkan umpan balik responsif meskipun kondisi jaringan sedang lambat."

---

### 5.3 Skenario Pertanyaan Pengujian Live Demo Sistem
Saat diminta mendemonstrasikan aplikasi di hadapan dosen:
1. **Langkah 1**: Buka halaman Login (`/login`), coba masukkan sembarang password 3 kali berturut-turut. Tunjukkan bahwa sistem mengunci form login dengan timer hitung mundur 60 detik (Membuktikan **Authentication** & Brute Force Protection).
2. **Langkah 2**: Masuk dengan akun administrator yang valid (`admin`). Tunjukkan bahwa sistem berhasil masuk ke `/admin/dashboard` (Membuktikan **Authorization**).
3. **Langkah 3**: Buka menu sidebar **Audit Keamanan (A5)**. Tunjukkan bahwa insiden kegagalan login tadi sudah tercatat lengkap dengan status DANGER dan rincian waktu (Membuktikan **Accounting**).
4. **Langkah 4**: Gunakan dropdown filter severity untuk memilih "DANGER" atau "WARNING", kemudian klik tombol **Export CSV** (Membuktikan **Auditing**).
5. **Langkah 5**: Buka halaman Storefront (`/`), masukkan barang ke keranjang dan lakukan checkout (Membuktikan integritas alur transaksi dan **Availability/Assurance**).

---

## BAB VI: LAMPIRAN BUKTI TANGKAPAN LAYAR (SCREENSHOT) SISTEM & PENGUJIAN 5A

Berikut merupakan tangkapan layar langsung pengujian fitur keamanan 5A pada web Luxury Store yang telah di-deploy (URL Produksi: `https://projectki2.vercel.app/`):

### 6.1 Antarmuka Login Kredensial Pengguna (`/login`)
![Login Kredensial](screenshots/ss1_login_normal.png)
*Keterangan: Halaman autentikasi utama untuk verifikasi username dan password administrator sebelum mendapatkan sesi token.*

### 6.2 Pengujian Autentikasi & Brute-Force Lockout Countdown
![Brute Force Lockout](screenshots/ss2_login_locked.png)
*Keterangan: Bukti nyata pencegahan serangan Brute-Force. Form login otomatis terkunci selama 60 detik disertai pesan peringatan merah dan hitung mundur setelah 3 kali percobaan gagal.*

### 6.3 Panel Dashboard Utama & Indikator Status Keamanan 5A (`/admin/dashboard`)
![Dashboard Status 5A](screenshots/ss3_dashboard.png)
*Keterangan: Dashboard administrator membuktikan otorisasi (RBAC). Menampilkan widget 'Keamanan (A5) Aktif (100%)' dan ringkasan inventaris produk.*

### 6.4 Konsol Audit Keamanan — Filter Insiden Bahaya / DANGER (`/admin/audit-logs`)
![Audit Log Danger](screenshots/ss4_audit_danger.png)
*Keterangan: Bukti Accounting & Auditing. Sistem mencatat insiden percobaan brute-force sebagai event 'AUTH_BRUTE_FORCE_LOCKOUT' dengan tingkat keparahan DANGER dan status LOCKED.*

### 6.5 Konsol Audit Keamanan — Filter Peringatan / WARNING
![Audit Log Warning](screenshots/ss5_audit_warning.png)
*Keterangan: Bukti pencatatan berkala setiap percobaan login salah sebagai event 'AUTH_LOGIN_FAILED' lengkap dengan jumlah percobaan (1/3, 2/3).*

### 6.6 Konsol Audit Keamanan — Filter Informasi / INFO & Bukti Ekspor CSV
![Audit Log Info](screenshots/ss6_audit_info.png)
*Keterangan: Bukti pencatatan aktivitas rutin (AUTH_LOGOUT, AUDIT_EXPORT_CSV, dan SYSTEM_BOOT) serta kesiapan laporan audit untuk diekspor.*
