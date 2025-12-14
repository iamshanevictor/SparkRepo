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
    
    # Supabase
    SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: Optional[str] = os.getenv("SUPABASE_KEY")
    SUPABASE_SERVICE_KEY: Optional[str] = os.getenv("SUPABASE_SERVICE_KEY")
    
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


class DevelopmentConfig(BaseConfig):
    """Development environment configuration."""
    
    DEBUG = True
    TESTING = False
    LOG_LEVEL = "DEBUG"
    
    # Use local Supabase for development
    SUPABASE_URL = os.getenv("SUPABASE_URL", "http://localhost:54321")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "local-dev-key")


class ProductionConfig(BaseConfig):
    """Production environment configuration."""
    
    DEBUG = False
    TESTING = False
    LOG_LEVEL = "WARNING"
    
    # Production MUST have these set via environment variables
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
    JWT_SECRET = os.getenv("JWT_SECRET")


class TestingConfig(BaseConfig):
    """Testing environment configuration."""
    
    DEBUG = True
    TESTING = True
    LOG_LEVEL = "DEBUG"
    
    # Use test database/keys
    SUPABASE_URL = os.getenv("TEST_SUPABASE_URL", "http://localhost:54321")
    SUPABASE_KEY = os.getenv("TEST_SUPABASE_KEY", "test-key")


def get_config() -> type[BaseConfig]:
    """Get the appropriate config class based on environment.
    
    Returns:
        BaseConfig: Configuration class for the current environment
        
    Raises:
        ValueError: If environment is invalid
    """
    env = os.environ.get("FLASK_ENV", "development").lower()
    
    config_map = {
        "production": ProductionConfig,
        "prod": ProductionConfig,
        "development": DevelopmentConfig,
        "dev": DevelopmentConfig,
        "testing": TestingConfig,
        "test": TestingConfig,
    }
    
    if env not in config_map:
        raise ValueError(f"Invalid FLASK_ENV: {env}. Must be one of: {', '.join(config_map.keys())}")
    
    return config_map[env]
