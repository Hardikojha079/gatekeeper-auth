from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import logging
import os
from datetime import datetime
import sys
import io

if sys.stdout.encoding != 'UTF-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from app.config import Config

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout) 
    ]
)
logger = logging.getLogger(__name__)

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=Config.REDIS_URL
    )

def create_app():
    app = Flask(__name__)
    
   
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    app.config.from_object(Config)
    try:
        Config.validate_config()
    except EnvironmentError as e:
        logger.critical(f"❌ Configuration error: {e}")
        os._exit(1)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    with app.app_context():
        try:
            start_time = datetime.now()
            conn = db.engine.raw_connection()
            cursor = conn.cursor()
            
         
            cursor.execute("SELECT 1")
            cursor.fetchone()
            
           
            cursor.execute("SELECT version()")
            pg_version = cursor.fetchone()[0]
            
       
            cursor.execute("SELECT current_database()")
            db_name = cursor.fetchone()[0]
            
            conn.close()
            elapsed = (datetime.now() - start_time).total_seconds() * 1000
            logger.info(f"✅ Database connection successful (took {elapsed:.2f}ms)")
            logger.info(f"📊 PostgreSQL Version: {pg_version}")
            logger.info(f"🗃️ Connected to database: {db_name}")
            
        except Exception as e:
            logger.critical(f"❌ Database connection failed: {str(e)}")
            logger.error("💡 Troubleshooting tips:")
            logger.error("1. Check if PostgreSQL service is running")
            logger.error("2. Verify DB credentials in .env file")
            logger.error("3. Ensure database exists and user has permissions")
            logger.error(f"4. Test manually with: psql -U {Config.DB_USER} -h {Config.DB_HOST} -p {Config.DB_PORT} -d {Config.DB_NAME}")
            os._exit(1)
    
    from .routes import auth_bp
    app.register_blueprint(auth_bp)
    
  
    from .utils import (
        handle_bad_request, 
        handle_unauthorized, 
        handle_not_found, 
        handle_internal_error,
        handle_rate_limit_error
    )
    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(401, handle_unauthorized)
    app.register_error_handler(404, handle_not_found)
    app.register_error_handler(429, handle_rate_limit_error)
    app.register_error_handler(500, handle_internal_error)
    

    @app.route('/health')
    def health_check():
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "connected",
            "version": "1.0.0"
        }
    
    logger.info(f"🚀 Application initialized successfully in {app.config.get('ENV', 'production')} mode")
    return app
