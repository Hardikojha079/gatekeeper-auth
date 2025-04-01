# from flask import jsonify, current_app
from flask_jwt_extended import create_access_token
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .models import DB, db
from datetime import timedelta
import logging
from sqlalchemy.exc import SQLAlchemyError
import redis

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

redis_client = redis.Redis(
    host='localhost', 
    port=6379,         
    db=0,
    decode_responses=True
)

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379",  
    strategy="fixed-window",  # or "moving-window"
    default_limits=["200 per day", "50 per hour"]
)

def validate_account_number(account_number):
    return account_number and account_number.isdigit() and len(account_number) == 12

@limiter.limit("5 per minute") 
def register_user(account_number, first_name, last_name, age, gender, phone_number, 
                 address, bank_account_type, date_of_account_opening, branch_code, password):
    
    if not validate_account_number(account_number):
        return {
            "success": False, 
            "message": "Invalid account number. Must be exactly 12 digits."
        }, 400

    if DB.query.filter_by(account_number=account_number).first():
        return {
            "success": False, 
            "message": "User with this account number already exists"
        }, 409

    try:
        new_user = DB(
            account_number=account_number,
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            phone_number=phone_number,
            address=address,
            bank_account_type=bank_account_type,
            date_of_account_opening=date_of_account_opening,
            branch_code=branch_code
        )
        
        try:
            new_user.set_password(password)
        except ValueError as e:
            return {"success": False, "message": str(e)}, 400

        db.session.add(new_user)
        db.session.commit()
        
        logger.info(f"User registered successfully: {account_number}")
        return {
            "success": True, 
            "message": "User registered successfully",
            "account_number": account_number
        }, 201

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error during registration: {str(e)}")
        return {
            "success": False, 
            "message": "Database error occurred"
        }, 500
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error during registration: {str(e)}")
        return {
            "success": False, 
            "message": "An unexpected error occurred"
        }, 500

@limiter.limit("10 per minute")  
def login_user(account_number, password):

    try:
        if not validate_account_number(account_number):
            return {
                "success": False, 
                "message": "Invalid account number format"
            }, 400

        user = DB.query.filter_by(account_number=account_number).first()
        if not user:
            logger.warning(f"Login attempt for non-existent user: {account_number}")
            return {
                "success": False, 
                "message": "Invalid credentials"
            }, 401
            
       
        try:
            if user.is_account_locked():
                logger.warning(f"Attempted login to locked account: {account_number}")
                return {
                    "success": False, 
                    "message": "Account is locked due to too many failed attempts. Please contact support."
                }, 403
        except TypeError:
            pass

        if user.check_password(password):
            claims = {
                "account_type": user.bank_account_type,
                "name": f"{user.first_name} {user.last_name}",
                "account_number": user.account_number
            }
            
            access_token = create_access_token(
                identity=user.account_number, 
                additional_claims=claims,
                expires_delta=timedelta(hours=1))
            
            user.record_login_attempt(success=True)
            
            logger.info(f"User logged in successfully: {account_number}")
            return {
                "success": True, 
                "token": access_token,
                "user": {
                    "name": f"{user.first_name} {user.last_name}",
                    "account_type": user.bank_account_type,
                    "account_number": user.account_number
                }
            }, 200
        else:
            user.record_login_attempt(success=False)
            
            logger.warning(f"Failed login attempt for user: {account_number}")
            return {
                "success": False, 
                "message": "Invalid credentials"
            }, 401

    except Exception as e:
        logger.error(f"Error during login process: {str(e)}", exc_info=True)
        return {
            "success": False, 
            "message": "An error occurred during authentication"
        }, 500