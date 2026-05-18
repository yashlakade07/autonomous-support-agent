from typing import Annotated, TypedDict, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
import httpx

class AgentState(TypedDict):
    ticket_id: str
    customer_id: str
    message: str
    customer_context: Dict[str, Any]
    resolution: str
    next_action: str

def get_local_llm():
    return ChatOllama(
        model="qwen2.5:7b", 
        temperature=0,
        base_url="http://host.docker.internal:11434"
    )

async def triage_agent(state: AgentState) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://mcp-server:8001/tools/get_customer_context?customer_id={state['customer_id']}"
        )
        crm_data = response.json().get("data", {})
    
    llm = get_local_llm()
    prompt = f"Analyze message: '{state['message']}'. Is this a routine account inquiry or an escalation request? Respond with exactly 'resolve' or 'escalate' and nothing else."
    ai_response = llm.invoke([HumanMessage(content=prompt)])
    
    action = ai_response.content.strip().lower()
    next_step = "resolve" if "resolve" in action else "escalate"
    
    return {
        "customer_context": crm_data,
        "next_action": next_step
    }

async def resolution_agent(state: AgentState) -> Dict[str, Any]:
    llm = get_local_llm()
    system_msg = SystemMessage(content=f"You are an automated support handler. Customer context: {state['customer_context']}")
    user_msg = HumanMessage(content=f"Resolve this message concisely: {state['message']}")
    
    ai_response = llm.invoke([system_msg, user_msg])
    
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://mcp-server:8001/tools/update_ticket_status",
            params={"ticket_id": state['ticket_id'], "status": "resolved", "notes": ai_response.content}
        )
        
    return {"resolution": ai_response.content, "next_action": "end"}

async def escalation_agent(state: AgentState) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://mcp-server:8001/tools/update_ticket_status",
            params={"ticket_id": state['ticket_id'], "status": "escalated", "notes": "Route to human team."}
        )
    return {"resolution": "This ticket requires specialized human intervention and has been escalated.", "next_action": "end"}

def router(state: AgentState):
    if state["next_action"] == "resolve":
        return "resolution_agent"
    elif state["next_action"] == "escalate":
        return "escalation_agent"
    return END

workflow = StateGraph(AgentState)
workflow.add_node("triage_agent", triage_agent)
workflow.add_node("resolution_agent", resolution_agent)
workflow.add_node("escalation_agent", escalation_agent)

workflow.set_entry_point("triage_agent")
workflow.add_conditional_edges("triage_agent", router, {
    "resolution_agent": "resolution_agent",
    "escalation_agent": "escalation_agent"
})
workflow.add_edge("resolution_agent", END)
workflow.add_edge("escalation_agent", END)

compiled_graph = workflow.compile()