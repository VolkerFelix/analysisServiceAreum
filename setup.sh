#!/bin/bash

# Areum Analysis Service Setup Script

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file
echo "Creating .env file from example..."
cp .env.example .env

# Create test directories if they don't exist
echo "Creating test directories..."
mkdir -p tests/test_api
mkdir -p tests/test_services
mkdir -p tests/test_utils

# Touch __init__.py files in all directories to make them proper packages
find . -type d -not -path "*/\.*" -not -path "*/venv*" -exec touch {}/__init__.py \;

echo "Setup complete! You can now run the service with:"
echo "source venv/bin/activate  # If not already activated"
echo "uvicorn app.main:app --reload"