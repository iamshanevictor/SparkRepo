"""Application configuration classes for different environments.

Loads values from environment variables when present, with safe defaults
for development. This module does not read .env directly; that should be
handled at app startup via python-dotenv.
"""
from __future__ import annotations

import os


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", 86400))  # 24h

    # Database

    # CORS
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:5173")

    # JWT
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False


def get_config() -> type[BaseConfig]:
    env = os.environ.get("FLASK_ENV", "development").lower()
    if env.startswith("prod"):
        return ProductionConfig
    return DevelopmentConfig
