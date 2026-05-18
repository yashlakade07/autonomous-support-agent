import os
from fastapi import FastAPI, HTTPException
from app.schemas import TicketInput, TicketResponse
from app.graph import compiled_graph

app = FastAPI(title="Production Support Agent Service")

@app.post("/api/v1/tickets/process", response_model=TicketResponse)
async def process_ticket(payload: TicketInput):
    try:
        initial_state = {
            "ticket_id": payload.ticket_id,
            "customer_id": payload.customer_id,
            "message": payload.message,
            "customer_context": {},
            "resolution": "",
            "next_action": ""
        }
        
        final_state = await compiled_graph.ainvoke(initial_state)
        status_mapping = "escalated" if final_state["next_action"] == "end" and "escalated" in final_state["resolution"] else "resolved"
        
        return TicketResponse(
            ticket_id=final_state["ticket_id"],
            status=status_mapping,
            resolution_summary=final_state["resolution"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))