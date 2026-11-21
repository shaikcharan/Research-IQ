import pytest
import numpy as np
from backend.services.embedding_service import EmbeddingService
from backend.services.retrieval_service import RetrievalService
from backend.database import get_db_connection

def test_embedding_generation_and_normalization():
    """Verify Sentence Transformers produces 384-dim unit-normalized vectors."""
    texts = [
        "Solid-state battery cells offer superior thermal stability.",
        "Rapid charging causes mechanical fatigue at electrode interfaces."
    ]
    embs = EmbeddingService.generate_embeddings(texts)

    assert embs.shape == (2, 384)
    # Check L2 unit length
    for vec in embs:
        norm = np.linalg.norm(vec)
        assert abs(norm - 1.0) < 1e-4

def test_hybrid_retrieval_and_document_isolation():
    """Verify hybrid search respects selected_document_ids filter and uses RRF."""
    # Ensure sample docs are indexed
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM documents WHERE processing_status = 'Ready'")
    docs = cursor.fetchall()
    conn.close()

    if len(docs) < 2:
        pytest.skip("Requires at least two indexed documents to test isolation.")

    target_doc_id = docs[0]["id"]
    other_doc_id = docs[1]["id"]

    # Search with only target_doc_id selected
    results = RetrievalService.search_hybrid(
        query="battery charging degradation",
        selected_doc_ids=[target_doc_id],
        top_k=5
    )

    for item in results:
        assert item["document_id"] == target_doc_id, "Retrieved chunk must strictly belong to selected_doc_ids"
        assert item["document_id"] != other_doc_id
        assert item["score"] > 0
        assert "rank" in item
