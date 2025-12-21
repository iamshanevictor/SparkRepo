"""Flask application factory for SparkRepo backend with Firebase."""
import os
import secrets
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Import blueprints
from .api import api
from .auth import auth
from .admin import admin_api
from .config import get_config
from .firebase_client import initialize_firebase
from .models import User

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app(test_config=None):
    """Create and configure the Flask application."""
    # Load environment variables from .env (if present)
    load_dotenv()

    app = Flask(__name__)
    
    logger.info("Initializing SparkRepo Flask application with Firebase...")

    # Load config class
    try:
        ConfigClass = get_config()
        app.config.from_object(ConfigClass)
        logger.info(f"Configuration loaded: {ConfigClass.__name__}")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        raise

    # Initialize Firebase
    try:
        initialize_firebase()
        logger.info("Firebase initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {e}")
        raise

    # Configure JWT
    jwt_secret = os.environ.get('JWT_SECRET_KEY') or secrets.token_hex(32)
    app.config['JWT_SECRET_KEY'] = jwt_secret
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 86400))
    
    # Initialize JWT
    jwt = JWTManager(app)
    logger.info("JWT manager initialized successfully")

    # Setup CORS
    cors_origins = app.config.get('CORS_ORIGINS', 'http://localhost:5173')
    CORS(app, 
         origins=cors_origins.split(','),
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization'],
         supports_credentials=True)
    logger.info(f"CORS configured for origins: {cors_origins}")

    # Register blueprints
    try:
        logger.info("Registering blueprints...")
        app.register_blueprint(api, url_prefix='/api')
        app.register_blueprint(auth, url_prefix='/auth')
        app.register_blueprint(admin_api, url_prefix='/admin')
        logger.info("Blueprints registered successfully")
    except Exception as e:
        logger.error(f"Error registering blueprints: {e}")
        raise

    # Root endpoint
    @app.route('/')
    def index():
        """Root endpoint with API info."""
        return jsonify({
            'message': 'SparkRepo API',
            'version': '2.0.0',
            'database': 'Firebase Firestore',
            'endpoints': {
                'categories': '/api/categories',
                'weeks': '/api/categories/<id>/weeks',
                'submissions': '/api/weeks/<id>/submissions',
                'auth': '/auth/login',
                'admin': '/admin/*'
            }
        })

    # Health check endpoint
    @app.route('/health')
    def health():
        """Health check endpoint."""
        try:
            # Test Firebase connection
            from .firebase_client import get_firestore_client
            db = get_firestore_client()
            # Simple test query
            list(db.collection('categories').limit(1).stream())
            return jsonify({'status': 'healthy', 'database': 'connected'}), 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

    # Create default admin user if not exists
    with app.app_context():
        try:
            admin_username = app.config.get('ADMIN_USERNAME', 'admin')
            existing_user = User.get_by_username(admin_username)
            
            if not existing_user:
                admin_password = app.config.get('ADMIN_PASSWORD', 'admin123')
                User.create(
                    username=admin_username,
                    password=admin_password,
                    email='admin@sparkrepo.com',
                    is_admin=True
                )
                logger.info(f"Default admin user created: {admin_username}")
            else:
                logger.info(f"Admin user already exists: {admin_username}")
        except Exception as e:
            logger.warning(f"Could not create default admin user: {e}")

    logger.info("SparkRepo application initialized successfully")
    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
