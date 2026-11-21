import sqlite3
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Generator, Optional, List, Dict, Any
from backend.config import settings

def get_now_iso() -> str:
    """Return current UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()

def get_db_connection() -> sqlite3.Connection:
    """Create and return a configured SQLite connection with foreign keys and row factory."""
    conn = sqlite3.connect(settings.DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables, FTS5 virtual tables, indexes, and triggers."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Documents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            title TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_hash TEXT UNIQUE NOT NULL,
            file_size INTEGER NOT NULL,
            page_count INTEGER NOT NULL DEFAULT 0,
            processing_status TEXT NOT NULL DEFAULT 'Uploaded',
            processing_error TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
    """)

    # Document chunks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS document_chunks (
            id TEXT PRIMARY KEY,
            document_id TEXT NOT NULL,
            chunk_index INTEGER NOT NULL,
            page_number INTEGER NOT NULL,
            text TEXT NOT NULL,
            metadata_json TEXT,
            FOREIGN KEY (document_id) REFERENCES documents (id) ON DELETE CASCADE
        );
    """)

    # Indexes on document_chunks
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_chunks_document_id ON document_chunks (document_id);
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_chunks_page_number ON document_chunks (page_number);
    """)

    # SQLite FTS5 for Keyword Search
    try:
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS document_chunks_fts USING fts5(
                chunk_id UNINDEXED,
                document_id UNINDEXED,
                page_number UNINDEXED,
                text,
                tokenize = 'porter unicode61'
            );
        """)
    except sqlite3.OperationalError:
        # Fallback if porter stemmer fails on any platform
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS document_chunks_fts USING fts5(
                chunk_id UNINDEXED,
                document_id UNINDEXED,
                page_number UNINDEXED,
                text
            );
        """)

    # Research Sessions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS research_sessions (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
    """)

    # Chat Messages
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            citations_json TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (session_id) REFERENCES research_sessions (id) ON DELETE CASCADE
        );
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_chat_session ON chat_messages (session_id);
    """)

    # Research Reports
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS research_reports (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            research_question TEXT NOT NULL,
            purpose TEXT NOT NULL DEFAULT 'Executive Decision Making',
            content_markdown TEXT NOT NULL,
            selected_document_ids_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
    """)

    conn.commit()
    conn.close()

# Auto-initialize on import
init_db()
