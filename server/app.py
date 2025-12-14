"""Flask application factory for SparkRepo backend.

Initializes extensions, loads configuration, registers blueprints, and
exposes basic health and API discovery endpoints.
"""
import os
import secrets
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Initialize extensions
from api import api
from auth import auth, init_jwt
from admin import admin_api
from config import get_config
from db_service import DatabaseService
from utils.logger import setup_logger

logger = setup_logger(__name__)

def create_app(test_config=None):
    """Create and configure the Flask application."""
    # Load environment variables from .env (if present)
    load_dotenv()

    app = Flask(__name__)
    
    # Setup logging
    setup_logger('sparkrepo')
    logger.info("Initializing SparkRepo Flask application...")

    # Load config class
    try:
        ConfigClass = get_config()
        app.config.from_object(ConfigClass)
        logger.info(f"Configuration loaded: {ConfigClass.__name__}")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        raise

    # Verify Supabase configuration
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_KEY')
    if not supabase_url or not supabase_key:
        error_msg = "SUPABASE_URL and SUPABASE_KEY must be set in environment variables"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Configure JWT
    jwt_secret = os.environ.get('JWT_SECRET_KEY') or secrets.token_hex(32)
    app.config['JWT_SECRET_KEY'] = jwt_secret
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 86400))
    
    logger.info(f"JWT configured with {len(jwt_secret)} character secret")

    # Initialize JWT
    try:
        init_jwt(app)
        logger.info("JWT manager initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize JWT: {e}")
        raise

    # Register blueprints
    try:
        logger.info("Registering blueprints...")
        app.register_blueprint(api, url_prefix='/api')
        app.register_blueprint(auth, url_prefix='/auth')
        app.register_blueprint(admin_api, url_prefix='/admin')
        logger.info("Blueprints registered successfully")
        
        # Log all registered routes
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        logger.debug(f"Registered routes: {routes}")
    except Exception as e:
        logger.error(f"Error registering blueprints: {e}")
        raise

    # Enable CORS for the Vue.js frontend
    try:
        cors_origins_str = os.environ.get('CORS_ORIGINS', 'http://localhost:5173')
        cors_origins = [origin.strip() for origin in cors_origins_str.split(',')]
        CORS(app, resources={r"/*": {"origins": cors_origins}})
        logger.info(f"CORS enabled for origins: {cors_origins}")
    except Exception as e:
        logger.error(f"Failed to configure CORS: {e}")
        raise

    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'SparkRepo API is running',
            'environment': app.config.get('ENV', 'production')
        }), 200

    # API discovery endpoint
    @app.route('/api', methods=['GET'])
    def api_root():
        """Simple discovery endpoint listing primary routes."""
        return jsonify({
            'message': 'Welcome to the SparkRepo API',
            'version': '1.0.0',
            'endpoints': {
                'public': [
                    '/api/categories',
                    '/api/categories/{id}',
                    '/api/categories/{id}/weeks',
                    '/api/categories/{id}/weeks/{week}',
                    '/api/categories/{id}/weeks/{week}/submissions'
                ],
                'auth': [
                    '/auth/login',
                    '/auth/me',
                    '/auth/users'
                ],
                'admin': [
                    '/admin/weeks',
                    '/admin/weeks/{id}',
                    '/admin/categories/{category_id}/weeks',
                    '/admin/submissions',
                    '/admin/submissions/{id}'
                ]
            }
        })

    # Initialize default admin user if not exists
    try:
        db = DatabaseService(use_admin=True)
        admin_user = db.get_user_by_username('admin')
        if admin_user:
            logger.info("Admin user already exists")
        else:
            admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
            admin_email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
            new_admin = db.create_user(
                username='admin',
                password=admin_password,
                email=admin_email,
                is_admin=True
            )
            if new_admin:
                logger.info(f"Default admin user created: {admin_email}")
            else:
                logger.warning("Failed to create default admin user")
    except Exception as e:
        logger.warning(f"Could not initialize admin user (database may not be ready): {e}")

    logger.info("✓ SparkRepo application initialized successfully")
    return app

if __name__ == '__main__':
    app = create_app()
    logger.info("Starting SparkRepo server on http://0.0.0.0:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
