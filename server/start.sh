#!/usr/bin/env bash
# Exit on error
set -o errexit

# Set Python path
export PYTHONPATH="$PYTHONPATH:$(pwd)"

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=production

# Initialize database
echo "Running database migrations..."
python -c "from app import create_app; app = create_app();"

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
    "app:create_app()"
