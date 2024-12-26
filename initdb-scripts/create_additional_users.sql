-- create_additional_users.sql
CREATE ROLE new_user WITH LOGIN PASSWORD 'newpassword';
ALTER ROLE new_user CREATEDB CREATEROLE;
GRANT ALL PRIVILEGES ON DATABASE dbname TO new_user;