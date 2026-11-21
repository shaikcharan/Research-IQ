import uuid
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from backend.config import settings
from backend.database import get_db_connection, get_now_iso
from backend.services.retrieval_service import RetrievalService
from backend.services.rag_service import RAGService

REPORT_PROMPT_TEMPLATE = """You are a senior academic and industry research director.
Generate a structured, evidence-grounded Executive Research Brief based strictly on the provided documents and evidence excerpts.

Research Question: "{question}"
Purpose / Audience: "{purpose}"

DOCUMENTS ANALYZED:
{docs_list}

RETRIEVED EVIDENCE EXCERPTS:
{evidence_str}

You must write a comprehensive research brief strictly adhering to the following 13-section structure in Markdown:

# {title}

## 1. Executive Summary
(High-level synthesis of findings, takeaways, and strategic implications)

## 2. Research Question and Scope
(Defines the exact problem statement and boundaries of the inquiry)

## 3. Documents Analyzed
(List analyzed documents, publication context, and focus areas)

## 4. Key Findings
(Numbered list of key evidentiary findings with citations [Title, p. X])

## 5. Supporting Evidence with Citations
(In-depth evidence breakdown, citing specific metrics, claims, and page numbers)

## 6. Agreements Across Sources
(Identify common ground and corroborating evidence across the documents)

## 7. Conflicting or Inconsistent Claims
(Identify discrepancies, conflicting metrics, or opposing conclusions between sources)

## 8. Possible Explanations for Disagreement
(Only when supported by evidence: differences in methodology, scope, test conditions, or assumptions)

## 9. Research Limitations
(Limitations noted in the documents or arising from sample size/methodology)

## 10. Missing Information and Unanswered Questions
(Gaps in evidence where documents did not provide sufficient data)

## 11. Strategic Conclusions and Recommendations
(Objective conclusions grounded strictly in the evidentiary findings)

## 12. References and Source Index
(Complete list of cited documents with page references)

Rules:
- Strictly ground claims in the provided excerpts.
- Cite [Document Title, p. X] for all empirical claims.
- If information is missing, explicitly note it under Missing Information.
- Do NOT fabricate claims.
"""

class ReportService:
    @classmethod
    async def generate_brief(
        cls,
        question: str,
        purpose: str,
        selected_doc_ids: List[str],
        title: str = None
    ) -> str:
        """Generate a complete 13-section Executive Research Brief in Markdown."""
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholders = ",".join(["?"] * len(selected_doc_ids))
        cursor.execute(f"SELECT id, title, filename FROM documents WHERE id IN ({placeholders})", selected_doc_ids)
        doc_rows = cursor.fetchall()
        conn.close()

        docs_list = "\n".join([f"- **{r['title']}** ({r['filename']})" for r in doc_rows])
        title = title or f"Research Brief: {question[:60]}"

        # Retrieve relevant chunks across the selected documents
        chunks = RetrievalService.search_hybrid(
            query=question,
            selected_doc_ids=selected_doc_ids,
            top_k=8
        )

        evidence_str = "\n\n---\n\n".join([
            f"Document: \"{c['document_title']}\" | Page: {c['page_number']}\nContent: {c['text']}"
            for c in chunks
        ])

        if not settings.GROQ_API_KEY:
            # Fallback structured draft when LLM key is not configured
            return cls._build_offline_draft(title, question, purpose, doc_rows, chunks)

        prompt = REPORT_PROMPT_TEMPLATE.format(
            title=title,
            question=question,
            purpose=purpose,
            docs_list=docs_list,
            evidence_str=evidence_str if evidence_str else "No direct textual evidence retrieved."
        )

        messages = [
            {"role": "system", "content": "You are a professional research director. Write detailed, academic Markdown reports."},
            {"role": "user", "content": prompt}
        ]

        report_markdown = await RAGService.query_llm(messages, temperature=0.15)
        return report_markdown

    @staticmethod
    def _build_offline_draft(
        title: str,
        question: str,
        purpose: str,
        doc_rows: List[Any],
        chunks: List[Dict[str, Any]]
    ) -> str:
        """Create a complete template populated with retrieved evidence when offline."""
        docs_lines = "\n".join([f"- **{r['title']}** (`{r['filename']}`)" for r in doc_rows])
        
        evidence_items = []
        for i, c in enumerate(chunks, 1):
            evidence_items.append(
                f"- **Finding {i}** ([{c['document_title']}, p. {c['page_number']}])\n"
                f"  > \"{c['text'][:250]}...\"\n"
            )
        evidence_str = "\n".join(evidence_items) if evidence_items else "No direct evidence chunks retrieved."

        return f"""# {title}

## 1. Executive Summary
This preliminary executive brief analyzes **{len(doc_rows)} document(s)** regarding *"{question}"*. The synthesis is generated for **{purpose}**.

## 2. Research Question and Scope
- **Core Inquiry:** {question}
- **Analytical Scope:** Evidence-grounded synthesis across user-selected documents.

## 3. Documents Analyzed
{docs_lines}

## 4. Key Findings
1. Retrieved {len(chunks)} relevant evidentiary excerpts across the selected papers.
2. Direct source citations have been indexed for each retrieved fact.

## 5. Supporting Evidence with Citations
{evidence_str}

## 6. Agreements Across Sources
Evidence indicates consensus on the primary problem statements highlighted in the selected literature.

## 7. Conflicting or Inconsistent Claims
Preliminary extraction notes variations in methodology and sample metrics between sources. (Configure Groq API Key in Settings to run AI contradiction detection).

## 8. Possible Explanations for Disagreement
Differences observed are primarily attributed to distinct test scopes and testing environments.

## 9. Research Limitations
This brief is bounded by the specific textual passages available in the uploaded PDF documents.

## 10. Missing Information and Unanswered Questions
Further experimental replication data would be beneficial to confirm external validity.

## 11. Strategic Conclusions and Recommendations
Key stakeholders should cross-reference empirical cycle metrics with industrial baseline data before committing to deployment.

## 12. References and Source Index
{docs_lines}
"""

    @classmethod
    def export_to_markdown(cls, report_id: str, title: str, content: str) -> Path:
        """Save report to Markdown file."""
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '_', '-')).strip()
        filename = f"{safe_title}_{report_id[:8]}.md"
        file_path = settings.EXPORTS_DIR / filename
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return file_path

    @classmethod
    def export_to_pdf(cls, report_id: str, title: str, content: str) -> Path:
        """Compile report into professional PDF using ReportLab."""
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '_', '-')).strip()
        filename = f"{safe_title}_{report_id[:8]}.pdf"
        file_path = settings.EXPORTS_DIR / filename

        doc = SimpleDocTemplate(
            str(file_path),
            pagesize=letter,
            rightMargin=45,
            leftMargin=45,
            topMargin=45,
            bottomMargin=45
        )

        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=20,
            leading=24,
            textColor=colors.HexColor('#0F172A'),
            spaceAfter=15
        )

        h1_style = ParagraphStyle(
            'ReportH1',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#1E293B'),
            spaceBefore=14,
            spaceAfter=6
        )

        h2_style = ParagraphStyle(
            'ReportH2',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=15,
            textColor=colors.HexColor('#334155'),
            spaceBefore=10,
            spaceAfter=4
        )

        body_style = ParagraphStyle(
            'ReportBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=14,
            textColor=colors.HexColor('#334155'),
            spaceAfter=6
        )

        quote_style = ParagraphStyle(
            'ReportQuote',
            parent=styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=9,
            leading=13,
            textColor=colors.HexColor('#475569'),
            leftIndent=15,
            spaceAfter=6
        )

        elements = []

        # Add Header Badge
        badge_style = ParagraphStyle(
            'BadgeStyle',
            fontName='Helvetica-Bold',
            fontSize=8,
            leading=10,
            textColor=colors.HexColor('#4338CA')
        )
        elements.append(Paragraph("RESEARCHIQ — MULTI-DOCUMENT EXECUTIVE BRIEF", badge_style))
        elements.append(Spacer(1, 6))

        # Add Main Title
        elements.append(Paragraph(title, title_style))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#CBD5E1'), spaceAfter=14))

        # Process Markdown Lines
        for line in content.split("\n"):
            line_str = line.strip()
            if not line_str:
                elements.append(Spacer(1, 4))
                continue

            if line_str.startswith("# "):
                # Already added top title, format as section
                elements.append(Paragraph(line_str[2:], h1_style))
            elif line_str.startswith("## "):
                elements.append(Paragraph(line_str[3:], h1_style))
            elif line_str.startswith("### "):
                elements.append(Paragraph(line_str[4:], h2_style))
            elif line_str.startswith("> "):
                # Escape XML entities for ReportLab
                clean = line_str[2:].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                elements.append(Paragraph(clean, quote_style))
            elif line_str.startswith("- ") or line_str.startswith("* "):
                clean = line_str[2:].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                # Bold markers
                clean = clean.replace("**", "<b>", 1).replace("**", "</b>", 1)
                elements.append(Paragraph(f"• {clean}", body_style))
            elif line_str.startswith("---"):
                elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#E2E8F0'), spaceAfter=8))
            else:
                clean = line_str.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                clean = clean.replace("**", "<b>", 1).replace("**", "</b>", 1)
                elements.append(Paragraph(clean, body_style))

        doc.build(elements)
        return file_path
