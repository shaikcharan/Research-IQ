# report_data.py - Structured Data and Comprehensive Content for ResearchIQ Internship Project Report

STUDENT_INFO = {
    "name": "Shaik Charan",
    "reg_no": "72311068",
    "degree": "Bachelor of Technology (B.Tech)",
    "branch": "Computer Science and Engineering",
    "specialization": "Artificial Intelligence and Data Science",
    "university": "CT University, Ludhiana, Punjab, India",
    "academic_year": "2026–2027",
    "project_title": "ResearchIQ – Academic & Industrial Research Intelligence",
    "domain": "Artificial Intelligence, Machine Learning, Natural Language Processing, Retrieval-Augmented Generation, Document Intelligence and Information Retrieval"
}

COMPANY_INFO = {
    "name": "MegaViz Technologies Pvt Ltd",
    "website": "https://megaviztech.com/",
    "url_display": "www.megaviztech.com",
    "position": "AI & ML Developer",
    "duration": "45 DAYS",
    "start_date": "20 June 2026",
    "end_date": "04 August 2026",
    "supervisor_name": "Ms. Kolla Geetha Madhuri",
    "supervisor_designation": "Chief Executive Officer (CEO)",
    "address": "#806, 8th Floor, Manjeera Trinity Corporate, Besides Manjeera Cinepolis Mall, Kukatpally Housing Board Colony, Hyderabad, Telangana, India – 500072",
    "email": "info@megaviztech.com",
    "phone": "+91 91541-83243"
}

# 39 Working Days (excluding Sundays) from 20 June 2026 to 04 August 2026
# Chronologically aligned with the 45 DAYS internship curriculum & ResearchIQ development lifecycle
DAILY_DIARY = [
    {
        "date": "20-06-2026", "day": "Saturday",
        "activity": "Internship Orientation & Company Onboarding",
        "work": "Attended orientation session at MegaViz Technologies Pvt Ltd conducted by CEO Ms. Kolla Geetha Madhuri. Briefed on organizational policies, AI engineering ethics, research domain, and internship objectives.",
        "outcome": "Understood corporate expectations, project lifecycle requirements, and scope of industrial RAG applications."
    },
    {
        "date": "22-06-2026", "day": "Monday",
        "activity": "Introduction to AI & Machine Learning Workflows",
        "work": "Reviewed state-of-the-art Natural Language Processing (NLP) architectures and information retrieval workflows. Formulated foundational problem statement for multi-document research synthesis.",
        "outcome": "Acquired comprehensive understanding of current challenges in automated document intelligence and literature analysis."
    },
    {
        "date": "23-06-2026", "day": "Tuesday",
        "activity": "Document Intelligence & Literature Survey",
        "work": "Conducted literature survey on Retrieval-Augmented Generation (RAG) paradigms. Explored limitations of standard generative models regarding context window constraints and parametric hallucinations.",
        "outcome": "Identified critical need for evidence-grounded retrieval systems supporting page-level citations in academia and industry."
    },
    {
        "date": "24-06-2026", "day": "Wednesday",
        "activity": "Development Environment Setup & Tooling",
        "work": "Configured local Windows 11 workstation development environment. Installed Python 3.11, Node.js 24, VS Code, Git, and initialized project directory structure for ResearchIQ.",
        "outcome": "Established a standardized, reproducible virtual environment (.venv) and verified core build dependencies."
    },
    {
        "date": "25-06-2026", "day": "Thursday",
        "activity": "Exploration of PDF Document Processing Libraries",
        "work": "Evaluated multiple PDF processing libraries including PyPDF, pdfplumber, and PyMuPDF (fitz). Benchmarked extraction speed, formatting preservation, and text extraction accuracy.",
        "outcome": "Selected PyMuPDF (fitz) due to superior C-level execution speed, accurate page-by-page parsing, and robust metadata extraction."
    },
    {
        "date": "26-06-2026", "day": "Friday",
        "activity": "PDF Text Extraction Pipeline Development",
        "work": "Implemented Python service using PyMuPDF to extract text from multi-page PDFs while strictly preserving 1-indexed page metadata. Implemented checks for empty and encrypted PDF files.",
        "outcome": "Developed reliable extraction script ensuring every extracted sentence remains traceable to its original PDF page."
    },
    {
        "date": "27-06-2026", "day": "Saturday",
        "activity": "Text Preprocessing & Sanitization Implementation",
        "work": "Designed text sanitization algorithms to eliminate hyphenated line breaks, control characters, extra whitespaces, and unreadable character sequences while preserving mathematical symbols.",
        "outcome": "Built a clean text preprocessing pipeline that prepares extracted raw text for high-quality embedding generation."
    },
    {
        "date": "29-06-2026", "day": "Monday",
        "activity": "Scanned & Image-Only PDF Detection Logic",
        "work": "Engineered automated validation module to detect scanned, image-only, or corrupted PDFs lacking extractable text layers (<50 characters threshold) and provide transparent error logging.",
        "outcome": "Prevented silent indexing failures by alerting users when OCR-dependent documents are uploaded."
    },
    {
        "date": "30-06-2026", "day": "Tuesday",
        "activity": "Text Chunking Strategies & Sentence Boundary Analysis",
        "work": "Analyzed trade-offs between fixed-character chunking and sentence-aware boundary chunking. Formulated regex-based sentence boundary segmentation using lookahead/lookbehind patterns.",
        "outcome": "Demonstrated that sentence-boundary chunking prevents syntactic fragmentation across chunk transitions."
    },
    {
        "date": "01-07-2026", "day": "Wednesday",
        "activity": "Implementation of Overlapping Chunking Engine",
        "work": "Developed ChunkingService featuring a 750-character window with a 150-character sliding overlap. Maintained unique chunk identifiers (docId_pX_cY) with page-number metadata.",
        "outcome": "Constructed robust chunking algorithm preserving complete semantic thoughts across adjoining text segments."
    },
    {
        "date": "02-07-2026", "day": "Thursday",
        "activity": "Introduction to Vector Embeddings & Similarity",
        "work": "Studied theoretical principles of transformer-based dense semantic embeddings, cosine similarity metrics, and normalized vector dot products for semantic information retrieval.",
        "outcome": "Gained strong foundational knowledge of how text passages are represented as points in high-dimensional vector spaces."
    },
    {
        "date": "03-07-2026", "day": "Friday",
        "activity": "Evaluation & Selection of Embedding Models",
        "work": "Evaluated lightweight Sentence-Transformers models. Selected sentence-transformers/all-MiniLM-L6-v2 for its optimal balance of 384-dimensional dense vectors and local CPU inference speed.",
        "outcome": "Established efficient embedding generation without requiring expensive GPU infrastructure."
    },
    {
        "date": "04-07-2026", "day": "Saturday",
        "activity": "Embedding Generation Service Implementation",
        "work": "Implemented EmbeddingService in Python utilizing batch encoding (batch_size=32), L2 unit normalization, and float32 array conversions to prepare vectors for inner-product indexing.",
        "outcome": "Achieved sub-second vector generation for full academic papers on standard development hardware."
    },
    {
        "date": "06-07-2026", "day": "Monday",
        "activity": "Study of Vector Databases & FAISS Architecture",
        "work": "Investigated vector indexing structures. Explored Facebook AI Similarity Search (FAISS) and its index types including IndexFlatL2, IndexIVFFlat, and IndexFlatIP.",
        "outcome": "Selected IndexFlatIP on unit-normalized vectors to achieve exact, lossless Cosine Similarity search with zero quantization distortion."
    },
    {
        "date": "07-07-2026", "day": "Tuesday",
        "activity": "FAISS Index Creation & Persistence Service",
        "work": "Engineered RetrievalService module to manage FAISS index creation, vector appending, disk serialization (faiss_index.bin), and chunk ID mapping serialization (chunk_id_map.json).",
        "outcome": "Implemented persistent vector storage that retains indexing across application and server restarts."
    },
    {
        "date": "08-07-2026", "day": "Wednesday",
        "activity": "SQLite Relational Database Schema Design",
        "work": "Designed relational database schema in SQLite with PRAGMA foreign_keys=ON. Created tables for documents, document_chunks, research_sessions, chat_messages, and research_reports.",
        "outcome": "Established a normalized data model supporting atomic transactions and automatic cascade deletion."
    },
    {
        "date": "09-07-2026", "day": "Thursday",
        "activity": "SQLite FTS5 Full-Text Search Integration",
        "work": "Implemented SQLite FTS5 virtual table (document_chunks_fts) configured with porter stemmer tokenization. Added full-text indexing for BM25 keyword matching.",
        "outcome": "Built a native sparse keyword retrieval layer capable of matching exact chemical symbols, numbers, and acronyms."
    },
    {
        "date": "10-07-2026", "day": "Friday",
        "activity": "Design of Hybrid Retrieval Architecture",
        "work": "Analyzed limitations of vector-only retrieval for technical terms. Designed a hybrid retrieval architecture combining dense semantic vectors with sparse BM25 keyword scores.",
        "outcome": "Formulated a unified search strategy bridging conceptual similarity and exact keyword precision."
    },
    {
        "date": "11-07-2026", "day": "Saturday",
        "activity": "Implementation of Reciprocal Rank Fusion (RRF)",
        "work": "Implemented Reciprocal Rank Fusion algorithm using constant k=60. Programmed parallel querying of FAISS and FTS5, scoring chunks by reciprocal rank to eliminate score scale mismatches.",
        "outcome": "Built an explainable, robust rank-aggregation pipeline outperforming individual retrieval methods."
    },
    {
        "date": "13-07-2026", "day": "Monday",
        "activity": "Multi-Document Isolation & Scope Filtering",
        "work": "Added document isolation filtering to hybrid retrieval pipeline, ensuring retrieved passages strictly belong to documents selected by the user in the research workspace.",
        "outcome": "Guaranteed strict analytical isolation when conducting research across specific subsets of uploaded papers."
    },
    {
        "date": "14-07-2026", "day": "Tuesday",
        "activity": "RAG Context Assembly & Prompt Engineering",
        "work": "Formulated strict academic system prompt for RAG synthesis. Engineered context assembly module packaging top-K retrieved excerpts with explicit document title and page markers.",
        "outcome": "Created a grounding prompt enforcing that all factual assertions cite [Document Title, p. X] and penalizing hallucination."
    },
    {
        "date": "15-07-2026", "day": "Wednesday",
        "activity": "Groq Cloud API & LLM Service Integration",
        "work": "Integrated asynchronous httpx client communicating with Groq Cloud API. Implemented model orchestration using llama-3.3-70b-versatile with temperature=0.2 for deterministic synthesis.",
        "outcome": "Achieved ultrafast, high-reasoning evidence synthesis with sub-2-second generation times."
    },
    {
        "date": "16-07-2026", "day": "Thursday",
        "activity": "Evidence Sufficiency Check Implementation",
        "work": "Developed an automated relevance validation check. Programmed system to return explicit 'Insufficient Evidence' notices when retrieved chunks fall below the relevance threshold.",
        "outcome": "Prevented deceptive generative guessing when uploaded documents do not contain answers to user inquiries."
    },
    {
        "date": "17-07-2026", "day": "Friday",
        "activity": "Cross-Document Contradiction Analysis Engine",
        "work": "Engineered ComparisonService module performing isolated retrieval per document, extracting empirical claims, and aligning entities across papers to identify disagreements.",
        "outcome": "Built automated capability to identify whether papers Agree, Differ in scope, or directly Contradict each other."
    },
    {
        "date": "18-07-2026", "day": "Saturday",
        "activity": "Structured Contradiction Matrix Classification",
        "work": "Constructed structured JSON schema for comparison outputs. Added classification rules distinguishing genuine empirical conflicts from methodology or demographic variances.",
        "outcome": "Enabled multi-source comparison tables complete with citations, explanations, and human-review flags."
    },
    {
        "date": "20-07-2026", "day": "Monday",
        "activity": "Executive Research Brief Generation Service",
        "work": "Developed ReportService implementing a 13-section academic research brief structure including Executive Summary, Key Findings, Conflicting Claims, Limitations, and Source References.",
        "outcome": "Enabled comprehensive automated synthesis of publication-grade literature reviews from selected documents."
    },
    {
        "date": "21-07-2026", "day": "Tuesday",
        "activity": "ReportLab PDF Compilation & Markdown Export",
        "work": "Built ReportLab PDF generation pipeline utilizing SimpleDocTemplate, custom paragraph styles, table formatters, and horizontal rules to compile saved reports into downloadable PDFs.",
        "outcome": "Delivered dual-format export functionality producing clean Markdown (.md) and professional PDF (.pdf) files."
    },
    {
        "date": "22-07-2026", "day": "Wednesday",
        "activity": "FastAPI Backend Architecture & Endpoints",
        "work": "Architected modular FastAPI backend across dedicated API routers: dashboard, documents, research, comparison, reports, settings, and evaluation. Enforced Pydantic validation.",
        "outcome": "Created a clean, documented RESTful backend with interactive Swagger documentation (/docs)."
    },
    {
        "date": "23-07-2026", "day": "Thursday",
        "activity": "File Upload & Duplicate Detection Endpoints",
        "work": "Implemented /api/documents/upload handling multi-file multipart uploads, SHA-256 hash duplication verification, safe disk writing, and triggering indexing pipelines.",
        "outcome": "Prevented redundant storage consumption and vector index corruption caused by duplicate document ingestion."
    },
    {
        "date": "24-07-2026", "day": "Friday",
        "activity": "Chat Session Persistence & History APIs",
        "work": "Created REST endpoints for session lifecycle management (/api/research/sessions), message persistence, and citation JSON serialization in SQLite.",
        "outcome": "Ensured user research sessions, conversation logs, and evidence citations persist across application restarts."
    },
    {
        "date": "25-07-2026", "day": "Saturday",
        "activity": "Frontend Architecture & Component Setup",
        "work": "Scaffolded React 19 + TypeScript frontend with Vite. Configured Tailwind CSS design system with custom navy, indigo, and violet palette, and responsive typography.",
        "outcome": "Established a professional commercial SaaS UI foundation with light and dark theme capabilities."
    },
    {
        "date": "27-07-2026", "day": "Monday",
        "activity": "Dashboard & Document Management UI Development",
        "work": "Developed DashboardPage showing live database counters and DocumentsPage featuring drag-and-drop file upload, status badges, chunk inspector modal, and delete actions.",
        "outcome": "Implemented polished document management interfaces providing full visibility into indexing states."
    },
    {
        "date": "28-07-2026", "day": "Tuesday",
        "activity": "3-Panel Research Workspace UI Implementation",
        "work": "Created 3-panel desktop layout: SourcesPanel (Left), ChatPanel (Center), and EvidencePanel (Right). Built collapsible panel behavior and smooth scrolling citation pills.",
        "outcome": "Constructed an intuitive research workspace enabling simultaneous source selection, conversation, and excerpt inspection."
    },
    {
        "date": "29-07-2026", "day": "Wednesday",
        "activity": "Comparison & Reports UI Pages Development",
        "work": "Developed ComparePage rendering the comparative contradiction matrix and ReportsPage featuring in-place Markdown editing, preview toggles, and PDF download triggers.",
        "outcome": "Completed specialized user interfaces for cross-document analysis and executive report generation."
    },
    {
        "date": "30-07-2026", "day": "Thursday",
        "activity": "Academic Evaluation Benchmark Implementation",
        "work": "Engineered EvaluationService and EvaluationPage implementing empirical metrics: HitRate@K, Mean Recall@K, and Citation Coverage Rate against indexed documents.",
        "outcome": "Equipped the platform with academic benchmarking tools demonstrating RAG retrieval efficacy."
    },
    {
        "date": "31-07-2026", "day": "Friday",
        "activity": "Comprehensive Automated Testing Suite (pytest)",
        "work": "Wrote 11 automated test cases in backend/tests covering database schema, PyMuPDF extraction, sentence chunking, FAISS isolation, API endpoints, and PDF compilation.",
        "outcome": "Achieved 100% test pass rate across the entire core processing, retrieval, and synthesis pipeline."
    },
    {
        "date": "01-08-2026", "day": "Saturday",
        "activity": "Production Frontend Build & SPA Integration",
        "work": "Executed Vite production build compiling TypeScript into optimized static assets (frontend/dist). Configured FastAPI StaticFiles mounting to serve UI and API from a single server.",
        "outcome": "Eliminated the need for separate frontend servers, enabling unified local execution on http://127.0.0.1:8000."
    },
    {
        "date": "03-08-2026", "day": "Monday",
        "activity": "One-Command Startup Automation (run.bat)",
        "work": "Developed robust Windows startup automation batch script (run.bat). Implemented automated checks for Python and Node.js, virtual environment activation, and browser auto-launch.",
        "outcome": "Enabled seamless 1-command startup from cold extraction to running web application."
    },
    {
        "date": "04-08-2026", "day": "Tuesday",
        "activity": "Final Project Demonstration & Internship Review",
        "work": "Presented live working demonstration of ResearchIQ to MegaViz Technologies CEO Ms. Kolla Geetha Madhuri. Verified multi-PDF Q&A, contradiction matrix, and executive PDF brief exports.",
        "outcome": "Successfully concluded 45 DAYS industrial internship with formal project approval and performance evaluation."
    }
]

# 15 Test Cases for Chapter 9
TEST_CASES = [
    {
        "id": "TC-01",
        "scenario": "Application Launch & Server Initialization",
        "input": "Execute run.bat or start Uvicorn server on 127.0.0.1:8000",
        "expected": "FastAPI starts successfully, SQLite DB initialized, frontend SPA served at root URL, health check returns 200 OK",
        "actual": "FastAPI started on port 8000; database tables created; health check returned status 'healthy' with status code 200",
        "status": "PASS"
    },
    {
        "id": "TC-02",
        "scenario": "Single & Multi-PDF Document Upload",
        "input": "Upload 3 academic PDFs (Solid_State_Batteries_Vance, Automotive_Cell_Degradation_Chen, Grid_EV_Integration_Jenkins)",
        "expected": "Files validated for .pdf format and size <= 20MB; saved to storage/uploads with unique UUID filename prefix",
        "actual": "All 3 PDF files accepted, validated, stored in storage/uploads, and initial document records created with status 'Uploaded'",
        "status": "PASS"
    },
    {
        "id": "TC-03",
        "scenario": "Valid PDF Ingestion & End-to-End Processing",
        "input": "Trigger ingestion pipeline for uploaded valid research PDF",
        "expected": "Status transitions from Uploaded -> Extracting -> Indexing -> Ready; page count and metadata updated in database",
        "actual": "Document status transitioned smoothly to 'Ready'; page count correctly registered as 3 pages; chunks saved in SQLite",
        "status": "PASS"
    },
    {
        "id": "TC-04",
        "scenario": "Invalid File Format & Size Upload Rejection",
        "input": "Attempt to upload non-PDF file (executable/script) or file exceeding 20 MB",
        "expected": "HTTP 400 Bad Request returned with descriptive error message; file rejected without disk storage",
        "actual": "Server returned HTTP 400 with detail 'Only PDF files are supported'; invalid file was safely rejected",
        "status": "PASS"
    },
    {
        "id": "TC-05",
        "scenario": "PyMuPDF Text & Page Number Extraction",
        "input": "Extract text from 3-page research document with mixed headings and paragraphs",
        "expected": "Text extracted per page preserving exact 1-indexed page number; title extracted from metadata or fallback filename stem",
        "actual": "Extracted text accurately separated into 3 page records with page_number attributes 1, 2, and 3 matching original document",
        "status": "PASS"
    },
    {
        "id": "TC-06",
        "scenario": "Scanned & Empty PDF Rejection Verification",
        "input": "Upload blank or image-only PDF containing zero extractable text characters (<50 chars threshold)",
        "expected": "Extraction raises PDFExtractionError with message indicating scanned/image-only document without OCR; status set to 'Failed'",
        "actual": "Extraction failed gracefully with error 'Scanned or image-only PDF: no extractable text found'; status recorded as 'Failed'",
        "status": "PASS"
    },
    {
        "id": "TC-07",
        "scenario": "Sentence-Boundary Overlapping Chunking",
        "input": "Page text with multiple paragraphs chunked at chunk_size=750 and chunk_overlap=150",
        "expected": "Chunks split along sentence boundaries; overlap retained between adjacent chunks; each chunk tagged with doc_id and page_no",
        "actual": "Chunks generated cleanly without breaking sentences mid-word; average chunk length 680 chars; overlap preserved successfully",
        "status": "PASS"
    },
    {
        "id": "TC-08",
        "scenario": "Dense Vector Embedding Generation",
        "input": "Batch of extracted chunk text strings passed to SentenceTransformer all-MiniLM-L6-v2",
        "expected": "Returns 2D float32 numpy array with shape (N, 384); all vectors L2 unit-normalized (norm = 1.0 +/- 1e-4)",
        "actual": "Generated 384-dimensional dense vectors; Euclidean norm verified equal to 1.0 for each vector across all test chunks",
        "status": "PASS"
    },
    {
        "id": "TC-09",
        "scenario": "FAISS Vector Indexing & ID Map Persistence",
        "input": "Add batch of normalized embeddings to FAISS IndexFlatIP; save to disk",
        "expected": "FAISS index updated; faiss_index.bin and chunk_id_map.json written to storage/indexes; vectors retrievable",
        "actual": "FAISS index saved successfully; ntotal matched total chunk count; binary index and JSON mapping reloaded cleanly",
        "status": "PASS"
    },
    {
        "id": "TC-10",
        "scenario": "SQLite FTS5 Keyword Indexing & BM25 Retrieval",
        "input": "Search for technical chemical term 'LLZO' or metric '4C' using FTS5 match query",
        "expected": "Returns relevant chunks containing exact terms ranked by BM25 relevance score",
        "actual": "FTS5 returned chunks containing exact keyword matches with BM25 rankings matching the expected target paragraphs",
        "status": "PASS"
    },
    {
        "id": "TC-11",
        "scenario": "Hybrid Reciprocal Rank Fusion & Document Isolation",
        "input": "Execute hybrid query with selected_document_ids restricted to Document 1 only",
        "expected": "Dense and sparse candidate lists merged via RRF score = sum(1/(60+rank)); 100% of returned chunks belong to Document 1",
        "actual": "All top-K retrieved chunks belonged exclusively to Document 1; chunks from Document 2 and 3 were completely excluded",
        "status": "PASS"
    },
    {
        "id": "TC-12",
        "scenario": "Evidence-Grounded RAG Answer Generation",
        "input": "Inquiry: 'What capacity retention was achieved under 4C fast charging?' with Document 1 selected",
        "expected": "LLM generates structured response citing [Solid-State Batteries Vance, p. 2]; claims 84.5% retention at 2,000 cycles",
        "actual": "Answer correctly stated 84.5% capacity retention after 2,000 cycles at 4C with exact citation [Solid-State Batteries Vance, p. 2]",
        "status": "PASS"
    },
    {
        "id": "TC-13",
        "scenario": "Multi-Document Contradiction Analysis",
        "input": "Compare Document 1 (Vance 2024) and Document 2 (Chen 2023) on fast-charging degradation limits",
        "expected": "Identifies empirical conflict: Doc 1 claims 2,000 cycles at 45°C vs Doc 2 claims 850 cycles with decomposition above 40°C",
        "actual": "Comparison matrix classified cycle life and temperature claims as 'Potential Contradiction' with citations to both papers",
        "status": "PASS"
    },
    {
        "id": "TC-14",
        "scenario": "Interactive Citation Explorer Navigation",
        "input": "User clicks citation badge '[Solid-State Batteries Vance, p. 2]' in chat panel",
        "expected": "Right Evidence Explorer panel expands; scrolls smoothly to chunk; highlights exact excerpt with active border",
        "actual": "Evidence panel opened automatically, navigated to the referenced chunk, and applied the visual highlight border ring",
        "status": "PASS"
    },
    {
        "id": "TC-15",
        "scenario": "Executive Research Brief Generation & PDF Export",
        "input": "Generate 13-section research brief and request PDF download via /api/reports/{id}/export?format=pdf",
        "expected": "Generates 13-section Markdown brief; ReportLab compiles valid PDF; browser downloads styled .pdf document",
        "actual": "13-section report generated; ReportLab built PDF with headers and tables; downloaded PDF binary verified intact (>500KB)",
        "status": "PASS"
    }
]
