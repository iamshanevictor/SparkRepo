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

    app = Flask(__name__, static_folder='../client/dist', static_url_path='')

    # Load config class
    ConfigClass = get_config()
    app.config.from_object(ConfigClass)

    # Configure database
    if 'DATABASE_URL' in os.environ:
        # Handle PostgreSQL URL for SQLAlchemy
        if os.environ['DATABASE_URL'].startswith('postgres://'):
            app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace('postgres://', 'postgresql://', 1)
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    elif not app.config.get('SQLALCHEMY_DATABASE_URI'):
        # Fallback to SQLite if no database URL is provided
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
    db.init_app(app)
    init_jwt(app)

    # Register blueprints
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin_api, url_prefix='/admin')

    # Enable CORS for the Vue.js frontend
    CORS(app, resources={
        r"/*": {
            "origins": app.config.get('CORS_ORIGINS', 'http://localhost:5173').split(',')
        }
    })

    # Serve React Frontend
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'SparkRepo API is running',
            'environment': app.config.get('ENV', 'production')
        }), 200

    # Initialize database
    with app.app_context():
        db.create_all()
        # Create default admin user if not exists
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
    
    # Initialize the database
    db.init_app(app)
    
    # Initialize JWT
    jwt = init_jwt(app)
    
    # Register the API blueprints
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(auth, url_prefix='/api/auth')
    app.register_blueprint(admin_api, url_prefix='/api/admin')
    
    # Create a route for the API root
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
                    '/api/auth/login',
                    '/api/auth/me',
                    '/api/auth/users'
                ],
                'admin': [
                    '/api/admin/weeks',
                    '/api/admin/weeks/{id}',
                    '/api/admin/categories/{category_id}/weeks',
                    '/api/admin/submissions',
                    '/api/admin/submissions/{id}'
                ]
            }
        })
    
    # Create a simple health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy'})
    
    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
