#!/bin/bash

echo "Starting MCP Chatbot Web - Web Server"
echo "====================================="
echo
echo "Make sure you have:"
echo "1. Started the API server first (run ./start_api.sh)"
echo "2. Activated your virtual environment (source .venv/bin/activate)"
echo "3. Created .env file with your GOOGLE_API_KEY"
echo
echo "Once started, open your browser to: http://127.0.0.1:8001"
echo
read -p "Press Enter to continue..."
python web/main.py