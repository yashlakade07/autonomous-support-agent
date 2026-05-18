import pytest
from fastapi.testclient import TestClient
import unittest.mock as mock
from app.main import app

client = TestClient(app)

def test_process_ticket_routine_resolution():
    payload = {
        "ticket_id": "T_TEST_01",
        "customer_id": "CUST_101",
        "message": "How do I update my billing profile data?"
    }
    
    with mock.patch("app.graph.ChatOllama") as mock_llm, \
         mock.patch("app.graph.httpx.AsyncClient") as mock_http:
        
        mock_http.return_value.__aenter__.return_value.get.return_value.json.return_value = {
            "status": "success", 
            "data": {"name": "Alice Smith", "tier": "Premium", "status": "Active"}
        }
        mock_http.return_value.__aenter__.return_value.post.return_value.json.return_value = {"status": "success"}
        
        mock_instance = mock_llm.return_value
        mock_triage_response = mock.MagicMock()
        mock_triage_response.content = "resolve"
        
        mock_resolution_response = mock.MagicMock()
        mock_resolution_response.content = "To update billing data, go to Settings > Billing."
        
        mock_instance.invoke.side_effect = [mock_triage_response, mock_resolution_response]

        response = client.post("/api/v1/tickets/process", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["ticket_id"] == "T_TEST_01"
        assert data["status"] == "resolved"
        assert "Settings > Billing" in data["resolution_summary"]

def test_process_ticket_escalation_path():
    payload = {
        "ticket_id": "T_TEST_02",
        "customer_id": "CUST_102",
        "message": "I demand a full refund immediately!"
    }
    
    with mock.patch("app.graph.ChatOllama") as mock_llm, \
         mock.patch("app.graph.httpx.AsyncClient") as mock_http:
        
        mock_http.return_value.__aenter__.return_value.get.return_value.json.return_value = {
            "status": "success", 
            "data": {"name": "Bob Jones", "tier": "Free", "status": "Suspended"}
        }
        mock_http.return_value.__aenter__.return_value.post.return_value.json.return_value = {"status": "success"}
        
        mock_instance = mock_llm.return_value
        mock_triage_response = mock.MagicMock()
        mock_triage_response.content = "escalate"
        
        mock_instance.invoke.return_value = mock_triage_response

        response = client.post("/api/v1/tickets/process", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["ticket_id"] == "T_TEST_02"
        assert data["status"] == "escalated"
        assert "human intervention" in data["resolution_summary"]

def test_invalid_payload_validation():
    malformed_payload = {
        "ticket_id": "T_INVALID",
        "customer_id": "CUST_101"
    }
    response = client.post("/api/v1/tickets/process", json=malformed_payload)
    assert response.status_code == 422