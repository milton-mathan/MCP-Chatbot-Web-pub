# Production MCP Web Architecture Startup Guide

This guide demonstrates **real-world MCP architecture** with proper process separation for the web chatbot.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Server    │    │   MCP Server    │    │  Web Server     │
│   (Port 8000)   │◄──►│   (stdio)       │◄──►│   (Port 8001)   │
│                 │    │                 │    │                 │
│ • Serves data   │    │ • Exposes tools │    │ • WebSocket     │
│ • JSON files    │    │ • MCP protocol  │    │ • Claude LLM    │
│ • REST API      │    │ • Tool logic    │    │ • Web interface │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Startup Process (3 Terminals Required)

### Prerequisites
```bash
# Navigate to project directory
cd /path/to/MCP-Chatbot-Web

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify .env file has ANTHROPIC_API_KEY
cat .env
```

### Terminal 1: API Server
```bash
# Start the data API server
python api/main.py

# Expected output:
# ✅ API Server started on http://localhost:8000
# ✅ Serving data from JSON files
```

### Terminal 2: MCP Server
```bash
# Start the MCP server
python mcp_server/server.py

# Expected output:
# (MCP server starts and waits silently for client connections)
# Note: No output is normal - the server waits for stdio connections
```

### Terminal 3: Web Server
```bash
# Start the web chatbot server
python web/main.py

# Expected output:
# 🤖 Initializing MCP Chatbot Web...
# ✅ Chatbot initialized successfully!
# 🌐 Web interface ready at http://127.0.0.1:8001
# 📍 Make sure MCP server is running: python mcp_server/server.py
```

### Access the Application
Open your web browser and go to: **http://127.0.0.1:8001**

## 🔄 Process Communication Flow

1. **User Input** → Web Browser → Web Server (WebSocket)
2. **Claude Processing** → Web Server → MCP Client
3. **Tool Request** → MCP Server (via stdio MCP protocol)
4. **Data Request** → API Server (via HTTP)
5. **Data Response** ← API Server
6. **Tool Response** ← MCP Server
7. **Claude Final Response** → Web Server
8. **Final Response** → User (via WebSocket)

## 💡 Educational Benefits

This setup demonstrates:

- **Process Isolation**: Each component runs independently
- **Protocol Standards**: Real MCP stdio transport with official SDK
- **Service Dependencies**: Proper startup order matters
- **Error Handling**: Connection failures and recovery
- **Production Patterns**: How real systems are architected
- **WebSocket Communication**: Real-time web chat
- **LLM Integration**: Claude with MCP tool calling

## 🔍 Monitoring Each Process

### Check API Server
```bash
# Test the API endpoints
curl http://localhost:8000/products
curl http://localhost:8000/tickets
curl http://localhost:8000/faq
```

### Check MCP Server
The MCP server runs via stdio - you'll see connection messages when clients connect.

### Check Web Server
```bash
# Health check endpoint
curl http://localhost:8001/health

# Expected response:
# {"status":"healthy","chatbot_ready":true,"message":"MCP Chatbot Web is running"}
```

### Check Web Interface
1. Open browser to `http://127.0.0.1:8001`
2. Try sample questions:
   - "What products do you have?"
   - "Show me open tickets"
   - "What's your return policy?"

## 🛑 Shutdown Process

**Important**: Shutdown in reverse order to avoid connection errors:

1. **Ctrl+C** in Web Server terminal (Terminal 3)
2. **Ctrl+C** in MCP Server terminal (Terminal 2)
3. **Ctrl+C** in API Server terminal (Terminal 1)

## 🚨 Troubleshooting

### "Connection failed" errors:
- Ensure API server is running first: `python api/main.py`
- Check that MCP server started successfully: `python mcp_server/server.py`
- Verify .env has valid ANTHROPIC_API_KEY

### "Port already in use" errors:
```bash
# Kill existing processes
pkill -f "python api/main.py"
pkill -f "python web/main.py"

# Check port usage
lsof -i :8000
lsof -i :8001
```

### Import/dependency errors:
```bash
# Verify virtual environment is activated
which python

# Reinstall dependencies
pip install -r requirements.txt
```

### WebSocket connection issues:
- Use a modern browser that supports WebSockets
- Check browser console for JavaScript errors
- Try refreshing the page if connection seems stuck

### MCP connection issues:
- Ensure MCP server is running before starting web server
- Check that `mcp>=1.0.0` is installed properly
- Verify FastMCP compatibility

## 🎯 Compare to Development Mode

**Development (automated - 2 processes):**
```bash
# Old simplified approach
python web/main.py  # Everything auto-managed internally
```

**Production (manual - 3 processes):**
```bash
# Terminal 1
python api/main.py

# Terminal 2
python mcp_server/server.py

# Terminal 3
python web/main.py
```

## 🌟 Key Differences from CLI Version

| Aspect | CLI Version | Web Version |
|--------|-------------|-------------|
| **Interface** | Command-line | Web browser + WebSocket |
| **User Input** | stdin/stdout | WebSocket messages |
| **Real-time** | Sequential | Concurrent WebSocket |
| **Deployment** | Local terminal | Web server deployment |
| **Scalability** | Single user | Multiple concurrent users |

## ✅ Testing Your Setup

Expected behavior when everything is working:

1. **API Server**: Returns JSON data when curl tested
2. **MCP Server**: Silent startup, handles stdio connections
3. **Web Server**: Shows health check as "healthy"
4. **Web Interface**: Loads chat interface successfully
5. **Chat Functionality**: Claude responds to questions using MCP tools
6. **Tool Integration**: Product/ticket/FAQ queries work properly

The production approach teaches proper **service orchestration**, **dependency management**, and **real-world MCP architecture patterns**!

## 📚 Next Steps

After mastering this architecture:
- Deploy to cloud platforms (AWS, GCP, Azure)
- Add authentication and user sessions
- Implement chat history persistence
- Scale with load balancers and multiple instances
- Add monitoring and logging
- Integrate with CI/CD pipelines