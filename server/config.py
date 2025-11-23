"""Application configuration classes for different environments.

Loads values from environment variables when present, with safe defaults
for development. This module does not read .env directly; that should be
handled at app startup via python-dotenv.
"""
from __future__ import annotations
import os
from typing import Optional


class BaseConfig:
    # Application
    DEBUG: bool = False
    SECRET_KEY: str = os.getenv("FLASK_SECRET_KEY", "dev")
    
    # Supabase
    SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: Optional[str] = os.getenv("SUPABASE_KEY")
    SUPABASE_SERVICE_KEY: Optional[str] = os.getenv("SUPABASE_SERVICE_KEY")
    
    # JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-jwt-secret")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "86400"))  # 24h
    
    # CORS
    CORS_ORIGINS: list[str] = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    
    # File uploads
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16MB max upload
    UPLOAD_FOLDER: str = "uploads"
    ALLOWED_EXTENSIONS: set[str] = {"png", "jpg", "jpeg", "gif", "pdf"}


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SUPABASE_URL = os.getenv("SUPABASE_URL", "http://localhost:54321")  # Local Supabase
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "local-dev-key")


class ProductionConfig(BaseConfig):
    DEBUG = False
    # Production should have these set via environment variables
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
    JWT_SECRET = os.getenv("JWT_SECRET")


def get_config() -> type[BaseConfig]:
    env = os.environ.get("FLASK_ENV", "development").lower()
    return ProductionConfig if env == "production" else DevelopmentConfig
