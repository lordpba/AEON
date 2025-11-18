#!/bin/bash
# AEON Quick Setup Script

echo "🚀 AEON GovTech Platform - Quick Setup"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $python_version"
echo ""

# Create necessary directories
echo "Creating directories..."
mkdir -p saves logs data
echo "✓ Directories created"
echo ""

# Install Python dependencies
echo "Installing dependencies..."
echo "This may take a few minutes..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "⚠️  Some dependencies may have failed to install"
    echo "   Please check the output above"
fi
echo ""

# Create a simple test script
echo "Updating quick start instructions..."
echo ""

echo "======================================"
echo "✅ Setup Complete!"
echo ""
echo "Quick Start:"
echo ""
echo "  1️⃣  Avvia il backend API:"
echo "     cd backend/app"
echo "     uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "  2️⃣  (Opzionale) Abilita AI Groq:"
echo "     export GROQ_API_KEY=\"<la_tua_chiave>\""
echo "     # opzionale: export GROQ_MODEL=\"llama-3.1-70b-versatile\""
echo ""
echo "  3️⃣  Verifica health e WebSocket:"
echo "     curl http://localhost:8000/health"
echo "     # ws://localhost:8000/ws/simulation"
echo ""
echo "📚 For more information, see README_NEW.md"
echo ""
echo "🚀 Welcome to AEON!"
echo "======================================"
