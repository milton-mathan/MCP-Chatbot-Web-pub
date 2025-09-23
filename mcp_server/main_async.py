import aiohttp
from typing import Optional

# Tool to get all products or a specific product by ID
async def get_products(product_id: Optional[str] = None):
    """
    Fetches a list of all products or a specific product by its ID from the API.
    :param product_id: The ID of the product to fetch. If None, all products are returned.
    """
    url = "http://localhost:8000/products"
    if product_id:
        url = f"{url}/{product_id}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {"error": "Failed to fetch products", "status_code": response.status}

# Tool to get all tickets or tickets filtered by status
async def get_tickets(
    ticket_id: Optional[str] = None,
    status: Optional[str] = None,
    customer_name: Optional[str] = None,
    issue_keyword: Optional[str] = None
):
    """
    Fetches tickets. Can filter by status, customer name, or keywords in the issue description.
    :param ticket_id: The ID of the ticket to fetch. If provided, other filters are ignored.
    :param status: The status to filter tickets by (e.g., 'open', 'closed').
    :param customer_name: The name of the customer to fetch tickets for.
    :param issue_keyword: A keyword to search for in the ticket's issue description.
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
        
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {"error": "Failed to fetch tickets", "status_code": response.status}

# Tool to get all FAQs or a specific FAQ by ID
async def get_faq(faq_id: Optional[str] = None, keyword: Optional[str] = None):
    """
    Fetches FAQs. Can fetch a specific FAQ by ID or search for FAQs by a keyword.
    :param faq_id: The ID of the FAQ to fetch. If provided, the keyword is ignored.
    :param keyword: A keyword to search for in the FAQ's question and answer.
    """
    url = "http://localhost:8000/faq"
    if faq_id:
        url = f"{url}/{faq_id}"
        params = {}
    else:
        params = {"keyword": keyword}
        params = {k: v for k, v in params.items() if v is not None}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {"error": "Failed to fetch FAQs", "status_code": response.status}

# MCP Server to expose tools
class MCPServer:
    def __init__(self):
        self.tools = {
            "get_products": get_products,
            "get_tickets": get_tickets,
            "get_faq": get_faq,
        }

    async def handle_request(self, tool_name: str, **kwargs):
        if tool_name in self.tools:
            return await self.tools[tool_name](**kwargs)
        else:
            return {"error": f"Tool '{tool_name}' not found."} 