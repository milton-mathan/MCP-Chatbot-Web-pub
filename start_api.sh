#!/bin/bash

echo "Starting MCP Chatbot Web - API Server"
echo "====================================="
echo
echo "Make sure you have:"
echo "1. Activated your virtual environment (source .venv/bin/activate)"
echo "2. Installed dependencies (pip install -r requirements.txt)"
echo "3. Created .env file with your GOOGLE_API_KEY"
echo
read -p "Press Enter to continue..."
python api/main.py