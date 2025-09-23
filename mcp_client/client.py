#!/usr/bin/env python3
"""
MCP Client implementation using the official MCP Python SDK.
This client connects to the MCP server via stdio transport.
"""

import asyncio
import subprocess
from typing import Dict, Any, Optional
from contextlib import asynccontextmanager

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClient:
    """
    MCP Client that connects to an external MCP server process via stdio transport.
    """

    def __init__(self, server_path: str = "python", server_args: list = None):
        """
        Initialize the MCP client.

        Args:
            server_path: Path to the server executable
            server_args: Arguments to pass to the server
        """
        self.server_path = server_path
        self.server_args = server_args or ["mcp_server/server.py"]
        self.session: Optional[ClientSession] = None
        self.available_tools: Dict[str, Any] = {}

    async def connect(self) -> bool:
        """
        Connect to the MCP server and initialize the session.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Create server parameters for stdio transport
            server_params = StdioServerParameters(
                command=self.server_path,
                args=self.server_args,
                env=None
            )

            # Connect to the server
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    self.session = session

                    # Initialize the session
                    await session.initialize()

                    # List available tools
                    tools_result = await session.list_tools()
                    self.available_tools = {tool.name: tool for tool in tools_result.tools}

                    print(f"✅ Connected to MCP server! Found {len(self.available_tools)} tools:")
                    for tool_name in self.available_tools.keys():
                        print(f"   - {tool_name}")

                    return True

        except Exception as e:
            print(f"❌ Failed to connect to MCP server: {e}")
            return False

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Call a tool on the MCP server.

        Args:
            tool_name: Name of the tool to call
            arguments: Arguments to pass to the tool

        Returns:
            Tool result or error message
        """
        if not self.session:
            return {"error": "MCP client not connected"}

        if tool_name not in self.available_tools:
            return {"error": f"Tool '{tool_name}' not found"}

        try:
            # Call the tool
            result = await self.session.call_tool(tool_name, arguments or {})

            # Process the result
            if result.content:
                if len(result.content) == 1 and hasattr(result.content[0], 'text'):
                    # Single text result
                    import json
                    try:
                        return json.loads(result.content[0].text)
                    except json.JSONDecodeError:
                        return {"result": result.content[0].text}
                else:
                    # Multiple or complex results
                    return {"result": [item.text if hasattr(item, 'text') else str(item) for item in result.content]}
            else:
                return {"result": "No content returned"}

        except Exception as e:
            return {"error": f"Tool call failed: {str(e)}"}

    async def list_tools(self) -> Dict[str, Any]:
        """
        Get information about available tools.

        Returns:
            Dictionary of tool names and their information
        """
        return {name: {
            "name": tool.name,
            "description": tool.description,
            "inputSchema": tool.inputSchema
        } for name, tool in self.available_tools.items()}

    async def disconnect(self):
        """
        Disconnect from the MCP server.
        """
        if self.session:
            # The session will be closed when the context manager exits
            self.session = None
            print("🔄 Disconnected from MCP server")


class SimpleMCPClient:
    """
    Simplified MCP Client for web application use.
    This version manages the connection lifecycle automatically.
    """

    def __init__(self):
        self.server_process = None

    async def call_tool_with_connection(self, tool_name: str, arguments: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Call a tool by creating a temporary connection to the MCP server.

        Args:
            tool_name: Name of the tool to call
            arguments: Arguments to pass to the tool

        Returns:
            Tool result or error message
        """
        try:
            # Create server parameters
            server_params = StdioServerParameters(
                command="python",
                args=["mcp_server/server.py"],
                env=None
            )

            # Connect and call tool
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    # Initialize the session
                    await session.initialize()

                    # Call the tool
                    result = await session.call_tool(tool_name, arguments or {})

                    # Process the result
                    if result.content:
                        if len(result.content) == 1 and hasattr(result.content[0], 'text'):
                            # Single text result
                            import json
                            try:
                                return json.loads(result.content[0].text)
                            except json.JSONDecodeError:
                                return {"result": result.content[0].text}
                        else:
                            # Multiple or complex results
                            return {"result": [item.text if hasattr(item, 'text') else str(item) for item in result.content]}
                    else:
                        return {"result": "No content returned"}

        except Exception as e:
            return {"error": f"MCP tool call failed: {str(e)}"}


# Example usage
async def test_client():
    """Test the MCP client functionality."""
    client = MCPClient()

    if await client.connect():
        # Test each tool
        tools_to_test = [
            ("get_products", {}),
            ("get_tickets", {"status": "open"}),
            ("get_faq", {"keyword": "return"})
        ]

        for tool_name, args in tools_to_test:
            print(f"\n🧪 Testing {tool_name}:")
            result = await client.call_tool(tool_name, args)
            print(f"   Result: {result}")

        await client.disconnect()
    else:
        print("❌ Failed to connect to MCP server")

if __name__ == "__main__":
    asyncio.run(test_client())