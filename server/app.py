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
from models import db, init_app as init_models
from api import api
from auth import auth, init_jwt
from admin import admin_api
from config import get_config

def create_app(test_config=None):
    """Create and configure the Flask application."""
    # Load environment variables from .env (if present)
    load_dotenv()

    app = Flask(__name__)

    # Load config class
    ConfigClass = get_config()
    app.config.from_object(ConfigClass)

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

    # Configure JWT
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY') or secrets.token_hex(32)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 86400))

    # Initialize extensions
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

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
