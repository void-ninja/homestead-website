DROP TABLE IF EXISTS eggs;

CREATE TABLE eggs(
    collection_date TEXT UNIQUE NOT NULL,
    amount INTEGER NOT NULL
);