import json
import re
from typing import List, Dict, Any
from backend.config import settings
from backend.database import get_db_connection
from backend.services.retrieval_service import RetrievalService
from backend.services.rag_service import RAGService

COMPARISON_PROMPT = """You are ResearchIQ's Comparative Analysis Engine.
You are comparing evidence from multiple scientific or technical documents regarding a specific research inquiry.

Documents to compare:
{document_list_str}

Retrieved evidence per document:
{evidence_per_doc_str}

Task:
Analyze the retrieved excerpts across the documents for the inquiry: "{question}".
Extract specific factual topics or claims, compare what each document states, and determine their relationship.
Relationships must be strictly one of:
- "Agreement": Both documents reach the same finding or support identical conclusions.
- "Difference": The documents discuss different aspects, scopes, methodologies, or conditions without direct mutual exclusion.
- "Potential Contradiction": The documents make mutually incompatible or directly conflicting factual claims under similar conditions.
- "Insufficient Evidence": One or more documents lack sufficient data on this specific sub-claim.

You must return valid JSON ONLY, with NO extra commentary or markdown fencing around the JSON.
Format:
{{
  "summary": "Executive overview of comparison findings and major discrepancies.",
  "comparisons": [
    {{
      "topic": "Specific metric or claim topic (e.g., Battery Cycle Life at 4C)",
      "document_a_evidence": "Exact claim and metric from Document A (cite page)",
      "document_b_evidence": "Exact claim and metric from Document B (cite page)",
      "relationship": "Agreement" | "Difference" | "Potential Contradiction" | "Insufficient Evidence",
      "explanation": "Detailed rationale explaining why this is an agreement, methodology difference, or contradiction.",
      "human_review_recommended": false
    }}
  ]
}}
"""

class ComparisonService:
    @classmethod
    async def compare_documents(
        cls,
        document_ids: List[str],
        question: str
    ) -> Dict[str, Any]:
        """
        Perform multi-document comparison and contradiction detection.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Fetch document titles
        placeholders = ",".join(["?"] * len(document_ids))
        cursor.execute(f"SELECT id, title, filename FROM documents WHERE id IN ({placeholders})", document_ids)
        doc_rows = cursor.fetchall()
        conn.close()

        docs_map = {r["id"]: {"title": r["title"], "filename": r["filename"]} for r in doc_rows}

        if len(document_ids) < 2:
            raise ValueError("Document comparison requires at least 2 documents.")

        # Step 1: Retrieve evidence separately per document
        evidence_per_doc = {}
        all_citations = []

        for doc_id in document_ids:
            chunks = RetrievalService.search_hybrid(
                query=question,
                selected_doc_ids=[doc_id],
                top_k=4
            )
            doc_title = docs_map.get(doc_id, {}).get("title", f"Doc {doc_id}")
            evidence_per_doc[doc_id] = {
                "title": doc_title,
                "chunks": chunks
            }
            for c in chunks:
                all_citations.append({
                    "chunk_id": c["chunk_id"],
                    "document_id": doc_id,
                    "document_title": doc_title,
                    "page_number": c["page_number"],
                    "excerpt": c["text"],
                    "score": c["score"]
                })

        # Step 2: Build LLM prompt
        doc_list_str = "\n".join([f"- {info['title']} (ID: {doc_id})" for doc_id, info in evidence_per_doc.items()])
        
        evidence_blocks = []
        for doc_id, info in evidence_per_doc.items():
            chunks_text = "\n".join([
                f"  [p. {c['page_number']}]: {c['text']}"
                for c in info["chunks"]
            ])
            evidence_blocks.append(f"DOCUMENT: \"{info['title']}\"\n{chunks_text if chunks_text else '  (No direct matches found)'}")

        evidence_per_doc_str = "\n\n".join(evidence_blocks)

        prompt = COMPARISON_PROMPT.format(
            document_list_str=doc_list_str,
            evidence_per_doc_str=evidence_per_doc_str,
            question=question
        )

        messages = [
            {"role": "system", "content": "You are a specialized scientific contradiction analysis system. Output valid JSON only."},
            {"role": "user", "content": prompt}
        ]

        if not settings.GROQ_API_KEY:
            # Fallback heuristic if no API key is configured
            return cls._heuristic_comparison(docs_map, evidence_per_doc, question, all_citations)

        # Call LLM
        response_text = await RAGService.query_llm(messages, temperature=0.1)

        # Parse JSON
        try:
            # Strip markdown json blocks if returned
            clean_json = re.sub(r'^```json\s*', '', response_text.strip())
            clean_json = re.sub(r'\s*```$', '', clean_json)
            parsed = json.loads(clean_json)
            
            comparisons = parsed.get("comparisons", [])
            # Attach citations to each item
            for comp in comparisons:
                comp["citations"] = all_citations[:6]
                
            return {
                "question": question,
                "documents_compared": [{"id": k, "title": v["title"]} for k, v in docs_map.items()],
                "comparisons": comparisons,
                "summary": parsed.get("summary", "Comparative analysis completed across selected documents.")
            }
        except Exception:
            # If JSON parsing failed, build fallback from raw response
            return {
                "question": question,
                "documents_compared": [{"id": k, "title": v["title"]} for k, v in docs_map.items()],
                "comparisons": [
                    {
                        "topic": "Synthesis Findings",
                        "document_a_evidence": response_text[:300] + "...",
                        "document_b_evidence": "Refer to attached citations for full cross-document excerpts.",
                        "relationship": "Difference",
                        "citations": all_citations[:4],
                        "explanation": "Comparative synthesis generated from multi-document evidence.",
                        "human_review_recommended": True
                    }
                ],
                "summary": response_text[:500]
            }

    @staticmethod
    def _heuristic_comparison(
        docs_map: Dict[str, Any],
        evidence_per_doc: Dict[str, Any],
        question: str,
        all_citations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Provides heuristic evidence comparison when LLM key is not configured."""
        doc_ids = list(evidence_per_doc.keys())
        doc_a_id = doc_ids[0]
        doc_b_id = doc_ids[1] if len(doc_ids) > 1 else doc_ids[0]

        doc_a_chunks = evidence_per_doc[doc_a_id]["chunks"]
        doc_b_chunks = evidence_per_doc[doc_b_id]["chunks"]

        ev_a = doc_a_chunks[0]["text"] if doc_a_chunks else "No direct evidence retrieved."
        ev_b = doc_b_chunks[0]["text"] if doc_b_chunks else "No direct evidence retrieved."

        return {
            "question": question,
            "documents_compared": [{"id": k, "title": v["title"]} for k, v in docs_map.items()],
            "comparisons": [
                {
                    "topic": "Retrieved Document Evidence",
                    "document_a_evidence": f"[{docs_map[doc_a_id]['title']}]: {ev_a}",
                    "document_b_evidence": f"[{docs_map[doc_b_id]['title']}]: {ev_b}",
                    "relationship": "Difference",
                    "citations": all_citations[:4],
                    "explanation": "Extracted evidence from both documents is available for manual comparison. Add your Groq API key in Settings for automated contradiction extraction.",
                    "human_review_recommended": True
                }
            ],
            "summary": "Retrieved evidence across selected documents. Configure Groq API key in Settings for automated contradiction classification."
        }
