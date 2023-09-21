-- Database creation with user creation also
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
USE hbnb_dev_db;
CREATE USER IF NOT EXISTS "hbnb_dev"@"localhost" identified by "hbnb_dev_pwd";
GRANT ALL privileges ON hbnb_dev_db.* TO "hbnb_dev"@"localhost";
GRANT SELECT ON performance_schema.* TO "hbnb_dev"@"localhost";
