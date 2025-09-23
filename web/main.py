#!/usr/bin/env python3
"""
Web server with WebSocket support for MCP Chatbot using Anthropic Claude.
This server uses the proper MCP client to communicate with the MCP server via stdio.
"""

import asyncio
import os
import json
from typing import Dict, Any, Optional
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from anthropic import Anthropic
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mcp_client.client import SimpleMCPClient

# Load environment variables
load_dotenv()

class MCPChatbot:
    """
    Chatbot that combines Anthropic Claude with MCP tool calling.
    """

    def __init__(self):
        """Initialize the chatbot with Claude client and MCP client."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in .env file. Please check your .env configuration.")

        self.claude = Anthropic(api_key=api_key)
        self.mcp_client = SimpleMCPClient()

        # Define tools for Claude
        self.tools = [
            {
                "name": "get_products",
                "description": "Fetches a list of all products or a specific product by its ID from the API.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "product_id": {
                            "type": "string",
                            "description": "The ID of the product to fetch. If not provided, all products are returned."
                        }
                    }
                }
            },
            {
                "name": "get_tickets",
                "description": "Fetches support tickets. Can filter by status, customer name, or keywords in the issue description.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "ticket_id": {
                            "type": "string",
                            "description": "The ID of the ticket to fetch. If provided, other filters are ignored."
                        },
                        "status": {
                            "type": "string",
                            "description": "The status to filter tickets by (e.g., 'open', 'closed')."
                        },
                        "customer_name": {
                            "type": "string",
                            "description": "The name of the customer to fetch tickets for."
                        },
                        "issue_keyword": {
                            "type": "string",
                            "description": "A keyword to search for in the ticket's issue description."
                        }
                    }
                }
            },
            {
                "name": "get_faq",
                "description": "Fetches FAQs. Can fetch a specific FAQ by ID or search for FAQs by a keyword.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "faq_id": {
                            "type": "string",
                            "description": "The ID of the FAQ to fetch. If provided, the keyword is ignored."
                        },
                        "keyword": {
                            "type": "string",
                            "description": "A keyword to search for in the FAQ's question and answer."
                        }
                    }
                }
            }
        ]

    async def get_response(self, user_message: str, conversation_history: list = None) -> str:
        """
        Get a response from Claude, potentially using MCP tools.

        Args:
            user_message: The user's message
            conversation_history: Previous conversation messages

        Returns:
            Claude's response as a string
        """
        try:
            # Build conversation messages
            messages = conversation_history or []
            messages.append({"role": "user", "content": user_message})

            # Get response from Claude
            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                tools=self.tools,
                messages=messages
            )

            # Check if Claude wants to use tools
            if response.stop_reason == "tool_use":
                # Process tool calls
                tool_results = []
                for content_block in response.content:
                    if content_block.type == "tool_use":
                        tool_name = content_block.name
                        tool_input = content_block.input
                        tool_use_id = content_block.id

                        # Call the MCP tool
                        tool_result = await self.mcp_client.call_tool_with_connection(
                            tool_name, tool_input
                        )

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": json.dumps(tool_result)
                        })

                # Send tool results back to Claude for final response
                messages.append({"role": "assistant", "content": response.content})
                messages.append({
                    "role": "user",
                    "content": tool_results
                })

                final_response = self.claude.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1000,
                    messages=messages
                )

                return final_response.content[0].text

            else:
                # No tool use, return direct response
                return response.content[0].text

        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}. Please make sure the API server is running on port 8000."


# Global chatbot instance
chatbot_instance: Optional[MCPChatbot] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - startup and shutdown."""
    global chatbot_instance

    print("🤖 Initializing MCP Chatbot Web...")
    try:
        chatbot_instance = MCPChatbot()
        print("✅ Chatbot initialized successfully!")
        print("🌐 Web interface ready at http://127.0.0.1:8001")
        print("📍 Make sure MCP server is running: python mcp_server/server.py")
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {e}")
        import traceback
        traceback.print_exc()
        chatbot_instance = None

    yield

    # Cleanup on shutdown
    print("🔄 Closing chatbot resources...")
    chatbot_instance = None

# Create FastAPI application
app = FastAPI(
    title="MCP Chatbot Web",
    description="Web-based chatbot powered by Claude and Model Context Protocol",
    version="1.0.0",
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="web/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_homepage():
    """Serve the main chat interface."""
    try:
        with open("web/static/index.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Error: Chat interface not found</h1>", status_code=404)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "chatbot_ready": chatbot_instance is not None,
        "message": "MCP Chatbot Web is running"
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time chat."""
    await websocket.accept()
    print("🔌 Client connected to WebSocket")

    conversation_history = []

    try:
        while True:
            # Receive message from client
            user_message = await websocket.receive_text()
            print(f"👤 User: {user_message}")

            if chatbot_instance is None:
                await websocket.send_text("❌ Chatbot is not ready. Please check server logs.")
                continue

            try:
                # Get response from chatbot
                bot_response = await chatbot_instance.get_response(
                    user_message,
                    conversation_history.copy()
                )

                # Update conversation history
                conversation_history.extend([
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": bot_response}
                ])

                # Keep history manageable (last 10 messages)
                if len(conversation_history) > 20:
                    conversation_history = conversation_history[-20:]

                print(f"🤖 Bot: {bot_response}")
                await websocket.send_text(bot_response)

            except Exception as e:
                error_message = f"I apologize, but I encountered an error: {str(e)}"
                print(f"❌ Error: {e}")
                await websocket.send_text(error_message)

    except WebSocketDisconnect:
        print("🔌 Client disconnected from WebSocket")
    except Exception as e:
        print(f"❌ WebSocket error: {e}")

if __name__ == "__main__":
    print("🚀 Starting MCP Chatbot Web Server...")
    print("📝 Architecture: 3-process MCP system")
    print("   1. API Server (port 8000) - python api/main.py")
    print("   2. MCP Server (stdio) - python mcp_server/server.py")
    print("   3. Web Server (port 8001) - python web/main.py")
    print("-" * 60)

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8001,
        log_level="info"
    )