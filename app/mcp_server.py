import json
from fastapi import FastAPI

mcp_app = FastAPI(title="CRM Mock MCP Server")

MOCK_CRM = {
    "CUST_101": {"name": "Alice Smith", "tier": "Premium", "status": "Active"},
    "CUST_102": {"name": "Bob Jones", "tier": "Free", "status": "Suspended"}
}

@mcp_app.get("/tools/get_customer_context")
async def get_customer_context(customer_id: str):
    customer = MOCK_CRM.get(customer_id)
    if not customer:
        return {"error": f"Customer {customer_id} not found."}
    return {"status": "success", "data": customer}

@mcp_app.post("/tools/update_ticket_status")
async def update_ticket_status(ticket_id: str, status: str, notes: str):
    return {"status": "success", "message": f"Ticket {ticket_id} marked as {status}."}