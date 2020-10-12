-- prepares a MySQL server for the CrossMe project

CREATE DATABASE IF NOT EXISTS crossmedb;
CREATE USER IF NOT EXISTS 'cm_dev'@'localhost' IDENTIFIED BY 'test';
GRANT ALL PRIVILEGES ON `crossmedb`.* TO 'cm_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'cm_dev'@'localhost';
FLUSH PRIVILEGES;
