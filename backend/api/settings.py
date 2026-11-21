import httpx
from fastapi import APIRouter, HTTPException

from backend.config import settings
from backend.database import get_db_connection
from backend.models import (
    SettingsResponse,
    SettingsUpdateRequest,
    TestConnectionResponse
)
from backend.services.retrieval_service import RetrievalService

router = APIRouter(prefix="/settings", tags=["Settings & Configuration"])

@router.get("", response_model=SettingsResponse)
def get_settings():
    """Retrieve system configuration and indexing stats (without exposing raw secrets)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM documents WHERE processing_status = 'Ready'")
    indexed_docs = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM document_chunks")
    total_chunks = cursor.fetchone()[0]
    conn.close()

    return SettingsResponse(
        groq_api_key_configured=bool(settings.GROQ_API_KEY),
        groq_model=settings.GROQ_MODEL,
        app_host=settings.APP_HOST,
        app_port=settings.APP_PORT,
        max_upload_mb=settings.MAX_UPLOAD_MB,
        embedding_model=settings.EMBEDDING_MODEL_NAME,
        total_indexed_documents=indexed_docs,
        total_chunks=total_chunks
    )

@router.post("", response_model=SettingsResponse)
def update_settings(data: SettingsUpdateRequest):
    """Update Groq API key and model in runtime and persist to .env."""
    settings.save_settings(
        groq_api_key=data.groq_api_key,
        groq_model=data.groq_model
    )
    return get_settings()

@router.post("/test-connection", response_model=TestConnectionResponse)
async def test_llm_connection():
    """Verify validity of Groq API key and model availability."""
    if not settings.GROQ_API_KEY:
        return TestConnectionResponse(
            success=False,
            message="No GROQ_API_KEY is configured. Please provide an API key.",
            model=settings.GROQ_MODEL
        )

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": settings.GROQ_MODEL,
        "messages": [{"role": "user", "content": "Respond with 'OK' if connected."}],
        "max_tokens": 10
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload
            )
            if resp.status_code == 200:
                return TestConnectionResponse(
                    success=True,
                    message=f"Connection successful! Groq API verified with model '{settings.GROQ_MODEL}'.",
                    model=settings.GROQ_MODEL
                )
            else:
                err_text = resp.text
                try:
                    err_json = resp.json()
                    if "error" in err_json and "message" in err_json["error"]:
                        err_text = err_json["error"]["message"]
                except Exception:
                    pass
                return TestConnectionResponse(
                    success=False,
                    message=f"Groq API Error ({resp.status_code}): {err_text}",
                    model=settings.GROQ_MODEL
                )
        except Exception as e:
            return TestConnectionResponse(
                success=False,
                message=f"Connection failed: {str(e)}",
                model=settings.GROQ_MODEL
            )

@router.post("/rebuild-index")
def rebuild_vector_index():
    """Trigger a full rebuild of FAISS index and FTS5 table from database chunks."""
    try:
        RetrievalService.rebuild_index_from_db()
        return {"message": "Vector index and FTS5 keyword table successfully rebuilt."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Index rebuild failed: {str(e)}")
