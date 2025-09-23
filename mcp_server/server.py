#!/usr/bin/env python3
"""
MCP Server implementation using FastMCP with stdio transport.
This server exposes tools for products, tickets, and FAQ data retrieval.
"""

import asyncio
import httpx
from typing import Optional
from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("MCP Web Chatbot Server")

@mcp.tool()
async def get_products(product_id: Optional[str] = None) -> dict:
    """
    Fetches a list of all products or a specific product by its ID from the API.

    Args:
        product_id: The ID of the product to fetch. If None, all products are returned.

    Returns:
        Dictionary containing product data or error message
    """
    url = "http://localhost:8000/products"
    if product_id:
        url = f"{url}/{product_id}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                return {"products": data}
            else:
                return {"error": "Failed to fetch products", "status_code": response.status_code}
        except Exception as e:
            return {"error": f"Connection failed: {str(e)}"}

@mcp.tool()
async def get_tickets(
    ticket_id: Optional[str] = None,
    status: Optional[str] = None,
    customer_name: Optional[str] = None,
    issue_keyword: Optional[str] = None
) -> dict:
    """
    Fetches tickets. Can filter by status, customer name, or keywords in the issue description.

    Args:
        ticket_id: The ID of the ticket to fetch. If provided, other filters are ignored.
        status: The status to filter tickets by (e.g., 'open', 'closed').
        customer_name: The name of the customer to fetch tickets for.
        issue_keyword: A keyword to search for in the ticket's issue description.

    Returns:
        Dictionary containing ticket data or error message
    """
    url = "http://localhost:8000/tickets"
    if ticket_id:
        url = f"{url}/{ticket_id}"
        params = {}
    else:
        params = {
            "status": status,
            "customer_name": customer_name,
            "issue_keyword": issue_keyword
        }
        params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return {"tickets": data}
            else:
                return {"error": "Failed to fetch tickets", "status_code": response.status_code}
        except Exception as e:
            return {"error": f"Connection failed: {str(e)}"}

@mcp.tool()
async def get_faq(faq_id: Optional[str] = None, keyword: Optional[str] = None) -> dict:
    """
    Fetches FAQs. Can fetch a specific FAQ by ID or search for FAQs by a keyword.

    Args:
        faq_id: The ID of the FAQ to fetch. If provided, the keyword is ignored.
        keyword: A keyword to search for in the FAQ's question and answer.

    Returns:
        Dictionary containing FAQ data or error message
    """
    url = "http://localhost:8000/faq"
    if faq_id:
        url = f"{url}/{faq_id}"
        params = {}
    else:
        params = {"keyword": keyword}
        params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return {"faqs": data}
            else:
                return {"error": "Failed to fetch FAQs", "status_code": response.status_code}
        except Exception as e:
            return {"error": f"Connection failed: {str(e)}"}

if __name__ == "__main__":
    # Run the MCP server with stdio transport
    mcp.run()