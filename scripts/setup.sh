#!/usr/bin/env bash

echo "🛠 Initializing Arbitronix Core Local Environment..."

# Check Python version
python3 --version || { echo "❌ Python 3 not found."; exit 1; }

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r trading_system/requirements.txt

# Create .env if missing
if [ ! -f ".env" ]; then
    echo "📝 Creating .env from template..."
    cp .env.example .env
fi

echo "✅ Environment ready!"
echo "🚀 To start the system, run: source venv/bin/activate && python main.py"
