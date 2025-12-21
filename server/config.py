"""Application configuration classes for different environments.

Loads values from environment variables when present, with safe defaults
for development. This module does not read .env directly; that should be
handled at app startup via python-dotenv.
"""
from __future__ import annotations
import os
from typing import Optional


class BaseConfig:
    """Base configuration for all environments."""
    
    # Application
    DEBUG: bool = False
    TESTING: bool = False
    SECRET_KEY: str = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")
    ENV: str = os.getenv("FLASK_ENV", "development")
    
    # Firebase
    FIREBASE_SERVICE_ACCOUNT_KEY: Optional[str] = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")
    FIREBASE_SERVICE_ACCOUNT_PATH: Optional[str] = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "serviceAccountKey.json")
    
    # JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-jwt-secret")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "86400"))  # 24h
    
    # CORS
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:5173")
    
    # File uploads
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16MB max upload
    UPLOAD_FOLDER: str = "uploads"
    ALLOWED_EXTENSIONS: set[str] = {"png", "jpg", "jpeg", "gif", "pdf"}
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Admin defaults
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin123")


class DevelopmentConfig(BaseConfig):
    """Development environment configuration."""
    
    DEBUG = True
    TESTING = False
    LOG_LEVEL = "DEBUG"


class ProductionConfig(BaseConfig):
    """Production environment configuration."""
    
    DEBUG = False
    TESTING = False
    LOG_LEVEL = "INFO"
    
    # Note: Secrets should be provided via environment in production.
    # Do NOT raise at import time to avoid breaking local environments.
    # Validation is performed at app startup.
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")


class TestingConfig(BaseConfig):
    """Testing environment configuration."""
    
    TESTING = True
    DEBUG = True
    LOG_LEVEL = "DEBUG"


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name: Optional[str] = None) -> type[BaseConfig]:
    """Get configuration class by name.
    
    Args:
        config_name: Name of the configuration ('development', 'production', 'testing').
                    If None, uses FLASK_ENV environment variable.
    
    Returns:
        Configuration class for the specified environment.
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    return config.get(config_name, DevelopmentConfig)
