from flask import Flask, jsonify
from flask_cors import CORS
from models import db
from api import api
from auth import auth, init_jwt
from admin import admin_api
import os
import secrets

def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    
    # Configure the SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sparkrepo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configure JWT
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', secrets.token_hex(32))
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400  # 24 hours in seconds
    
    # Enable CORS for the Vue.js frontend
    CORS(app, resources={r"/*": {"origins": "*"}})
    
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
        return jsonify({
                        'message': 'Welcome to the SparkRepo API',
            'version': '1.0.0',
            'endpoints': [
                '/api/classes',
                '/api/classes/{id}',
                '/api/classes/{id}/weeks',
                '/api/classes/{id}/weeks/{week}',
                '/api/classes/{id}/weeks/{week}/submissions',
                '/api/students',
                '/api/students/{id}/submissions'
            ]
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
