
import json
from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any, Optional

app = FastAPI()

def load_data(filename: str) -> List[Dict[str, Any]]:
    with open(f"data/{filename}") as f:
        return json.load(f)

@app.get("/products")
async def get_products():
    return load_data("products.json")

@app.get("/products/{product_id}")
async def get_product(product_id: str):
    products = load_data("products.json")
    product = next((p for p in products if p["id"] == product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/tickets")
async def get_tickets(
    status: Optional[str] = None,
    customer_name: Optional[str] = None,
    issue_keyword: Optional[str] = None
):
    tickets = load_data("tickets.json")
    
    if status:
        tickets = [t for t in tickets if t['status'] == status]
    
    if customer_name:
        tickets = [t for t in tickets if customer_name.lower() in t['customer_name'].lower()]

    if issue_keyword:
        tickets = [t for t in tickets if issue_keyword.lower() in t['issue'].lower()]
        
    return tickets

@app.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: str):
    tickets = load_data("tickets.json")
    ticket = next((t for t in tickets if t["id"] == ticket_id), None)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@app.get("/faq")
async def get_faq(keyword: Optional[str] = None):
    faqs = load_data("faq.json")
    
    if keyword:
        keyword = keyword.lower()
        faqs = [
            f for f in faqs 
            if keyword in f['question'].lower() or keyword in f['answer'].lower()
        ]
        
    return faqs

@app.get("/faq/{faq_id}")
async def get_faq_item(faq_id: str):
    faqs = load_data("faq.json")
    faq = next((f for f in faqs if f["id"] == faq_id), None)
    if faq is None:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return faq

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 