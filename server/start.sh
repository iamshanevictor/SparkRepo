#!/usr/bin/env bash
# Exit on error
set -o errexit

# Initialize database
python -c "from app import create_app; app = create_app(); from models import db; db.create_all(app=app)"

# Start the application
exec gunicorn --worker-tmp-dir /dev/shm --workers=2 --threads=4 --worker-class=gthread --timeout 120 --bind :$PORT "app:create_app()"
