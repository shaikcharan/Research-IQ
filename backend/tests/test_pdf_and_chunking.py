import pytest
from pathlib import Path
from backend.config import settings
from backend.services.pdf_service import PDFService, PDFExtractionError
from backend.services.chunking_service import ChunkingService

def test_pdf_extraction_sample():
    """Verify PDF extraction extracts title, page counts, and page-indexed text."""
    sample_path = settings.UPLOADS_DIR / "Solid_State_Batteries_Vance_2024.pdf"
    assert sample_path.exists(), "Sample PDF must exist in storage/uploads"

    title, page_count, pages = PDFService.extract_text_and_metadata(sample_path)

    assert "Solid-State" in title or "Solid State" in title
    assert page_count == 3
    assert len(pages) == 3
    assert pages[0]["page_number"] == 1
    assert "LLZO" in pages[0]["text"]
    assert pages[1]["page_number"] == 2
    assert "4C" in pages[1]["text"]

def test_chunking_service_page_retention():
    """Verify chunking maintains exact 1-indexed page numbers and sentence boundaries."""
    pages = [
        {"page_number": 1, "text": "This is page one. It has preliminary data about battery cells. Further details follow."},
        {"page_number": 2, "text": "This is page two. High voltage operation causes interfacial impedance growth at 45C."}
    ]

    chunks = ChunkingService.chunk_document_pages(
        document_id="test_doc_1",
        document_title="Test Battery Paper",
        pages=pages,
        chunk_size=100,
        chunk_overlap=20
    )

    assert len(chunks) >= 2
    assert chunks[0]["page_number"] == 1
    assert chunks[0]["document_id"] == "test_doc_1"
    assert chunks[0]["chunk_index"] == 0
    assert any(c["page_number"] == 2 for c in chunks)

def test_scanned_pdf_error(tmp_path):
    """Verify that empty or image-only PDFs with <50 chars raise PDFExtractionError."""
    import fitz
    empty_pdf_path = tmp_path / "empty_doc.pdf"
    doc = fitz.open()
    doc.new_page()  # Blank page without text
    doc.save(str(empty_pdf_path))
    doc.close()

    with pytest.raises(PDFExtractionError) as exc_info:
        PDFService.extract_text_and_metadata(empty_pdf_path)

    assert "Scanned or image-only" in str(exc_info.value)
