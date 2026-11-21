import os
import uuid
import shutil
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, Query, BackgroundTasks

from backend.config import settings
from backend.database import get_db_connection, get_now_iso
from backend.models import DocumentResponse, DocumentDetailResponse, DocumentChunkModel
from backend.services.pdf_service import PDFService, PDFExtractionError
from backend.services.chunking_service import ChunkingService
from backend.services.retrieval_service import RetrievalService

router = APIRouter(prefix="/documents", tags=["Documents"])

def process_document_pipeline(document_id: str, file_path: Path):
    """Synchronous or background worker for extracting and indexing PDF."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Step 1: Extracting
        cursor.execute(
            "UPDATE documents SET processing_status = 'Extracting', updated_at = ? WHERE id = ?",
            (get_now_iso(), document_id)
        )
        conn.commit()

        title, page_count, pages = PDFService.extract_text_and_metadata(file_path)

        # Update title & page count
        cursor.execute(
            "UPDATE documents SET title = ?, page_count = ?, processing_status = 'Indexing', updated_at = ? WHERE id = ?",
            (title, page_count, get_now_iso(), document_id)
        )
        conn.commit()

        # Step 2: Chunking
        chunks = ChunkingService.chunk_document_pages(
            document_id=document_id,
            document_title=title,
            pages=pages
        )

        if not chunks:
            raise PDFExtractionError("No valid text chunks could be produced from document.")

        # Save chunks in SQLite
        for c in chunks:
            cursor.execute(
                """
                INSERT OR REPLACE INTO document_chunks (id, document_id, chunk_index, page_number, text, metadata_json)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (c["id"], c["document_id"], c["chunk_index"], c["page_number"], c["text"], str(c["metadata_json"]))
            )
        conn.commit()

        # Step 3: Embed and Index
        RetrievalService.index_chunks(chunks)

        # Mark Ready
        cursor.execute(
            "UPDATE documents SET processing_status = 'Ready', processing_error = NULL, updated_at = ? WHERE id = ?",
            (get_now_iso(), document_id)
        )
        conn.commit()

    except Exception as e:
        error_msg = str(e)
        cursor.execute(
            "UPDATE documents SET processing_status = 'Failed', processing_error = ?, updated_at = ? WHERE id = ?",
            (error_msg, get_now_iso(), document_id)
        )
        conn.commit()
    finally:
        conn.close()

@router.get("", response_model=List[DocumentResponse])
def list_documents(
    search: Optional[str] = None,
    status: Optional[str] = None,
    sort_by: str = Query("created_at", pattern="^(created_at|title|file_size|page_count|processing_status)$"),
    order: str = Query("desc", pattern="^(asc|desc)$")
):
    """List all documents with filtering and sorting."""
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM documents WHERE 1=1"
    params = []

    if search:
        query += " AND (title LIKE ? OR filename LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    if status:
        query += " AND processing_status = ?"
        params.append(status)

    query += f" ORDER BY {sort_by} {order.upper()}"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [
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
        ) for r in rows
    ]

@router.post("/upload", response_model=List[DocumentResponse])
async def upload_documents(
    files: List[UploadFile] = File(...),
    background_tasks: BackgroundTasks = None
):
    """Upload one or multiple PDF documents."""
    max_bytes = settings.MAX_UPLOAD_MB * 1024 * 1024
    created_docs = []

    conn = get_db_connection()
    cursor = conn.cursor()

    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file '{file.filename}'. Only PDF files are supported."
            )

        # Read content
        content = await file.read()
        file_size = len(content)

        if file_size > max_bytes:
            raise HTTPException(
                status_code=400,
                detail=f"File '{file.filename}' exceeds maximum allowed size of {settings.MAX_UPLOAD_MB}MB."
            )

        if file_size == 0:
            raise HTTPException(
                status_code=400,
                detail=f"File '{file.filename}' is empty (0 bytes)."
            )

        # Compute SHA256
        import hashlib
        file_hash = hashlib.sha256(content).hexdigest()

        # Check duplicate
        cursor.execute("SELECT id, title, filename FROM documents WHERE file_hash = ?", (file_hash,))
        existing = cursor.fetchone()
        if existing:
            raise HTTPException(
                status_code=409,
                detail=f"Duplicate detected: '{file.filename}' has identical content to existing document '{existing['title']}'."
            )

        doc_id = str(uuid.uuid4())
        safe_filename = f"{doc_id}_{Path(file.filename).name}"
        save_path = settings.UPLOADS_DIR / safe_filename

        with open(save_path, "wb") as f:
            f.write(content)

        now_iso = get_now_iso()
        cursor.execute(
            """
            INSERT INTO documents (id, filename, title, file_path, file_hash, file_size, page_count, processing_status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, 0, 'Uploaded', ?, ?)
            """,
            (doc_id, file.filename, file.filename.replace(".pdf", "").replace("_", " ").title(), str(save_path), file_hash, file_size, now_iso, now_iso)
        )
        conn.commit()

        # Process immediately (local performance is snappy)
        process_document_pipeline(doc_id, save_path)

        cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
        new_row = cursor.fetchone()
        created_docs.append(DocumentResponse(
            id=new_row["id"],
            filename=new_row["filename"],
            title=new_row["title"],
            file_size=new_row["file_size"],
            page_count=new_row["page_count"],
            processing_status=new_row["processing_status"],
            processing_error=new_row["processing_error"],
            created_at=new_row["created_at"],
            updated_at=new_row["updated_at"]
        ))

    conn.close()
    return created_docs

@router.get("/{document_id}", response_model=DocumentDetailResponse)
def get_document(document_id: str):
    """Retrieve detailed document metadata and sample chunks."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM documents WHERE id = ?", (document_id,))
    doc_row = cursor.fetchone()
    if not doc_row:
        conn.close()
        raise HTTPException(status_code=404, detail="Document not found.")

    cursor.execute("SELECT COUNT(*) FROM document_chunks WHERE document_id = ?", (document_id,))
    chunks_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT id, document_id, chunk_index, page_number, text FROM document_chunks WHERE document_id = ? ORDER BY chunk_index ASC LIMIT 5",
        (document_id,)
    )
    sample_rows = cursor.fetchall()
    conn.close()

    sample_chunks = [
        DocumentChunkModel(
            id=r["id"],
            document_id=r["document_id"],
            chunk_index=r["chunk_index"],
            page_number=r["page_number"],
            text=r["text"]
        ) for r in sample_rows
    ]

    return DocumentDetailResponse(
        id=doc_row["id"],
        filename=doc_row["filename"],
        title=doc_row["title"],
        file_size=doc_row["file_size"],
        page_count=doc_row["page_count"],
        processing_status=doc_row["processing_status"],
        processing_error=doc_row["processing_error"],
        created_at=doc_row["created_at"],
        updated_at=doc_row["updated_at"],
        chunks_count=chunks_count,
        sample_chunks=sample_chunks
    )

@router.delete("/{document_id}")
def delete_document(document_id: str):
    """Delete a document, its database chunks, vector index entries, and local file."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT file_path FROM documents WHERE id = ?", (document_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Document not found.")

    file_path = Path(row["file_path"])
    if file_path.exists():
        try:
            file_path.unlink()
        except Exception:
            pass

    # Delete document record (foreign keys cascade to document_chunks)
    cursor.execute("DELETE FROM documents WHERE id = ?", (document_id,))
    conn.commit()
    conn.close()

    # Rebuild FAISS index from remaining chunks in DB
    RetrievalService.rebuild_index_from_db()

    return {"message": "Document and associated vectors successfully removed."}

@router.post("/{document_id}/reprocess", response_model=DocumentResponse)
def reprocess_document(document_id: str):
    """Retry extraction and re-indexing of a failed or existing document."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM documents WHERE id = ?", (document_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Document not found.")

    file_path = Path(row["file_path"])
    if not file_path.exists():
        conn.close()
        raise HTTPException(status_code=400, detail="Original PDF file is missing from storage.")

    # Remove existing chunks for this doc first
    cursor.execute("DELETE FROM document_chunks WHERE document_id = ?", (document_id,))
    cursor.execute("DELETE FROM document_chunks_fts WHERE document_id = ?", (document_id,))
    conn.commit()
    conn.close()

    process_document_pipeline(document_id, file_path)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documents WHERE id = ?", (document_id,))
    updated_row = cursor.fetchone()
    conn.close()

    return DocumentResponse(
        id=updated_row["id"],
        filename=updated_row["filename"],
        title=updated_row["title"],
        file_size=updated_row["file_size"],
        page_count=updated_row["page_count"],
        processing_status=updated_row["processing_status"],
        processing_error=updated_row["processing_error"],
        created_at=updated_row["created_at"],
        updated_at=updated_row["updated_at"]
    )

@router.post("/seed-samples", response_model=List[DocumentResponse])
def seed_sample_documents():
    """Convenience endpoint: seed and index the 3 sample academic papers."""
    sample_files = [
        "Solid_State_Batteries_Vance_2024.pdf",
        "Automotive_Cell_Degradation_Chen_2023.pdf",
        "Grid_EV_Integration_Jenkins_2024.pdf"
    ]

    indexed_docs = []
    conn = get_db_connection()
    cursor = conn.cursor()

    for filename in sample_files:
        file_path = settings.UPLOADS_DIR / filename
        if not file_path.exists():
            continue

        with open(file_path, "rb") as f:
            content = f.read()

        import hashlib
        file_hash = hashlib.sha256(content).hexdigest()

        cursor.execute("SELECT id FROM documents WHERE file_hash = ?", (file_hash,))
        existing = cursor.fetchone()
        if existing:
            # Already seeded
            cursor.execute("SELECT * FROM documents WHERE id = ?", (existing["id"],))
            r = cursor.fetchone()
            indexed_docs.append(DocumentResponse(
                id=r["id"],
                filename=r["filename"],
                title=r["title"],
                file_size=r["file_size"],
                page_count=r["page_count"],
                processing_status=r["processing_status"],
                processing_error=r["processing_error"],
                created_at=r["created_at"],
                updated_at=r["updated_at"]
            ))
            continue

        doc_id = str(uuid.uuid4())
        now_iso = get_now_iso()
        cursor.execute(
            """
            INSERT INTO documents (id, filename, title, file_path, file_hash, file_size, page_count, processing_status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, 0, 'Uploaded', ?, ?)
            """,
            (doc_id, filename, filename.replace(".pdf", "").replace("_", " ").title(), str(file_path), file_hash, len(content), now_iso, now_iso)
        )
        conn.commit()

        process_document_pipeline(doc_id, file_path)

        cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
        r = cursor.fetchone()
        indexed_docs.append(DocumentResponse(
            id=r["id"],
            filename=r["filename"],
            title=r["title"],
            file_size=r["file_size"],
            page_count=r["page_count"],
            processing_status=r["processing_status"],
            processing_error=r["processing_error"],
            created_at=r["created_at"],
            updated_at=r["updated_at"]
        ))

    conn.close()
    return indexed_docs
