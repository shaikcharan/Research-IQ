import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_research_report_lifecycle_and_export():
    """Verify saving report, retrieving it, exporting to Markdown and PDF, and deleting it."""
    # 1. Save Report
    payload = {
        "title": "Comprehensive Battery Lifespan Evaluation",
        "research_question": "What factors govern cycle life under rapid charging?",
        "purpose": "Academic Literature Review",
        "content_markdown": "# Comprehensive Battery Lifespan Evaluation\n\n## 1. Executive Summary\nAnalysis of experimental papers.\n\n## 4. Key Findings\n- Pre-heating to 45C reduces interfacial impedance.",
        "selected_document_ids": ["doc_sample_1"]
    }
    save_resp = client.post("/api/reports/save", json=payload)
    assert save_resp.status_code == 200
    report_data = save_resp.json()
    report_id = report_data["id"]

    # 2. Get Report
    get_resp = client.get(f"/api/reports/{report_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == payload["title"]

    # 3. Export to Markdown
    md_resp = client.get(f"/api/reports/{report_id}/export?format=markdown")
    assert md_resp.status_code == 200
    assert "text/markdown" in md_resp.headers["content-type"]
    assert b"Comprehensive Battery Lifespan Evaluation" in md_resp.content

    # 4. Export to PDF
    pdf_resp = client.get(f"/api/reports/{report_id}/export?format=pdf")
    assert pdf_resp.status_code == 200
    assert "application/pdf" in pdf_resp.headers["content-type"]
    assert len(pdf_resp.content) > 500  # PDF binary exists

    # 5. Delete Report
    del_resp = client.delete(f"/api/reports/{report_id}")
    assert del_resp.status_code == 200

    # 6. Verify 404 after deletion
    check_resp = client.get(f"/api/reports/{report_id}")
    assert check_resp.status_code == 404
