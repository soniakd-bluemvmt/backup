import psycopg2
import os
import sys
DB_USER = os.getenv("DB_USER", "postgres")  
DB_NAME = os.getenv("POSTGRES_DB", "search_db")
DB_HOST = os.getenv("POSTGRES_HOST", "bluemvmt")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_PASS = os.getenv("POSTGRES_PASS", "thisispostgres")


def create_db_if_not_exists():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT,
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        exists = cur.fetchone()

        if not exists:
            print(f"Creating database '{DB_NAME}'...")
            cur.execute(f"CREATE DATABASE {DB_NAME}")
        else:
            print(f"Database '{DB_NAME}' already exists.")

        cur.close()
        conn.close()
    except Exception as e:
        print("❌ Failed to check/create database:", e, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    create_db_if_not_exists()
