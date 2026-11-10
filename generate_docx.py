import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def style_heading(p, text, font_size=14, bold=True, color_rgb=(184, 134, 11), space_before=12, space_after=6):
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor(*color_rgb)
    return run

def add_p(doc, text="", font_size=11, bold=False, italic=False, color_rgb=(44, 62, 80), space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if text:
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(font_size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = RGBColor(*color_rgb)
    return p

# -------------------------------------------------------------
# 1. GENERATE DOKUMENTASI_TUGAS_BESAR_KEAMANAN_INFORMASI.docx
# -------------------------------------------------------------
def generate_main_doc():
    doc = Document()
    
    # Page setup
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(4)
    run_t1 = p_title.add_run("DOKUMENTASI SISTEM & KONTROL KEAMANAN 5A\n")
    run_t1.font.name = 'Calibri'
    run_t1.font.size = Pt(20)
    run_t1.font.bold = True
    run_t1.font.color.rgb = RGBColor(184, 134, 11) # Gold

    run_t2 = p_title.add_run("TUGAS BESAR KEAMANAN INFORMASI (UTS & UAS)\n")
    run_t2.font.name = 'Calibri'
    run_t2.font.size = Pt(14)
    run_t2.font.bold = True
    run_t2.font.color.rgb = RGBColor(80, 80, 80)

    run_t3 = p_title.add_run("Aplikasi Web: Luxury Store E-Commerce Platform")
    run_t3.font.name = 'Calibri'
    run_t3.font.size = Pt(12)
    run_t3.font.italic = True
    run_t3.font.color.rgb = RGBColor(120, 120, 120)

    # Divider line
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(16)
    r_div = p_div.add_run("―" * 58)
    r_div.font.color.rgb = RGBColor(212, 175, 55)

    # Identitas Tim Box
    p_box = doc.add_paragraph()
    p_box.paragraph_format.space_after = Pt(16)
    r_box = p_box.add_run("IDENTITAS MAHASISWA / KELOMPOK:\n")
    r_box.font.bold = True
    r_box.font.color.rgb = RGBColor(184, 134, 11)
    p_box.add_run("Mata Kuliah       : Keamanan Informasi\n")
    p_box.add_run("Program Studi     : Teknik Informatika / Sistem Informasi\n")
    p_box.add_run("Nama Anggota      : [Isi Nama Anggota Kelompok Anda]\n")
    p_box.add_run("NIM Anggota       : [Isi NIM Anggota Kelompok Anda]\n")
    p_box.add_run("Target Penilaian  : Memenuhi Standar Nilai A (Dokumentasi Lengkap, Source Code 5A, Database Relasional, & Siap Wawancara)")

    # BAB I
    style_heading(doc.add_paragraph(), "BAB I: GAMBARAN UMUM SISTEM", 15, True, (184, 134, 11), 16, 6)
    add_p(doc, "1.1 Latar Belakang & Deskripsi Aplikasi", 12, True, False, (50, 50, 50), 4)
    add_p(doc, "Luxury Store adalah platform e-commerce modern berbasis web yang dibangun untuk memfasilitasi transaksi barang mewah (jam tangan mewah, tas branded, perhiasan, dan koleksi fesyen eksklusif). Mengingat platform ini menangani transaksi dengan nilai finansial tinggi dan data sensitif konsumen, aspek Keamanan Informasi menjadi pondasi terpenting dari seluruh siklus perangkat lunak. Seluruh sistem dirancang secara ketat mengikuti pedoman Konsep 5A (Authentication, Authorization, Accounting, Auditing, Availability/Assurance).")
    
    add_p(doc, "1.2 Arsitektur Sistem & Spesifikasi Teknologi", 12, True, False, (50, 50, 50), 4)
    add_p(doc, "Sistem menerapkan arsitektur Decoupled Client-Server dengan rincian:")
    add_p(doc, "• Frontend: Vue.js 3 (Composition API), Vite, Vuetify 3 (Material Design), Vue Router 4 (Navigation Guards).\n• Security Layer: Modul terpusat security.js untuk mitigasi serangan Brute Force (lockout timer), audit logger lokal, sanitasi input XSS, dan ekspor berkas audit.\n• API & Komunikasi: REST API terstandar over HTTPS/TLS dengan injeksi otomatis Bearer Token pada HTTP Authorization header.\n• Database: Skema RDBMS relasional (MySQL / MariaDB) dengan tabel keamanan audit_logs dan login_attempts.")

    # BAB II
    style_heading(doc.add_paragraph(), "BAB II: PENJELASAN KONSEP 5A PADA SETIAP PROSES APLIKASI", 15, True, (184, 134, 11), 18, 6)
    add_p(doc, "Konsep 5A merupakan kerangka kerja keamanan berlapis yang diterapkan secara nyata pada setiap alur transaksi dan pengelolaan data di web Luxury Store:")

    processes = [
        ("1. Proses Login & Autentikasi Pengguna", [
            ("Authentication", "Verifikasi identitas melalui username dan password hash (BCrypt salted). Dilengkapi proteksi Brute-Force Rate Limiting: jika pengguna gagal 3 kali berturut-turut, akun dikunci sementara selama 60 detik disertai hitung mundur visual di antarmuka."),
            ("Authorization", "Setelah login valid, sistem menerbitkan JWT token yang memuat identitas peran (role: admin). Pengguna tanpa token dilarang mengakses modul administrasi."),
            ("Accounting", "Setiap aktivitas login dicatat seketika oleh sistem. Event sukses dicatat sebagai AUTH_LOGIN_SUCCESS, kegagalan dicatat sebagai AUTH_LOGIN_FAILED, dan kondisi penguncian dicatat sebagai AUTH_BRUTE_FORCE_LOCKOUT (Severity: DANGER)."),
            ("Auditing", "Admin dapat meninjau log percobaan login pada Pusat Audit Keamanan untuk mendeteksi pola serangan credential stuffing atau tebakan sandi berulang."),
            ("Availability/Assurance", "Rate limiting mencegah server kebanjiran ribuan request palsu (anti-DoS). Input pengguna divalidasi agar tidak mengekspos detail pesan galat sensitif server.")
        ]),
        ("2. Proses Akses Panel Administrator (RBAC)", [
            ("Authentication", "Pemeriksaan Bearer Token secara aktif oleh router navigation guard (beforeEach) sebelum rute diizinkan untuk dirender."),
            ("Authorization", "Penegakan Role-Based Access Control (RBAC). Rute admin ditandai meta: { requiresAuth: true }. Upaya akses tanpa token secara otomatis dialihkan (redirect) ke /login."),
            ("Accounting", "Pencatatan event logout (AUTH_LOGOUT) dan percobaan akses tidak sah (HTTP 401 Unauthorized)."),
            ("Auditing", "Peninjauan rekam jejak durasi sesi kerja administrator dan histori pergantian hak akses."),
            ("Availability/Assurance", "Arsitektur Single Page Application (SPA) memuat modul halaman secara asinkron dengan loading indicator transparan.")
        ]),
        ("3. Proses Pengelolaan Data (CRUD Produk, Merek, & Pengguna)", [
            ("Authentication", "Setiap request mutasi data (POST, PUT, DELETE) wajib menyertakan token otorisasi yang valid pada header request."),
            ("Authorization", "Hanya pengguna berstatus Administrator yang memiliki izin untuk menambah, memperbarui, atau menghapus master data produk dan pengguna."),
            ("Accounting", "Mencatat secara terperinci setiap perubahan data: PRODUCT_CREATE, USER_UPDATE (misal upgrade membership), dan USER_DELETE (Severity: WARNING)."),
            ("Auditing", "Menjamin asas Non-Repudiation (anti-penyangkalan) karena riwayat mencatat dengan jelas siapa yang melakukan perubahan dan objek apa yang diubah."),
            ("Availability/Assurance", "Sanitasi karakter masukan (sanitizeInput) untuk mematikan potensi XSS, serta penggunaan foreign key constraints pada database demi integritas referensial data.")
        ]),
        ("4. Proses Transaksi Belanja & Checkout Pelanggan", [
            ("Authentication", "Pelanggan dapat melakukan transaksi dengan akun terdaftar maupun pengisian form data pengiriman terverifikasi."),
            ("Authorization", "Pelanggan hanya memiliki wewenang membaca data pesanan miliknya sendiri, mencegah celah Insecure Direct Object References (IDOR)."),
            ("Accounting", "Pencatatan transaksi penjualan pada tabel orders dan order_items, serta event CHECKOUT_ORDER pada log audit keamanan."),
            ("Auditing", "Rekonsiliasi data inventaris produk dan omset penjualan untuk mencegah ketidaksesuaian nominal transaksi."),
            ("Availability/Assurance", "Validasi kuantitas stok barang dan kalkulasi harga Rupiah yang konsisten di sisi klien dan server.")
        ]),
        ("5. Modul Pusat Audit Keamanan (A5 Audit Trail Console)", [
            ("Authentication", "Hanya dapat dibuka oleh akun Administrator terautentikasi."),
            ("Authorization", "Otorisasi tingkat tertinggi (Security Auditor Privilege)."),
            ("Accounting", "Menghimpun seluruh data log dari seluruh modul aplikasi secara terstruktur (Timestamp, Aktor, Kategori, Aksi, Severity, Status)."),
            ("Auditing", "Tersedia filter tingkat keparahan (Info, Success, Warning, Danger), filter kategori 5A, pencarian kata kunci, serta tombol Ekspor ke berkas CSV resmi."),
            ("Availability/Assurance", "Penyimpanan log tahan terhadap gangguan jaringan (offline-resilient), menjamin transparansi data audit.")
        ])
    ]

    for proc_title, subitems in processes:
        add_p(doc, proc_title, 12, True, False, (184, 134, 11), 6)
        table = doc.add_table(rows=1, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = "Elemen 5A"
        hdr_cells[1].text = "Penerapan Nyata pada Sistem Luxury Store"
        set_cell_background(hdr_cells[0], "B8860B")
        set_cell_background(hdr_cells[1], "B8860B")
        for hc in hdr_cells:
            for p in hc.paragraphs:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        
        table.columns[0].width = Inches(1.8)
        table.columns[1].width = Inches(4.7)

        for el_name, el_desc in subitems:
            row_cells = table.add_row().cells
            row_cells[0].text = el_name
            row_cells[1].text = el_desc
            set_cell_background(row_cells[0], "FDFBF7")
            row_cells[0].paragraphs[0].runs[0].font.bold = True
            row_cells[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(184, 134, 11)
            row_cells[1].paragraphs[0].runs[0].font.size = Pt(10)
            set_cell_margins(row_cells[0])
            set_cell_margins(row_cells[1])
        
        doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # BAB III
    style_heading(doc.add_paragraph(), "BAB III: MITIGASI KERENTANAN OWASP TOP 10", 15, True, (184, 134, 11), 16, 6)
    owasp_items = [
        ("A01: Broken Access Control", "Dicegah dengan Navigation Guard terenkapsulasi dan verifikasi token Bearer pada setiap rute admin."),
        ("A02: Cryptographic Failures", "Enkripsi transmisi data via HTTPS/TLS dan penyimpanan kata sandi menggunakan salted hash BCrypt."),
        ("A03: Injection (SQLi & XSS)", "Pembersihan input klien dengan sanitizeInput() dan Prepared Statements pada query database."),
        ("A04: Insecure Design", "Menerapkan prinsip Defense in Depth dan pemisahan wewenang (Separation of Concerns)."),
        ("A05: Security Misconfiguration", "Pengaturan CORS aman dan standarisasi penanganan error tanpa membocorkan info sensitif."),
        ("A06: Vulnerable Components", "Audit dependensi berkala dan penggunaan framework resmi stabil (Vue 3, Vuetify 3)."),
        ("A07: Auth & ID Failures", "Proteksi brute force account lockout 60 detik setelah 3 kali gagal dan session cleanup saat logout."),
        ("A08: Software Integrity", "Verifikasi paket melalui lockfile terisolasi dan validasi integritas struktur relasi data."),
        ("A09: Logging & Monitoring", "Penerapan tabel audit_logs dan antarmuka visual AuditLogs.vue untuk pemantauan insiden real-time."),
        ("A10: SSRF Prevention", "Endpoint API hanya melayani rute terdaftar dan tidak melakukan pemanggilan URL sembarang.")
    ]
    for code, desc in owasp_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        r1 = p.add_run(f"• {code}: ")
        r1.font.bold = True
        r1.font.color.rgb = RGBColor(184, 134, 11)
        r2 = p.add_run(desc)

    # BAB IV
    style_heading(doc.add_paragraph(), "BAB IV: SKEMA BASIS DATA & KONTROL KEAMANAN DATA", 15, True, (184, 134, 11), 16, 6)
    add_p(doc, "Skema basis data relasional luxury_store_db dirancang secara normal (3NF) dan dilengkapi tabel keamanan khusus. Berkas database.sql disertakan secara lengkap dengan struktur tabel sebagai berikut:")
    add_p(doc, "1. users: user_id (PK), username, email, password_hash, role (admin/customer), membership_level, failed_login_count, locked_until.\n2. brands: brand_id (PK), name, description, created_at.\n3. products: product_id (PK), brand_id (FK), name, description, price, stock, image_url.\n4. orders: order_id (PK), user_id (FK), customer_name, customer_email, total_amount, status, payment_method.\n5. order_items: item_id (PK), order_id (FK), product_id (FK), product_name, price, quantity, subtotal.\n6. audit_logs: log_id (PK), actor, role, category, action, details, severity, status, ip_address, created_at.\n7. login_attempts: attempt_id (PK), ip_address, username, attempts_count, locked_until, last_attempt_at.")

    # BAB V
    style_heading(doc.add_paragraph(), "BAB V: PANDUAN DAN SIMULASI WAWANCARA DOSEN (INTERVIEW PREP)", 15, True, (184, 134, 11), 16, 6)
    add_p(doc, "Seluruh anggota kelompok wajib mempelajari pertanyaan di bawah ini untuk menghindari nilai 0 saat sesi wawancara individu:")

    qa_list = [
        ("Pertanyaan 1: Coba jelaskan konsep 5A pada aplikasi Luxury Store Anda!",
         "Jawaban: Konsep 5A terdiri dari Authentication (verifikasi identitas via form login, password hash, dan brute-force lockout 60 detik), Authorization (pembatasan hak akses admin via Vue Router guard dan Bearer Token), Accounting (pencatatan otomatis seluruh operasi login dan CRUD ke log aktivitas), Auditing (fasilitas inspeksi log, filter keparahan bahaya, dan ekspor CSV di menu Audit Keamanan), serta Availability/Assurance (pembersihan input XSS, pencegahan crash server, dan jaminan ketersediaan layanan)."),
        ("Pertanyaan 2: Apa yang terjadi jika ada pengguna salah memasukkan password berkali-kali?",
         "Jawaban: Sistem kami memiliki Brute-Force Protection pada security.js. Jika salah password 3 kali berturut-turut, tombol login terkunci otomatis selama 60 detik dengan hitung mundur visual, dan sistem mencatat insiden keamanan tingkat DANGER pada log audit."),
        ("Pertanyaan 3: Apa bedanya Accounting dan Auditing di sistem Anda?",
         "Jawaban: Accounting adalah proses pencatatan data mentah aktivitas (siapa, apa, kapan, status) secara otomatis di balik layar. Sedangkan Auditing adalah proses peninjauan, analisis, dan pemeriksaan rekaman tersebut oleh administrator melalui halaman Audit Keamanan untuk mendeteksi anomali atau mencetak laporan kepatuhan."),
        ("Pertanyaan 4: Bagaimana sistem mencegah orang membuka menu admin tanpa login?",
         "Jawaban: Melalui mekanisme Authorization di src/router/index.js menggunakan fungsi router.beforeEach. Jika rute memiliki meta.requiresAuth dan tidak ditemukan token login di browser, pengguna langsung dialihkan paksa (redirect) ke halaman /login."),
        ("Pertanyaan 5: Di mana letak implementasi Availability dan Assurance?",
         "Jawaban: Assurance diwujudkan melalui fungsi sanitizeInput() untuk mencegah serangan injeksi skrip XSS pada form produk dan pelanggan. Availability diwujudkan dengan pembatasan laju login untuk mencegah serangan DoS serta penanganan error terpusat agar web tidak pernah crash.")
    ]

    for q, a in qa_list:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(6)
        p_q.paragraph_format.space_after = Pt(2)
        r_q = p_q.add_run(q)
        r_q.font.bold = True
        r_q.font.color.rgb = RGBColor(184, 134, 11)

        p_a = doc.add_paragraph()
        p_a.paragraph_format.space_after = Pt(6)
        r_a = p_a.add_run(a)
        r_a.font.size = Pt(10.5)

    doc.save("c:/Users/ASUS/tugas ki/DOKUMENTASI_TUGAS_BESAR_KEAMANAN_INFORMASI.docx")
    print("Main Docx Generated!")

# -------------------------------------------------------------
# 2. GENERATE FORM_PEMBAGIAN_TUGAS.docx
# -------------------------------------------------------------
def generate_pembagian_tugas():
    doc = Document()
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(4)
    r1 = p_title.add_run("FORM PEMBAGIAN TUGAS KELOMPOK\n")
    r1.font.bold = True
    r1.font.size = Pt(16)
    r1.font.color.rgb = RGBColor(184, 134, 11)

    r2 = p_title.add_run("TUGAS BESAR KEAMANAN INFORMASI (UTS & UAS)\n")
    r2.font.bold = True
    r2.font.size = Pt(12)
    r2.font.color.rgb = RGBColor(70, 70, 70)

    add_p(doc, "Judul Proyek: Implementasi Konsep Keamanan 5A pada Sistem E-Commerce Luxury Store", 11, True, False, (50, 50, 50), 10, WD_ALIGN_PARAGRAPH.CENTER)

    table = doc.add_table(rows=1, cols=6)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["No", "Nama Mahasiswa", "NIM", "Peran", "Rincian Tugas & Kontribusi", "Paraf"]
    widths = [Inches(0.4), Inches(1.4), Inches(1.0), Inches(1.3), Inches(2.2), Inches(0.8)]
    
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "B8860B")
        cell.width = widths[i]

    data = [
        ("1", "[Nama Anggota 1]", "[NIM 1]", "Ketua & Security Specialist", "Merancang arsitektur 5A, implementasi mitigasi Brute Force lockout & audit logger (security.js), pengujian keamanan OWASP Top 10.", "[.......]"),
        ("2", "[Nama Anggota 2]", "[NIM 2]", "Frontend Dev (Storefront)", "Membangun tampilan katalog publik Storefront, keranjang belanja (Cart Drawer), integrasi form checkout, dan penanganan input sanitization.", "[.......]"),
        ("3", "[Nama Anggota 3]", "[NIM 3]", "Frontend Dev (Admin Panel)", "Mengembangkan layout Admin Dashboard, implementasi Vue Router navigation guard (RBAC), dan halaman Pusat Audit Keamanan (AuditLogs.vue).", "[.......]"),
        ("4", "[Nama Anggota 4]", "[NIM 4]", "Database & Tech Writer", "Merancang skema database relasional 3NF (database.sql) termasuk tabel audit_logs & login_attempts, menyusun dokumen laporan lengkap dan berkas administrasi tim.", "[.......]")
    ]

    for row_idx, item in enumerate(data):
        row_cells = table.add_row().cells
        for col_idx, val in enumerate(item):
            row_cells[col_idx].text = val
            row_cells[col_idx].width = widths[col_idx]
            set_cell_margins(row_cells[col_idx], 80, 80, 100, 100)
            if col_idx == 0:
                row_cells[col_idx].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[col_idx].paragraphs[0].runs[0].font.size = Pt(9.5)
            if row_idx % 2 == 1:
                set_cell_background(row_cells[col_idx], "F7F5F0")

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(24)
    p_sig.add_run("Mengetahui,\nKetua Kelompok\n\n\n\n___________________________\nNIM. ")

    doc.save("c:/Users/ASUS/tugas ki/FORM_PEMBAGIAN_TUGAS.docx")
    print("Pembagian Tugas Docx Generated!")

# -------------------------------------------------------------
# 3. GENERATE FORM_ANGGOTA_TIDAK_BEKERJA.docx
# -------------------------------------------------------------
def generate_anggota_tidak_bekerja():
    doc = Document()
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(4)
    r1 = p_title.add_run("FORM EVALUASI ANGGOTA KELOMPOK / KONTRIBUSI TIM\n")
    r1.font.bold = True
    r1.font.size = Pt(15)
    r1.font.color.rgb = RGBColor(184, 134, 11)

    r2 = p_title.add_run("TUGAS BESAR KEAMANAN INFORMASI (UTS & UAS)\n")
    r2.font.bold = True
    r2.font.size = Pt(12)
    r2.font.color.rgb = RGBColor(70, 70, 70)

    add_p(doc, "Petunjuk: Formulir ini digunakan untuk mendokumentasikan kinerja dan kedisiplinan anggota kelompok secara transparan.", 10.5, False, True, (90, 90, 90), 10)

    add_p(doc, "STATUS KONTRIBUSI KELOMPOK (Beri tanda [X] pada pilihan yang sesuai):", 11, True, False, (50, 50, 50), 4)
    add_p(doc, "[ X ] OPSI A: SEMUA ANGGOTA BEKERJA DENGAN BAIK & MEMAHAMI KONSEP 5A\nSeluruh anggota kelompok berpartisipasi aktif, menyelesaikan tanggung jawab masing-masing, dan siap mengikuti ujian wawancara.", 10.5, False, False, (40, 40, 40), 6)
    add_p(doc, "[   ] OPSI B: TERDAPAT ANGGOTA YANG TIDAK BERKONTRIBUSI / TIDAK BEKERJA\nTerdapat anggota yang melalaikan tugas, tidak hadir dalam koordinasi, dan dilaporkan untuk ditindaklanjuti oleh dosen pengampu.", 10.5, False, False, (40, 40, 40), 10)

    add_p(doc, "TABEL EVALUASI KINERJA REKAN SEJAWAT (PEER REVIEW):", 11, True, False, (50, 50, 50), 4)

    table = doc.add_table(rows=1, cols=6)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["No", "Nama Mahasiswa", "NIM", "Kehadiran (1-5)", "Kualitas Tugas (1-5)", "Status Kontribusi"]
    widths = [Inches(0.4), Inches(1.8), Inches(1.1), Inches(1.1), Inches(1.2), Inches(1.4)]
    
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "B8860B")
        cell.width = widths[i]

    members = [
        ("1", "[Nama Anggota 1]", "[NIM 1]", "5", "5", "Sangat Aktif"),
        ("2", "[Nama Anggota 2]", "[NIM 2]", "5", "5", "Sangat Aktif"),
        ("3", "[Nama Anggota 3]", "[NIM 3]", "5", "5", "Sangat Aktif"),
        ("4", "[Nama Anggota 4]", "[NIM 4]", "5", "5", "Sangat Aktif")
    ]

    for row_idx, item in enumerate(members):
        row_cells = table.add_row().cells
        for col_idx, val in enumerate(item):
            row_cells[col_idx].text = val
            row_cells[col_idx].width = widths[col_idx]
            set_cell_margins(row_cells[col_idx], 80, 80, 100, 100)
            if col_idx in [0, 3, 4, 5]:
                row_cells[col_idx].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[col_idx].paragraphs[0].runs[0].font.size = Pt(9.5)

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(20)
    p_sig.add_run("Pengesahan Tim:\nTanggal: ........................................, 2024/2025\n\n")
    p_sig.add_run("Tanda Tangan Anggota 1      Tanda Tangan Anggota 2      Tanda Tangan Anggota 3      Tanda Tangan Anggota 4\n\n\n\n")
    p_sig.add_run("(...................................)      (...................................)      (...................................)      (...................................)")

    doc.save("c:/Users/ASUS/tugas ki/FORM_ANGGOTA_TIDAK_BEKERJA.docx")
    print("Anggota Tidak Bekerja Docx Generated!")

if __name__ == '__main__':
    generate_main_doc()
    generate_pembagian_tugas()
    generate_anggota_tidak_bekerja()
