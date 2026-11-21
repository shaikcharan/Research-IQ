import json
import re
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
import faiss

from backend.config import settings
from backend.database import get_db_connection
from backend.services.embedding_service import EmbeddingService

INDEX_FILE = settings.INDEXES_DIR / "faiss_index.bin"
MAPPING_FILE = settings.INDEXES_DIR / "chunk_id_map.json"

class RetrievalService:
    _index: Optional[faiss.Index] = None
    _chunk_ids: List[str] = []

    @classmethod
    def load_index(cls):
        """Load FAISS index and chunk ID mapping from disk, or initialize empty."""
        if INDEX_FILE.exists() and MAPPING_FILE.exists():
            try:
                cls._index = faiss.read_index(str(INDEX_FILE))
                with open(MAPPING_FILE, "r", encoding="utf-8") as f:
                    cls._chunk_ids = json.load(f)
                return
            except Exception as e:
                print(f"[Warning] Failed to load FAISS index: {e}. Reinitializing.")
        
        # Initialize fresh index
        cls._index = faiss.IndexFlatIP(settings.EMBEDDING_DIM)
        cls._chunk_ids = []

    @classmethod
    def save_index(cls):
        """Save FAISS index and chunk ID mapping to disk."""
        if cls._index is not None:
            faiss.write_index(cls._index, str(INDEX_FILE))
            with open(MAPPING_FILE, "w", encoding="utf-8") as f:
                json.dump(cls._chunk_ids, f)

    @classmethod
    def index_chunks(cls, chunks: List[Dict[str, Any]]):
        """
        Embed chunks and add them to FAISS index, and insert into FTS5.
        """
        if not chunks:
            return

        if cls._index is None:
            cls.load_index()

        texts = [c["text"] for c in chunks]
        embeddings = EmbeddingService.generate_embeddings(texts)

        cls._index.add(embeddings)
        new_ids = [c["id"] for c in chunks]
        cls._chunk_ids.extend(new_ids)
        cls.save_index()

        # Add to FTS5 table
        conn = get_db_connection()
        cursor = conn.cursor()
        for c in chunks:
            try:
                cursor.execute(
                    """
                    INSERT INTO document_chunks_fts (chunk_id, document_id, page_number, text)
                    VALUES (?, ?, ?, ?)
                    """,
                    (c["id"], c["document_id"], c["page_number"], c["text"])
                )
            except Exception as e:
                print(f"[Warning] Failed to index chunk in FTS5: {e}")
        conn.commit()
        conn.close()

    @classmethod
    def rebuild_index_from_db(cls):
        """
        Safely rebuild entire FAISS index and FTS5 table from SQLite database.
        Use when a document is deleted or index is corrupted.
        """
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch all chunks
        cursor.execute("SELECT id, document_id, page_number, text FROM document_chunks ORDER BY id ASC")
        rows = cursor.fetchall()

        # Reset FTS5
        cursor.execute("DELETE FROM document_chunks_fts")
        for r in rows:
            cursor.execute(
                """
                INSERT INTO document_chunks_fts (chunk_id, document_id, page_number, text)
                VALUES (?, ?, ?, ?)
                """,
                (r["id"], r["document_id"], r["page_number"], r["text"])
            )
        conn.commit()
        conn.close()

        # Reset FAISS
        cls._index = faiss.IndexFlatIP(settings.EMBEDDING_DIM)
        cls._chunk_ids = []

        if rows:
            chunk_dicts = [{"id": r["id"], "text": r["text"]} for r in rows]
            texts = [c["text"] for c in chunk_dicts]
            embeddings = EmbeddingService.generate_embeddings(texts)
            cls._index.add(embeddings)
            cls._chunk_ids = [c["id"] for c in chunk_dicts]

        cls.save_index()

    @classmethod
    def search_semantic(
        cls,
        query: str,
        selected_doc_ids: Optional[List[str]] = None,
        top_k: int = 15
    ) -> List[Dict[str, Any]]:
        """
        Search FAISS index with cosine similarity. Filter to selected_doc_ids.
        """
        if cls._index is None:
            cls.load_index()

        if cls._index.ntotal == 0 or not cls._chunk_ids:
            return []

        query_vec = EmbeddingService.embed_query(query).reshape(1, -1)
        
        # Search more candidates in case filtering removes many
        k_search = min(max(top_k * 4, 30), cls._index.ntotal)
        scores, indices = cls._index.search(query_vec, k_search)

        selected_set = set(selected_doc_ids) if selected_doc_ids else None

        # Look up chunk details from DB
        conn = get_db_connection()
        cursor = conn.cursor()

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(cls._chunk_ids):
                continue
            chunk_id = cls._chunk_ids[idx]
            
            cursor.execute(
                """
                SELECT c.id, c.document_id, c.page_number, c.text, d.title as document_title
                FROM document_chunks c
                JOIN documents d ON c.document_id = d.id
                WHERE c.id = ?
                """,
                (chunk_id,)
            )
            row = cursor.fetchone()
            if not row:
                continue

            doc_id = row["document_id"]
            if selected_set and doc_id not in selected_set:
                continue

            results.append({
                "chunk_id": row["id"],
                "document_id": doc_id,
                "document_title": row["document_title"],
                "page_number": row["page_number"],
                "text": row["text"],
                "score": float(score)
            })

            if len(results) >= top_k:
                break

        conn.close()
        return results

    @classmethod
    def search_keyword(
        cls,
        query: str,
        selected_doc_ids: Optional[List[str]] = None,
        top_k: int = 15
    ) -> List[Dict[str, Any]]:
        """
        Search SQLite FTS5 for keyword matches.
        """
        # Sanitize query for FTS5
        clean_terms = re.findall(r'\b[a-zA-Z0-9_\-]{2,}\b', query)
        if not clean_terms:
            return []

        # Join terms with OR or NEAR
        fts_query = " OR ".join(f'"{term}"' for term in clean_terms[:8])

        conn = get_db_connection()
        cursor = conn.cursor()

        doc_filter_sql = ""
        params = [fts_query]

        if selected_doc_ids:
            placeholders = ",".join(["?"] * len(selected_doc_ids))
            doc_filter_sql = f"AND c.document_id IN ({placeholders})"
            params.extend(selected_doc_ids)

        params.append(top_k)

        query_sql = f"""
            SELECT c.id, c.document_id, c.page_number, c.text, d.title as document_title,
                   bm25(document_chunks_fts) as bm25_score
            FROM document_chunks_fts fts
            JOIN document_chunks c ON fts.chunk_id = c.id
            JOIN documents d ON c.document_id = d.id
            WHERE document_chunks_fts MATCH ? {doc_filter_sql}
            ORDER BY bm25_score ASC
            LIMIT ?
        """

        try:
            cursor.execute(query_sql, params)
            rows = cursor.fetchall()
        except sqlite3.OperationalError:
            # Fallback if FTS5 match fails
            conn.close()
            return []

        results = []
        for row in rows:
            results.append({
                "chunk_id": row["id"],
                "document_id": row["document_id"],
                "document_title": row["document_title"],
                "page_number": row["page_number"],
                "text": row["text"],
                # bm25 is lower is better (negative), invert or scale
                "score": float(abs(row["bm25_score"]))
            })

        conn.close()
        return results

    @classmethod
    def search_hybrid(
        cls,
        query: str,
        selected_doc_ids: Optional[List[str]] = None,
        top_k: int = None
    ) -> List[Dict[str, Any]]:
        """
        Reciprocal Rank Fusion (RRF) combining semantic search and keyword search.
        Score = sum(1 / (k + rank))
        """
        top_k = top_k or settings.DEFAULT_TOP_K
        k = settings.RRF_K

        dense_results = cls.search_semantic(query, selected_doc_ids, top_k=top_k * 3)
        sparse_results = cls.search_keyword(query, selected_doc_ids, top_k=top_k * 3)

        chunk_pool: Dict[str, Dict[str, Any]] = {}
        rrf_scores: Dict[str, float] = {}

        # Process dense rankings
        for rank, item in enumerate(dense_results):
            cid = item["chunk_id"]
            chunk_pool[cid] = item
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (k + rank + 1))

        # Process sparse rankings
        for rank, item in enumerate(sparse_results):
            cid = item["chunk_id"]
            if cid not in chunk_pool:
                chunk_pool[cid] = item
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (k + rank + 1))

        # Sort by RRF score descending
        sorted_cids = sorted(rrf_scores.keys(), key=lambda cid: rrf_scores[cid], reverse=True)

        final_results = []
        for rank_idx, cid in enumerate(sorted_cids[:top_k]):
            item = chunk_pool[cid].copy()
            item["score"] = round(rrf_scores[cid], 5)
            item["rank"] = rank_idx + 1
            final_results.append(item)

        return final_results
