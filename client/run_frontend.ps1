# PowerShell script to run the SparkRepo frontend
# This script will install dependencies if needed and start the Vue development server

# Stop on any error
$ErrorActionPreference = "Stop"

Write-Host "Starting SparkRepo Frontend..." -ForegroundColor Green

# Check if node_modules exists
if (-not (Test-Path ".\node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    npm install
}

# Check if package.json is newer than node_modules
if ((Get-Item ".\package.json").LastWriteTime -gt (Get-Item ".\node_modules").LastWriteTime) {
    Write-Host "Dependencies may be outdated, updating..." -ForegroundColor Yellow
    npm install
}

# Run the Vue development server
Write-Host "Starting Vue development server..." -ForegroundColor Green
Write-Host "The frontend will be available at http://localhost:5173" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
npm run dev
