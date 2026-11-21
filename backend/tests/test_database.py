import pytest
import sqlite3
from backend.database import get_db_connection, init_db

def test_database_initialization():
    """Verify all tables, FTS5 virtual tables, and indexes exist in SQLite."""
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r["name"] for r in cursor.fetchall()]

    expected_tables = [
        "documents",
        "document_chunks",
        "document_chunks_fts",
        "research_sessions",
        "chat_messages",
        "research_reports"
    ]

    for table in expected_tables:
        assert table in tables, f"Table '{table}' was not created during init_db."

    # Verify foreign key cascade enforcement
    cursor.execute("PRAGMA foreign_keys")
    fk_status = cursor.fetchone()[0]
    assert fk_status == 1, "SQLite foreign keys must be enabled (PRAGMA foreign_keys = ON)."

    conn.close()
