from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from .models import DB, db
from .auth import register_user, login_user
from . import limiter
from datetime import datetime
import re
import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text 


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


auth_bp = Blueprint('auth', __name__)


def validate_phone_number(phone_number):
    return bool(re.match(r"^\(\d{3}\) \d{3}-\d{4}$", phone_number))

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
        
def validate_account_number(account_number):
    return bool(re.match(r"^\d{12}$", account_number))


@auth_bp.route('/register', methods=['POST'])
@limiter.limit("10 per minute") 
def register():
    data = request.get_json()
    if not data:
        logger.error("No JSON data in request")
        return jsonify({"success": False, "message": "Request must contain JSON data"}), 400

    required_fields = [
        'account_number', 'first_name', 'last_name', 'age', 'gender', 
        'phone_number', 'address', 'bank_account_type', 
        'date_of_account_opening', 'branch_code', 'password'
    ]

 
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        logger.error(f"Missing required fields during registration: {missing_fields}")
        return jsonify({"success": False, "message": f"Missing required fields: {', '.join(missing_fields)}"}), 400


    if not validate_account_number(data['account_number']):
        logger.error(f"Invalid account number format: {data['account_number']}")
        return jsonify({"success": False, "message": "Invalid account number format. Must be 12 digits."}), 400

    if not validate_phone_number(data['phone_number']):
        logger.error(f"Invalid phone number format: {data['phone_number']}")
        return jsonify({"success": False, "message": "Invalid phone number format. Use (XXX) XXX-XXXX."}), 400

    if not validate_date(data['date_of_account_opening']):
        logger.error(f"Invalid date format: {data['date_of_account_opening']}")
        return jsonify({"success": False, "message": "Invalid date format. Use YYYY-MM-DD."}), 400
        
  
    try:
        age = int(data['age'])
        if age < 18 or age > 120:
            logger.error(f"Invalid age: {age}")
            return jsonify({"success": False, "message": "Age must be between 18 and 120."}), 400
    except (ValueError, TypeError):
        logger.error(f"Invalid age format: {data['age']}")
        return jsonify({"success": False, "message": "Age must be a valid number."}), 400


    response, status_code = register_user(
        account_number=data['account_number'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        age=age,
        gender=data['gender'],
        phone_number=data['phone_number'],
        address=data['address'],
        bank_account_type=data['bank_account_type'],
        date_of_account_opening=data['date_of_account_opening'],
        branch_code=data['branch_code'],
        password=data['password']
    )

    return jsonify(response), status_code

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute") 
def login():
    data = request.get_json()
    if not data:
        logger.error("No JSON data in login request")
        return jsonify({"success": False, "message": "Request must contain JSON data"}), 400

   
    if not data.get('account_number'):
        logger.error("Missing account number during login")
        return jsonify({"success": False, "message": "Account number is required"}), 400
        
    if not data.get('password'):
        logger.error("Missing password during login")
        return jsonify({"success": False, "message": "Password is required"}), 400

    response, status_code = login_user(data['account_number'], data['password'])
    return jsonify(response), status_code

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:

        account_number = get_jwt_identity()
        user = DB.query.filter_by(account_number=account_number).first()
        if not user:
            logger.error(f"User not found for profile fetch: {account_number}")
            return jsonify({"success": False, "message": "User not found"}), 404
   
        return jsonify({
            "success": True,
            "profile": user.to_dict()
        }), 200
    except Exception as e:
        logger.error(f"Error fetching user profile: {e}")
        return jsonify({"success": False, "message": "An error occurred while fetching profile"}), 500


@auth_bp.route('/', methods=['GET'])
@jwt_required()
def get_details():
    try:
    
        claims = get_jwt()
    
        users = DB.query.all()
        return jsonify({
            "success": True,
            "users": [user.to_dict() for user in users]
        }), 200
    except Exception as e:
        logger.error(f"Error fetching user details: {e}")
        return jsonify({"success": False, "message": "Internal server error"}), 500


@auth_bp.route('/', methods=['POST'])
@jwt_required()
def add_details():
    data = request.get_json()
    if not data:
        logger.error("No JSON data in add customer request")
        return jsonify({"success": False, "message": "Request must contain JSON data"}), 400

    required_fields = [
        'account_number', 'first_name', 'last_name', 'age', 'gender', 
        'phone_number', 'address', 'bank_account_type', 
        'date_of_account_opening', 'branch_code', 'password'
    ]


    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        logger.error(f"Missing required fields while adding a new customer: {missing_fields}")
        return jsonify({"success": False, "message": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    if not validate_account_number(data['account_number']):
        logger.error(f"Invalid account number format: {data['account_number']}")
        return jsonify({"success": False, "message": "Invalid account number format. Must be 12 digits."}), 400

    if not validate_phone_number(data['phone_number']):
        logger.error(f"Invalid phone number format: {data['phone_number']}")
        return jsonify({"success": False, "message": "Invalid phone number format. Use (XXX) XXX-XXXX."}), 400

    if not validate_date(data['date_of_account_opening']):
        logger.error(f"Invalid date format: {data['date_of_account_opening']}")
        return jsonify({"success": False, "message": "Invalid date format. Use YYYY-MM-DD."}), 400


    response, status_code = register_user(
        account_number=data['account_number'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        age=data['age'],
        gender=data['gender'],
        phone_number=data['phone_number'],
        address=data['address'],
        bank_account_type=data['bank_account_type'],
        date_of_account_opening=data['date_of_account_opening'],
        branch_code=data['branch_code'],
        password=data['password']
    )

    return jsonify(response), status_code


@auth_bp.route('/<string:account_number>', methods=['PUT'])
@jwt_required()
def update_details(account_number):
    if not validate_account_number(account_number):
        logger.error(f"Invalid account number format in update: {account_number}")
        return jsonify({"success": False, "message": "Invalid account number format. Must be 12 digits."}), 400
        
    data = request.get_json()
    if not data:
        logger.error("No JSON data in update request")
        return jsonify({"success": False, "message": "Request must contain JSON data"}), 400

    try:
     
        user = DB.query.filter_by(account_number=account_number).first()
        if not user:
            logger.error(f"Customer with account number {account_number} not found for update")
            return jsonify({"success": False, "message": f"Customer with account number {account_number} not found"}), 404


        if 'phone_number' in data:
            if not validate_phone_number(data['phone_number']):
                logger.error(f"Invalid phone number format in update: {data['phone_number']}")
                return jsonify({"success": False, "message": "Invalid phone number format. Use (XXX) XXX-XXXX."}), 400
            user.phone_number = data['phone_number']

        if 'date_of_account_opening' in data:
            if not validate_date(data['date_of_account_opening']):
                logger.error(f"Invalid date format in update: {data['date_of_account_opening']}")
                return jsonify({"success": False, "message": "Invalid date format. Use YYYY-MM-DD."}), 400
            user.date_of_account_opening = datetime.strptime(data['date_of_account_opening'], "%Y-%m-%d").date()

        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'age' in data:
            try:
                age = int(data['age'])
                if age < 18 or age > 120:
                    return jsonify({"success": False, "message": "Age must be between 18 and 120."}), 400
                user.age = age
            except (ValueError, TypeError):
                return jsonify({"success": False, "message": "Age must be a valid number."}), 400
        if 'gender' in data:
            user.gender = data['gender']
        if 'address' in data:
            user.address = data['address']
        if 'bank_account_type' in data:
            user.bank_account_type = data['bank_account_type']
        if 'branch_code' in data:
            user.branch_code = data['branch_code']
        if 'password' in data:
            user.set_password(data['password'])

        db.session.commit()
        logger.info(f"User details updated successfully: {account_number}")
        return jsonify({"success": True, "message": "Details updated successfully"}), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error updating user details: {e}")
        return jsonify({"success": False, "message": "Database error occurred"}), 500
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating user details: {e}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@auth_bp.route('/<string:account_number>', methods=['DELETE'])
@jwt_required()
def remove_details(account_number):
    if not validate_account_number(account_number):
        logger.error(f"Invalid account number format in delete: {account_number}")
        return jsonify({"success": False, "message": "Invalid account number format. Must be 12 digits."}), 400

    try:
        
        user = DB.query.filter_by(account_number=account_number).first()
        if not user:
            logger.error(f"Customer with account number {account_number} not found for deletion")
            return jsonify({"success": False, "message": f"Customer with account number {account_number} not found"}), 404

        db.session.delete(user)
        db.session.commit()
        logger.info(f"User details removed successfully: {account_number}")
        return jsonify({"success": True, "message": "Details removed successfully"}), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error deleting user: {e}")
        return jsonify({"success": False, "message": "Database error occurred"}), 500
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting user details: {e}")
        return jsonify({"success": False, "message": "Internal server error"}), 500
@auth_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"status": "Backend is running!"})
@auth_bp.route('/db_check', methods=['GET'])
def db_check():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"database": "connected"})
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return jsonify({
            "database": "error", 
            "details": str(e),
            "solution": "Check PostgreSQL service and connection parameters"
        }), 500
