from flask import Blueprint, request, jsonify, current_app, session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from db_service import DatabaseService
from datetime import datetime, timedelta
import functools

auth = Blueprint('auth', __name__)

# Helper function to check if user is admin
def admin_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        db = DatabaseService()
        user = db.get_user_by_id(current_user_id)
        
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
        "password": "admin"
    }
    
    Example response:
    {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "user": {
            "id": 1,
            "username": "admin",
            "is_admin": true
        }
    }
    """
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing username or password"}), 400
    
    db = DatabaseService()
    user = db.get_user_by_username(data['username'])
    
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401
    
    # Verify password
    if not db.verify_password(user['password_hash'], data['password']):
        return jsonify({"error": "Invalid username or password"}), 401
    
    # Update last login time
    db.update_user_last_login(user['id'])
    
    # Create access token
    access_token = create_access_token(
        identity=user['id'],
        expires_delta=timedelta(hours=24)
    )
    
    return jsonify({
        "access_token": access_token,
        "user": {
            "id": user['id'],
            "username": user['username'],
            "is_admin": user.get('is_admin', False)
        }
    }), 200

# Get current user info
@auth.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current authenticated user information.
    
    Example response:
    {
        "user": {
            "id": 1,
            "username": "admin",
            "email": "admin@sparkrepo.com",
            "is_admin": true
        }
    }
    """
    current_user_id = get_jwt_identity()
    db = DatabaseService()
    user = db.get_user_by_id(current_user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Remove password_hash from response
    user_dict = {k: v for k, v in user.items() if k != 'password_hash'}
    
    return jsonify({
        "user": user_dict
    }), 200

# Admin only - Get all users
@auth.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    """
    Admin only - Get all users.
    
    Example response:
    {
        "users": [
            {
                "id": 1,
                "username": "admin",
                "email": "admin@sparkrepo.com",
                "is_admin": true
            }
        ]
    }
    """
    db = DatabaseService()
    users = db.get_all_users()
    
    # Remove password_hash from response
    users_list = [{k: v for k, v in user.items() if k != 'password_hash'} for user in users]
    
    return jsonify({
        "users": users_list
    }), 200

# Admin only - Create new user
@auth.route('/users', methods=['POST'])
@jwt_required()
@admin_required
def create_user():
    """
    Admin only - Create a new user.
    
    Example request:
    {
        "username": "teacher1",
        "password": "password123",
        "email": "teacher1@example.com",
        "is_admin": false
    }
    
    Example response:
    {
        "message": "User created successfully",
        "user": {
            "id": 2,
            "username": "teacher1",
            "email": "teacher1@example.com",
            "is_admin": false
        }
    }
    """
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    db = DatabaseService(use_admin=True)
    
    # Check if username already exists
    existing_user = db.get_user_by_username(data['username'])
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400
    
    # Check if email already exists (if provided)
    if 'email' in data and data['email']:
        existing_email = db.get_user_by_email(data['email'])
        if existing_email:
            return jsonify({"error": "Email already exists"}), 400
    
    # Create new user
    new_user = db.create_user(
        username=data['username'],
        password=data['password'],
        email=data.get('email'),
        is_admin=data.get('is_admin', False)
    )
    
    if not new_user:
        return jsonify({"error": "Failed to create user"}), 500
    
    # Remove password_hash from response
    user_dict = {k: v for k, v in new_user.items() if k != 'password_hash'}
    
    return jsonify({
        "message": "User created successfully",
        "user": user_dict
    }), 201

# Initialize JWT for the app
def init_jwt(app):
    jwt = JWTManager(app)
    return jwt
