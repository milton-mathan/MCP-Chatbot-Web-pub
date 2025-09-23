
import sys
import os

from mcp_server.main import MCPServer

class MCPClient:
    def __init__(self, server: MCPServer):
        self.server = server

    async def call_tool(self, tool_name: str, **kwargs):
        """
        Calls a tool on the MCP server.
        :param tool_name: The name of the tool to call.
        :param kwargs: The arguments for the tool.
        """
        return await self.server.handle_request(tool_name, **kwargs) 