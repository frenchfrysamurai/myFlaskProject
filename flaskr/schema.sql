-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
  --My work in progress
  --email TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  --Old stuff below
  --title TEXT NOT NULL,
  --body TEXT NOT NULL,
  --My stuff below
  train TEXT NOT NULL,
  workout TEXT NOT NULL,
  sets INTEGER NOT NULL,
  reps INTEGER NOT NULL,
  weight REAL NOT NULL,
  date TEXT NOT NULL,
  duration INTEGER NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
