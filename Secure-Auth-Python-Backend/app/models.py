from . import db
from bcrypt import hashpw, gensalt, checkpw
import logging
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DB(db.Model):
    __tablename__ = '<Your_Table_Name>'
    account_number = db.Column(db.String(12), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    bank_account_type = db.Column(db.String(50), nullable=False)
    date_of_account_opening = db.Column(db.Date, nullable=False)
    branch_code = db.Column(db.String(10), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    login_attempts = db.Column(db.Integer, default=0)
    last_failed_attempt = db.Column(db.DateTime)

    def set_password(self, password):
        try:
            if not password or len(password) < 8:
                raise ValueError("Password must be at least 8 characters long")

            if password.startswith("$2b$"):
                self.password_hash = password 
            else:
                self.password_hash = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

        except Exception as e:
            logger.error(f"Error hashing password: {e}")
            raise

    def check_password(self, password):
        try:
            if not self.password_hash:
                logger.error("No password hash stored for user")
                return False
            return checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
        except Exception as e:
            logger.error(f"Error checking password: {e}")
            return False

    def is_account_locked(self):
        if self.login_attempts < 5:
            return False
        if not self.last_failed_attempt:
            return False
        return datetime.utcnow() < (self.last_failed_attempt + timedelta(minutes=1))

    def record_login_attempt(self, success=False):
        try:
            if success:
                self.login_attempts = 0
                self.last_failed_attempt = None
                self.last_login = datetime.utcnow() 
            else:
                self.login_attempts += 1
                self.last_failed_attempt = datetime.utcnow()
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error recording login attempt: {e}")

    def to_dict(self):
        return {
            "account_number": self.account_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "gender": self.gender,
            "phone_number": self.phone_number,
            "address": self.address,
            "bank_account_type": self.bank_account_type,
            "date_of_account_opening": self.date_of_account_opening.strftime("%Y-%m-%d") if self.date_of_account_opening else None,
            "branch_code": self.branch_code,
            "last_login": self.last_login.strftime("%Y-%m-%d %H:%M:%S") if self.last_login else None
        }