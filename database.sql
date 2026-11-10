-- =====================================================================
-- TUGAS BESAR KEAMANAN INFORMASI (UTS & UAS)
-- SISTEM: LUXURY STORE E-COMMERCE
-- SKEMA BASIS DATA & KONTROL KEAMANAN DATA (A5 COMPLIANT)
-- RDBMS: MySQL 8.0+ / MariaDB 10.4+ / PostgreSQL Compatible
-- =====================================================================

CREATE DATABASE IF NOT EXISTS `luxury_store_db` 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE `luxury_store_db`;

-- Matikan foreign key check sementara untuk setup bersih
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `order_items`;
DROP TABLE IF EXISTS `orders`;
DROP TABLE IF EXISTS `products`;
DROP TABLE IF EXISTS `brands`;
DROP TABLE IF EXISTS `audit_logs`;
DROP TABLE IF EXISTS `login_attempts`;
DROP TABLE IF EXISTS `users`;

SET FOREIGN_KEY_CHECKS = 1;

-- -------------------------------------------------------------
-- 1. TABEL: users (Menyimpan identitas pengguna & otorisasi RBAC)
-- Konsep 5A: Authentication (password_hash) & Authorization (role)
-- -------------------------------------------------------------
CREATE TABLE `users` (
    `user_id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL COMMENT 'BCrypt / Argon2 hashed password (Salted)',
    `role` ENUM('admin', 'customer', 'staff') NOT NULL DEFAULT 'customer' COMMENT 'Prinsip Least Privilege & RBAC',
    `membership_level` ENUM('Silver', 'Gold', 'Platinum') NOT NULL DEFAULT 'Silver',
    `is_active` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '1 = Aktif, 0 = Diblokir/Suspended',
    `failed_login_count` INT NOT NULL DEFAULT 0,
    `locked_until` DATETIME NULL DEFAULT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_users_username` (`username`),
    INDEX `idx_users_email` (`email`),
    INDEX `idx_users_role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -------------------------------------------------------------
-- 2. TABEL: brands (Kategori merek produk mewah)
-- -------------------------------------------------------------
CREATE TABLE `brands` (
    `brand_id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL UNIQUE,
    `description` TEXT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -------------------------------------------------------------
-- 3. TABEL: products (Katalog inventaris barang)
-- -------------------------------------------------------------
CREATE TABLE `products` (
    `product_id` INT AUTO_INCREMENT PRIMARY KEY,
    `brand_id` INT NOT NULL,
    `name` VARCHAR(150) NOT NULL,
    `description` TEXT NULL,
    `price` DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    `stock` INT NOT NULL DEFAULT 0,
    `image_url` VARCHAR(500) NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_products_brand` FOREIGN KEY (`brand_id`) 
        REFERENCES `brands` (`brand_id`) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX `idx_products_brand` (`brand_id`),
    INDEX `idx_products_price` (`price`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -------------------------------------------------------------
-- 4. TABEL: orders (Header transaksi pembelian pelanggan)
-- Konsep 5A: Accounting & Non-Repudiation (Jejak transaksi)
-- -------------------------------------------------------------
CREATE TABLE `orders` (
    `order_id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NULL COMMENT 'NULL jika tamu (guest checkout)',
    `customer_name` VARCHAR(100) NOT NULL,
    `customer_email` VARCHAR(100) NOT NULL,
    `customer_phone` VARCHAR(25) NOT NULL,
    `shipping_address` TEXT NOT NULL,
    `total_amount` DECIMAL(15, 2) NOT NULL,
    `status` ENUM('Pending', 'Diproses', 'Dikirim', 'Selesai', 'Batal') NOT NULL DEFAULT 'Pending',
    `payment_method` VARCHAR(50) NOT NULL DEFAULT 'Bank Transfer / VA',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_orders_user` FOREIGN KEY (`user_id`) 
        REFERENCES `users` (`user_id`) 
        ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX `idx_orders_user` (`user_id`),
    INDEX `idx_orders_status` (`status`),
    INDEX `idx_orders_created` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -------------------------------------------------------------
-- 5. TABEL: order_items (Detail barang dalam pesanan)
-- -------------------------------------------------------------
CREATE TABLE `order_items` (
    `item_id` INT AUTO_INCREMENT PRIMARY KEY,
    `order_id` INT NOT NULL,
    `product_id` INT NULL,
    `product_name` VARCHAR(150) NOT NULL,
    `price` DECIMAL(15, 2) NOT NULL,
    `quantity` INT NOT NULL DEFAULT 1,
    `subtotal` DECIMAL(15, 2) NOT NULL,
    CONSTRAINT `fk_items_order` FOREIGN KEY (`order_id`) 
        REFERENCES `orders` (`order_id`) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_items_product` FOREIGN KEY (`product_id`) 
        REFERENCES `products` (`product_id`) 
        ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX `idx_items_order` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -------------------------------------------------------------
-- 6. TABEL: audit_logs (Perekaman jejak keamanan sistem)
-- Konsep 5A: Accounting & Auditing (Pemeriksaan & Forensik Digital)
-- -------------------------------------------------------------
CREATE TABLE `audit_logs` (
    `log_id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `actor` VARCHAR(50) NOT NULL COMMENT 'Username atau Anonymous',
    `role` VARCHAR(30) NOT NULL COMMENT 'Administrator, Customer, Guest, System',
    `category` ENUM('Authentication', 'Authorization', 'Data Management', 'Auditing', 'System') NOT NULL,
    `action` VARCHAR(100) NOT NULL COMMENT 'Contoh: AUTH_LOGIN_SUCCESS, USER_DELETE',
    `details` TEXT NULL COMMENT 'Deskripsi detail aktivitas / perubahan',
    `severity` ENUM('INFO', 'SUCCESS', 'WARNING', 'DANGER') NOT NULL DEFAULT 'INFO',
    `status` ENUM('SUCCESS', 'FAILED', 'BLOCKED', 'LOCKED') NOT NULL DEFAULT 'SUCCESS',
    `ip_address` VARCHAR(45) NOT NULL DEFAULT '127.0.0.1',
    `user_agent` VARCHAR(255) NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_audit_actor` (`actor`),
    INDEX `idx_audit_category` (`category`),
    INDEX `idx_audit_severity` (`severity`),
    INDEX `idx_audit_created` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -------------------------------------------------------------
-- 7. TABEL: login_attempts (Rate limiting & mitigasi Brute Force)
-- Konsep 5A: Authentication & Availability
-- -------------------------------------------------------------
CREATE TABLE `login_attempts` (
    `attempt_id` INT AUTO_INCREMENT PRIMARY KEY,
    `ip_address` VARCHAR(45) NOT NULL,
    `username` VARCHAR(50) NOT NULL,
    `attempts_count` INT NOT NULL DEFAULT 1,
    `locked_until` DATETIME NULL DEFAULT NULL,
    `last_attempt_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY `uk_ip_user` (`ip_address`, `username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================================
-- DATA AWAL (SEEDING SAMPLE DATA UNTUK PENGUJIAN)
-- =============================================================

-- 1. Sample Users (Password default: 'Admin@Luxury2024!' -> hash BCrypt simulasi)
INSERT INTO `users` (`username`, `email`, `password_hash`, `role`, `membership_level`, `is_active`) VALUES
('admin', 'admin@luxurystore.com', '$2y$10$wE9V1L0dHQwPqv1hGzO0eeZ2F6W5Z1R4eW2k3qP9w8x0Y1z2a3b4c', 'admin', 'Platinum', 1),
('steven_tan', 'steven@example.com', '$2y$10$wE9V1L0dHQwPqv1hGzO0eeZ2F6W5Z1R4eW2k3qP9w8x0Y1z2a3b4c', 'customer', 'Platinum', 1),
('clarissa_w', 'clarissa@example.com', '$2y$10$wE9V1L0dHQwPqv1hGzO0eeZ2F6W5Z1R4eW2k3qP9w8x0Y1z2a3b4c', 'customer', 'Gold', 1),
('budi_santoso', 'budi@example.com', '$2y$10$wE9V1L0dHQwPqv1hGzO0eeZ2F6W5Z1R4eW2k3qP9w8x0Y1z2a3b4c', 'customer', 'Silver', 1);

-- 2. Sample Brands
INSERT INTO `brands` (`name`, `description`) VALUES
('Rolex', 'Jam tangan mewah Swiss dengan presisi tinggi dan bahan eksklusif'),
('Gucci', 'Brand fesyen mewah legendaris asal Italia'),
('Louis Vuitton', 'Rumah mode asal Prancis terkemuka dengan lini koper dan tas mewah'),
('Hermes', 'Produsen barang mewah spesialis kulit dan aksesori gaya hidup Prancis');

-- 3. Sample Products
INSERT INTO `products` (`brand_id`, `name`, `description`, `price`, `stock`, `image_url`) VALUES
(1, 'Rolex Submariner Date 41mm', 'Oystersteel dengan bezel Cerachrom hitam dan dial hitam elegan', 215000000.00, 3, 'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=600'),
(1, 'Rolex Daytona Cosmograph', 'Emas putih 18 karat dengan bezel Cerachrom dan dial baja cerah', 580000000.00, 1, 'https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=600'),
(2, 'Gucci Horsebit 1955 Bag', 'Tas selempang kulit bertekstur dengan ornamen logam khas Horsebit', 48500000.00, 5, 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=600'),
(3, 'Louis Vuitton Keepall Bandoulière 50', 'Tas bepergian berbahan Monogram Eclipse Canvas ikonik', 39000000.00, 4, 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600'),
(4, 'Hermès Birkin 25 Togo Gold Hardware', 'Tas legendaris kulit Togo asli dengan finishing emas murni', 420000000.00, 2, 'https://images.unsplash.com/photo-1594223274512-ad4803739b7c?w=600');

-- 4. Sample Orders
INSERT INTO `orders` (`user_id`, `customer_name`, `customer_email`, `customer_phone`, `shipping_address`, `total_amount`, `status`, `payment_method`) VALUES
(2, 'Steven Tan', 'steven@example.com', '081298765432', 'Jl. Sudirman No. 88, Penthouse Tower, Jakarta Selatan', 215000000.00, 'Selesai', 'Bank Transfer (BCA Priority)'),
(3, 'Clarissa Wijaya', 'clarissa@example.com', '081387654321', 'Jl. Bukit Darmo Golf No. 12, Surabaya', 48500000.00, 'Diproses', 'Credit Card Platinum');

-- 5. Sample Order Items
INSERT INTO `order_items` (`order_id`, `product_id`, `product_name`, `price`, `quantity`, `subtotal`) VALUES
(1, 1, 'Rolex Submariner Date 41mm', 215000000.00, 1, 215000000.00),
(2, 3, 'Gucci Horsebit 1955 Bag', 48500000.00, 1, 48500000.00);

-- 6. Sample Initial Audit Logs
INSERT INTO `audit_logs` (`actor`, `role`, `category`, `action`, `details`, `severity`, `status`, `ip_address`, `user_agent`) VALUES
('system', 'System', 'System', 'DATABASE_INITIALIZATION', 'Skema basis data dan tabel keamanan 5A berhasil dibuat', 'INFO', 'SUCCESS', '127.0.0.1', 'DB-Migration-Runner'),
('admin', 'Administrator', 'Authentication', 'AUTH_LOGIN_SUCCESS', 'Administrator login dari IP terotorisasi', 'SUCCESS', 'SUCCESS', '192.168.1.10', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0'),
('clarissa_w', 'Customer', 'Data Management', 'CHECKOUT_ORDER', 'Pelanggan berhasil membuat transaksi pesanan #2', 'INFO', 'SUCCESS', '180.252.12.4', 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0) Mobile');

-- Selesai
