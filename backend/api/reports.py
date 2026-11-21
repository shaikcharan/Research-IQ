import uuid
import json
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse

from backend.database import get_db_connection, get_now_iso
from backend.models import (
    ReportGenerateRequest,
    ReportSaveRequest,
    ReportUpdateRequest,
    ReportResponse
)
from backend.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["Research Reports"])

@router.post("/generate")
async def generate_report_draft(data: ReportGenerateRequest):
    """Generate a structured 13-section research brief draft."""
    if not data.selected_document_ids:
        raise HTTPException(
            status_code=400,
            detail="Please select at least one document to generate a research brief."
        )

    try:
        content_markdown = await ReportService.generate_brief(
            question=data.research_question,
            purpose=data.purpose,
            selected_doc_ids=data.selected_document_ids,
            title=data.title
        )
        return {
            "title": data.title or f"Executive Brief: {data.research_question[:50]}",
            "content_markdown": content_markdown
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

@router.post("/save", response_model=ReportResponse)
def save_report(data: ReportSaveRequest):
    """Save generated or edited research brief to database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    report_id = str(uuid.uuid4())
    now_iso = get_now_iso()
    docs_json = json.dumps(data.selected_document_ids)

    cursor.execute(
        """
        INSERT INTO research_reports (id, title, research_question, purpose, content_markdown, selected_document_ids_json, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (report_id, data.title, data.research_question, data.purpose, data.content_markdown, docs_json, now_iso, now_iso)
    )
    conn.commit()
    conn.close()

    return ReportResponse(
        id=report_id,
        title=data.title,
        research_question=data.research_question,
        purpose=data.purpose,
        content_markdown=data.content_markdown,
        selected_document_ids=data.selected_document_ids,
        created_at=now_iso,
        updated_at=now_iso
    )

@router.get("", response_model=List[ReportResponse])
def list_reports():
    """List all saved research reports."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, research_question, purpose, content_markdown, selected_document_ids_json, created_at, updated_at
        FROM research_reports
        ORDER BY updated_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    reports = []
    for r in rows:
        docs = []
        if r["selected_document_ids_json"]:
            try:
                docs = json.loads(r["selected_document_ids_json"])
            except Exception:
                pass

        reports.append(ReportResponse(
            id=r["id"],
            title=r["title"],
            research_question=r["research_question"],
            purpose=r["purpose"],
            content_markdown=r["content_markdown"],
            selected_document_ids=docs,
            created_at=r["created_at"],
            updated_at=r["updated_at"]
        ))

    return reports

@router.get("/{report_id}", response_model=ReportResponse)
def get_report(report_id: str):
    """Get single report by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM research_reports WHERE id = ?", (report_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Report not found.")

    docs = []
    if row["selected_document_ids_json"]:
        try:
            docs = json.loads(row["selected_document_ids_json"])
        except Exception:
            pass

    return ReportResponse(
        id=row["id"],
        title=row["title"],
        research_question=row["research_question"],
        purpose=row["purpose"],
        content_markdown=row["content_markdown"],
        selected_document_ids=docs,
        created_at=row["created_at"],
        updated_at=row["updated_at"]
    )

@router.put("/{report_id}", response_model=ReportResponse)
def update_report(report_id: str, data: ReportUpdateRequest):
    """Update title or markdown content of an existing report."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM research_reports WHERE id = ?", (report_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Report not found.")

    new_title = data.title if data.title is not None else row["title"]
    new_content = data.content_markdown if data.content_markdown is not None else row["content_markdown"]
    now_iso = get_now_iso()

    cursor.execute(
        "UPDATE research_reports SET title = ?, content_markdown = ?, updated_at = ? WHERE id = ?",
        (new_title, new_content, now_iso, report_id)
    )
    conn.commit()
    conn.close()

    docs = []
    if row["selected_document_ids_json"]:
        try:
            docs = json.loads(row["selected_document_ids_json"])
        except Exception:
            pass

    return ReportResponse(
        id=report_id,
        title=new_title,
        research_question=row["research_question"],
        purpose=row["purpose"],
        content_markdown=new_content,
        selected_document_ids=docs,
        created_at=row["created_at"],
        updated_at=now_iso
    )

@router.delete("/{report_id}")
def delete_report(report_id: str):
    """Delete a saved report."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM research_reports WHERE id = ?", (report_id,))
    conn.commit()
    conn.close()

    return {"message": "Report deleted successfully."}

@router.get("/{report_id}/export")
def export_report(
    report_id: str,
    format: str = Query("markdown", pattern="^(markdown|pdf)$")
):
    """Export a saved report to Markdown or compiled PDF."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM research_reports WHERE id = ?", (report_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Report not found.")

    title = row["title"]
    content = row["content_markdown"]

    if format == "pdf":
        try:
            pdf_path = ReportService.export_to_pdf(report_id, title, content)
            return FileResponse(
                path=str(pdf_path),
                media_type="application/pdf",
                filename=pdf_path.name
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"PDF compilation failed: {str(e)}")
    else:
        md_path = ReportService.export_to_markdown(report_id, title, content)
        return FileResponse(
            path=str(md_path),
            media_type="text/markdown",
            filename=md_path.name
        )
