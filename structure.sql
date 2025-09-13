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