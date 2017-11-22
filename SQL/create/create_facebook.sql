DROP TABLE facebook;

CREATE TABLE IF NOT EXISTS facebook(
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(30),
  trend VARCHAR(100),
  link VARCHAR(300),
  loadtime TIMESTAMP,
  FOREIGN KEY (username) REFERENCES users(username)
);

TRUNCATE TABLE facebook;