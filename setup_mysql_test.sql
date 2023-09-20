CREATE DATABASE IF NOT EXISTS hbnb_test_db;
USE hbnb_test_db;
CREATE USER IF NOT EXISTS "hbnb_test"@"localhost" identified by "hbnb_test_pwd";
GRANT ALL privileges ON hbnb_dev_db.* TO "hbnb_test"@"localhost";
GRANT SELECT ON performance_schema.* TO "hbnb_test"@"localhost";
