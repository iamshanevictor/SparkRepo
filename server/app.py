"""Flask application factory for SparkRepo backend.

Initializes extensions, loads configuration, registers blueprints, and
exposes basic health and API discovery endpoints.
"""
from flask import Flask, jsonify
from flask_cors import CORS
from models import db
from api import api
from auth import auth, init_jwt
from admin import admin_api
import os
import secrets
from dotenv import load_dotenv
from config import get_config

def create_app(test_config=None):
    """Create and configure the Flask application."""
    # Load environment variables from .env (if present)
    load_dotenv()

    app = Flask(__name__)

    # Load config class
    ConfigClass = get_config()
    app.config.from_object(ConfigClass)

    # Configure the SQLite database fallback using an absolute path if none provided
    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'sparkrepo.db')

    # Configure JWT (use provided secret or fall back to a generated one for dev)
    app.config['JWT_SECRET_KEY'] = app.config.get('JWT_SECRET_KEY') or os.environ.get('JWT_SECRET_KEY') or secrets.token_hex(32)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', app.config.get('JWT_ACCESS_TOKEN_EXPIRES', 86400)))

    # Enable CORS for the Vue.js frontend (restrict to configured origins)
    cors_origins = app.config.get('CORS_ORIGINS', 'http://localhost:5173')
    CORS(app, resources={r"/*": {"origins": cors_origins}})
    
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
