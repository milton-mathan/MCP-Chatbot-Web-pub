#!/bin/bash
# Production MCP Web Chatbot Startup Script
# This script demonstrates the 3-process architecture startup

echo "🎯 MCP Web Chatbot - Production Architecture"
echo "🏗️  Architecture: 3 separate processes"
echo "📍 This script will guide you through starting each process"
echo ""

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: Virtual environment not detected"
    echo "💡 Recommendation: Run 'source .venv/bin/activate' first"
    echo ""
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found"
    echo "💡 Copy .env.example to .env and add your ANTHROPIC_API_KEY"
    echo "   cp .env.example .env"
    exit 1
fi

# Check if ANTHROPIC_API_KEY is set
if ! grep -q "^ANTHROPIC_API_KEY=" .env || grep -q "^ANTHROPIC_API_KEY=$" .env || grep -q "^ANTHROPIC_API_KEY=your_anthropic_api_key_here" .env; then
    echo "❌ Error: ANTHROPIC_API_KEY not configured in .env"
    echo "💡 Edit .env and add your Anthropic API key"
    exit 1
fi

echo "✅ Environment setup looks good!"
echo ""

echo "📋 Production Startup Instructions:"
echo "   You need to run these commands in 3 separate terminals:"
echo ""
echo "🔸 Terminal 1 (API Server):"
echo "   cd $(pwd)"
echo "   source .venv/bin/activate  # if needed"
echo "   python api/main.py"
echo ""
echo "🔸 Terminal 2 (MCP Server):"
echo "   cd $(pwd)"
echo "   source .venv/bin/activate  # if needed"
echo "   python mcp_server/server.py"
echo ""
echo "🔸 Terminal 3 (Web Server):"
echo "   cd $(pwd)"
echo "   source .venv/bin/activate  # if needed"
echo "   python web/main.py"
echo ""
echo "🌐 Then open: http://127.0.0.1:8001"
echo ""
echo "📚 For detailed instructions, see: PRODUCTION_STARTUP.md"
echo ""
echo "💡 This approach teaches real-world service orchestration!"

# Offer to start the first process
echo ""
read -p "🚀 Would you like to start the API server now? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🏃 Starting API Server..."
    echo "📝 After this starts, run the MCP server and Web server in separate terminals"
    echo ""
    python api/main.py
fi