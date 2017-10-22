-- Creates database wellness_dev_db
CREATE DATABASE IF NOT EXISTS wellness_dev_db;
USE wellness_dev_db;
CREATE USER IF NOT EXISTS 'wellness_dev'@'localhost';
SET PASSWORD FOR 'wellness_dev'@'localhost' = 'wellness_dev_pwd';
GRANT ALL PRIVILEGES ON wellness_dev_db.* TO 'wellness_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'wellness_dev'@'localhost';
