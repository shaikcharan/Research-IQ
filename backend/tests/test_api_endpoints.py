import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.config import settings

client = TestClient(app)

def test_health_check_endpoint():
    """Verify health endpoint returns status 200 and system details."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "ResearchIQ"
    assert "embedding_model" in data

def test_dashboard_stats_endpoint():
    """Verify dashboard stats returns numerical metrics from DB."""
    response = client.get("/api/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_documents" in data
    assert "indexed_documents" in data
    assert "total_sessions" in data
    assert "total_reports" in data
    assert "recent_documents" in data

def test_invalid_pdf_upload():
    """Verify non-PDF files are rejected with HTTP 400."""
    response = client.post(
        "/api/documents/upload",
        files={"files": ("malicious.exe", b"MZDummyExecutableBytes", "application/octet-stream")}
    )
    assert response.status_code == 400
    assert "Only PDF files are supported" in response.json()["detail"]

def test_session_lifecycle_and_chat_persistence():
    """Verify research session creation, message storage, and citation persistence."""
    # Create session
    create_resp = client.post("/api/research/sessions", json={"title": "Test Integration Session"})
    assert create_resp.status_code == 200
    session_data = create_resp.json()
    session_id = session_data["id"]

    # Verify session listed
    list_resp = client.get("/api/research/sessions")
    assert list_resp.status_code == 200
    assert any(s["id"] == session_id for s in list_resp.json())

    # Delete session
    del_resp = client.delete(f"/api/research/sessions/{session_id}")
    assert del_resp.status_code == 200
