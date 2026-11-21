import httpx
import json
from typing import List, Dict, Any, Tuple
from backend.config import settings
from backend.services.retrieval_service import RetrievalService

SYSTEM_PROMPT = """You are ResearchIQ, an advanced multi-document research assistant. 
Your goal is to provide accurate, strictly evidence-grounded research answers based ONLY on the provided source excerpts.

Rules:
1. Cite the source document and page number for each factual claim using brackets: [Document Title, p. X].
2. Distinguish concrete factual evidence from interpretations and uncertainty.
3. If the provided excerpts do not contain sufficient evidence to answer the question, state explicitly: "Based on the selected documents, there is insufficient evidence to answer this question."
4. Do NOT invent statistics, metrics, quotations, citations, or external claims.
5. If sources contradict or present differing viewpoints, explicitly highlight the disagreement, cite both documents and page numbers, and contrast their claims.
6. Provide a structured response:
   - ### Direct Summary
   - ### Key Evidence & Findings (with [Title, p. X] citations)
   - ### Agreements & Disagreements (if applicable)
   - ### Research Limitations / Missing Information
"""

class RAGService:
    @staticmethod
    async def query_llm(messages: List[Dict[str, str]], temperature: float = 0.2) -> str:
        """
        Send chat completion request to Groq API.
        """
        if not settings.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is not configured. Please configure your free Groq API key "
                "in Settings to enable AI synthesis."
            )

        headers = {
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": settings.GROQ_MODEL,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 2048,
        }

        async with httpx.AsyncClient(timeout=45.0) as client:
            try:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
            except httpx.RequestError as exc:
                raise RuntimeError(f"Network error while connecting to Groq API: {exc}")

            if response.status_code != 200:
                error_detail = response.text
                try:
                    err_json = response.json()
                    if "error" in err_json and "message" in err_json["error"]:
                        error_detail = err_json["error"]["message"]
                except Exception:
                    pass
                raise RuntimeError(f"Groq API Error ({response.status_code}): {error_detail}")

            data = response.json()
            return data["choices"][0]["message"]["content"]

    @classmethod
    async def generate_grounded_answer(
        cls,
        query: str,
        selected_doc_ids: List[str],
        top_k: int = 6
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Execute Hybrid Retrieval, build grounded context, and call LLM.
        Returns: (answer_text, citations_list)
        """
        # Step 1: Hybrid Retrieval
        retrieved_chunks = RetrievalService.search_hybrid(
            query=query,
            selected_doc_ids=selected_doc_ids,
            top_k=top_k
        )

        citations = []
        for chunk in retrieved_chunks:
            citations.append({
                "chunk_id": chunk["chunk_id"],
                "document_id": chunk["document_id"],
                "document_title": chunk["document_title"],
                "page_number": chunk["page_number"],
                "excerpt": chunk["text"],
                "score": chunk["score"],
                "rank": chunk.get("rank", 1)
            })

        # Step 2: Evidence Sufficiency Check
        if not retrieved_chunks:
            return (
                "**Insufficient Evidence Found**\n\n"
                "No matching evidence could be retrieved from the selected documents for your query. "
                "Please verify that the relevant documents are selected in the left panel, or try rephrasing your search terms.",
                []
            )

        # Step 3: Format Context for LLM
        context_blocks = []
        for i, c in enumerate(retrieved_chunks, 1):
            block = (
                f"[Source {i}]: Document: \"{c['document_title']}\" | Page: {c['page_number']}\n"
                f"Content: {c['text']}"
            )
            context_blocks.append(block)

        context_str = "\n\n---\n\n".join(context_blocks)

        user_content = (
            f"RESEARCH INQUIRY:\n{query}\n\n"
            f"RETRIEVED SOURCE EXCERPTS:\n{context_str}\n\n"
            f"Synthesize a rigorous, evidence-grounded research answer adhering strictly to the system instructions."
        )

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ]

        # Step 4: Call LLM
        answer = await cls.query_llm(messages)
        return answer, citations
