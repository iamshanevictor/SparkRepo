#!/usr/bin/env bash
# Exit on error
set -o errexit

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=production

# Set Python path
export PYTHONPATH="$PYTHONPATH:$(pwd)"

# Ensure we're using the correct Python version
echo "=== Python Version ==="
python --version

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3.11 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip and install dependencies
echo "=== Installing Dependencies ==="
python -m pip install --upgrade pip
pip install -r requirements.txt

# Initialize database
echo "=== Setting Up Database ==="
python -c "
import os
from app import create_app
from models import db

app = create_app()
with app.app_context():
    try:
        db.create_all()
        print('✅ Database tables created successfully')
    except Exception as e:
        print(f'❌ Error creating database tables: {e}')
        raise
"

# Start the application
echo "=== Starting Gunicorn ==="
exec gunicorn \
    --worker-tmp-dir /dev/shm \
    --workers=2 \
    --threads=4 \
    --worker-class=gthread \
    --timeout 120 \
    --bind :$PORT \
    --access-logfile - \
    --error-logfile - \
    --log-level=info \
    --preload \
    "app:create_app()"
