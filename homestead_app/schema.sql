DROP TABLE IF EXISTS eggs;

CREATE TABLE eggs(
    collection_date TEXT UNIQUE NOT NULL,
    amount INTEGER NOT NULL,
    notes TEXT
);

INSERT INTO eggs (collection_date, amount) VALUES ('0000/10/01',12);
INSERT INTO eggs (collection_date, amount, notes) VALUES ('1000/11/02',20,'test notes');
-- INSERT INTO eggs (collection_date, amount) VALUES ('A little later (test)',3);
-- INSERT INTO eggs (collection_date, amount) VALUES ('Sometime (test)',0);