DROP TABLE IF EXISTS eggs;

CREATE TABLE eggs(
    collection_date TEXT UNIQUE NOT NULL,
    amount INTEGER NOT NULL,
    notes TEXT
);

--INSERT INTO eggs (collection_date, amount, notes) VALUES ('2024/01/24',12,'1 from second coop');