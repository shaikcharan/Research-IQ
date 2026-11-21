import re
import uuid
from typing import List, Dict, Any
from backend.config import settings

class ChunkingService:
    @staticmethod
    def split_into_sentences(text: str) -> List[str]:
        """Split text into sentences while respecting common abbreviations."""
        # Simple regex-based sentence splitter
        sentence_endings = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9"\'\(\[])')
        sentences = sentence_endings.split(text)
        return [s.strip() for s in sentences if s.strip()]

    @classmethod
    def chunk_document_pages(
        cls,
        document_id: str,
        document_title: str,
        pages: List[Dict[str, Any]],
        chunk_size: int = None,
        chunk_overlap: int = None
    ) -> List[Dict[str, Any]]:
        """
        Produce overlapping chunks per page, preserving exact page numbers and metadata.
        """
        chunk_size = chunk_size or settings.CHUNK_SIZE
        chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP

        all_chunks = []
        global_chunk_idx = 0

        for page in pages:
            page_number = page["page_number"]
            page_text = page["text"]
            if not page_text or len(page_text.strip()) == 0:
                continue

            # First split by paragraphs
            paragraphs = [p.strip() for p in page_text.split("\n\n") if p.strip()]
            current_chunk_sentences = []
            current_chunk_len = 0

            for para in paragraphs:
                sentences = cls.split_into_sentences(para)
                if not sentences:
                    sentences = [para]

                for sentence in sentences:
                    sentence_len = len(sentence)

                    if current_chunk_len + sentence_len > chunk_size and current_chunk_sentences:
                        # Flush current chunk
                        chunk_text = " ".join(current_chunk_sentences).strip()
                        if chunk_text:
                            chunk_id = f"{document_id}_p{page_number}_c{global_chunk_idx}"
                            all_chunks.append({
                                "id": chunk_id,
                                "document_id": document_id,
                                "document_title": document_title,
                                "chunk_index": global_chunk_idx,
                                "page_number": page_number,
                                "text": chunk_text,
                                "metadata_json": {
                                    "char_count": len(chunk_text),
                                    "page": page_number
                                }
                            })
                            global_chunk_idx += 1

                        # Keep overlap from previous sentences
                        overlap_sentences = []
                        overlap_len = 0
                        for s in reversed(current_chunk_sentences):
                            if overlap_len + len(s) <= chunk_overlap:
                                overlap_sentences.insert(0, s)
                                overlap_len += len(s)
                            else:
                                break
                        current_chunk_sentences = overlap_sentences
                        current_chunk_len = overlap_len

                    current_chunk_sentences.append(sentence)
                    current_chunk_len += sentence_len

            # Flush remaining sentences on this page
            if current_chunk_sentences:
                chunk_text = " ".join(current_chunk_sentences).strip()
                if chunk_text:
                    chunk_id = f"{document_id}_p{page_number}_c{global_chunk_idx}"
                    all_chunks.append({
                        "id": chunk_id,
                        "document_id": document_id,
                        "document_title": document_title,
                        "chunk_index": global_chunk_idx,
                        "page_number": page_number,
                        "text": chunk_text,
                        "metadata_json": {
                            "char_count": len(chunk_text),
                            "page": page_number
                        }
                    })
                    global_chunk_idx += 1

        return all_chunks
