#!/usr/bin/env bash
# Exit on error
set -o errexit

# Set Python path
export PYTHONPATH="$PYTHONPATH:$(pwd)"

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=production

# Ensure we're using the correct Python version
echo "Using Python version:"
python --version

# Install dependencies
echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

# Initialize database
echo "Running database migrations..."
python -c "
from app import create_app
from models import db

app = create_app()
with app.app_context():
    db.create_all()
    print('Database tables created')
"

# Start the application
echo "Starting Gunicorn..."
exec gunicorn --worker-tmp-dir /dev/shm \
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
