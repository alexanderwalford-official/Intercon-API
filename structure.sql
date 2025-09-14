-- ===========================
-- Main Database Schema
-- ===========================


-- Table: unique identifiers
CREATE TABLE IF NOT EXISTS uid_data (
    uid TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table: dictionary data
CREATE TABLE IF NOT EXISTS dict_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid INTEGER NOT NULL,
    oid INTEGER NOT NULL,
    data TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uid) REFERENCES uid_data(uid)
);

-- Table: product versions
CREATE TABLE IF NOT EXISTS product_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product VARCHAR(255) NOT NULL,
    version VARCHAR(20) NOT NULL,
    changelog TEXT NOT NULL
);

-- Table: API keys
CREATE TABLE IF NOT EXISTS api_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT NOT NULL
);

-- Table: Users
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);