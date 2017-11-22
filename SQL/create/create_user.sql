DROP TABLE users;

CREATE TABLE IF NOT EXISTS users(
  username VARCHAR(30),
  email VARCHAR(100),
  password VARCHAR(300),
  loadtime TIMESTAMP,
  PRIMARY KEY (username)
);

TRUNCATE TABLE users;