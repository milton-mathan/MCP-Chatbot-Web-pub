# MCP Chatbot Web

A modern web-based chatbot powered by **Anthropic's Claude LLM** and **proper Model Context Protocol (MCP)** architecture. This project provides a sleek web interface for interacting with an intelligent assistant that can retrieve information about products, support tickets, and FAQs.

> **📚 Learning Purpose**: This project is created for educational purposes to demonstrate **real MCP architecture** using the official MCP Python SDK, LLM integration, WebSocket communication, and modern web development practices.

## 🏗️ Architecture

The project uses a **proper Model Context Protocol (MCP)** architecture with three separate processes:

- **API Server**: FastAPI server that serves data from JSON files (Port 8000)
- **MCP Server**: Standalone MCP server process that exposes tools via MCP protocol (stdio transport)
- **MCP Client**: Official MCP client that connects to the server via stdio
- **Web Server**: FastAPI server with WebSocket support for real-time chat (Port 8001)
- **Chatbot**: Anthropic Claude LLM integration with proper MCP client connection
- **Frontend**: Clean HTML/CSS/JavaScript interface with real-time updates

## 🚀 Features

- 🌐 Modern web interface with real-time chat
- 🤖 Natural language conversation with Anthropic Claude
- 📦 Product information retrieval
- 🎫 Support ticket management
- ❓ FAQ system
- ⚡ WebSocket communication for instant responses
- 📱 Responsive design for mobile and desktop
- 🎨 Beautiful gradient UI with smooth animations
- 🔧 **Proper MCP architecture** using official Python SDK
- 🔌 **Real MCP server** with stdio transport
- 📡 **Official MCP client** connection
- 🛠️ **JSON-RPC 2.0** protocol implementation

## 📋 Prerequisites

- Python 3.8 or higher
- Anthropic API Key (Claude access)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection for LLM API calls

## 🛠️ Installation

1. **Clone or download this project**

2. **Create a virtual environment**:
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your Anthropic API key**:
   - Get your API key from [Anthropic Console](https://console.anthropic.com/)
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your API key:
     ```
     ANTHROPIC_API_KEY=your_actual_anthropic_api_key_here
     ```

## 🏃‍♂️ Running the Application

This project supports **production MCP architecture** with proper process separation:

### 🎯 Production Mode (Recommended for Learning)
**Real-world 3-process architecture** - demonstrates proper MCP service separation:

```bash
# Terminal 1: Start API Server
python api/main.py

# Terminal 2: Start MCP Server
python mcp_server/server.py

# Terminal 3: Start Web Server
python web/main.py
```

📋 **See [PRODUCTION_STARTUP.md](PRODUCTION_STARTUP.md) for detailed instructions**

### Quick Start Script
```bash
# Guided startup (provides instructions)
./start_mcp_web.sh
```

### Access the Application
Open your web browser and go to: **http://127.0.0.1:8001**

## 💬 Example Conversations

Try these sample questions in the web interface:

- "What products do you have?"
- "Tell me about the high-performance laptop"
- "Show me all open tickets"
- "What's ticket tkt_10 about?"
- "Who created ticket tkt_05?"
- "What's your return policy?"
- "How do I cancel an order?"
- "Show me FAQs about shipping"

## 📁 Project Structure

```
MCP-Chatbot-Web/
├── api/
│   └── main.py              # FastAPI data server
├── data/
│   ├── faq.json            # FAQ data
│   ├── products.json       # Product data
│   └── tickets.json        # Support ticket data
├── mcp_client/
│   ├── client.py           # Official MCP client implementation
│   └── main.py             # Legacy client (deprecated)
├── mcp_server/
│   ├── server.py           # FastMCP server with stdio transport
│   ├── main.py             # Legacy sync tools (deprecated)
│   └── main_async.py       # Legacy async tools (deprecated)
├── web/
│   ├── main.py             # Main web server with WebSocket
│   └── static/
│       ├── index.html      # Chat interface
│       ├── style.css       # Beautiful responsive styles
│       └── script.js       # WebSocket chat logic
├── requirements.txt        # Python dependencies with MCP SDK
├── .env.example           # Environment configuration template
├── .gitignore             # Git ignore rules
├── start_mcp_web.sh       # Production startup script
├── PRODUCTION_STARTUP.md  # Detailed production setup guide
├── LICENSE                # MIT license
└── README.md              # This documentation
```

## 🎨 Features Breakdown

### Frontend Features
- **Real-time Chat**: Instant message delivery via WebSockets
- **Typing Indicators**: Shows when the AI is thinking
- **Responsive Design**: Works perfectly on mobile and desktop
- **Modern UI**: Beautiful gradients and smooth animations
- **Connection Status**: Visual feedback for connection state

### Backend Features
- **Async Processing**: Non-blocking request handling
- **Error Handling**: Graceful error recovery and user feedback
- **WebSocket Management**: Stable real-time connections
- **MCP Integration**: Clean separation of concerns

## 🔧 Configuration

The application uses environment variables for configuration:

- `ANTHROPIC_API_KEY`: Your Anthropic Claude API key

## 🛡️ Security Notes

- Never commit your `.env` file to version control
- The `.env.example` file shows the required format without real keys
- Keep your API keys secure and rotate them regularly
- The application runs on localhost by default for security

## 🌟 Technical Highlights

This project demonstrates:
- **Proper Model Context Protocol (MCP)**: Clean architecture for LLM tool integration using official SDK
- **JSON-RPC 2.0**: Standard protocol communication
- **stdio transport**: For MCP client-server communication
- **MCP tool definitions**: Server implementation with FastMCP
- **WebSocket Communication**: Real-time bidirectional communication
- **LLM Integration**: Anthropic Claude with MCP tool calling
- **Async/Await Patterns**: Modern Python async programming
- **FastAPI**: Modern Python web framework
- **Responsive Web Design**: Mobile-first CSS approach
- **Error Handling**: Graceful degradation and user feedback
- **Real-world MCP architecture**: Patterns for production deployment

## 🤝 Contributing

This is a learning project! Feel free to:
- Experiment with the UI design
- Add new data sources or tools
- Implement additional features like chat history
- Try different LLM models or providers
- Improve the responsive design

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🎯 Learning Objectives

This project helps you learn:
- **Proper Model Context Protocol (MCP)** implementation using official SDK
- **JSON-RPC 2.0** protocol communication
- **stdio transport** for MCP client-server communication
- **MCP tool definitions** and server implementation
- LLM integration with Anthropic Claude and MCP
- WebSocket programming for real-time applications
- Modern web development with HTML5, CSS3, and ES6+
- Async programming in Python
- FastAPI for web APIs
- Responsive web design principles
- Environment-based configuration
- Clean code structure and separation of concerns
- **Real-world MCP architecture** patterns

## 🚧 Troubleshooting

**Connection Issues**:
- Ensure all three servers are running in correct order (API → MCP → Web)
- Check that ports 8000 and 8001 are not being used by other applications
- Verify your firewall isn't blocking the connections

**API Key Issues**:
- Ensure your Anthropic API key is valid and has Claude access enabled
- Check that your `.env` file is in the root directory and properly formatted

**MCP Issues**:
- Verify MCP server is running: `python mcp_server/server.py`
- Check that `mcp>=1.0.0` is installed properly
- Ensure FastMCP compatibility with your MCP SDK version

**Browser Issues**:
- Use a modern browser that supports WebSockets
- Check the browser console for JavaScript errors
- Try refreshing the page if the connection seems stuck

**Dependencies**:
- If you encounter import errors, ensure all dependencies are installed: `pip install -r requirements.txt`
- Make sure you're using Python 3.8 or higher
- Verify virtual environment is activated

---

## 👨‍💻 Author & Contributing

**Created by**: Milton Mathan
**Purpose**: Educational demonstration of MCP architecture
**License**: MIT License

### Contributing
This is a learning project! Feel free to:
- Fork and experiment with the code
- Try different LLM providers or MCP tools
- Add new data sources or functionality
- Submit issues or improvements

### Useful Links
- [Anthropic MCP Documentation](https://modelcontextprotocol.io/)
- [Claude API Documentation](https://docs.anthropic.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

🎉 Enjoy building and learning with MCP Chatbot Web!