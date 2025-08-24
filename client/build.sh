#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line to point to your frontend directory if needed
cd client

# Install dependencies
npm install

# Build the frontend
npm run build

# Copy build files to the static directory
cp -R dist/* ../server/static/
