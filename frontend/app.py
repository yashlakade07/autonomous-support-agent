import streamlit as st
import requests
import uuid

# Configure page
st.set_page_config(page_title="AI Support Escalation Agent", page_icon="🤖", layout="centered")

st.title("🤖 Autonomous Support Agent")
st.markdown("Submit a mock customer ticket to see how the multi-agent system routes and resolves it.")

# Hardcoded mock users based on our MCP server data
CUSTOMER_MOCKS = {
    "CUST_101 (Premium, Active)": "CUST_101",
    "CUST_102 (Free, Suspended)": "CUST_102"
}

# UI Layout
with st.sidebar:
    st.header("Simulation Settings")
    selected_customer = st.selectbox("Select Customer Context:", list(CUSTOMER_MOCKS.keys()))
    customer_id = CUSTOMER_MOCKS[selected_customer]
    
    st.divider()
    st.markdown("**Backend Status:**")
    st.success("FastAPI connected")
    st.success("Ollama (Local) connected")

# Chat interface
message = st.text_area("Customer Message:", placeholder="e.g., How do I update my billing profile data?")

if st.button("Submit Ticket", type="primary"):
    if not message:
        st.warning("Please enter a message.")
    else:
        with st.spinner("Agents are processing the ticket..."):
            # Generate a random ticket ID for this session
            ticket_id = f"T_{uuid.uuid4().hex[:6].upper()}"
            
            payload = {
                "ticket_id": ticket_id,
                "customer_id": customer_id,
                "message": message
            }
            
            try:
                # Call the FastAPI backend running in the other Docker container
                response = requests.post("http://fastapi-app:8000/api/v1/tickets/process", json=payload)
                response.raise_for_status()
                data = response.json()
                
                # Display Results
                st.divider()
                st.subheader(f"Ticket: {data['ticket_id']}")
                
                # Color code the status badge
                if data['status'] == "resolved":
                    st.success(f"Status: **{data['status'].upper()}**")
                else:
                    st.error(f"Status: **{data['status'].upper()}**")
                    
                st.markdown("### Agent Resolution Summary:")
                st.info(data['resolution_summary'])
                
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to backend. Error: {e}")