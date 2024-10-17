CREATE TABLE articletable
(
    ID SERIAL PRIMARY KEY,
    source VARCHAR(255),
    title TEXT,
    body TEXT,
    published TIMESTAMP,
    link TEXT,
    category VARCHAR(255),
    summary TEXT
);