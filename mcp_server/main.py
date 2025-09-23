
import requests
from typing import Optional

# Tool to get all products or a specific product by ID
def get_products(product_id: Optional[str] = None):
    """
    Fetches a list of all products or a specific product by its ID from the API.
    :param product_id: The ID of the product to fetch. If None, all products are returned.
    """
    url = "http://localhost:8000/products"
    if product_id:
        url = f"{url}/{product_id}"
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch products", "status_code": response.status_code}

# Tool to get all tickets or tickets filtered by status
def get_tickets(ticket_id: Optional[str] = None, status: Optional[str] = None):
    """
    Fetches a list of all tickets or filters tickets by status from the API.
    :param status: The status to filter tickets by (e.g., 'open', 'closed'). If None, all tickets are returned.
    """
    url = "http://localhost:8000/tickets"
    if ticket_id:
        url = f"{url}/{ticket_id}"

    params = {}
    if status:
        params['status'] = status
        
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch tickets", "status_code": response.status_code}

# Tool to get all FAQs or a specific FAQ by ID
def get_faq(faq_id: Optional[str] = None):
    """
    Fetches a list of all FAQs or a specific FAQ by its ID from the API.
    :param faq_id: The ID of the FAQ to fetch. If None, all FAQs are returned.
    """
    url = "http://localhost:8000/faq"
    if faq_id:
        url = f"{url}/{faq_id}"
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch FAQs", "status_code": response.status_code}

# MCP Server to expose tools
class MCPServer:
    def __init__(self):
        self.tools = {
            "get_products": get_products,
            "get_tickets": get_tickets,
            "get_faq": get_faq,
        }

    def handle_request(self, tool_name: str, **kwargs):
        if tool_name in self.tools:
            return self.tools[tool_name](**kwargs)
        else:
            return {"error": f"Tool '{tool_name}' not found."} 