import uuid
import json
from typing import List
from fastapi import APIRouter, HTTPException

from backend.database import get_db_connection, get_now_iso
from backend.models import (
    ResearchSessionCreate,
    ResearchSessionResponse,
    ChatMessageCreate,
    ChatMessageResponse,
    CitationItem
)
from backend.services.rag_service import RAGService

router = APIRouter(prefix="/research", tags=["Research Workspace"])

@router.post("/sessions", response_model=ResearchSessionResponse)
def create_session(data: ResearchSessionCreate):
    """Create a new research workspace session."""
    conn = get_db_connection()
    cursor = conn.cursor()

    session_id = str(uuid.uuid4())
    now_iso = get_now_iso()
    title = data.title or "New Research Session"

    cursor.execute(
        "INSERT INTO research_sessions (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
        (session_id, title, now_iso, now_iso)
    )
    conn.commit()
    conn.close()

    return ResearchSessionResponse(
        id=session_id,
        title=title,
        created_at=now_iso,
        updated_at=now_iso,
        message_count=0
    )

@router.get("/sessions", response_model=List[ResearchSessionResponse])
def list_sessions():
    """List all research sessions ordered by latest activity."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.id, s.title, s.created_at, s.updated_at, COUNT(m.id) as message_count
        FROM research_sessions s
        LEFT JOIN chat_messages m ON s.id = m.session_id
        GROUP BY s.id
        ORDER BY s.updated_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    return [
        ResearchSessionResponse(
            id=r["id"],
            title=r["title"],
            created_at=r["created_at"],
            updated_at=r["updated_at"],
            message_count=r["message_count"]
        ) for r in rows
    ]

@router.get("/sessions/{session_id}", response_model=ResearchSessionResponse)
def get_session(session_id: str):
    """Get single session metadata."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.id, s.title, s.created_at, s.updated_at, COUNT(m.id) as message_count
        FROM research_sessions s
        LEFT JOIN chat_messages m ON s.id = m.session_id
        WHERE s.id = ?
        GROUP BY s.id
    """, (session_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Research session not found.")

    return ResearchSessionResponse(
        id=row["id"],
        title=row["title"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        message_count=row["message_count"]
    )

@router.delete("/sessions/{session_id}")
def delete_session(session_id: str):
    """Delete a research session and all chat messages."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM research_sessions WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()

    return {"message": "Session successfully deleted."}

@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessageResponse])
def get_session_messages(session_id: str):
    """Retrieve full chat history for a session."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, session_id, role, content, citations_json, created_at
        FROM chat_messages
        WHERE session_id = ?
        ORDER BY created_at ASC
    """, (session_id,))
    rows = cursor.fetchall()
    conn.close()

    messages = []
    for r in rows:
        cits = []
        if r["citations_json"]:
            try:
                parsed = json.loads(r["citations_json"])
                cits = [CitationItem(**item) for item in parsed]
            except Exception:
                pass

        messages.append(ChatMessageResponse(
            id=r["id"],
            session_id=r["session_id"],
            role=r["role"],
            content=r["content"],
            citations=cits,
            created_at=r["created_at"]
        ))

    return messages

@router.post("/sessions/{session_id}/chat", response_model=ChatMessageResponse)
async def send_chat_message(session_id: str, data: ChatMessageCreate):
    """
    Process a user research inquiry with hybrid retrieval and evidence-grounded generation.
    """
    if not data.selected_document_ids:
        raise HTTPException(
            status_code=400,
            detail="Please select at least one document from the Sources panel to conduct research."
        )

    user_query = data.content.strip()
    if not user_query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Verify session exists
    cursor.execute("SELECT id, title FROM research_sessions WHERE id = ?", (session_id,))
    session_row = cursor.fetchone()
    if not session_row:
        conn.close()
        raise HTTPException(status_code=404, detail="Research session not found.")

    # 1. Store User Message
    user_msg_id = str(uuid.uuid4())
    user_now = get_now_iso()
    cursor.execute(
        """
        INSERT INTO chat_messages (id, session_id, role, content, citations_json, created_at)
        VALUES (?, ?, 'user', ?, NULL, ?)
        """,
        (user_msg_id, session_id, user_query, user_now)
    )

    # Update session title if first inquiry
    if session_row["title"] == "New Research Session":
        new_title = user_query[:50] + ("..." if len(user_query) > 50 else "")
        cursor.execute("UPDATE research_sessions SET title = ? WHERE id = ?", (new_title, session_id))

    conn.commit()

    # 2. Run Grounded RAG Pipeline
    citations_data = []
    try:
        answer_text, citations_data = await RAGService.generate_grounded_answer(
            query=user_query,
            selected_doc_ids=data.selected_document_ids,
            top_k=6
        )
    except Exception as e:
        error_msg = str(e)
        # Even on LLM failure, retrieve raw evidence chunks for user transparency
        from backend.services.retrieval_service import RetrievalService
        raw_chunks = RetrievalService.search_hybrid(
            query=user_query,
            selected_doc_ids=data.selected_document_ids,
            top_k=5
        )
        citations_data = [
            {
                "chunk_id": c["chunk_id"],
                "document_id": c["document_id"],
                "document_title": c["document_title"],
                "page_number": c["page_number"],
                "excerpt": c["text"],
                "score": c["score"],
                "rank": c.get("rank", 1)
            } for c in raw_chunks
        ]
        answer_text = (
            f"**LLM Generation Notice:**\n\n{error_msg}\n\n"
            f"> *Note: Hybrid retrieval successfully identified {len(citations_data)} relevant source excerpts shown in the Evidence Explorer panel.*"
        )

    # 3. Store Assistant Message
    assistant_msg_id = str(uuid.uuid4())
    assistant_now = get_now_iso()
    cits_json = json.dumps(citations_data)

    cursor.execute(
        """
        INSERT INTO chat_messages (id, session_id, role, content, citations_json, created_at)
        VALUES (?, ?, 'assistant', ?, ?, ?)
        """,
        (assistant_msg_id, session_id, answer_text, cits_json, assistant_now)
    )
    cursor.execute(
        "UPDATE research_sessions SET updated_at = ? WHERE id = ?",
        (assistant_now, session_id)
    )
    conn.commit()
    conn.close()

    return ChatMessageResponse(
        id=assistant_msg_id,
        session_id=session_id,
        role="assistant",
        content=answer_text,
        citations=[CitationItem(**c) for c in citations_data],
        created_at=assistant_now
    )
