
PRAGMA foreign_keys = ON;

-- Удаление старых таблиц в обратном порядке
DROP TABLE IF EXISTS driver_blocks;
DROP TABLE IF EXISTS drivers;
DROP TABLE IF EXISTS driver_statuses;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS roles;

-- 1. Роли пользователей
CREATE TABLE roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- 2. Пользователи
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role_id INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

-- 3. Статусы водителей
CREATE TABLE driver_statuses (
    status_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- 4. Данные водителей
CREATE TABLE drivers (
    driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    age INTEGER NOT NULL CHECK (age >= 18),
    experience_years INTEGER NOT NULL
        CHECK (experience_years >= 0),
    status_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (status_id)
        REFERENCES driver_statuses(status_id),
    CHECK (experience_years <= age - 18)
);

-- 5. Блокировки водителей
CREATE TABLE driver_blocks (
    block_id INTEGER PRIMARY KEY AUTOINCREMENT,
    driver_id INTEGER NOT NULL,
    admin_id INTEGER NOT NULL,
    reason TEXT NOT NULL,
    blocked_at TEXT NOT NULL,
    FOREIGN KEY (driver_id) REFERENCES drivers(driver_id),
    FOREIGN KEY (admin_id) REFERENCES users(user_id)
);

-- Тестовые роли
INSERT INTO roles (name) VALUES
    ('Водитель'),
    ('Администратор');

-- Тестовые статусы
INSERT INTO driver_statuses (name) VALUES
    ('Активен'),
    ('Заблокирован'),
    ('На проверке');

-- Тестовые учётные записи
-- Хеши ниже являются демонстрационными значениями
INSERT INTO users (login, password_hash, role_id) VALUES
    ('driver01', 'demo_hash_001', 1),
    ('driver02', 'demo_hash_002', 1),
    ('admin01',  'demo_hash_003', 2);

-- Тестовые водители
INSERT INTO drivers
    (user_id, full_name, age, experience_years, status_id)
VALUES
    (1, 'Иванов Иван Иванович', 30, 8, 1),
    (2, 'Петров Пётр Петрович', 25, 4, 3);

-- Пример блокировки
INSERT INTO driver_blocks
    (driver_id, admin_id, reason, blocked_at)
VALUES
    (1, 3, 'Тестовая блокировка', '2026-10-14 12:00:00');
