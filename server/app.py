"""Flask application factory for SparkRepo backend.

Initializes extensions, loads configuration, registers blueprints, and
exposes basic health and API discovery endpoints.
"""
import os
import secrets
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Initialize extensions
from api import api
from auth import auth, init_jwt
from admin import admin_api
from config import get_config
from db_service import DatabaseService

def create_app(test_config=None):
    """Create and configure the Flask application."""
    # Load environment variables from .env (if present)
    load_dotenv()

    app = Flask(__name__)

    # Load config class
    ConfigClass = get_config()
    app.config.from_object(ConfigClass)

<<<<<<< HEAD
    # Verify Supabase configuration
    if not os.environ.get('SUPABASE_URL') or not os.environ.get('SUPABASE_KEY'):
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
=======
    # Configure database
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        if database_url.startswith('postgres://'):
            app.config['SQLALCHEMY_DATABASE_URI'] = database_url.replace('postgres://', 'postgresql://', 1)
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Fallback to SQLite if no DATABASE_URL is provided
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "sparkrepo.db")}'

    # Configure SQLAlchemy
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
>>>>>>> 20b2416fc49e14871dfbee82dfa8edfbc23e87be

    # Configure JWT
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY') or secrets.token_hex(32)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 86400))

<<<<<<< HEAD
    # Initialize JWT
=======
    # Initialize extensions
>>>>>>> 20b2416fc49e14871dfbee82dfa8edfbc23e87be
    init_jwt(app)

    # Initialize database with models FIRST
    try:
        print("Initializing models...")
        init_models(app)
        print("Models initialized successfully")
    except Exception as e:
        print(f"Error initializing models: {e}")
        # Don't fail completely, but log the error
        import traceback
        traceback.print_exc()

    # Register blueprints AFTER models are initialized
    try:
        print("Registering blueprints...")
        app.register_blueprint(api, url_prefix='/api')
        app.register_blueprint(auth, url_prefix='/auth')
        app.register_blueprint(admin_api, url_prefix='/admin')
        print("Blueprints registered successfully")
        print(f"Final app routes: {[rule.rule for rule in app.url_map.iter_rules()]}")
    except Exception as e:
        print(f"Error registering blueprints: {e}")
        import traceback
        traceback.print_exc()

    # Enable CORS for the Vue.js frontend
    cors_origins = os.environ.get('CORS_ORIGINS', 'http://localhost:5173').split(',')
    CORS(app, resources={
        r"/*": {
            "origins": cors_origins
        }
    })

    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'SparkRepo API is running',
            'environment': app.config.get('ENV', 'production')
        }), 200

<<<<<<< HEAD
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
        if not admin_user:
            db.create_user(
                username='admin',
                password=os.environ.get('ADMIN_PASSWORD', 'admin123'),
                email=os.environ.get('ADMIN_EMAIL', 'admin@example.com'),
                is_admin=True
            )
    except Exception as e:
        # Log error but don't fail startup - tables might not exist yet
        print(f"Warning: Could not initialize admin user: {e}")
=======
    # Create default admin user if not exists (models already initialized)
    with app.app_context():
        from models import User
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email=os.environ.get('ADMIN_EMAIL', 'admin@example.com'),
                is_admin=True
            )
            admin.set_password(os.environ.get('ADMIN_PASSWORD', 'admin123'))
            db.session.add(admin)
            db.session.commit()
>>>>>>> 20b2416fc49e14871dfbee82dfa8edfbc23e87be

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
