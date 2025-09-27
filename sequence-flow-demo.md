# MCP Chatbot Web - Sequence Flow Demo

This document traces the complete sequence flow from when a user types something in the chatbot to receiving a response with data from the MCP tools.

## Complete Sequence Flow: User Input → Tool Data Response

Here's the detailed step-by-step flow when a user types something like "Show me open tickets" in the chatbot:

### 1. **Frontend (Browser)**
**File: `web/static/script.js:45-59`**
- User types message and hits Enter/Submit
- Form submit event prevents default behavior
- Message extracted from input field (`messageInput.value.trim()`)
- Message displayed in chat (`appendMessage(userMessage, "user")`)
- WebSocket sends message (`ws.send(userMessage)`)
- Typing indicator shown (`appendTypingIndicator()`)

### 2. **WebSocket Transport**
**Connection: Browser ↔ Web Server (port 8001)**
- Message travels over WebSocket connection established at `ws://localhost:8001/ws`
- Raw text message sent over the wire

### 3. **Web Server - WebSocket Handler**
**File: `web/main.py:224-270`**
- WebSocket endpoint receives message (`user_message = await websocket.receive_text()`)
- Message logged: `👤 User: {user_message}`
- Calls chatbot instance: `bot_response = await chatbot_instance.get_response(user_message, conversation_history.copy())`

### 4. **Claude LLM Integration & Tool Calling**
**File: `web/main.py:101-167`**

**A. Initial Claude Request:**
- Creates conversation messages with user input
- Sends to Claude API with available tools defined (`self.tools`)
- Model: `claude-3-5-sonnet-20241022`
- Tools available: `get_products`, `get_tickets`, `get_faq`

**B. Claude Decides to Use Tools:**
- Claude analyzes "Show me open tickets"
- Determines `get_tickets` tool should be called
- Response includes `stop_reason == "tool_use"`
- Tool call details: `tool_name = "get_tickets"`, `tool_input = {"status": "open"}`

**C. Tool Execution Flow:**
```python
# web/main.py:136-138
tool_result = await self.mcp_client.call_tool_with_connection(
    tool_name, tool_input
)
```

### 5. **MCP Client → MCP Server Communication**
**File: `mcp_client/client.py:141-186`**

**A. Process Creation:**
- Creates `StdioServerParameters` with command: `"python"`, args: `["mcp_server/server.py"]`
- Spawns MCP server subprocess via stdio transport

**B. MCP Protocol Communication:**
- Establishes stdio connection (`read`, `write` streams)
- Creates `ClientSession` with read/write streams
- Initializes session with JSON-RPC 2.0 handshake
- Calls tool: `await session.call_tool("get_tickets", {"status": "open"})`

### 6. **MCP Server - Tool Execution**
**File: `mcp_server/server.py:41-81`**

**A. Tool Handler:**
- `get_tickets()` function receives parameters: `status="open"`
- Constructs API URL: `"http://localhost:8000/tickets"`
- Adds query parameters: `{"status": "open"}`

**B. API Call:**
```python
# mcp_server/server.py:72-77
async with httpx.AsyncClient() as client:
    response = await client.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {"tickets": data}
```

### 7. **API Server - Data Retrieval**
**File: `api/main.py:24-41`**

**A. Endpoint Handler:**
- `get_tickets()` function receives request with `status="open"`
- Loads data: `tickets = load_data("tickets.json")`
- Filters tickets: `tickets = [t for t in tickets if t['status'] == status]`
- Returns filtered JSON data

**B. Data Source:**
- Reads from `data/tickets.json` file
- Filters based on status field
- Returns matching ticket records

### 8. **Response Journey Back**

**A. API → MCP Server:**
- JSON response with filtered tickets returned via HTTP
- MCP server packages response: `{"tickets": data}`

**B. MCP Server → MCP Client:**
- Tool result sent back via stdio JSON-RPC 2.0
- Client processes result and extracts JSON content

**C. MCP Client → Web Server:**
- Tool result returned to `MCPChatbot.get_response()`
- Formatted as tool result for Claude: `{"type": "tool_result", "tool_use_id": tool_use_id, "content": json.dumps(tool_result)}`

**D. Final Claude Request:**
- Tool results sent back to Claude for natural language formatting
- Claude generates human-readable response about the tickets
- Returns formatted text response

**E. Web Server → Browser:**
- Response sent via WebSocket: `await websocket.send_text(bot_response)`
- Conversation history updated

### 9. **Frontend Display**
**File: `web/static/script.js:20-25, 61-80`**
- WebSocket receives message (`ws.onmessage`)
- Typing indicator removed
- Response displayed: `appendMessage(botMessage, "bot")`
- UI state updated (enable send button)

## Summary Flow Diagram

```
User Input → WebSocket → Web Server → Claude API → MCP Client → MCP Server → API Server → Data File
    ↓                                     ↑                        ↓           ↓           ↓
Browser ← WebSocket ← Web Server ← Claude API ← MCP Client ← MCP Server ← HTTP Response ← JSON Data
```

## Key Protocol Communications

- **Browser ↔ Web Server**: WebSocket (real-time)
- **Web Server ↔ Claude**: HTTPS API calls
- **MCP Client ↔ MCP Server**: stdio + JSON-RPC 2.0
- **MCP Server ↔ API Server**: HTTP REST API
- **API Server ↔ Data**: File I/O (JSON)

## Architecture Benefits

This architecture demonstrates proper MCP separation of concerns with each process having a specific responsibility in the data flow chain:

1. **Frontend**: User interface and real-time communication
2. **Web Server**: WebSocket management and LLM orchestration
3. **MCP Client**: Official MCP protocol implementation
4. **MCP Server**: Tool definitions and business logic
5. **API Server**: Data access and REST endpoints
6. **Data Layer**: JSON file storage

This separation allows for:
- Independent scaling of each component
- Clear protocol boundaries
- Easy debugging and monitoring
- Proper MCP standard compliance
- Educational demonstration of enterprise patterns

## Example User Queries

Here are some example queries and the tools they would trigger:

### Product Queries
- "What products do you have?" → `get_products()`
- "Tell me about laptop prod_002" → `get_products(product_id="prod_002")`

### Ticket Queries
- "Show me open tickets" → `get_tickets(status="open")`
- "Find tickets for John Smith" → `get_tickets(customer_name="John Smith")`
- "What's ticket tkt_05 about?" → `get_tickets(ticket_id="tkt_05")`

### FAQ Queries
- "What's your return policy?" → `get_faq(keyword="return")`
- "How do I cancel an order?" → `get_faq(keyword="cancel")`
- "Show me shipping FAQs" → `get_faq(keyword="shipping")`

Each query follows the same 9-step sequence flow outlined above, with different tool parameters and data responses.

## Alternative Architecture: Dynamic Tool Binding

The current implementation uses **static tool binding** where tool definitions are hardcoded in the web server. A more robust approach would be **dynamic tool binding** where tools are discovered from the MCP server during initialization.

### Current Static Binding Limitations

**File: `web/main.py:42-99`**
- Tool definitions are **hardcoded** in the web server
- **Duplicate definitions** exist in both MCP server and web server
- Changes to MCP tools require manual updates to web server
- Risk of schema mismatches between components

### How Dynamic Binding Would Work

Dynamic binding involves **two separate phases**:

#### Phase 1: Initialization (One-time during startup)
```
Web Server Startup → MCP Client → MCP Server → MCP Client → Web Server
```

**Detailed initialization flow:**
1. **Web Server starts** (`python web/main.py`)
2. **Web Server** creates MCP Client and calls `mcp_client.connect()`
3. **MCP Client** connects to MCP Server via stdio
4. **MCP Client** calls `session.list_tools()`
5. **MCP Server** returns available tools with schemas
6. **MCP Client** receives tool definitions
7. **Web Server** converts MCP tool format to Claude API format
8. **Web Server** stores discovered tools for use with Claude

#### Phase 2: User Request (Runtime - same as current)
```
User → WebSocket → Web Server → Claude API → MCP Client → MCP Server → API Server → Data
                                     ↑                        ↓           ↓           ↓
Browser ← WebSocket ← Web Server ← Claude API ← MCP Client ← MCP Server ← HTTP ← JSON Data
```

### Dynamic Binding Implementation Example

```python
# web/main.py - Dynamic version
class MCPChatbot:
    async def initialize(self):
        """Initialize with dynamic tool discovery"""
        if await self.mcp_client.connect():
            self.tools = await self.discover_tools_from_mcp()
            print(f"✅ Discovered {len(self.tools)} tools from MCP server")

    async def discover_tools_from_mcp(self):
        """Convert MCP tools to Claude format"""
        mcp_tools = await self.mcp_client.list_tools()
        claude_tools = []

        for tool_name, tool_info in mcp_tools.items():
            claude_tool = {
                "name": tool_info["name"],
                "description": tool_info["description"],
                "input_schema": tool_info["inputSchema"]
            }
            claude_tools.append(claude_tool)

        return claude_tools
```

### Benefits of Dynamic Binding

**Advantages:**
- ✅ **Single Source of Truth**: Tools only defined in MCP Server
- ✅ **Auto-Discovery**: New MCP tools automatically available to Claude
- ✅ **Schema Sync**: No risk of mismatched schemas
- ✅ **Scalability**: Easy to add new tools without web server changes
- ✅ **Maintenance**: Eliminates code duplication

**Trade-offs:**
- ❌ More complex startup (requires MCP connection during initialization)
- ❌ Dependency on MCP server availability at startup
- ❌ Slightly more complex error handling

### Timeline Comparison

**Current Static Binding:**
```
Startup: Web Server starts with hardcoded tools
Runtime: User → Web Server → Claude (hardcoded tools) → MCP Client → MCP Server
```

**Dynamic Binding:**
```
Startup: Web Server → MCP Client → MCP Server (list_tools) → Tool Discovery
Runtime: User → Web Server → Claude (discovered tools) → MCP Client → MCP Server
```

The MCP client code already has the `list_tools()` capability in `mcp_client/client.py:109-120` - it would just need to be utilized during web server initialization instead of using hardcoded tool definitions.