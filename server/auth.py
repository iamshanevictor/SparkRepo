from flask import Blueprint, request, jsonify, current_app, session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User
from datetime import datetime, timedelta
import functools

auth = Blueprint('auth', __name__)

# Helper function to check if user is admin
def admin_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_admin:
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
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid username or password"}), 401
    
    # Update last login time
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # Create access token
    access_token = create_access_token(
        identity=user.id,
        expires_delta=timedelta(hours=24)
    )
    
    return jsonify({
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "is_admin": user.is_admin
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
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "user": user.to_dict()
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
    users = User.query.all()
    return jsonify({
        "users": [user.to_dict() for user in users]
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
    
    # Check if username already exists
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400
    
    # Check if email already exists (if provided)
    if 'email' in data and data['email']:
        existing_email = User.query.filter_by(email=data['email']).first()
        if existing_email:
            return jsonify({"error": "Email already exists"}), 400
    
    # Create new user
    new_user = User(
        username=data['username'],
        email=data.get('email'),
        is_admin=data.get('is_admin', False)
    )
    new_user.set_password(data['password'])
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        "message": "User created successfully",
        "user": new_user.to_dict()
    }), 201

# Initialize JWT for the app
def init_jwt(app):
    jwt = JWTManager(app)
    return jwt
