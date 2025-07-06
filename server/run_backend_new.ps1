# PowerShell script to run the SparkRepo backend server
# This script will activate the .venv environment, install dependencies if needed, and start the Flask server

# Stop on any error
$ErrorActionPreference = "Stop"

Write-Host "Starting SparkRepo Backend Server..." -ForegroundColor Green

# Create .venv if it doesn't exist
if (-not (Test-Path ".\.venv")) {
    Write-Host "Creating virtual environment (.venv)..." -ForegroundColor Yellow
    python -m venv .venv
}

# Directly activate the virtual environment
Write-Host "Activating .venv environment..." -ForegroundColor Yellow
.\.venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies in .venv..." -ForegroundColor Yellow
pip install -r requirements.txt

# Check if database exists, if not, run seed script
if (-not (Test-Path ".\sparkrepo.db")) {
    Write-Host "Initializing database with sample data..." -ForegroundColor Yellow
    python seed.py
}

# Run the Flask application
Write-Host "Starting Flask server..." -ForegroundColor Green
Write-Host "The server will be available at http://localhost:5000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
python app.py
