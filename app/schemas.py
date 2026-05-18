from pydantic import BaseModel, Field

class TicketInput(BaseModel):
    ticket_id: str = Field(..., description="Unique identifier for the ticket")
    customer_id: str = Field(..., description="Unique identifier for the customer")
    message: str = Field(..., description="The customer's support request message")

class TicketResponse(BaseModel):
    ticket_id: str
    status: str = Field(..., description="resolved, escalated, or pending")
    resolution_summary: str