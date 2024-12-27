-- schema.sql
DROP TABLE IF EXISTS trainings;

DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    current_training TEXT, -- storing JSON as TEXT
    finished_training TEXT -- storing JSON as TEXT
);

CREATE TABLE IF NOT EXISTS trainings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    domain TEXT NOT NULL,
    description TEXT NOT NULL,
    chapters TEXT -- storing JSON as TEXT
);