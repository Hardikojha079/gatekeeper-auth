import psycopg2
from config import Config

try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        port=Config.DB_PORT,
        connect_timeout=5
    )
    print("✅ Connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")