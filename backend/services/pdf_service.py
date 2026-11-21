import hashlib
from pathlib import Path
from typing import List, Dict, Any, Tuple
import fitz  # PyMuPDF

class PDFExtractionError(Exception):
    pass

class PDFService:
    @staticmethod
    def compute_sha256(file_path: Path) -> str:
        """Compute SHA-256 hash of a file for duplicate detection."""
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()

    @staticmethod
    def extract_text_and_metadata(file_path: Path) -> Tuple[str, int, List[Dict[str, Any]]]:
        """
        Extract text per page and metadata from PDF using PyMuPDF.
        Returns:
            title (str)
            page_count (int)
            pages (List[Dict[str, Any]]): [{'page_number': 1, 'text': '...'}]
        """
        try:
            doc = fitz.open(file_path)
        except Exception as e:
            raise PDFExtractionError(f"Failed to open PDF document: {str(e)}")

        if doc.is_encrypted:
            try:
                # Try empty password in case of standard view permissions
                if not doc.authenticate(""):
                    raise PDFExtractionError("PDF is password protected and encrypted.")
            except Exception:
                raise PDFExtractionError("PDF is password protected and encrypted.")

        page_count = len(doc)
        if page_count == 0:
            raise PDFExtractionError("The uploaded PDF has 0 pages.")

        raw_title = doc.metadata.get("title") if doc.metadata else ""
        if not raw_title or raw_title.lower() in ["(anonymous)", "untitled", "none", "unknown"]:
            title = file_path.stem.replace("_", " ").replace("-", " ").title()
        else:
            title = raw_title.strip()

        pages = []
        total_extracted_chars = 0

        for i, page in enumerate(doc):
            page_number = i + 1
            text = page.get_text("text").strip()
            total_extracted_chars += len(text)
            pages.append({
                "page_number": page_number,
                "text": text
            })

        doc.close()

        # Check for image-only or scanned PDF without extractable text
        if total_extracted_chars < 50:
            raise PDFExtractionError(
                "Scanned or image-only PDF: no extractable text found. "
                "OCR is not included in the current version."
            )

        return title, page_count, pages
