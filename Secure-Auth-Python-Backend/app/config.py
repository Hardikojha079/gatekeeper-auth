import os
from datetime import timedelta
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    REDIS_URL = os.getenv('REDIS_URL')

    encoded_password = quote_plus(DB_PASSWORD)
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}?client_encoding=utf8&connect_timeout=5"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    REDIS_URL = 'redis://localhost:6379/0'
    print("🔍 DEBUG: Database Connection Details")
    print(f"    DB_USER: {DB_USER}")
    print(f"    DB_HOST: {DB_HOST}")
    print(f"    DB_PORT: {DB_PORT}")
    print(f"    DB_NAME: {DB_NAME}")
    print(f"    SQLALCHEMY_DATABASE_URI: {SQLALCHEMY_DATABASE_URI.replace(DB_PASSWORD, '******')}")  

    @classmethod
    def validate_config(cls):
        if not cls.SQLALCHEMY_DATABASE_URI:
            raise EnvironmentError("❌ ERROR: DATABASE_URL environment variable not set")
        if not cls.JWT_SECRET_KEY:
            raise EnvironmentError("❌ ERROR: JWT_SECRET_KEY environment variable not set")
        print("✅ Configuration validated successfully!")

Config.validate_config()
