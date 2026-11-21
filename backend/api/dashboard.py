from fastapi import APIRouter
from backend.database import get_db_connection
from backend.models import DashboardStatsResponse, DocumentResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats():
    """Retrieve actual aggregate metrics from SQLite database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Documents counts
    cursor.execute("SELECT COUNT(*) FROM documents")
    total_docs = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM documents WHERE processing_status = 'Ready'")
    indexed_docs = cursor.fetchone()[0]

    # Sessions count
    cursor.execute("SELECT COUNT(*) FROM research_sessions")
    total_sessions = cursor.fetchone()[0]

    # Reports count
    cursor.execute("SELECT COUNT(*) FROM research_reports")
    total_reports = cursor.fetchone()[0]

    # Chunks count
    cursor.execute("SELECT COUNT(*) FROM document_chunks")
    total_chunks = cursor.fetchone()[0]

    # Recent documents
    cursor.execute("""
        SELECT id, filename, title, file_size, page_count, processing_status, processing_error, created_at, updated_at
        FROM documents
        ORDER BY created_at DESC
        LIMIT 5
    """)
    doc_rows = cursor.fetchall()
    recent_docs = [
        DocumentResponse(
            id=r["id"],
            filename=r["filename"],
            title=r["title"],
            file_size=r["file_size"],
            page_count=r["page_count"],
            processing_status=r["processing_status"],
            processing_error=r["processing_error"],
            created_at=r["created_at"],
            updated_at=r["updated_at"]
        ) for r in doc_rows
    ]

    # Recent sessions with message counts
    cursor.execute("""
        SELECT s.id, s.title, s.created_at, s.updated_at, COUNT(m.id) as message_count
        FROM research_sessions s
        LEFT JOIN chat_messages m ON s.id = m.session_id
        GROUP BY s.id
        ORDER BY s.updated_at DESC
        LIMIT 5
    """)
    session_rows = cursor.fetchall()
    recent_sessions = [
        {
            "id": r["id"],
            "title": r["title"],
            "created_at": r["created_at"],
            "updated_at": r["updated_at"],
            "message_count": r["message_count"]
        } for r in session_rows
    ]

    conn.close()

    return DashboardStatsResponse(
        total_documents=total_docs,
        indexed_documents=indexed_docs,
        total_sessions=total_sessions,
        total_reports=total_reports,
        total_chunks=total_chunks,
        recent_documents=recent_docs,
        recent_sessions=recent_sessions
    )
