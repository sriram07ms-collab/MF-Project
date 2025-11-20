#!/bin/bash

# Setup script for backend

echo "Setting up MF Assistant Backend..."

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create data directory
mkdir -p data

# Check for .env file
if [ ! -f ".env" ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    echo "ℹ️  Optional: edit .env and add your GEMINI_API_KEY for better answers."
    echo "    Embeddings use Hugging Face models and do not require an API key."
fi

echo "Setup complete!"
echo "Next steps:"
echo "1. (Optional) Edit .env and add GEMINI_API_KEY"
echo "2. Run: python scripts/ingest_data.py"
echo "3. Run: uvicorn main:app --reload"



