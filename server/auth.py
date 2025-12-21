"""Authentication and user management blueprint with Firebase."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User
from datetime import timedelta
import functools
import logging

logger = logging.getLogger(__name__)

auth = Blueprint('auth', __name__)


# Helper function to check if user is admin
def admin_required(f):
    """Decorator to require admin privileges."""
    @functools.wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.get_by_id(current_user_id)
        
        if not user or not user.get('is_admin'):
            return jsonify({"error": "Admin privileges required"}), 403
        return f(*args, **kwargs)
    return decorated_function


# Login route
@auth.route('/login', methods=['POST'])
def login():
    """
    Login endpoint for users and admins.
    
    Example request:
    {
        "username": "admin",
        "password": "admin123"
    }
    
    Example response:
    {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "user": {
            "id": "abc123",
            "username": "admin",
            "is_admin": true
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"error": "Missing username or password"}), 400
        
        # Get user by username
        user = User.get_by_username(data['username'])
        
        if not user:
            return jsonify({"error": "Invalid username or password"}), 401
        
        # Verify password
        if not User.check_password(user, data['password']):
            return jsonify({"error": "Invalid username or password"}), 401
        
        # Create access token
        access_token = create_access_token(
            identity=user['id'],
            expires_delta=timedelta(hours=24)
        )
        
        logger.info(f"User logged in: {user['username']}")
        
        return jsonify({
            "access_token": access_token,
            "user": {
                "id": user['id'],
                "username": user['username'],
                "is_admin": user.get('is_admin', False),
                "email": user.get('email')
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({"error": "An error occurred during login"}), 500


# Get current user
@auth.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current user details.
    Requires JWT token in Authorization header.
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.get_by_id(current_user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({
            "user": {
                "id": user['id'],
                "username": user['username'],
                "email": user.get('email'),
                "is_admin": user.get('is_admin', False)
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Get current user error: {e}")
        return jsonify({"error": "An error occurred"}), 500


# Create new user (admin only)
@auth.route('/users', methods=['POST'])
@admin_required
def create_user():
    """
    Create a new user (admin only).
    
    Example request:
    {
        "username": "newuser",
        "password": "password123",
        "email": "user@example.com",
        "is_admin": false
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"error": "Missing required fields"}), 400
        
        # Check if username already exists
        existing_user = User.get_by_username(data['username'])
        if existing_user:
            return jsonify({"error": "Username already exists"}), 400
        
        # Create user
        user = User.create(
            username=data['username'],
            password=data['password'],
            email=data.get('email'),
            is_admin=data.get('is_admin', False)
        )
        
        logger.info(f"New user created: {user['username']}")
        
        return jsonify({
            "message": "User created successfully",
            "user": user
        }), 201
        
    except Exception as e:
        logger.error(f"Create user error: {e}")
        return jsonify({"error": "An error occurred while creating user"}), 500


# Change password
@auth.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """
    Change password for current user.
    
    Example request:
    {
        "current_password": "oldpass",
        "new_password": "newpass"
    }
    """
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'current_password' not in data or 'new_password' not in data:
            return jsonify({"error": "Missing required fields"}), 400
        
        # Get user
        user = User.get_by_id(current_user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Verify current password
        if not User.check_password(user, data['current_password']):
            return jsonify({"error": "Current password is incorrect"}), 401
        
        # Update password
        User.update_password(current_user_id, data['new_password'])
        
        logger.info(f"Password changed for user: {user['username']}")
        
        return jsonify({"message": "Password changed successfully"}), 200
        
    except Exception as e:
        logger.error(f"Change password error: {e}")
        return jsonify({"error": "An error occurred while changing password"}), 500
