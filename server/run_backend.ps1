# PowerShell script to run the SparkRepo backend server
# This script will set up the virtual environment if it doesn't exist,
# install dependencies, and start the Flask server

# Stop on any error
$ErrorActionPreference = "Stop"

Write-Host "Starting SparkRepo Backend Server..." -ForegroundColor Green

# Check if virtual environment exists
if (-not (Test-Path ".\.venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\.venv\Scripts\Activate.ps1

# Install dependencies if requirements.txt is newer than last install
if (-not (Test-Path ".\.venv\.requirements_installed") -or 
    (Get-Item ".\requirements.txt").LastWriteTime -gt (Get-Item ".\.venv\.requirements_installed").LastWriteTime) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Get-Date | Out-File -FilePath ".\.venv\.requirements_installed"
}
;
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