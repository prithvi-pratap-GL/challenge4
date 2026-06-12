#!/bin/bash
# Start FastAPI backend server

echo "Starting VentureMind AI Backend (Person 2 - Research Intelligence)..."
echo "API will be available at: http://localhost:8000"
echo "API Docs at: http://localhost:8000/docs"
echo ""

cd "$(dirname "$0")"

# Check if venv exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate venv
if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install -q fastapi uvicorn pydantic python-dotenv

# Start server
echo "Starting server..."
python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload
