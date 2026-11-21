# append_chapters.py - Script to complete Chapters 4 through 11, References, and Appendices in ResearchIQ DOCX Report
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from report_data import TEST_CASES

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'ResearchIQ_Internship_Report')
DOCX_PATH = os.path.join(OUTPUT_DIR, 'ResearchIQ_Internship_Report.docx')
FIGURES_DIR = os.path.join(OUTPUT_DIR, 'figures')

C_BLACK = RGBColor(0, 0, 0)
C_DARK_BLUE = RGBColor(15, 23, 42)
C_INDIGO = RGBColor(67, 56, 202)
C_MUTED = RGBColor(71, 85, 105)

def format_paragraph(p, space_after=6, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.0):
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if indent > 0:
        p.paragraph_format.first_line_indent = Inches(indent)

def add_body_p(doc, text, indent=0.0):
    p = doc.add_paragraph()
    format_paragraph(p, space_after=6, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=indent)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.font.color.rgb = C_BLACK
    return p

def add_bullet_p(doc, bold_prefix, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.3
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    r_bold = p.add_run(bold_prefix + " ")
    r_bold.font.name = "Times New Roman"
    r_bold.font.size = Pt(11.5)
    r_bold.font.bold = True
    r_bold.font.color.rgb = C_BLACK

    r_text = p.add_run(text)
    r_text.font.name = "Times New Roman"
    r_text.font.size = Pt(11.5)
    r_text.font.color.rgb = C_BLACK
    return p

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.cell(0, 0).width = Inches(6.0)
    
    shading = OxmlElement('w:shd')
    shading.set(qn('w:val'), 'clear')
    shading.set(qn('w:color'), 'auto')
    shading.set(qn('w:fill'), 'F8FAFC')
    tbl.cell(0, 0)._tc.get_or_add_tcPr().append(shading)
    
    p = tbl.cell(0, 0).paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_text)
    run.font.name = "Courier New"
    run.font.size = Pt(9.0)
    run.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_chap_heading(doc, text):
    doc.add_page_break()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(14)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = C_BLACK
    return p

def add_sec_heading(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = C_BLACK
    return p

def add_subsec_heading(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = C_BLACK
    return p

def add_figure(doc, img_name, fig_num, caption):
    img_path = os.path.join(FIGURES_DIR, img_name)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(5.8))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(12)
        r_num = p_cap.add_run(f"Figure {fig_num}: ")
        r_num.font.name = "Times New Roman"
        r_num.font.size = Pt(10)
        r_num.font.bold = True
        r_cap = p_cap.add_run(caption)
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(10)
        r_cap.font.italic = True

def format_cell(cell, text, bold=False, italic=False, font_size=9.5, bg_hex=None, align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.text = text
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    for r in p.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(font_size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = C_BLACK
    if bg_hex:
        shading = OxmlElement('w:shd')
        shading.set(qn('w:val'), 'clear')
        shading.set(qn('w:color'), 'auto')
        shading.set(qn('w:fill'), bg_hex)
        cell._tc.get_or_add_tcPr().append(shading)

def append_remaining_chapters():
    print("Loading existing document...")
    doc = docx.Document(DOCX_PATH)

    # -------------------------------------------------------------------------
    # CHAPTER 4: PROBLEM IDENTIFICATION AND SCOPE
    # -------------------------------------------------------------------------
    add_chap_heading(doc, "CHAPTER 4\nPROBLEM IDENTIFICATION AND SCOPE")

    add_sec_heading(doc, "4.1 Project Introduction")
    add_body_p(doc, "ResearchIQ is conceptualized as an enterprise-grade document intelligence platform that bridges academic research rigors with full-stack software engineering. In both academic institutions and corporate R&D divisions, researchers encounter severe informational friction when trying to assimilate multiple extensive technical reports. The project focuses on transforming static PDF documents into interactive, semantically searchable, and auditable knowledge bases.")

    add_sec_heading(doc, "4.2 Existing System")
    add_body_p(doc, "In the prevailing workflow, researchers utilize basic keyword searches (Ctrl+F), manual skimming, or generic consumer AI chatbots. Commercial cloud chat tools typically require users to copy-paste snippets or upload single documents to public servers. These systems process documents in a black-box fashion, offering conversational answers without transparently revealing how the source text was parsed, chunked, or mapped to vector spaces.")

    add_sec_heading(doc, "4.3 Limitations of Existing System")
    add_bullet_p(doc, "1. Severe Token Limits & High Costs:", "Passing hundreds of pages of raw text directly to commercial LLM APIs exhausts context windows and results in excessive API billing.")
    add_bullet_p(doc, "2. Parametric Hallucination:", "Consumer LLMs answer queries based on training probability rather than verified document evidence, generating fabricated statistics, dates, and claims.")
    add_bullet_p(doc, "3. Lack of Cross-Document Analysis:", "Conventional RAG systems retrieve chunks from individual documents in isolation, failing to compare competing assertions or detect empirical contradictions between different studies.")
    add_bullet_p(doc, "4. Unverifiable Citations:", "Standard conversational AI tools generate answers with generic references (e.g., 'according to the paper') without citing the exact 1-indexed PDF page number, making audit impossible.")
    add_bullet_p(doc, "5. Privacy & Data Sovereignty Risks:", "Uploading proprietary corporate intellectual property, medical reports, or pre-publication academic papers to remote third-party clouds compromises enterprise confidentiality.")

    add_sec_heading(doc, "4.4 Problem Identification")
    add_body_p(doc, "The core problem identified is the absence of an open, verifiable, and local-first research platform capable of ingesting multiple heterogeneous scientific PDFs, conducting hybrid semantic-lexical retrieval, isolating research scope to user-selected papers, automatically categorizing contradictory empirical findings, and compiling structured research briefs backed by page-level proof.")

    add_sec_heading(doc, "4.5 Proposed System")
    add_body_p(doc, "The proposed ResearchIQ platform introduces a four-tiered engineering architecture: (1) Robust PyMuPDF Ingestion preserving 1-indexed page boundaries and rejecting unreadable scanned PDFs; (2) Sentence-Aware Chunking (750-character window with 150-character sliding overlap); (3) Hybrid Retrieval combining FAISS dense vector search (all-MiniLM-L6-v2) and SQLite FTS5 BM25 keyword matching via Reciprocal Rank Fusion (RRF); and (4) Evidence-Grounded Synthesis using Groq Cloud LLM APIs enforced by strict citation prompts, accompanied by a dedicated Contradiction Analysis Engine and ReportLab PDF brief compiler.")

    add_sec_heading(doc, "4.6 Advantages of Proposed System")
    add_bullet_p(doc, "• Auditable Verifiability:", "Every factual statement cites [Document Title, p. X]. Clicking citation badges in the UI navigates directly to the original passage in the Evidence Explorer.")
    add_bullet_p(doc, "• Superior Hybrid Recall:", "Combining dense vector embeddings with sparse BM25 keyword matching ensures exact numbers, chemical formulas, and acronyms are never missed.")
    add_bullet_p(doc, "• Automated Contradiction Detection:", "Classifies cross-document claims as Agreement, Difference, or Potential Contradiction with human-in-the-loop review flags.")
    add_bullet_p(doc, "• 100% Local Vector Processing:", "Document parsing, sentence chunking, vector embedding, and FAISS indexing execute locally on the developer's workstation without cloud database dependencies.")
    add_bullet_p(doc, "• One-Command Deployment:", "Packaged with run.bat for instant setup, automated environment validation, and single-port web serving on http://127.0.0.1:8000.")

    add_sec_heading(doc, "4.7 Functional Requirements")
    add_bullet_p(doc, "FR-01 Document Upload:", "The system shall accept multiple PDF files via drag-and-drop or browse, validating file format and a maximum size of 20MB per file.")
    add_bullet_p(doc, "FR-02 SHA-256 Duplicate Check:", "The system shall compute cryptographic SHA-256 hashes of uploaded files to block duplicate ingestion.")
    add_bullet_p(doc, "FR-03 Text Extraction & Page Retention:", "The system shall extract textual contents page-by-page using PyMuPDF while maintaining 1-indexed page numbers.")
    add_bullet_p(doc, "FR-04 Sentence Chunking:", "The system shall split text into overlapping chunks of 750 characters with a 150-character overlap along sentence boundaries.")
    add_bullet_p(doc, "FR-05 Dense Vector Generation:", "The system shall convert chunks into 384-dimensional normalized vector embeddings using all-MiniLM-L6-v2.")
    add_bullet_p(doc, "FR-06 FAISS Indexing:", "The system shall index embeddings using FAISS IndexFlatIP and persist the index and ID mapping locally.")
    add_bullet_p(doc, "FR-07 SQLite FTS5 Keyword Indexing:", "The system shall index chunk texts in an SQLite FTS5 virtual table for Porter-stemmed BM25 keyword retrieval.")
    add_bullet_p(doc, "FR-08 Reciprocal Rank Fusion:", "The system shall combine dense and sparse rankings using RRF with constant k=60 to produce unified relevance scores.")
    add_bullet_p(doc, "FR-09 Document Scope Isolation:", "The system shall strictly restrict retrieval to documents selected by the user in the research workspace.")
    add_bullet_p(doc, "FR-10 Evidence-Grounded Q&A:", "The system shall generate structured answers citing [Doc Title, p. X] and output explicit warnings if evidence is insufficient.")
    add_bullet_p(doc, "FR-11 Cross-Document Comparison:", "The system shall extract and compare empirical claims across two or more selected papers in a tabular contradiction matrix.")
    add_bullet_p(doc, "FR-12 Executive Brief Generation:", "The system shall generate 13-section research briefs and export them to Markdown (.md) and ReportLab PDF (.pdf).")

    add_sec_heading(doc, "4.8 Non-Functional Requirements")
    add_bullet_p(doc, "NFR-01 Performance & Latency:", "Local vector retrieval across 1,000 chunks shall execute in under 150 milliseconds on a standard multi-core CPU.")
    add_bullet_p(doc, "NFR-02 Precision & Grounding:", "The system shall achieve 100% citation coverage for empirical assertions, preventing unsupported claims.")
    add_bullet_p(doc, "NFR-03 Reliability & Fault Tolerance:", "Corrupted, encrypted, or empty image-only PDFs shall be flagged with clear error messages without crashing the server.")
    add_bullet_p(doc, "NFR-04 Usability & SaaS Aesthetics:", "The UI shall provide responsive 3-panel layouts, collapsible drawers, dark mode support, and smooth scroll navigation.")
    add_bullet_p(doc, "NFR-05 Security & Privacy:", "Server shall bind strictly to 127.0.0.1; API keys shall remain server-side and never be exposed to frontend code.")

    add_sec_heading(doc, "4.9 Project Applications")
    add_body_p(doc, "ResearchIQ provides high utility across multiple sectors: (1) Academic Researchers conducting systematic literature reviews; (2) Pharmaceutical & Biotech Analysts evaluating drug clinical trials across competing medical journals; (3) Intellectual Property Attorneys cross-referencing patent claims; (4) Engineering R&D Teams reviewing material specifications; and (5) Financial & Investment Analysts assessing corporate disclosures.")

    add_sec_heading(doc, "4.10 Project Scope")
    add_body_p(doc, "The current scope focuses on multi-document processing of digital text PDFs on local Windows environments. The system provides local vector persistence, relational SQLite metadata management, and fast Groq Cloud LLM synthesis. Out of scope for the current release are multi-modal image OCR for scanned historical manuscripts, real-time web scraping, and multi-tenant distributed cloud infrastructure, which are documented as future scope.")

    # -------------------------------------------------------------------------
    # CHAPTER 5: SYSTEM REQUIREMENTS
    # -------------------------------------------------------------------------
    add_chap_heading(doc, "CHAPTER 5\nSYSTEM REQUIREMENTS")

    add_sec_heading(doc, "5.1 Introduction")
    add_body_p(doc, "To ensure high technical reproducibility and seamless execution on standard student and corporate hardware, ResearchIQ was engineered to run locally without requiring expensive cloud database servers, enterprise GPUs, or complex Docker configurations. This chapter details the verified hardware, operating system, runtime, library, and configuration specifications.")

    add_sec_heading(doc, "5.2 Hardware Requirements")
    add_body_p(doc, "The platform is optimized for commodity laptop and desktop development workstations. The verified hardware specifications are detailed in Table 5.1.")

    p_t = doc.add_paragraph()
    p_t.paragraph_format.space_before = Pt(8)
    p_t.paragraph_format.space_after = Pt(4)
    r = p_t.add_run("Table 5.1: Hardware Environment Specifications")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.bold = True

    tbl_hw = doc.add_table(rows=6, cols=3)
    tbl_hw.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_hw.autofit = False
    hw_headers = ["Component", "Minimum Requirement", "Recommended / Tested Workstation"]
    for c_idx, h in enumerate(hw_headers):
        format_cell(tbl_hw.cell(0, c_idx), h, bold=True, font_size=9.5, bg_hex="E2E8F0")
    
    hw_data = [
        ("Processor (CPU)", "Intel Core i5 / AMD Ryzen 5 (4 Cores)", "Intel Core i5/i7 (8 Cores, 2.4 GHz or higher)"),
        ("System Memory (RAM)", "8 GB DDR4", "16 GB DDR4/DDR5 (Supports concurrent vector batching)"),
        ("Storage (Disk Space)", "10 GB Free Storage Space", "512 GB NVMe SSD (Ensures rapid disk I/O for FAISS)"),
        ("Graphics (GPU)", "Not Required (CPU inference used)", "Integrated Intel Iris Xe or dedicated NVIDIA GPU"),
        ("Network Connectivity", "Broadband Internet (Initial model download)", "Active Internet Connection (Groq Cloud LLM API calls)")
    ]
    for r_idx, (comp, min_req, rec_req) in enumerate(hw_data):
        format_cell(tbl_hw.cell(r_idx + 1, 0), comp, bold=True)
        format_cell(tbl_hw.cell(r_idx + 1, 1), min_req)
        format_cell(tbl_hw.cell(r_idx + 1, 2), rec_req)

    add_sec_heading(doc, "5.3 Software Requirements")
    add_body_p(doc, "Table 5.2 outlines the host operating system, web browser standards, and core development runtimes required to execute the ResearchIQ platform.")

    p_t = doc.add_paragraph()
    p_t.paragraph_format.space_before = Pt(8)
    p_t.paragraph_format.space_after = Pt(4)
    r = p_t.add_run("Table 5.2: Software & Operating System Specifications")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.bold = True

    tbl_sw = doc.add_table(rows=6, cols=2)
    tbl_sw.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_sw.autofit = False
    format_cell(tbl_sw.cell(0, 0), "Software Environment", bold=True, font_size=9.5, bg_hex="E2E8F0")
    format_cell(tbl_sw.cell(0, 1), "Specification / Version", bold=True, font_size=9.5, bg_hex="E2E8F0")

    sw_data = [
        ("Operating System", "Microsoft Windows 10 / Windows 11 (64-bit)"),
        ("Python Runtime", "Python 3.11.4 (64-bit) with pip package manager"),
        ("Node.js Runtime", "Node.js v24.13.0 LTS with npm 11.6.2+"),
        ("Web Browser", "Google Chrome 120+, Mozilla Firefox, or Microsoft Edge (Chromium)"),
        ("Shell Environment", "Windows PowerShell 5.1 / PowerShell 7+ or Command Prompt (cmd.exe)")
    ]
    for r_idx, (env, spec) in enumerate(sw_data):
        format_cell(tbl_sw.cell(r_idx + 1, 0), env, bold=True)
        format_cell(tbl_sw.cell(r_idx + 1, 1), spec)

    add_sec_heading(doc, "5.4 Programming Languages")
    add_body_p(doc, "ResearchIQ utilizes two primary programming languages: Python for backend services, data processing, and machine learning pipelines; and TypeScript for type-safe, modular frontend development, complemented by SQL for relational queries (Table 5.3).")

    p_t = doc.add_paragraph()
    p_t.paragraph_format.space_before = Pt(8)
    p_t.paragraph_format.space_after = Pt(4)
    r = p_t.add_run("Table 5.3: Programming Languages and Core Runtime Versions")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.bold = True

    tbl_pl = doc.add_table(rows=4, cols=3)
    tbl_pl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_pl.autofit = False
    for c_idx, h in enumerate(["Language", "Version", "Role in ResearchIQ"]):
        format_cell(tbl_pl.cell(0, c_idx), h, bold=True, font_size=9.5, bg_hex="E2E8F0")
    pl_data = [
        ("Python", "3.11.4", "Backend services, PDF extraction, vector embeddings, FAISS indexing, RRF ranking"),
        ("TypeScript", "5.4+", "Type-safe frontend development, React state management, API data contracts"),
        ("SQL (SQLite)", "3.40+", "Relational database schema, metadata persistence, FTS5 full-text indexing")
    ]
    for r_idx, (lang, ver, role) in enumerate(pl_data):
        format_cell(tbl_pl.cell(r_idx + 1, 0), lang, bold=True)
        format_cell(tbl_pl.cell(r_idx + 1, 1), ver)
        format_cell(tbl_pl.cell(r_idx + 1, 2), role)

    add_sec_heading(doc, "5.5 Frameworks and Libraries")
    add_body_p(doc, "Table 5.4 enumerates the primary Python packages and frontend frameworks used in ResearchIQ, along with their functional roles.")

    p_t = doc.add_paragraph()
    p_t.paragraph_format.space_before = Pt(8)
    p_t.paragraph_format.space_after = Pt(4)
    r = p_t.add_run("Table 5.4: Primary Python Libraries & Frameworks")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.bold = True

    tbl_pk = doc.add_table(rows=9, cols=3)
    tbl_pk.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_pk.autofit = False
    for c_idx, h in enumerate(["Package / Framework", "Version", "Technical Functional Role"]):
        format_cell(tbl_pk.cell(0, c_idx), h, bold=True, font_size=9.5, bg_hex="E2E8F0")
    pk_data = [
        ("FastAPI", ">= 0.110.0", "Asynchronous web framework providing high-throughput REST API endpoints"),
        ("Uvicorn", ">= 0.28.0", "ASGI web server implementation supporting asynchronous Python execution"),
        ("Pydantic", ">= 2.6.0", "Data validation, serialization, and schema definition for request/response payloads"),
        ("PyMuPDF (fitz)", ">= 1.23.0", "High-speed C-based PDF parsing, per-page text and metadata extraction"),
        ("sentence-transformers", ">= 2.5.0", "Transformer encoder generating 384-dimensional dense semantic vectors"),
        ("faiss-cpu", ">= 1.8.0", "Facebook AI Similarity Search library for dense cosine vector indexing"),
        ("ReportLab", ">= 4.1.0", "Programmatic compilation of 13-section executive research briefs into styled PDF"),
        ("httpx", ">= 0.27.0", "Asynchronous HTTP client for non-blocking communication with Groq Cloud LLM APIs")
    ]
    for r_idx, (pkg, ver, role) in enumerate(pk_data):
        format_cell(tbl_pk.cell(r_idx + 1, 0), pkg, bold=True)
        format_cell(tbl_pk.cell(r_idx + 1, 1), ver)
        format_cell(tbl_pk.cell(r_idx + 1, 2), role)

    add_sec_heading(doc, "5.6 Database and Storage Requirements")
    add_body_p(doc, "Data storage is structured into relational SQLite tables, an FTS5 full-text search index, local FAISS vector binaries, and organized filesystem directories (Table 5.5).")

    p_t = doc.add_paragraph()
    p_t.paragraph_format.space_before = Pt(8)
    p_t.paragraph_format.space_after = Pt(4)
    r = p_t.add_run("Table 5.5: Database Schema & Entity Specifications")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.bold = True

    tbl_db = doc.add_table(rows=7, cols=3)
    tbl_db.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_db.autofit = False
    for c_idx, h in enumerate(["Table / Entity Name", "Type / Engine", "Primary Role & Attributes"]):
        format_cell(tbl_db.cell(0, c_idx), h, bold=True, font_size=9.5, bg_hex="E2E8F0")
    db_data = [
        ("documents", "SQLite Table", "Stores document ID, title, filename, SHA-256 hash, size, pages, and status"),
        ("document_chunks", "SQLite Table", "Stores chunk ID, document foreign key, chunk index, page number, and text"),
        ("document_chunks_fts", "SQLite FTS5 Table", "Virtual full-text search table with Porter stemmer for BM25 keyword matching"),
        ("research_sessions", "SQLite Table", "Maintains session ID, title, and creation/update timestamps"),
        ("chat_messages", "SQLite Table", "Stores message ID, session ID, role (user/assistant), content, and citations JSON"),
        ("research_reports", "SQLite Table", "Persists 13-section research briefs, question, Markdown body, and selected doc IDs")
    ]
    for r_idx, (tbl, typ, desc) in enumerate(db_data):
        format_cell(tbl_db.cell(r_idx + 1, 0), tbl, bold=True)
        format_cell(tbl_db.cell(r_idx + 1, 1), typ)
        format_cell(tbl_db.cell(r_idx + 1, 2), desc)

    add_sec_heading(doc, "5.7 Development Environment")
    add_body_p(doc, "The development workflow was configured using Visual Studio Code with extensions for Python, Pylance, Tailwind CSS IntelliSense, and SQLite Viewer. Git was utilized for source control, following structured branch and commit conventions. Windows PowerShell served as the primary command execution shell.")

    add_sec_heading(doc, "5.8 System Configuration")
    add_body_p(doc, "Environment configuration is centralized in backend/config.py and driven by a local .env file. Key parameters include GROQ_API_KEY (stored strictly server-side), GROQ_MODEL (defaulting to llama-3.3-70b-versatile), APP_HOST (127.0.0.1), APP_PORT (8000), MAX_UPLOAD_MB (20), CHUNK_SIZE (750 chars), CHUNK_OVERLAP (150 chars), and RRF_K (60).")

    # -------------------------------------------------------------------------
    # CHAPTER 6: SYSTEM ARCHITECTURE AND DESIGN
    # -------------------------------------------------------------------------
    add_chap_heading(doc, "CHAPTER 6\nSYSTEM ARCHITECTURE AND DESIGN")

    add_sec_heading(doc, "6.1 Introduction")
    add_body_p(doc, "System architecture defines the structural organization, inter-module communication protocols, and processing pipelines governing the application. ResearchIQ is architected as a modular, local-first system designed for deterministic execution, high performance, and total transparency in evidence retrieval. This chapter details each functional module and presents the formal engineering architecture diagrams.")

    add_sec_heading(doc, "6.2 Overall System Architecture")
    add_body_p(doc, "The ResearchIQ architecture is structured across four primary layers: (1) The Client Presentation Layer (React 19 SPA); (2) The Application & API Gateway Layer (FastAPI 0.110); (3) The Core Services & Processing Layer; and (4) The Persistence & Storage Layer. Figure 6.1 illustrates the comprehensive system architecture.")

    add_figure(doc, "fig_6_1_architecture.png", "6.1", "Overall ResearchIQ System Architecture Diagram")

    add_sec_heading(doc, "6.3 Document Upload Module")
    add_body_p(doc, "The Document Upload Module (backend/api/documents.py) provides REST endpoints accepting single and multi-file multipart uploads. It enforces file format verification (.pdf), validates file size (<= 20MB), and calculates a cryptographic SHA-256 hash. If an identical hash exists in the database, the upload is rejected with HTTP 409 Conflict, preventing redundant indexing and index pollution.")

    add_sec_heading(doc, "6.4 PDF Text Extraction Module")
    add_body_p(doc, "The PDF Text Extraction Module (backend/services/pdf_service.py) integrates PyMuPDF (fitz). The workflow parses the document page-by-page, retaining the exact 1-indexed page number for every extracted segment. It checks for encryption and empty scanned documents (<50 characters threshold). Figure 6.2 illustrates the document processing pipeline.")

    add_figure(doc, "fig_6_2_doc_processing.png", "6.2", "Document Processing Workflow Pipeline")

    add_sec_heading(doc, "6.5 Text Preprocessing Module")
    add_body_p(doc, "The Preprocessing Module normalizes raw extracted strings by eliminating anomalous carriage returns, unbreaking hyphenated end-of-line words, stripping non-printable ASCII control characters, and normalizing multi-whitespace sequences. This guarantees high tokenization fidelity during embedding generation.")

    add_sec_heading(doc, "6.6 Text Chunking Module")
    add_body_p(doc, "The Text Chunking Module (backend/services/chunking_service.py) implements sentence-aware sliding window chunking. It splits paragraphs along sentence punctuation boundaries, assembling chunks up to 750 characters while maintaining a 150-character overlap with preceding sentences. Each chunk is tagged with doc_id, chunk_index, and page_number (Figure 6.3).")

    add_figure(doc, "fig_6_3_chunking_embedding.png", "6.3", "Sentence-Boundary Chunking and Embedding Workflow")

    add_sec_heading(doc, "6.7 Embedding Generation Module")
    add_body_p(doc, "The Embedding Generation Module (backend/services/embedding_service.py) utilizes the transformer model sentence-transformers/all-MiniLM-L6-v2. It generates 384-dimensional dense vectors in batches of 32. Crucially, embeddings are L2 unit-normalized, transforming standard dot products into exact cosine similarity scores.")

    add_sec_heading(doc, "6.8 FAISS Vector Indexing Module")
    add_body_p(doc, "The FAISS Indexing Module (backend/services/retrieval_service.py) manages vector storage via FAISS IndexFlatIP (Inner Product). Because embeddings are L2-normalized, IndexFlatIP computes exact, unquantized cosine similarity. The module maintains a parallel chunk_id_map.json linking FAISS integer positions to unique SQLite chunk UUIDs (Figure 6.4).")

    add_figure(doc, "fig_6_4_faiss_indexing.png", "6.4", "FAISS Vector Indexing & ID Mapping Architecture")

    add_sec_heading(doc, "6.9 Semantic Retrieval Module")
    add_body_p(doc, "When a query is received, the Semantic Retrieval Module embeds the query vector and searches the FAISS index for candidate vectors. It applies an isolated document filter, discarding candidate chunks that do not belong to the user's active document selection.")

    add_sec_heading(doc, "6.10 RAG Processing Module")
    add_body_p(doc, "The RAG Processing Module fuses dense semantic candidates with sparse SQLite FTS5 BM25 keyword matches using Reciprocal Rank Fusion (RRF with k=60). The top-6 ranked chunks are packaged into an evidence block and dispatched to the Groq Cloud LLM API with strict academic grounding prompts (Figure 6.5).")

    add_figure(doc, "fig_6_5_rag_architecture.png", "6.5", "Retrieval-Augmented Generation & Fusion Architecture")

    add_sec_heading(doc, "6.11 Research Analysis Module")
    add_body_p(doc, "The Research Analysis Module enforces strict evidentiary grounding. If retrieved chunks fail to satisfy relevance thresholds, the module bypasses LLM inference and outputs an explicit 'Insufficient Evidence' notice, preventing the system from guessing or fabricating claims.")

    add_sec_heading(doc, "6.12 Multi-Document Comparison")
    add_body_p(doc, "The Comparison Module (backend/services/comparison_service.py) performs isolated retrieval per document, extracts core empirical metrics, and aligns entities side-by-side. It categorizes claims into Agreement, Difference, or Potential Contradiction, complete with citations and human-review flags.")

    add_sec_heading(doc, "6.13 Evidence and Reference Generation")
    add_body_p(doc, "Every synthesized assertion is bound to verifiable citation metadata: document ID, document title, original PDF page number, and RRF relevance score. In the UI, citation tags act as interactive anchors that instantly highlight corresponding passages in the Evidence Explorer.")

    add_sec_heading(doc, "6.14 Complete System Workflow")
    add_body_p(doc, "Figure 6.6 illustrates the comprehensive end-to-end system workflow, tracing user interaction from PDF upload and indexing through hybrid query fusion, grounded LLM synthesis, contradiction matrix display, and PDF report compilation.")

    add_figure(doc, "fig_6_6_complete_workflow.png", "6.6", "Complete ResearchIQ End-to-End System Workflow")

    # Save progress
    doc.save(DOCX_PATH)
    print("Chapters 4-6 appended successfully.")

if __name__ == "__main__":
    append_remaining_chapters()
