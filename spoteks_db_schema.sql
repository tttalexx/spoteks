-- Создание таблицы для пользователей
CREATE TABLE IF NOT EXISTS bd_user (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    user_sname VARCHAR(100) NOT NULL,
    user_tel VARCHAR(20) NOT NULL,
    user_email VARCHAR(100) UNIQUE NOT NULL,
    user_role VARCHAR(50) NOT NULL
);

-- Создание таблицы для продавцов
CREATE TABLE IF NOT EXISTS bd_seller (
    seller_id SERIAL PRIMARY KEY,
    seller_name VARCHAR(100) NOT NULL,
    seller_edrpou VARCHAR(10) NOT NULL,
    seller_address VARCHAR(200),
    seller_address_mail VARCHAR(200),
    seller_req TEXT
);

-- Создание таблицы для покупателей
CREATE TABLE IF NOT EXISTS bd_buyer (
    buyer_id SERIAL PRIMARY KEY,
    buyer_name VARCHAR(100) NOT NULL,
    buyer_edrpou VARCHAR(10) NOT NULL,
    buyer_address VARCHAR(200),
    buyer_address_mail VARCHAR(200),
    buyer_req TEXT
);

-- Создание таблицы для названий культур
CREATE TABLE IF NOT EXISTS bd_culture_name (
    culture_name VARCHAR(100) PRIMARY KEY
);

-- Создание таблицы для актуальных цен на культуры
CREATE TABLE IF NOT EXISTS culture_actual_price (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    culture_name VARCHAR(100) REFERENCES bd_culture_name(culture_name),
    culture_price NUMERIC(10, 2) NOT NULL
);

-- Создание таблицы для заказов
CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES bd_user(user_id),
    seller_id INTEGER REFERENCES bd_seller(seller_id),
    bd_culture_name VARCHAR(100) REFERENCES bd_culture_name(culture_name),
    quantity NUMERIC(10, 2) NOT NULL,
    dterms VARCHAR(100),
    quality VARCHAR(100),
    price NUMERIC(10, 2),
    price_auto_dterms NUMERIC(10, 2),
    price_train_dterms NUMERIC(10, 2),
    price_dterms NUMERIC(10, 2),
    status VARCHAR(50),
    load_region VARCHAR(100),
    load_place VARCHAR(100),
    unload_region VARCHAR(100),
    unload_place VARCHAR(100),
    comment_user TEXT,
    comment_spoteks TEXT,
    sb BOOLEAN DEFAULT FALSE,
    docks BOOLEAN DEFAULT FALSE,
    dog BOOLEAN DEFAULT FALSE,
    date DATE NOT NULL DEFAULT CURRENT_DATE
);
