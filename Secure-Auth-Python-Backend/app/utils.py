from flask import jsonify
import logging

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("errors.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def handle_bad_request(e):
    logger.error(f"Bad request: {e}")
    return jsonify({
        "success": False, 
        "message": "Bad request",
        "error": str(e) if str(e) else "Invalid request parameters"
    }), 400

def handle_unauthorized(e):
    logger.error(f"Unauthorized: {e}")
    return jsonify({
        "success": False, 
        "message": "Authentication required",
        "error": "You must be logged in to access this resource"
    }), 401

def handle_not_found(e):
    logger.error(f"Not found: {e}")
    return jsonify({
        "success": False, 
        "message": "Resource not found",
        "error": str(e) if str(e) else "The requested resource was not found"
    }), 404

def handle_rate_limit_error(e):
    logger.error(f"Rate limit exceeded: {e}")
    return jsonify({
        "success": False, 
        "message": "Too many requests",
        "error": "Rate limit exceeded. Please try again later."
    }), 429

def handle_internal_error(e):
    logger.error(f"Internal server error: {e}")
    return jsonify({
        "success": False, 
        "message": "Internal server error",
        "error": "An unexpected error occurred on the server"
    }), 500