--this script creates a table users
CREATE TABLE IF NOT EXISTS users (
    id NOT NULL INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);
