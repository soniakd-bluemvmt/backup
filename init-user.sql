-- Create user bluemvmt with password
CREATE USER bluemvmt WITH PASSWORD 'thisispostgres';

-- Grant all privileges on database search_db to bluemvmt
GRANT ALL PRIVILEGES ON DATABASE search_db TO bluemvmt;
