-- 데이터베이스 생성 (docker-compose에서 자동 생성되지만 명시)
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

CREATE DATABASE IF NOT EXISTS asset_manager 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE asset_manager;

-- 계좌 테이블
CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL DEFAULT 1,
    name VARCHAR(100) NOT NULL COMMENT '계좌명',
    type ENUM('checking', 'savings', 'investment', 'cma') NOT NULL COMMENT '계좌 유형',
    balance DECIMAL(15, 2) NOT NULL DEFAULT 0 COMMENT '현재 잔액',
    institution VARCHAR(100) COMMENT '금융기관명',
    account_number VARCHAR(50) COMMENT '계좌번호',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_type (type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='계좌 정보';

-- 거래내역 테이블
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    type ENUM('income', 'expense', 'transfer') NOT NULL COMMENT '거래 유형',
    category VARCHAR(50) NOT NULL COMMENT '카테고리',
    amount DECIMAL(15, 2) NOT NULL COMMENT '금액',
    description TEXT COMMENT '설명',
    transaction_date DATE NOT NULL COMMENT '거래 날짜',
    is_recurring BOOLEAN DEFAULT FALSE COMMENT '정기 거래 여부',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE,
    INDEX idx_account_date (account_id, transaction_date),
    INDEX idx_type (type),
    INDEX idx_category (category),
    INDEX idx_transaction_date (transaction_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='거래 내역';

-- 정기 거래 테이블
CREATE TABLE recurring_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    type ENUM('income', 'expense') NOT NULL COMMENT '거래 유형',
    category VARCHAR(50) NOT NULL COMMENT '카테고리',
    amount DECIMAL(15, 2) NOT NULL COMMENT '금액',
    description TEXT COMMENT '설명',
    frequency ENUM('daily', 'weekly', 'monthly', 'yearly') NOT NULL DEFAULT 'monthly' COMMENT '주기',
    day_of_month INT COMMENT '매월 몇 일',
    is_active BOOLEAN DEFAULT TRUE COMMENT '활성화 여부',
    start_date DATE NOT NULL COMMENT '시작일',
    end_date DATE COMMENT '종료일',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE,
    INDEX idx_active (is_active),
    INDEX idx_day_of_month (day_of_month)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='정기 거래';

-- 지출 카테고리 테이블
CREATE TABLE budget_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL DEFAULT 1,
    name VARCHAR(50) NOT NULL COMMENT '카테고리명',
    monthly_limit DECIMAL(15, 2) COMMENT '월 예산',
    color VARCHAR(7) DEFAULT '#3B82F6' COMMENT 'UI 색상',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_category (user_id, name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='예산 카테고리';

-- 자산 스냅샷 테이블
CREATE TABLE asset_snapshots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL DEFAULT 1,
    total_assets DECIMAL(15, 2) NOT NULL COMMENT '총 자산',
    accounts_summary JSON COMMENT '계좌별 상세',
    snapshot_date DATE NOT NULL COMMENT '스냅샷 날짜',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_date (user_id, snapshot_date),
    UNIQUE KEY unique_user_snapshot_date (user_id, snapshot_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='자산 스냅샷';

-- 초기 데이터: 기본 카테고리
INSERT INTO budget_categories (name, color) VALUES
('급여', '#10B981'),
('청년도약', '#3B82F6'),
('ETF', '#8B5CF6'),
('CMA', '#F59E0B'),
('식비', '#EF4444'),
('교통비', '#06B6D4'),
('통신비', '#EC4899'),
('문화생활', '#F97316'),
('기타', '#6B7280');

-- 초기 데이터: 샘플 계좌 (당신의 실제 상황 기반)
INSERT INTO accounts (name, type, balance, institution) VALUES
('신한은행 입출금', 'checking', 0, '신한은행'),
('청년도약계좌', 'savings', 0, '은행'),
('ETF 투자계좌', 'investment', 0, '증권사'),
('CMA 계좌', 'cma', 0, '증권사');

-- 초기 데이터: 정기 수입/지출
INSERT INTO recurring_transactions (account_id, type, category, amount, description, day_of_month, start_date) VALUES
(1, 'income', '급여', 2700000, '월급', 25, '2025-01-01'),
(2, 'expense', '청년도약', 30000, '본인 기여금', 1, '2025-01-01'),
(3, 'expense', 'ETF', 300000, '월 적립', 1, '2025-01-01'),
(4, 'expense', 'CMA', 150000, '월 적립', 1, '2025-01-01');

-- 뷰: 총 자산 조회
CREATE VIEW v_total_assets AS
SELECT 
    user_id,
    SUM(balance) as total_balance,
    COUNT(*) as account_count
FROM accounts
GROUP BY user_id;

-- 뷰: 월별 고정 지출
CREATE VIEW v_monthly_fixed_expenses AS
SELECT 
    account_id,
    category,
    SUM(amount) as total_amount
FROM recurring_transactions
WHERE type = 'expense' AND is_active = TRUE
GROUP BY account_id, category;