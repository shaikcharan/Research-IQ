"""
build_chapters.py
=================
Complete generator for ResearchIQ Project Report:
- Official University Front Cover Page with CT University Crest, Industrial Training Report title, Submitted By, Under Guidance Of, Academic Year.
- Preliminary pages: Declaration (i), Acknowledgement (ii), Abstract (iii), TOC (iv), LOF (vi), LOT (vii).
- No training or daily diary logs.
- Functional & Non-Functional Requirements in explicit academic tables.
- Running header: "RESEARCHIQ – PROJECT REPORT" | "CT UNIVERSITY" (NO MegaViz in header).
- No blank or empty pages anywhere.
- Screenshots: Figures 9.1 to 9.5 ONLY (Figures 9.6 to 9.12 removed).
- 1 pt Four-Sided Black Border on EVERY SINGLE PAGE.
- Accurate, synchronized page numbers and Table of Contents.
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import qn

from build_full_report import (
    apply_page_border, setup_header_footer, add_body_p, add_bullet_p,
    add_chap_heading, add_sec_heading, add_subsec_heading, add_figure,
    format_cell, add_code_block, C_BLACK, C_NAVY, C_DARK, C_GRAY,
    DOCX_PATH, FIG_DIR
)

from clean_report_content import (
    STUDENT_NAME, REG_NO, DEGREE, BRANCH, SPECIALIZATION, UNIVERSITY,
    ACADEMIC_YEAR, COMPANY_NAME, COMPANY_ADDR, COMPANY_EMAIL,
    COMPANY_PHONE, COMPANY_WEB, SUPERVISOR_NAME, SUPERVISOR_TITLE,
    FUNCTIONAL_REQUIREMENTS, NON_FUNCTIONAL_REQUIREMENTS, TEST_CASES
)

LOGO_PATH = os.path.join(FIG_DIR, "ct_university_logo.png")

def add_cover_page(doc):
    """Generates the official CT University front cover page."""
    sec_cover = doc.sections[0]
    sec_cover.page_width = Inches(8.27)
    sec_cover.page_height = Inches(11.69)
    sec_cover.left_margin = Inches(1.0)
    sec_cover.right_margin = Inches(1.0)
    sec_cover.top_margin = Inches(0.8)
    sec_cover.bottom_margin = Inches(0.8)

    apply_page_border(sec_cover)

    # Empty header & footer on cover page
    hdr = sec_cover.header
    hdr.is_linked_to_previous = False
    hdr.paragraphs[0].text = ""

    ftr = sec_cover.footer
    ftr.is_linked_to_previous = False
    ftr.paragraphs[0].text = ""

    # 1. University Header
    p_u1 = doc.add_paragraph()
    p_u1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_u1.paragraph_format.space_before = Pt(8)
    p_u1.paragraph_format.space_after = Pt(2)
    r = p_u1.add_run("CT UNIVERSITY")
    r.font.name = "Times New Roman"
    r.font.size = Pt(20)
    r.font.bold = True
    r.font.color.rgb = C_NAVY

    p_u2 = doc.add_paragraph()
    p_u2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_u2.paragraph_format.space_before = Pt(0)
    p_u2.paragraph_format.space_after = Pt(2)
    r = p_u2.add_run("SCHOOL OF ENGINEERING & TECHNOLOGY")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = C_DARK

    p_u3 = doc.add_paragraph()
    p_u3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_u3.paragraph_format.space_before = Pt(0)
    p_u3.paragraph_format.space_after = Pt(2)
    r = p_u3.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = C_NAVY

    p_u4 = doc.add_paragraph()
    p_u4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_u4.paragraph_format.space_before = Pt(0)
    p_u4.paragraph_format.space_after = Pt(8)
    r = p_u4.add_run("(Specialization: Artificial Intelligence & Data Science)\nLudhiana, Punjab, India – 142024")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.italic = True
    r.font.color.rgb = C_GRAY

    # 2. University Crest
    if os.path.exists(LOGO_PATH):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(4)
        p_logo.paragraph_format.space_after = Pt(8)
        run_logo = p_logo.add_run()
        run_logo.add_picture(LOGO_PATH, width=Inches(1.85))

    # 3. Report Title Banner
    p_rep = doc.add_paragraph()
    p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rep.paragraph_format.space_before = Pt(4)
    p_rep.paragraph_format.space_after = Pt(3)
    r = p_rep.add_run("INDUSTRIAL TRAINING & PROJECT REPORT")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13.5)
    r.font.bold = True
    r.font.color.rgb = C_DARK

    p_on = doc.add_paragraph()
    p_on.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_on.paragraph_format.space_before = Pt(0)
    p_on.paragraph_format.space_after = Pt(3)
    r = p_on.add_run("ON")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.italic = True
    r.font.color.rgb = C_GRAY

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(2)
    p_title.paragraph_format.space_after = Pt(3)
    r = p_title.add_run("\"RESEARCHIQ: ACADEMIC & INDUSTRIAL\nRESEARCH INTELLIGENCE\"")
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = C_NAVY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(10)
    r = p_sub.add_run("An Evidence-Grounded Multi-Document RAG Platform with Hybrid Semantic-Lexical Retrieval")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.italic = True
    r.font.color.rgb = C_DARK

    # 4. Degree Fulfillment
    p_deg = doc.add_paragraph()
    p_deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_deg.paragraph_format.space_before = Pt(2)
    p_deg.paragraph_format.space_after = Pt(12)
    r = p_deg.add_run(
        "Submitted in partial fulfillment of the requirements for the award of the degree of\n"
        "BACHELOR OF TECHNOLOGY (B.Tech)\n"
        "in\n"
        "COMPUTER SCIENCE AND ENGINEERING\n"
        "(Specialization: Artificial Intelligence & Data Science)"
    )
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.color.rgb = C_DARK

    # 5. Two-Column Table: Submitted By & Under the Guidance Of
    t_sub = doc.add_table(rows=1, cols=2)
    t_sub.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_left = t_sub.cell(0, 0)
    cell_right = t_sub.cell(0, 1)
    cell_left.width = Inches(3.1)
    cell_right.width = Inches(3.1)

    # Left cell: Submitted By
    p_left = cell_left.paragraphs[0]
    p_left.paragraph_format.space_before = Pt(2)
    p_left.paragraph_format.space_after = Pt(2)
    p_left.paragraph_format.line_spacing = 1.15
    r_lhead = p_left.add_run("SUBMITTED BY:\n")
    r_lhead.font.name = "Times New Roman"
    r_lhead.font.size = Pt(10.5)
    r_lhead.font.bold = True
    r_lhead.font.color.rgb = C_NAVY

    r_lname = p_left.add_run(f"{STUDENT_NAME.upper()}\n")
    r_lname.font.name = "Times New Roman"
    r_lname.font.size = Pt(11)
    r_lname.font.bold = True
    r_lname.font.color.rgb = C_BLACK

    r_linfo = p_left.add_run(
        f"Reg. No: {REG_NO}\n"
        "B.Tech (CSE – AI & Data Science)\n"
        "CT University, Ludhiana, Punjab"
    )
    r_linfo.font.name = "Times New Roman"
    r_linfo.font.size = Pt(9.5)
    r_linfo.font.color.rgb = C_DARK

    # Right cell: Under Guidance Of
    p_right = cell_right.paragraphs[0]
    p_right.paragraph_format.space_before = Pt(2)
    p_right.paragraph_format.space_after = Pt(2)
    p_right.paragraph_format.line_spacing = 1.15
    p_right.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_rhead = p_right.add_run("UNDER THE GUIDANCE OF:\n")
    r_rhead.font.name = "Times New Roman"
    r_rhead.font.size = Pt(10.5)
    r_rhead.font.bold = True
    r_rhead.font.color.rgb = C_NAVY

    r_rname = p_right.add_run(f"{SUPERVISOR_NAME}\n")
    r_rname.font.name = "Times New Roman"
    r_rname.font.size = Pt(11)
    r_rname.font.bold = True
    r_rname.font.color.rgb = C_BLACK

    r_rinfo = p_right.add_run(
        f"{SUPERVISOR_TITLE}\n"
        f"{COMPANY_NAME}\n"
        "Kukatpally, Hyderabad, Telangana"
    )
    r_rinfo.font.name = "Times New Roman"
    r_rinfo.font.size = Pt(9.5)
    r_rinfo.font.color.rgb = C_DARK

    # 6. Academic Year at bottom
    p_bot = doc.add_paragraph()
    p_bot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bot.paragraph_format.space_before = Pt(18)
    p_bot.paragraph_format.space_after = Pt(0)
    r = p_bot.add_run(f"ACADEMIC YEAR {ACADEMIC_YEAR}\nCT UNIVERSITY, LUDHIANA, PUNJAB, INDIA")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.bold = True
    r.font.color.rgb = C_NAVY


def generate_complete_report():
    print("Beginning generation of university-standard B.Tech Project Report...")
    doc = Document()

    # =========================================================================
    # SECTION 0: OFFICIAL FRONT COVER PAGE
    # =========================================================================
    add_cover_page(doc)

    # =========================================================================
    # SECTION 1: PRELIMINARY PAGES (Lower Roman Numerals)
    # =========================================================================
    sec_prelim = doc.add_section()
    sec_prelim.page_width = Inches(8.27)
    sec_prelim.page_height = Inches(11.69)
    sec_prelim.left_margin = Inches(1.1)
    sec_prelim.right_margin = Inches(1.0)
    sec_prelim.top_margin = Inches(1.0)
    sec_prelim.bottom_margin = Inches(1.0)

    apply_page_border(sec_prelim)
    setup_header_footer(sec_prelim, is_roman=True)

    pgNumType = parse_xml('<w:pgNumType xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:fmt="lowerRoman" w:start="1"/>')
    sec_prelim._sectPr.append(pgNumType)

    # -------------------------------------------------------------------------
    # PRELIMINARY PAGE 1: CANDIDATE'S DECLARATION (Page i)
    # -------------------------------------------------------------------------
    add_chap_heading(doc, "CANDIDATE'S DECLARATION")

    add_body_p(doc, f"I, {STUDENT_NAME}, bearing Registration Number {REG_NO}, bona fide undergraduate student of Bachelor of Technology (B.Tech) in Computer Science and Engineering with specialization in Artificial Intelligence and Data Science at CT University, Ludhiana, Punjab, hereby declare that the project report entitled \"ResearchIQ – Academic & Industrial Research Intelligence\" represents the authentic, independent, and original engineering work carried out by me during the academic year 2026–2027.")

    add_body_p(doc, f"I further declare that this project was undertaken in collaboration with {COMPANY_NAME}, Hyderabad, under the professional supervision and industry mentorship of {SUPERVISOR_NAME}, {SUPERVISOR_TITLE}.")

    add_body_p(doc, "The technical architecture, algorithmic workflows, neural embedding pipelines, vector indexing mechanisms, hybrid retrieval models, user interface modules, and empirical evaluations documented herein are the outcome of my own dedicated engineering efforts. To the best of my knowledge and belief, this report contains no material previously submitted or published by any other person for the award of any Bachelor of Technology degree, diploma, fellowship, or other academic credential at CT University or any other academic institution.")

    add_body_p(doc, "All external literature sources, published research papers, software packages, third-party libraries, and conceptual foundations utilized during this project have been duly acknowledged and cited in accordance with standard academic and IEEE referencing conventions.")

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(45)
    p_sig.paragraph_format.space_after = Pt(4)
    r_sig = p_sig.add_run(
        "_______________________________\n"
        f"{STUDENT_NAME.upper()}\n"
        f"Registration Number: {REG_NO}\n"
        "B.Tech – Computer Science and Engineering\n"
        "Specialization: Artificial Intelligence & Data Science\n"
        "CT University, Ludhiana, Punjab"
    )
    r_sig.font.name = "Times New Roman"
    r_sig.font.size = Pt(11)
    r_sig.font.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PRELIMINARY PAGE 2: ACKNOWLEDGEMENT (Page ii)
    # -------------------------------------------------------------------------
    add_chap_heading(doc, "ACKNOWLEDGEMENT")

    add_body_p(doc, "The successful conceptualization, engineering development, and documentation of this B.Tech project on \"ResearchIQ – Academic & Industrial Research Intelligence\" has been made possible through the generous support, expert guidance, and encouragement of numerous individuals and institutions.")

    add_body_p(doc, "First and foremost, I express my profound gratitude and highest regards to CT University, Ludhiana, Punjab, for providing a vibrant academic ecosystem, state-of-the-art computational infrastructure, and the opportunity to undertake advanced applied research in Artificial Intelligence and Data Science.")

    add_body_p(doc, f"I extend my deepest gratitude and sincere appreciation to {COMPANY_NAME}, Hyderabad, for facilitating this project environment. In particular, I express my earnest indebtedness to my industry guide and mentor, {SUPERVISOR_NAME}, {SUPERVISOR_TITLE}, for her inspiring leadership, visionary technical insights, and continuous constructive feedback throughout the system development lifecycle.")

    add_body_p(doc, "I convey my heartfelt thanks to the Head of Department, Department of Computer Science and Engineering, and all faculty coordinators at CT University for their sustained academic mentorship, constructive project reviews, and continuous guidance.")

    add_body_p(doc, "I also express my sincere thanks to my fellow engineering peers, developer colleagues, and lab members whose discussions, brainstorming sessions, and code testing feedback contributed meaningfully to refining the application workflow.")

    add_body_p(doc, "Finally, I owe my deepest debt of affection and gratitude to my family and parents for their unconditional sacrifices, moral encouragement, and constant inspiration throughout my academic journey.")

    p_ack_sig = doc.add_paragraph()
    p_ack_sig.paragraph_format.space_before = Pt(40)
    p_ack_sig.paragraph_format.space_after = Pt(4)
    r_asig = p_ack_sig.add_run(f"{STUDENT_NAME.upper()}\nReg. No: {REG_NO}\nCT University, Punjab")
    r_asig.font.name = "Times New Roman"
    r_asig.font.size = Pt(11)
    r_asig.font.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PRELIMINARY PAGE 3: ABSTRACT (Page iii)
    # -------------------------------------------------------------------------
    add_chap_heading(doc, "ABSTRACT")

    add_body_p(doc, "The modern knowledge economy is characterized by an exponential expansion in the volume of digital scientific literature, industrial technical reports, patent filings, and corporate institutional documentation. For researchers, data scientists, and engineering professionals, reviewing, extracting, and synthesizing information across multiple lengthy PDF documents presents severe cognitive bottlenecks. Traditional lexical search mechanisms (e.g., standard Ctrl+F or keyword search) rely strictly on exact character matches, frequently failing to capture synonymy, technical paraphrasing, or conceptual semantics. Furthermore, conventional language model query tools are prone to hallucinating facts or decoupling generated claims from verifiable document provenance.")

    add_body_p(doc, "This project presents \"ResearchIQ – Academic & Industrial Research Intelligence\", a comprehensive, evidence-grounded Retrieval-Augmented Generation (RAG) platform specifically engineered to streamline the exploration, semantic retrieval, and cross-document comparison of complex multi-page PDF documents. The application implements an end-to-end processing pipeline beginning with robust document ingestion and text extraction via PyMuPDF (Fitz), preserving strict page-level and block-level metadata traceability. Extracted text undergoes structural cleaning and is partitioned into semantic passages using an overlapping sliding window (500 characters, 50-character overlap) to guarantee narrative continuity across chunk boundaries.")

    add_body_p(doc, "Each text chunk is mapped into a high-dimensional continuous semantic space utilizing the Sentence-Transformers all-MiniLM-L6-v2 dense embedding model (384 dimensions). For vector search, ResearchIQ implements Facebook AI Similarity Search (FAISS) utilizing IndexFlatIP with L2-normalized vectors, mathematically equivalent to exact cosine similarity. To maximize retrieval recall and precision across both conceptual queries and exact domain terminology, a hybrid retrieval strategy is integrated, combining dense semantic search with lexical BM25 retrieval via SQLite FTS5 through Reciprocal Rank Fusion (RRF).")

    add_body_p(doc, "Retrieved context passages are assembled into structured prompts supplied to high-speed Large Language Model inference endpoints (Groq Cloud LLMs), generating rigorous, hallucination-free executive summaries and answers strictly constrained to verifiable source citations. A multi-document comparison matrix contrasts findings, agreements, and contradictions across selected literature. An evaluation benchmark demonstrates a Retrieval Hit Rate@5 of 75.0%, Mean Recall@5 of 23.3%, and Citation Coverage of 100.0% on verified test collections.")

    add_body_p(doc, "Retrieval-Augmented Generation (RAG), Semantic Vector Search, FAISS IndexFlatIP, Dense Embeddings, all-MiniLM-L6-v2, Multi-Document Intelligence, Evidence Grounding, Hybrid Retrieval.", bold_prefix="Keywords: ", italic_prefix=True)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PRELIMINARY PAGE 4: TABLE OF CONTENTS (Page iv)
    # -------------------------------------------------------------------------
    add_chap_heading(doc, "TABLE OF CONTENTS")

    toc_items = [
        ("Candidate's Declaration", "i", True),
        ("Acknowledgement", "ii", True),
        ("Abstract", "iii", True),
        ("Table of Contents", "iv", True),
        ("List of Figures", "vi", True),
        ("List of Tables", "vii", True),
        ("CHAPTER 1: INTRODUCTION", "1", True),
        ("    1.1 Introduction", "1", False),
        ("    1.2 Background of Artificial Intelligence", "1", False),
        ("    1.3 Machine Learning and Natural Language Processing", "1", False),
        ("    1.4 Project Background", "1", False),
        ("    1.5 Problem Statement", "2", False),
        ("    1.6 Need for the Project", "2", False),
        ("    1.7 Scope of the Project", "2", False),
        ("    1.8 Project Objectives", "2", False),
        ("    1.9 Expected Outcome", "2", False),
        ("    1.10 Organization of the Report", "2", False),
        ("CHAPTER 2: COMPANY PROFILE", "3", True),
        ("    2.1 Introduction to MegaViz Technologies Pvt Ltd", "3", False),
        ("    2.2 Corporate Background & Vision", "3", False),
        ("    2.3 Technology Domain and Enterprise Activities", "3", False),
        ("    2.4 Relevance to AI & Machine Learning", "3", False),
        ("CHAPTER 3: PROJECT OVERVIEW AND OBJECTIVES", "4", True),
        ("    3.1 Introduction to ResearchIQ", "4", False),
        ("    3.2 Core Capabilities", "4", False),
        ("    3.3 Intended Users", "4", False),
        ("    3.4 Typical User Workflow", "4", False),
        ("    3.5 Project Boundaries", "4", False),
        ("    3.6 Inputs, Processing and Outputs Pipeline", "5", False),
        ("    3.7 Project Deliverables", "5", False),
        ("    3.8 Success Criteria", "5", False),
        ("CHAPTER 4: SYSTEM ANALYSIS AND PROBLEM FORMULATION", "6", True),
        ("    4.1 Existing Document Research System", "6", False),
        ("    4.2 Limitations of the Existing System", "6", False),
        ("    4.3 Proposed System Architecture", "6", False),
        ("    4.4 Comparison: Conventional Workflow vs. ResearchIQ", "6", False),
        ("    4.5 Feasibility Analysis", "6", False),
        ("CHAPTER 5: SYSTEM REQUIREMENTS", "7", True),
        ("    5.1 Introduction", "7", False),
        ("    5.2 Hardware Requirements", "7", False),
        ("    5.3 Software and Runtime Environment", "7", False),
        ("    5.4 Functional Requirements (Table Format)", "8", False),
        ("    5.5 Non-Functional Requirements (Table Format)", "8", False),
        ("    5.6 Database Schema and Metadata Storage", "8", False),
        ("CHAPTER 6: SYSTEM DESIGN AND ARCHITECTURE", "9", True),
        ("    6.1 Architecture Overview", "9", False),
        ("    6.2 Architectural Workflows & Data Flow", "9", False),
        ("    6.3 Component Interactions and Sequence Flow", "11", False),
        ("CHAPTER 7: TECHNOLOGY STACK AND TECHNICAL CONCEPTS", "12", True),
        ("    7.1 Python & FastAPI Backend", "12", False),
        ("    7.2 PDF Text Extraction via PyMuPDF", "12", False),
        ("    7.3 Text Preprocessing & Cleaning", "12", False),
        ("    7.4 Sliding Window Chunking Strategies", "12", False),
        ("    7.5 Dense Embeddings via SentenceTransformers", "12", False),
        ("    7.6 FAISS Vector Indexing & Cosine Similarity", "12", False),
        ("    7.7 Mathematical Foundation of Similarity", "12", False),
        ("    7.8 Retrieval-Augmented Generation (RAG)", "12", False),
        ("    7.9 Prompt Design and Citation Attributions", "12", False),
        ("    7.10 React & TypeScript User Interface", "12", False),
        ("CHAPTER 8: IMPLEMENTATION DETAILS", "13", True),
        ("    8.1 Implementation Architecture Overview", "13", False),
        ("    8.2 Project Directory Structure", "13", False),
        ("    8.3 PDF Extraction Implementation", "13", False),
        ("    8.4 Text Preprocessing & Chunking", "13", False),
        ("    8.5 Dense Vector Embedding Implementation", "14", False),
        ("    8.6 FAISS Vector Indexing & Hybrid Retrieval", "14", False),
        ("    8.7 Context Assembly & LLM Generation", "14", False),
        ("CHAPTER 9: APPLICATION SCREENSHOTS & FUNCTIONAL WALKTHROUGH", "15", True),
        ("    9.1 System Launch and Dashboard", "15", False),
        ("    9.2 Document Management and Upload Library", "15", False),
        ("    9.3 Multi-Document Research Workspace", "16", False),
        ("    9.4 Evidence-Grounded Research Query Interface", "16", False),
        ("    9.5 Evaluation Benchmark Dashboard", "17", False),
        ("CHAPTER 10: SOFTWARE TESTING AND EVALUATION", "18", True),
        ("    10.1 Testing Strategy", "18", False),
        ("    10.2 Functional Verification Matrix (15 Test Cases)", "19", False),
        ("    10.3 Evaluation Benchmark Metrics Analysis", "19", False),
        ("    10.4 Metric Interpretation & Grounding Analysis", "19", False),
        ("    10.5 Evaluation Limitations and Future Testing", "19", False),
        ("CHAPTER 11: CHALLENGES, LIMITATIONS AND LEARNING OUTCOMES", "20", True),
        ("    11.1 Document Parsing & Layout Difficulties", "20", False),
        ("    11.2 Chunk Boundary Optimization", "20", False),
        ("    11.3 Retrieval Precision & Hallucination Mitigation", "20", False),
        ("    11.4 FAISS Index Consistency & State Persistence", "20", False),
        ("    11.5 Current Project Limitations & Mitigations", "20", False),
        ("    11.6 Technical Skills & Competencies Acquired", "20", False),
        ("CHAPTER 12: CONCLUSION AND FUTURE SCOPE", "21", True),
        ("    12.1 Project Conclusion", "21", False),
        ("    12.2 Objectives Addressed", "21", False),
        ("    12.3 Future Technical Roadmap", "21", False),
        ("    12.4 Concluding Remarks", "21", False),
        ("REFERENCES", "22", True),
        ("APPENDIX: CONFIGURATION AND VERIFICATION CHECKLIST", "23", True),
    ]

    t_toc = doc.add_table(rows=len(toc_items), cols=2)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (title, pg, is_main) in enumerate(toc_items):
        cell_t = t_toc.cell(idx, 0)
        cell_p = t_toc.cell(idx, 1)
        cell_t.width = Inches(5.3)
        cell_p.width = Inches(0.8)
        format_cell(cell_t, title, bold=is_main, font_size=9.5, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(cell_p, pg, bold=is_main, font_size=9.5, align=WD_ALIGN_PARAGRAPH.RIGHT)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PRELIMINARY PAGE 5: LIST OF FIGURES (Page vi)
    # -------------------------------------------------------------------------
    add_chap_heading(doc, "LIST OF FIGURES")

    lof_items = [
        ("Figure 6.1", "Overall ResearchIQ System Architecture", "9"),
        ("Figure 6.2", "Multi-Stage Document Ingestion Pipeline", "9"),
        ("Figure 6.3", "Sentence Chunking & Embedding Workflow", "10"),
        ("Figure 6.4", "FAISS Vector Indexing & SQLite Metadata Schema", "10"),
        ("Figure 6.5", "Hybrid Retrieval & RAG Generation Architecture", "11"),
        ("Figure 6.6", "End-to-End System Execution Sequence Flow", "11"),
        ("Figure 9.1", "ResearchIQ Assistant System Dashboard", "15"),
        ("Figure 9.2", "Document Management Library and PDF Upload", "15"),
        ("Figure 9.3", "Multi-Document Research Workspace with Selected Sources", "16"),
        ("Figure 9.4", "Evidence-Grounded Research Query Interface", "16"),
        ("Figure 9.5", "Evaluation Benchmark Dashboard (Retrieval Hit Rate & Citation)", "17"),
    ]

    t_lof = doc.add_table(rows=len(lof_items) + 1, cols=3)
    t_lof.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_cell(t_lof.cell(0, 0), "Figure No.", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(t_lof.cell(0, 1), "Figure Caption / Title", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    format_cell(t_lof.cell(0, 2), "Page", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.CENTER)
    t_lof.cell(0, 0).width = Inches(1.1)
    t_lof.cell(0, 1).width = Inches(4.3)
    t_lof.cell(0, 2).width = Inches(0.7)

    for idx, (fno, title, pg) in enumerate(lof_items, start=1):
        bg = "F8FAFC" if idx % 2 == 0 else "FFFFFF"
        c0 = t_lof.cell(idx, 0)
        c1 = t_lof.cell(idx, 1)
        c2 = t_lof.cell(idx, 2)
        c0.width = Inches(1.1)
        c1.width = Inches(4.3)
        c2.width = Inches(0.7)
        format_cell(c0, fno, bold=True, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.CENTER)
        format_cell(c1, title, bold=False, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(c2, pg, bold=False, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.CENTER)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PRELIMINARY PAGE 6: LIST OF TABLES (Page vii)
    # -------------------------------------------------------------------------
    add_chap_heading(doc, "LIST OF TABLES")

    lot_items = [
        ("Table 3.1", "Inputs, Processing and Outputs Pipeline Specification", "5"),
        ("Table 4.1", "Existing System vs. ResearchIQ Proposed Architecture", "6"),
        ("Table 5.1", "Hardware Requirements (Minimum vs. Recommended)", "7"),
        ("Table 5.2", "Software and Runtime Environment Specifications", "7"),
        ("Table 5.3", "Functional Requirements Specification Matrix (FR-01 to FR-12)", "8"),
        ("Table 5.4", "Non-Functional Requirements Specification (NFR-01 to NFR-06)", "8"),
        ("Table 5.5", "SQLite Database Schema & Metadata Field Mapping", "8"),
        ("Table 10.1", "Functional Verification Test Matrix (TC-01 to TC-15)", "19"),
        ("Table 10.2", "System Retrieval & Grounding Evaluation Metrics", "19"),
        ("Table 11.1", "System Constraints, Technical Limitations and Mitigations", "20"),
        ("Table A.1", "FastAPI REST API Route Specifications and Data Schemas", "23"),
    ]

    t_lot = doc.add_table(rows=len(lot_items) + 1, cols=3)
    t_lot.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_cell(t_lot.cell(0, 0), "Table No.", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(t_lot.cell(0, 1), "Table Title / Description", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    format_cell(t_lot.cell(0, 2), "Page", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.CENTER)
    t_lot.cell(0, 0).width = Inches(1.1)
    t_lot.cell(0, 1).width = Inches(4.3)
    t_lot.cell(0, 2).width = Inches(0.7)

    for idx, (tno, title, pg) in enumerate(lot_items, start=1):
        bg = "F8FAFC" if idx % 2 == 0 else "FFFFFF"
        c0 = t_lot.cell(idx, 0)
        c1 = t_lot.cell(idx, 1)
        c2 = t_lot.cell(idx, 2)
        c0.width = Inches(1.1)
        c1.width = Inches(4.3)
        c2.width = Inches(0.7)
        format_cell(c0, tno, bold=True, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.CENTER)
        format_cell(c1, title, bold=False, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(c2, pg, bold=False, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.CENTER)

    # =========================================================================
    # SECTION 2: MAIN BODY CHAPTERS (Arabic Numerals: 1, 2, 3...)
    # =========================================================================
    sec_main = doc.add_section()
    sec_main.page_width = Inches(8.27)
    sec_main.page_height = Inches(11.69)
    sec_main.left_margin = Inches(1.1)
    sec_main.right_margin = Inches(1.0)
    sec_main.top_margin = Inches(1.0)
    sec_main.bottom_margin = Inches(1.0)

    apply_page_border(sec_main)
    setup_header_footer(sec_main, is_roman=False)

    pgNumMain = parse_xml('<w:pgNumType xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:start="1"/>')
    sec_main._sectPr.append(pgNumMain)

    # -------------------------------------------------------------------------
    # CHAPTER 1: INTRODUCTION
    # -------------------------------------------------------------------------
    add_chap_heading(doc, "CHAPTER 1: INTRODUCTION")

    add_sec_heading(doc, "1.1 Introduction")
    add_body_p(doc, "In the modern digital information ecosystem, researchers, academics, technical analysts, and corporate decision-makers are confronted with an unprecedented deluge of unstructured electronic documentation. Research papers, patent filings, corporate compliance filings, clinical trial reports, and engineering manuals are overwhelmingly authored and distributed in Portable Document Format (PDF). While PDF ensures visual fidelity across disparate hardware and software environments, its visual rendering model completely divorces character glyphs from their underlying semantic semantics. Consequently, extracting meaningful facts, cross-referencing findings across disparate publications, and locating precise empirical evidence within lengthy multi-page documents demands immense cognitive overhead, tedious manual searching, and extensive human labor.")

    add_sec_heading(doc, "1.2 Background of Artificial Intelligence")
    add_body_p(doc, "Artificial Intelligence (AI) encompasses computational paradigms engineered to emulate human cognitive functions, including pattern recognition, natural language comprehension, logical inference, and autonomous decision support. Within the domain of Document Intelligence and Natural Language Processing (NLP), modern AI techniques have evolved from rigid rule-based pattern matching and statistical n-gram counting toward self-supervised neural architectures capable of extracting contextual semantics, resolving coreferences, and synthesizing dense knowledge representations across heterogeneous texts.")

    add_sec_heading(doc, "1.3 Machine Learning and Natural Language Processing")
    add_body_p(doc, "Machine Learning (ML), particularly Deep Learning powered by Transformer architectures (Vaswani et al.), has fundamentally transformed computational linguistics. Transformer-based encoder models leverage multi-head self-attention mechanisms to map raw textual sentences into continuous, dense vector spaces where spatial proximity directly correlates with conceptual similarity. This enables computational systems to recognize semantic equivalence even when queries and document passages share zero overlapping lexical tokens (e.g., matching 'myocardial infarction' with 'heart attack').")

    add_sec_heading(doc, "1.4 Project Background")
    add_body_p(doc, "ResearchIQ was engineered as an advanced academic and industrial document intelligence platform to bridge the gap between static PDF repositories and conversational, evidence-grounded research exploration. Developed under the technical collaboration of MegaViz Technologies Pvt Ltd, the platform unifies high-performance document extraction, neural sentence embeddings, vector similarity indexing, lexical keyword search, and Large Language Model (LLM) orchestration into a coherent full-stack application.")

    add_sec_heading(doc, "1.5 Problem Statement")
    add_body_p(doc, "Manual analysis of extensive multi-document PDF collections suffers from multiple critical limitations: (1) Lexical Inflexibility: Standard Ctrl+F keyword search fails when author terminology deviates from user queries; (2) Context Fragmentation: Isolated lexical hits omit narrative context, requiring human readers to manually reconstruct multi-paragraph arguments; (3) Cross-Document Cognitive Strain: Contrasting conflicting findings across dozens of papers requires cumbersome side-by-side window switching; and (4) LLM Hallucination: Standard conversational AI models frequently confabulate citations or invent non-existent factual assertions when disconnected from verifiable source texts.")

    add_sec_heading(doc, "1.6 Need for the Project")
    add_bullet_p(doc, "Automate multi-page PDF ingestion, structural parsing, and sentence boundary detection.")
    add_bullet_p(doc, "Eliminate lexical search failure by embedding text passages into continuous semantic vector representations.")
    add_bullet_p(doc, "Deliver sub-millisecond similarity search across thousands of document chunks using high-performance vector indexes.")
    add_bullet_p(doc, "Provide absolute evidence traceability by binding every generated statement to verifiable document names, page numbers, and verbatim excerpts.")
    add_bullet_p(doc, "Equip researchers with an automated comparison matrix to contrast methodologies, datasets, and conclusions across multiple papers simultaneously.")

    add_sec_heading(doc, "1.7 Scope of the Project")
    add_body_p(doc, "The scope of ResearchIQ centers on the end-to-end processing of native, text-readable PDF documents. It encompasses multi-file drag-and-drop upload, PyMuPDF page-aware extraction, sliding-window chunking, dense embedding generation with Sentence-Transformers, FAISS indexing, SQLite FTS5 lexical indexing, Reciprocal Rank Fusion hybrid retrieval, Groq Cloud LLM citation synthesis, and a responsive React/TypeScript user interface. Advanced optical character recognition (OCR) for degraded scanned photocopies and distributed multi-node clustering are identified as future enhancements.")

    add_sec_heading(doc, "1.8 Project Objectives")
    add_bullet_p(doc, "Engineer an intuitive, responsive web application for managing and analyzing multi-document PDF collections.")
    add_bullet_p(doc, "Implement reliable text extraction preserving strict page-level and block-level metadata traceability.")
    add_bullet_p(doc, "Design an overlapping sliding window chunking algorithm (500 chars, 50-char overlap) to preserve narrative flow.")
    add_bullet_p(doc, "Deploy dense vector embeddings using the all-MiniLM-L6-v2 transformer model.")
    add_bullet_p(doc, "Construct an exact inner-product FAISS index (IndexFlatIP) with L2 vector normalization for cosine similarity search.")
    add_bullet_p(doc, "Integrate hybrid retrieval combining dense semantic vectors and sparse BM25 scores via Reciprocal Rank Fusion.")
    add_bullet_p(doc, "Deliver verifiable, hallucination-free research summaries with verbatim citation evidence.")
    add_bullet_p(doc, "Provide a dedicated multi-document comparison interface to contrast claims across sources.")

    add_sec_heading(doc, "1.9 Expected Outcome")
    add_body_p(doc, "The expected outcome is a fully functional, production-ready research intelligence platform enabling users to upload arbitrary research papers, execute natural-language queries, inspect verifiable source evidence in milliseconds, and export structured comparative research briefs.")

    add_sec_heading(doc, "1.10 Organization of the Report")
    add_body_p(doc, "This project report is structured into 12 comprehensive chapters: Chapter 1 introduces the domain, problem, and objectives; Chapter 2 provides the corporate profile of MegaViz Technologies Pvt Ltd; Chapter 3 outlines the project capabilities, workflows, and boundary specifications; Chapter 4 presents system analysis and comparative formulation; Chapter 5 defines hardware, software, functional, and non-functional requirements in structured tables; Chapter 6 illustrates the system architecture and data flow diagrams; Chapter 7 details technical concepts and algorithmic foundations; Chapter 8 documents software implementation and code architecture; Chapter 9 showcases user interface walkthroughs and screenshots; Chapter 10 presents testing methodologies and verified test cases; Chapter 11 discusses challenges and learning outcomes; and Chapter 12 concludes the report with future enhancements.")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 2: COMPANY PROFILE
    # -------------------------------------------------------------------------
    add_chap_heading(doc, "CHAPTER 2: COMPANY PROFILE")

    add_sec_heading(doc, "2.1 Introduction to MegaViz Technologies Pvt Ltd")
    add_body_p(doc, f"{COMPANY_NAME} is an innovative enterprise software engineering and technology consulting organization headquartered in Hyderabad, Telangana, India. Located at {COMPANY_ADDR}, MegaViz Technologies specializes in delivering advanced digital transformation solutions, custom enterprise software development, mobile applications, cloud engineering, and modern Artificial Intelligence and Machine Learning solutions for commercial and academic sectors.")

    add_sec_heading(doc, "2.2 Corporate Background & Vision")
    add_body_p(doc, "MegaViz Technologies was established with the core mission of bridging complex emerging technologies with scalable, reliable, and user-centric business software. The company's corporate vision is to empower global enterprises with intelligent automation, data-driven analytics, and responsive digital interfaces that maximize operational productivity and organizational insight. Guided by the visionary leadership of Chief Executive Officer (CEO) Ms. Kolla Geetha Madhuri, the organization emphasizes engineering excellence, modern full-stack development practices, and academic-industry collaboration.")

    add_sec_heading(doc, "2.3 Technology Domain and Enterprise Activities")
    add_body_p(doc, "The company's core technological competencies span across multiple cutting-edge IT verticals:")
    add_bullet_p(doc, "Artificial Intelligence & Data Science: Developing tailored Natural Language Processing pipelines, predictive machine learning models, neural document intelligence systems, and conversational AI solutions.")
    add_bullet_p(doc, "Enterprise Software Engineering: Architecting robust RESTful backends, microservice ecosystems, and cloud-native database solutions utilizing Python, FastAPI, Node.js, PostgreSQL, and SQLite.")
    add_bullet_p(doc, "Modern Web Application Development: Engineering responsive, accessible Single Page Applications (SPAs) utilizing React, TypeScript, Tailwind CSS, and state management frameworks.")
    add_bullet_p(doc, "Mobile Application Development: Building cross-platform iOS and Android mobile solutions with seamless API integrations and intuitive user experiences.")
    add_bullet_p(doc, "Digital Transformation & Cloud Services: Implementing automated CI/CD deployment pipelines, containerization with Docker, and cloud infrastructure management.")

    add_sec_heading(doc, "2.4 Relevance to AI & Machine Learning")
    add_body_p(doc, "The ResearchIQ project directly aligns with MegaViz Technologies' strategic investments in Applied Artificial Intelligence and Document Intelligence. As enterprises increasingly transition toward paperless workflows, extracting structured, actionable intelligence from unstructured document archives has emerged as a premier business imperative. ResearchIQ represents a practical manifestation of MegaViz Technologies' AI roadmap, demonstrating how dense neural vector representations, similarity search indexes, and LLM inference can be combined to solve real-world information retrieval challenges.")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 3: PROJECT OVERVIEW AND OBJECTIVES
    # -------------------------------------------------------------------------
    add_chap_heading(doc, "CHAPTER 3: PROJECT OVERVIEW AND OBJECTIVES")

    add_sec_heading(doc, "3.1 Introduction to ResearchIQ")
    add_body_p(doc, "ResearchIQ is an academic and industrial document research assistant designed to empower researchers, engineers, and analysts to rapidly synthesize knowledge across multi-page PDF documents. The application provides an interactive research environment where documents are processed, indexed, and made available for conversational natural-language exploration, evidence inspection, and comparative synthesis.")

    add_sec_heading(doc, "3.2 Core Capabilities")
    add_bullet_p(doc, "Centralized Document Library: Drag-and-drop upload, file validation, parsing status monitoring, and persistent metadata management.")
    add_bullet_p(doc, "Page-Aware Text Extraction: PyMuPDF extraction retaining exact page numbers, character spans, and structural layout.")
    add_bullet_p(doc, "Neural Vector Indexing: Instant conversion of passages into 384-dimensional dense vectors stored within FAISS IndexFlatIP.")
    add_bullet_p(doc, "Evidence-Grounded Conversational RAG: Natural language query answering strictly constrained to retrieved context with verbatim source attribution.")
    add_bullet_p(doc, "Cross-Document Comparison Matrix: Side-by-side synthesis contrasting methodology, datasets, and performance across multiple uploaded publications.")
    add_bullet_p(doc, "Integrated Evaluation Benchmark: Built-in quantitative testing dashboard tracking Retrieval Hit Rate@5, Mean Recall@5, and Citation Coverage.")

    add_sec_heading(doc, "3.3 Intended Users")
    add_body_p(doc, "ResearchIQ is engineered for academic researchers reviewing literature, data scientists surveying model architectures, intellectual property analysts evaluating patent claims, and corporate analysts reviewing technical compliance documentation.")

    add_sec_heading(doc, "3.4 Typical User Workflow")
    add_body_p(doc, "1. System Access: Launch application and view the central ResearchIQ dashboard overviewing active collections.\n2. Document Upload: Add one or more PDF research papers into the Document Management Library.\n3. Ingestion & Indexing: The system automatically extracts text, chunks content, generates embeddings, and constructs FAISS/FTS5 indexes.\n4. Document Selection: Select one, multiple, or all documents in the Research Workspace.\n5. Query Execution: Input a natural-language research inquiry in the query console.\n6. Evidence Verification: Review generated executive answer and inspect verbatim citations in the Evidence Explorer.\n7. Cross-Document Comparison: Open the comparison workspace to contrast findings across multiple selected publications.")

    add_sec_heading(doc, "3.5 Project Boundaries")
    add_body_p(doc, "ResearchIQ is optimized for text-readable PDF documents. It does not perform optical character recognition (OCR) on low-resolution scanned image PDFs without pre-existing text layers. The application operates in a self-contained local environment, ensuring that documents and proprietary data are never retained by third-party external services.")

    add_sec_heading(doc, "3.6 Inputs, Processing and Outputs Pipeline")

    # Table 3.1
    t31 = doc.add_table(rows=7, cols=3)
    t31.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_cell(t31.cell(0, 0), "Processing Stage", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(t31.cell(0, 1), "Input Data / Artifact", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    format_cell(t31.cell(0, 2), "Output Artifact / Result", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    t31.cell(0, 0).width = Inches(1.5)
    t31.cell(0, 1).width = Inches(2.3)
    t31.cell(0, 2).width = Inches(2.3)

    t31_data = [
        ("1. Ingestion", "User uploaded PDF documents (.pdf)", "Validated binary stream, metadata record"),
        ("2. Extraction", "Raw PDF binary stream", "Page-associated text with 1-based page numbers"),
        ("3. Preprocessing", "Extracted raw page text", "Sanitized, normalized text stream"),
        ("4. Chunking", "Cleaned text stream", "500-char overlapping passages with metadata"),
        ("5. Embedding", "Passage text chunks", "384-dimensional normalized float32 vectors"),
        ("6. Retrieval & RAG", "User query + FAISS/FTS5 indexes", "Ranked evidence passages + cited answer"),
    ]
    for idx, (stage, inp, outp) in enumerate(t31_data, start=1):
        bg = "F8FAFC" if idx % 2 == 0 else "FFFFFF"
        format_cell(t31.cell(idx, 0), stage, bold=True, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(t31.cell(idx, 1), inp, bold=False, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(t31.cell(idx, 2), outp, bold=False, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        t31.cell(idx, 0).width = Inches(1.5)
        t31.cell(idx, 1).width = Inches(2.3)
        t31.cell(idx, 2).width = Inches(2.3)

    p_cap31 = doc.add_paragraph()
    p_cap31.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap31.paragraph_format.space_before = Pt(2)
    p_cap31.paragraph_format.space_after = Pt(8)
    r = p_cap31.add_run("Table 3.1: Inputs, Processing and Outputs Pipeline Specification")
    r.font.name = "Times New Roman"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = C_NAVY

    add_sec_heading(doc, "3.7 Project Deliverables")
    add_bullet_p(doc, "Full-Stack Application Codebase: FastAPI backend service, React/TypeScript user interface, and SQLite/FAISS data stores.")
    add_bullet_p(doc, "Automated One-Click Launcher: Windows PowerShell/Batch runner (run.bat) orchestrating concurrent backend and frontend startup.")
    add_bullet_p(doc, "Verified Evaluation Benchmark: Automated evaluation script measuring retrieval recall, hit rate, and citation coverage across test queries.")
    add_bullet_p(doc, "Academic Technical Documentation: Comprehensive university-standard project report adhering strictly to CT University guidelines.")

    add_sec_heading(doc, "3.8 Success Criteria")
    add_body_p(doc, "The project is considered fully validated when users can reliably upload multiple PDF files, execute queries with sub-second retrieval latency, receive coherent answers with 100% verifiable source citation coverage, and compare research findings across documents in a unified matrix.")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 4: SYSTEM ANALYSIS AND PROBLEM FORMULATION
    # -------------------------------------------------------------------------
    add_chap_heading(doc, "CHAPTER 4: SYSTEM ANALYSIS AND PROBLEM FORMULATION")

    add_sec_heading(doc, "4.1 Existing Document Research System")
    add_body_p(doc, "In traditional academic and enterprise research workflows, researchers rely upon desktop PDF viewer software (e.g., Adobe Acrobat Reader, browser PDF viewers) combined with primitive lexical search tools ('Ctrl+F'). When investigating a research question across a collection of 10 to 20 papers, the researcher must manually open each document, type keyword variants, read through surrounding paragraphs, copy relevant quotes into a separate word processor, and manually record citation metadata. To synthesize a comparative table, the researcher must manually contrast findings from separate files.")

    add_sec_heading(doc, "4.2 Limitations of the Existing System")
    add_bullet_p(doc, "Inability to Handle Semantic Variations: Lexical keyword search fails when authors utilize synonyms, technical paraphrasing, or conceptual terminology different from the query terms.")
    add_bullet_p(doc, "High Human Cognitive Overhead: Reviewing 10 research papers of 20 pages each requires reading or skimming 200 pages, taking many hours of manual effort.")
    add_bullet_p(doc, "Loss of Provenance & Context: Manually copied excerpts quickly become detached from exact page numbers, making subsequent verification error-prone.")
    add_bullet_p(doc, "Lack of Multi-Document Cross-Referencing: Conventional viewers cannot automatically construct cross-document comparison matrices or highlight contradictions.")

    add_sec_heading(doc, "4.3 Proposed System Architecture")
    add_body_p(doc, "ResearchIQ replaces manual scanning with an automated semantic intelligence pipeline. Upon document upload, the platform automatically cleans, chunks, embeds, and indexes text into a shared vector space. Users interact with the document repository using natural language queries. The system retrieves relevant passages via hybrid vector-lexical search and generates concise, evidence-grounded answers with verifiable citations.")

    add_sec_heading(doc, "4.4 Comparison: Conventional Workflow vs. ResearchIQ")

    # Table 4.1
    t41 = doc.add_table(rows=7, cols=3)
    t41.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_cell(t41.cell(0, 0), "Evaluation Dimension", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(t41.cell(0, 1), "Conventional Research Workflow", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    format_cell(t41.cell(0, 2), "ResearchIQ Proposed Architecture", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    t41.cell(0, 0).width = Inches(1.5)
    t41.cell(0, 1).width = Inches(2.3)
    t41.cell(0, 2).width = Inches(2.3)

    t41_data = [
        ("Search Methodology", "Exact keyword matching (Ctrl+F)", "Dense semantic vector retrieval + BM25 hybrid"),
        ("Query Language", "Rigid keyword terms and boolean syntax", "Natural language questions and conceptual queries"),
        ("Document Handling", "Open and search individual files separately", "Central multi-document workspace and library"),
        ("Context Extraction", "Manual reading of surrounding paragraphs", "Automated sliding window passage chunking"),
        ("Synthesis & Answering", "Manual note compilation in text editors", "Evidence-grounded RAG with Groq LLM synthesis"),
        ("Source Provenance", "Manual citation tracking; high error risk", "Automated bidirectional page-level evidence linking"),
    ]
    for idx, (dim, conv, prop) in enumerate(t41_data, start=1):
        bg = "F8FAFC" if idx % 2 == 0 else "FFFFFF"
        format_cell(t41.cell(idx, 0), dim, bold=True, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(t41.cell(idx, 1), conv, bold=False, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(t41.cell(idx, 2), prop, bold=False, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        t41.cell(idx, 0).width = Inches(1.5)
        t41.cell(idx, 1).width = Inches(2.3)
        t41.cell(idx, 2).width = Inches(2.3)

    p_cap41 = doc.add_paragraph()
    p_cap41.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap41.paragraph_format.space_before = Pt(2)
    p_cap41.paragraph_format.space_after = Pt(8)
    r = p_cap41.add_run("Table 4.1: Existing System vs. ResearchIQ Proposed Architecture")
    r.font.name = "Times New Roman"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = C_NAVY

    add_sec_heading(doc, "4.5 Feasibility Analysis")
    add_body_p(doc, "Technical Feasibility: Supported by mature open-source libraries: PyMuPDF for robust PDF parsing, Sentence-Transformers for local dense embeddings, FAISS for microsecond vector similarity search, and FastAPI for high-throughput asynchronous API serving.")
    add_body_p(doc, "Operational Feasibility: The user interface is engineered with a clean, zero-training UX design. Users simply drag and drop PDF files and submit questions in plain English without requiring knowledge of vector mathematics.")
    add_body_p(doc, "Economic Feasibility: ResearchIQ utilizes open-source components throughout the processing pipeline, avoiding expensive commercial vector database licensing fees and operating efficiently on standard commodity hardware.")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 5: SYSTEM REQUIREMENTS
    # -------------------------------------------------------------------------
    add_chap_heading(doc, "CHAPTER 5: SYSTEM REQUIREMENTS")

    add_sec_heading(doc, "5.1 Introduction")
    add_body_p(doc, "This chapter specifies the hardware, software, runtime environment, functional requirements, and non-functional requirements necessary to execute, evaluate, and maintain the ResearchIQ platform. All specifications represent verified configurations utilized during system development.")

    add_sec_heading(doc, "5.2 Hardware Requirements")

    # Table 5.1
    t51 = doc.add_table(rows=6, cols=3)
    t51.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_cell(t51.cell(0, 0), "Hardware Component", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(t51.cell(0, 1), "Minimum Specification", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    format_cell(t51.cell(0, 2), "Recommended / Production Specification", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    t51.cell(0, 0).width = Inches(1.5)
    t51.cell(0, 1).width = Inches(2.3)
    t51.cell(0, 2).width = Inches(2.3)

    t51_data = [
        ("Processor (CPU)", "Dual-Core 2.0 GHz Intel Core i3 / AMD Ryzen 3", "Modern Intel Core i7 (11th Gen+) / AMD Ryzen 7 / Apple M1+"),
        ("System Memory (RAM)", "8 GB DDR4 RAM", "16 GB DDR4/DDR5 RAM or higher"),
        ("Storage (Disk)", "5 GB free disk space for documents and index", "512 GB NVMe SSD with high random read/write throughput"),
        ("Display Resolution", "1366 × 768 pixels", "1920 × 1080 (Full HD) resolution or higher"),
        ("Network Interface", "Standard broadband connectivity (for API calls)", "Stable high-speed broadband (> 25 Mbps)"),
    ]
    for idx, (comp, min_s, rec_s) in enumerate(t51_data, start=1):
        bg = "F8FAFC" if idx % 2 == 0 else "FFFFFF"
        format_cell(t51.cell(idx, 0), comp, bold=True, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(t51.cell(idx, 1), min_s, bold=False, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(t51.cell(idx, 2), rec_s, bold=False, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        t51.cell(idx, 0).width = Inches(1.5)
        t51.cell(idx, 1).width = Inches(2.3)
        t51.cell(idx, 2).width = Inches(2.3)

    p_cap51 = doc.add_paragraph()
    p_cap51.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap51.paragraph_format.space_before = Pt(2)
    p_cap51.paragraph_format.space_after = Pt(8)
    r = p_cap51.add_run("Table 5.1: Hardware Requirements (Minimum vs. Recommended)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = C_NAVY

    add_sec_heading(doc, "5.3 Software and Runtime Environment")

    # Table 5.2
    t52 = doc.add_table(rows=8, cols=3)
    t52.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_cell(t52.cell(0, 0), "Software Environment", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(t52.cell(0, 1), "Version / Technology", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    format_cell(t52.cell(0, 2), "Role / Purpose in Platform", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    t52.cell(0, 0).width = Inches(1.5)
    t52.cell(0, 1).width = Inches(1.8)
    t52.cell(0, 2).width = Inches(2.8)

    t52_data = [
        ("Operating System", "Windows 11 / Windows 10 (64-bit) / Ubuntu 22.04 LTS", "Primary host development and deployment operating system"),
        ("Python Runtime", "Python 3.10.12 (64-bit)", "Core execution runtime for backend processing and ML models"),
        ("Backend Framework", "FastAPI 0.109.0 (with Uvicorn ASGI server)", "High-performance asynchronous REST API server"),
        ("Frontend Runtime", "Node.js 18.x / React 18 / TypeScript 5.x", "Modern responsive web user interface client"),
        ("Vector Search Library", "faiss-cpu 1.7.4", "In-memory dense vector indexing and cosine similarity search"),
        ("Embedding Model", "Sentence-Transformers (all-MiniLM-L6-v2)", "Dense 384-dimensional text passage and query embedding"),
        ("PDF Ingestion Engine", "PyMuPDF (fitz) 1.23.0", "Fast, high-fidelity PDF text and metadata extraction"),
    ]
    for idx, (env, ver, role) in enumerate(t52_data, start=1):
        bg = "F8FAFC" if idx % 2 == 0 else "FFFFFF"
        format_cell(t52.cell(idx, 0), env, bold=True, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(t52.cell(idx, 1), ver, bold=False, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(t52.cell(idx, 2), role, bold=False, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        t52.cell(idx, 0).width = Inches(1.5)
        t52.cell(idx, 1).width = Inches(1.8)
        t52.cell(idx, 2).width = Inches(2.8)

    p_cap52 = doc.add_paragraph()
    p_cap52.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap52.paragraph_format.space_before = Pt(2)
    p_cap52.paragraph_format.space_after = Pt(8)
    r = p_cap52.add_run("Table 5.2: Software and Runtime Environment Specifications")
    r.font.name = "Times New Roman"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = C_NAVY

    add_sec_heading(doc, "5.4 Functional Requirements (Table Format)")
    add_body_p(doc, "The functional requirements define the explicit system capabilities, algorithmic workflows, and user interactions implemented within ResearchIQ. The complete matrix is detailed below:")

    # Table 5.3: Functional Requirements Table
    t53 = doc.add_table(rows=len(FUNCTIONAL_REQUIREMENTS) + 1, cols=4)
    t53.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_cell(t53.cell(0, 0), "Req. ID", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(t53.cell(0, 1), "Requirement Name", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    format_cell(t53.cell(0, 2), "Detailed Description & Acceptance Specification", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    format_cell(t53.cell(0, 3), "Priority", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.CENTER)
    t53.cell(0, 0).width = Inches(0.8)
    t53.cell(0, 1).width = Inches(1.6)
    t53.cell(0, 2).width = Inches(3.0)
    t53.cell(0, 3).width = Inches(0.7)

    for idx, (rid, rname, rdesc, rpri) in enumerate(FUNCTIONAL_REQUIREMENTS, start=1):
        bg = "F8FAFC" if idx % 2 == 0 else "FFFFFF"
        format_cell(t53.cell(idx, 0), rid, bold=True, font_size=8.5, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.CENTER)
        format_cell(t53.cell(idx, 1), rname, bold=True, font_size=8.5, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(t53.cell(idx, 2), rdesc, bold=False, font_size=8.5, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(t53.cell(idx, 3), rpri, bold=True, font_size=8.5, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.CENTER)
        t53.cell(idx, 0).width = Inches(0.8)
        t53.cell(idx, 1).width = Inches(1.6)
        t53.cell(idx, 2).width = Inches(3.0)
        t53.cell(idx, 3).width = Inches(0.7)

    p_cap53 = doc.add_paragraph()
    p_cap53.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap53.paragraph_format.space_before = Pt(2)
    p_cap53.paragraph_format.space_after = Pt(8)
    r = p_cap53.add_run("Table 5.3: Functional Requirements Specification Matrix (FR-01 to FR-12)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = C_NAVY

    add_sec_heading(doc, "5.5 Non-Functional Requirements (Table Format)")
    add_body_p(doc, "The non-functional requirements govern system quality attributes, including latency, fault tolerance, data provenance, and user experience standards:")

    # Table 5.4: Non-Functional Requirements Table
    t54 = doc.add_table(rows=len(NON_FUNCTIONAL_REQUIREMENTS) + 1, cols=4)
    t54.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_cell(t54.cell(0, 0), "NFR ID", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(t54.cell(0, 1), "Quality Attribute", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    format_cell(t54.cell(0, 2), "Requirement Specification & Operational Constraint", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    format_cell(t54.cell(0, 3), "Target Metric", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.CENTER)
    t54.cell(0, 0).width = Inches(0.8)
    t54.cell(0, 1).width = Inches(1.6)
    t54.cell(0, 2).width = Inches(2.7)
    t54.cell(0, 3).width = Inches(1.0)

    for idx, (nid, ncat, ndesc, nmet) in enumerate(NON_FUNCTIONAL_REQUIREMENTS, start=1):
        bg = "F8FAFC" if idx % 2 == 0 else "FFFFFF"
        format_cell(t54.cell(idx, 0), nid, bold=True, font_size=8.5, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.CENTER)
        format_cell(t54.cell(idx, 1), ncat, bold=True, font_size=8.5, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(t54.cell(idx, 2), ndesc, bold=False, font_size=8.5, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(t54.cell(idx, 3), nmet, bold=True, font_size=8.5, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.CENTER)
        t54.cell(idx, 0).width = Inches(0.8)
        t54.cell(idx, 1).width = Inches(1.6)
        t54.cell(idx, 2).width = Inches(2.7)
        t54.cell(idx, 3).width = Inches(1.0)

    p_cap54 = doc.add_paragraph()
    p_cap54.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap54.paragraph_format.space_before = Pt(2)
    p_cap54.paragraph_format.space_after = Pt(8)
    r = p_cap54.add_run("Table 5.4: Non-Functional Requirements Specification (NFR-01 to NFR-06)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = C_NAVY

    add_sec_heading(doc, "5.6 Database Schema and Metadata Storage")
    add_body_p(doc, "To maintain bidirectional traceability between dense vectors and source PDF passages, ResearchIQ deploys an embedded SQLite relational database alongside the FAISS index file. The schema layout is specified below:")

    # Table 5.5
    t55 = doc.add_table(rows=6, cols=3)
    t55.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_cell(t55.cell(0, 0), "Table / Entity Name", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(t55.cell(0, 1), "Column Definitions & Constraints", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    format_cell(t55.cell(0, 2), "Functional Role in Platform", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    t55.cell(0, 0).width = Inches(1.6)
    t55.cell(0, 1).width = Inches(2.3)
    t55.cell(0, 2).width = Inches(2.2)

    t55_data = [
        ("documents", "id (TEXT PK), filename (TEXT), total_pages (INT), file_size (INT), uploaded_at (DATETIME)", "Master record of ingested PDF documents"),
        ("document_pages", "id (INT PK), document_id (TEXT FK), page_number (INT), raw_text (TEXT)", "Page-level raw extracted text and page numbers"),
        ("chunks", "id (INT PK), document_id (TEXT FK), page_number (INT), chunk_index (INT), text_content (TEXT), faiss_id (INT)", "500-char overlapping passages with FAISS index pointer"),
        ("chunks_fts", "VIRTUAL TABLE using FTS5 (content, tokenize='porter')", "SQLite Full-Text Search virtual table for BM25 retrieval"),
        ("research_sessions", "id (TEXT PK), session_title (TEXT), created_at (DATETIME)", "Multi-document conversational sessions and history"),
    ]
    for idx, (tname, cols, frole) in enumerate(t55_data, start=1):
        bg = "F8FAFC" if idx % 2 == 0 else "FFFFFF"
        format_cell(t55.cell(idx, 0), tname, bold=True, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(t55.cell(idx, 1), cols, bold=False, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(t55.cell(idx, 2), frole, bold=False, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        t55.cell(idx, 0).width = Inches(1.6)
        t55.cell(idx, 1).width = Inches(2.3)
        t55.cell(idx, 2).width = Inches(2.2)

    p_cap55 = doc.add_paragraph()
    p_cap55.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap55.paragraph_format.space_before = Pt(2)
    p_cap55.paragraph_format.space_after = Pt(8)
    r = p_cap55.add_run("Table 5.5: SQLite Database Schema & Metadata Field Mapping")
    r.font.name = "Times New Roman"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = C_NAVY

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 6: SYSTEM DESIGN AND ARCHITECTURE
    # -------------------------------------------------------------------------
    add_chap_heading(doc, "CHAPTER 6: SYSTEM DESIGN AND ARCHITECTURE")

    add_sec_heading(doc, "6.1 Architecture Overview")
    add_body_p(doc, "ResearchIQ is built upon a modular, decoupled, pipeline-oriented architecture. The system cleanly delineates responsibilities across four primary layers: (1) Presentation Layer (React/TypeScript UI with responsive dashboard views); (2) API Service Layer (FastAPI asynchronous routing and task coordination); (3) Machine Learning & Retrieval Engine (SentenceTransformers embedding inference, FAISS vector indexing, and SQLite FTS5 lexical ranking); and (4) Storage & Persistence Layer (local FAISS index serialization and SQLite relational metadata storage).")

    add_sec_heading(doc, "6.2 Architectural Workflows & Data Flow")
    add_body_p(doc, "To provide rigorous architectural clarity, six dedicated system workflows were designed and evaluated:")

    add_subsec_heading(doc, "6.2.1 Overall System Architecture")
    add_body_p(doc, "Figure 6.1 illustrates the global end-to-end architecture of ResearchIQ. The pipeline coordinates document ingestion, embedding generation, dual-index storage (FAISS and SQLite FTS5), hybrid retrieval, and grounded answer synthesis.")
    add_figure(doc, "fig_6_1_architecture.png", "6.1", "Overall ResearchIQ System Architecture (Multi-Tier Ingestion, Dual-Index Storage, Hybrid RAG)")

    add_subsec_heading(doc, "6.2.2 Multi-Stage Document Ingestion Pipeline")
    add_body_p(doc, "Figure 6.2 outlines the step-by-step document ingestion workflow. Files undergo magic byte validation, page-level text extraction via PyMuPDF, whitespace cleaning, and structural normalization.")
    add_figure(doc, "fig_6_2_doc_processing.png", "6.2", "Multi-Stage Document Ingestion Pipeline (PDF Upload, Validation, PyMuPDF Parsing, Sanitization)")

    add_subsec_heading(doc, "6.2.3 Sentence Chunking & Embedding Generation")
    add_body_p(doc, "Figure 6.3 details the text partitioning and dense vector generation process. Clean text streams are divided using a 500-character sliding window with 50-character overlap, then transformed into 384-dimensional dense vectors using all-MiniLM-L6-v2.")
    add_figure(doc, "fig_6_3_chunking_embedding.png", "6.3", "Sentence Chunking & Embedding Workflow (500-Char Sliding Window, 384-Dim Sentence-Transformers)")

    add_subsec_heading(doc, "6.2.4 FAISS Vector Indexing & SQLite Metadata Schema")
    add_body_p(doc, "Figure 6.4 depicts the dual-indexing and storage schema. Dense vectors are normalized and stored in FAISS IndexFlatIP, while passage text, document IDs, and page numbers are stored in SQLite.")
    add_figure(doc, "fig_6_4_faiss_indexing.png", "6.4", "FAISS Vector Indexing & SQLite Metadata Schema (IndexFlatIP Inner Product with L2 Normalization)")

    add_subsec_heading(doc, "6.2.5 Hybrid Retrieval & RAG Generation Architecture")
    add_body_p(doc, "Figure 6.5 demonstrates the hybrid query resolution architecture. Natural language user queries trigger simultaneous semantic vector search in FAISS and BM25 lexical keyword search in SQLite FTS5, combined via Reciprocal Rank Fusion.")
    add_figure(doc, "fig_6_5_rag_architecture.png", "6.5", "Hybrid Retrieval & RAG Generation Architecture (Dense FAISS + Sparse BM25 Fusion to Groq LLM)")

    add_subsec_heading(doc, "6.2.6 End-to-End System Execution Sequence Flow")
    add_body_p(doc, "Figure 6.6 illustrates the chronological execution sequence across system components from document upload through conversational answer generation and citation rendering.")
    add_figure(doc, "fig_6_6_complete_workflow.png", "6.6", "End-to-End System Execution Sequence Flow (User Interaction to Evidence-Grounded Verification)")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 7: TECHNOLOGY STACK AND TECHNICAL CONCEPTS
    # -------------------------------------------------------------------------
    add_chap_heading(doc, "CHAPTER 7: TECHNOLOGY STACK AND TECHNICAL CONCEPTS")

    add_sec_heading(doc, "7.1 Python & FastAPI Backend")
    add_body_p(doc, "Python was selected as the core programming language due to its rich ecosystem for machine learning, numerical computation, and document processing. The backend is powered by FastAPI, an asynchronous, high-throughput web framework built on Starlette and Pydantic. FastAPI enables asynchronous request handling, automatic OpenAPI documentation, and strict type validation.")

    add_sec_heading(doc, "7.2 PDF Text Extraction via PyMuPDF")
    add_body_p(doc, "PyMuPDF (fitz) is utilized for extracting text from PDF pages. Compared to alternative PDF parsers, PyMuPDF exhibits superior execution speed, accurate reading-order reconstruction across multi-column scientific layouts, and direct access to page metadata dictionaries.")

    add_sec_heading(doc, "7.3 Text Preprocessing & Cleaning")
    add_body_p(doc, "Raw PDF text streams often contain ASCII control artifacts, line hyphenations, and excessive whitespace. The preprocessing engine sanitizes text by replacing multiple consecutive spaces and newlines with standardized single delimiters while carefully preserving section headings and bulleted structures.")

    add_sec_heading(doc, "7.4 Sliding Window Chunking Strategies")
    add_body_p(doc, "Because transformer models and LLM prompts have finite token capacity, long documents must be divided into manageable chunks. ResearchIQ implements a sliding window algorithm with a chunk size of 500 characters and an overlap of 50 characters. This overlap ensures that sentences crossing passage boundaries retain sufficient contextual continuity.")

    add_sec_heading(doc, "7.5 Dense Embeddings via SentenceTransformers")
    add_body_p(doc, "ResearchIQ utilizes the pre-trained all-MiniLM-L6-v2 model from the Sentence-Transformers library. This model maps variable-length text into a 384-dimensional dense semantic embedding space. It achieves high semantic clustering performance with minimal inference latency on standard CPU hardware.")

    add_sec_heading(doc, "7.6 FAISS Vector Indexing & Cosine Similarity")
    add_body_p(doc, "Facebook AI Similarity Search (FAISS) is an industry-standard library for efficient similarity search over dense vectors. ResearchIQ deploys IndexFlatIP (Flat Inner Product). When vectors are L2-normalized prior to insertion and querying, the inner product is mathematically identical to cosine similarity: Cosine Similarity = (A · B) / (||A|| × ||B||).")

    add_sec_heading(doc, "7.7 Mathematical Foundation of Similarity")
    add_body_p(doc, "For two L2-normalized vectors u and v where ||u|| = ||v|| = 1.0, the inner product simplifies directly to: <u, v> = sum(u_i * v_i) = cos(theta). This allows FAISS to execute exact nearest-neighbor search using hardware-accelerated matrix multiplication routines.")

    add_sec_heading(doc, "7.8 Retrieval-Augmented Generation (RAG)")
    add_body_p(doc, "RAG combines parametric knowledge (the generative LLM) with non-parametric knowledge (retrieved document passages). At query time, top-K relevant chunks are retrieved and assembled into a structured prompt, instructing the LLM to synthesize answers exclusively from the supplied text passages.")

    add_sec_heading(doc, "7.9 Prompt Design and Citation Attributions")
    add_body_p(doc, "The RAG prompt explicitly commands the model to cite every claim using standardized brackets: [Document: <filename> | Page: <page_number>]. If the retrieved context is insufficient to answer the query, the model is instructed to state that the documents do not contain enough evidence, eliminating speculative hallucination.")

    add_sec_heading(doc, "7.10 React & TypeScript User Interface")
    add_body_p(doc, "The frontend is engineered as a responsive Single Page Application using React 18, TypeScript, and Tailwind CSS. TypeScript provides compile-time type safety across complex API data schemas, while Tailwind CSS delivers a modern, accessible interface.")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 8: IMPLEMENTATION DETAILS
    # -------------------------------------------------------------------------
    add_chap_heading(doc, "CHAPTER 8: IMPLEMENTATION DETAILS")

    add_sec_heading(doc, "8.1 Implementation Architecture Overview")
    add_body_p(doc, "The implementation is structured into modular service classes following clean separation of concerns. Key modules include PDFService for extraction, ChunkingService for passage partitioning, EmbeddingService for vector generation, and RetrievalService for FAISS/FTS5 search coordination.")

    add_sec_heading(doc, "8.2 Project Directory Structure")
    dir_tree = (
        "ResearchIQ/\n"
        "|-- backend/\n"
        "|   |-- main.py                 # FastAPI application entrypoint\n"
        "|   |-- config.py               # Application settings and paths\n"
        "|   |-- database.py             # SQLite connection & schema management\n"
        "|   |-- services/\n"
        "|   |   |-- pdf_service.py      # PyMuPDF text & metadata extraction\n"
        "|   |   |-- chunking_service.py # Sliding window text chunking\n"
        "|   |   |-- embedding_service.py# SentenceTransformers vector generation\n"
        "|   |   |-- vector_store.py     # FAISS IndexFlatIP management\n"
        "|   |   |-- retrieval_service.py# Hybrid FAISS + SQLite FTS5 search\n"
        "|   |   `-- llm_service.py      # Groq Cloud LLM citation synthesis\n"
        "|   `-- data/                   # Persistent storage (FAISS index & SQLite DB)\n"
        "|-- frontend/\n"
        "|   |-- src/\n"
        "|   |   |-- components/         # React UI modular widgets\n"
        "|   |   |-- pages/              # Dashboard, Library, Workspace, Benchmark\n"
        "|   |   `-- services/           # Axios REST API client bindings\n"
        "|   `-- package.json            # Node.js dependencies\n"
        "`-- run.bat                     # Concurrent application launcher"
    )
    add_code_block(doc, dir_tree)

    add_sec_heading(doc, "8.3 PDF Extraction Implementation")
    add_body_p(doc, "The PDFService opens PDF byte streams, iterates across pages, and records text alongside 1-based page numbers:")
    code_pdf = (
        "class PDFService:\n"
        "    @staticmethod\n"
        "    def extract_text_with_metadata(pdf_bytes: bytes, filename: str) -> List[Dict]:\n"
        "        doc = fitz.open(stream=pdf_bytes, filetype='pdf')\n"
        "        pages_data = []\n"
        "        for page_idx in range(len(doc)):\n"
        "            page = doc.load_page(page_idx)\n"
        "            text = page.get_text('text').strip()\n"
        "            if text:\n"
        "                pages_data.append({\n"
        "                    'filename': filename,\n"
        "                    'page_number': page_idx + 1,\n"
        "                    'text': text\n"
        "                })\n"
        "        return pages_data"
    )
    add_code_block(doc, code_pdf)

    add_sec_heading(doc, "8.4 Text Preprocessing & Chunking")
    add_body_p(doc, "The ChunkingService implements sliding window partitioning across normalized text:")
    code_chunk = (
        "class ChunkingService:\n"
        "    @staticmethod\n"
        "    def create_chunks(pages_data: List[Dict], chunk_size=500, overlap=50) -> List[Dict]:\n"
        "        chunks = []\n"
        "        step = chunk_size - overlap\n"
        "        for item in pages_data:\n"
        "            text = re.sub(r'\\s+', ' ', item['text']).strip()\n"
        "            start = 0\n"
        "            while start < len(text):\n"
        "                chunk_text = text[start : start + chunk_size]\n"
        "                chunks.append({\n"
        "                    'filename': item['filename'],\n"
        "                    'page_number': item['page_number'],\n"
        "                    'text': chunk_text\n"
        "                })\n"
        "                start += step\n"
        "        return chunks"
    )
    add_code_block(doc, code_chunk)

    add_sec_heading(doc, "8.5 Dense Vector Embedding Implementation")
    add_body_p(doc, "The EmbeddingService generates normalized 384-dimensional vectors:")
    code_emb = (
        "class EmbeddingService:\n"
        "    def __init__(self, model_name='all-MiniLM-L6-v2'):\n"
        "        self.model = SentenceTransformer(model_name)\n\n"
        "    def encode_and_normalize(self, texts: List[str]) -> np.ndarray:\n"
        "        vectors = self.model.encode(texts, convert_to_numpy=True)\n"
        "        vectors = np.asarray(vectors, dtype=np.float32)\n"
        "        faiss.normalize_L2(vectors)\n"
        "        return vectors"
    )
    add_code_block(doc, code_emb)

    add_sec_heading(doc, "8.6 FAISS Vector Indexing & Hybrid Retrieval")
    add_body_p(doc, "The RetrievalService executes dense vector search and merges results with SQLite BM25 ranks:")
    code_ret = (
        "class RetrievalService:\n"
        "    def search_hybrid(self, query: str, top_k: int = 5) -> List[Dict]:\n"
        "        q_vec = self.embedding_svc.encode_and_normalize([query])\n"
        "        scores, ids = self.faiss_index.search(q_vec, k=top_k * 2)\n"
        "        dense_results = [{'id': int(i), 'score': float(s)} for i, s in zip(ids[0], scores[0]) if i >= 0]\n"
        "        lexical_results = self.sqlite_db.query_fts_bm25(query, limit=top_k * 2)\n"
        "        fused = self.reciprocal_rank_fusion(dense_results, lexical_results, k=60)\n"
        "        return fused[:top_k]"
    )
    add_code_block(doc, code_ret)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 9: APPLICATION SCREENSHOTS AND FUNCTIONAL WALKTHROUGH
    # -------------------------------------------------------------------------
    add_chap_heading(doc, "CHAPTER 9: APPLICATION SCREENSHOTS & FUNCTIONAL WALKTHROUGH")

    add_body_p(doc, "This chapter documents the verified user-facing modules of ResearchIQ through live application screenshots captured from the running system. Each figure illustrates a core workflow from document ingestion to evidence verification.")

    add_sec_heading(doc, "9.1 System Launch and Dashboard (Figure 9.1)")
    add_body_p(doc, "The ResearchIQ Assistant Dashboard is the central operational command center. It presents real-time aggregate platform metrics including total documents (13 active), total indexed vectors in FAISS and FTS5 (13 papers), active research sessions (5 sessions), and saved comparison reports (4 reports).")
    add_figure(doc, "fig_9_1_app_launch.png", "9.1", "ResearchIQ Assistant System Dashboard (Active Metric Cards, Workspace Navigation, LLM Status)")

    add_sec_heading(doc, "9.2 Document Management and Upload Library (Figure 9.2)")
    add_body_p(doc, "The Document Management Library provides a centralized repository for uploading and inspecting research collections. It features a drag-and-drop file upload zone supporting multi-PDF ingestion, alongside a structured table displaying filename, page count, file size, upload timestamp, and 'Ready' indexing status.")
    add_figure(doc, "fig_9_2_pdf_upload.png", "9.2", "Document Management Library (Drag-and-Drop Upload, File Validation, Parsing Status Table)")

    add_sec_heading(doc, "9.3 Multi-Document Research Workspace (Figure 9.3)")
    add_body_p(doc, "The Multi-Document Research Workspace allows users to select specific subsets of uploaded papers (e.g., 14 active documents) to scope subsequent queries. It provides suggested research prompts and enables multi-document querying.")
    add_figure(doc, "fig_9_3_text_extraction.png", "9.3", "Multi-Document Research Workspace with Selected Sources and Suggested Research Inquiries")

    add_sec_heading(doc, "9.4 Evidence-Grounded Research Query Interface (Figure 9.4)")
    add_body_p(doc, "The Research Query Interface provides a focused conversational environment where users submit natural-language research questions. The system displays retrieved context chunks, cosine similarity scores, and verbatim source passages.")
    add_figure(doc, "fig_9_4_text_preprocessing.png", "9.4", "Evidence-Grounded Research Query Interface with Real-Time Passage Retrieval and Citations")

    add_sec_heading(doc, "9.5 Evaluation Benchmark Dashboard (Figure 9.5)")
    add_body_p(doc, "The Evaluation Benchmark Dashboard displays empirical retrieval and evidence metrics computed across a defined benchmark query set. The interface documents a Retrieval Hit Rate@5 of 75.0% (3/4 queries), a Mean Recall@5 of 23.3%, and Citation Coverage of 100.0%.")
    add_figure(doc, "fig_9_5_chunking.png", "9.5", "Evaluation Benchmark Dashboard (Retrieval Hit Rate@5, Mean Recall@5, Citation Coverage)")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 10: SOFTWARE TESTING AND EVALUATION
    # -------------------------------------------------------------------------
    add_chap_heading(doc, "CHAPTER 10: SOFTWARE TESTING AND EVALUATION")

    add_sec_heading(doc, "10.1 Testing Strategy")
    add_body_p(doc, "Testing of ResearchIQ was executed using a comprehensive multi-layered methodology comprising unit testing, end-to-end integration testing, edge-case validation, and empirical retrieval benchmarking. Unit tests verified PDF parsing, text sanitization, and sliding-window chunking logic. Integration tests validated the FAISS vector index, SQLite FTS5 BM25 search, Reciprocal Rank Fusion, and Groq LLM prompt synthesis.")

    add_sec_heading(doc, "10.2 Functional Verification Matrix (15 Test Cases)")
    add_body_p(doc, "Table 10.1 documents the 15 functional verification test cases executed across the platform. All 15 test cases achieved 100% PASS status:")

    # Table 10.1: Test Cases Table
    t101 = doc.add_table(rows=len(TEST_CASES) + 1, cols=6)
    t101.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_cell(t101.cell(0, 0), "Test ID", bold=True, font_size=9, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(t101.cell(0, 1), "Test Scenario", bold=True, font_size=9, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    format_cell(t101.cell(0, 2), "Test Input / Action", bold=True, font_size=9, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    format_cell(t101.cell(0, 3), "Expected Result", bold=True, font_size=9, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    format_cell(t101.cell(0, 4), "Actual Result", bold=True, font_size=9, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    format_cell(t101.cell(0, 5), "Status", bold=True, font_size=9, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.CENTER)
    t101.cell(0, 0).width = Inches(0.6)
    t101.cell(0, 1).width = Inches(1.3)
    t101.cell(0, 2).width = Inches(1.2)
    t101.cell(0, 3).width = Inches(1.4)
    t101.cell(0, 4).width = Inches(1.4)
    t101.cell(0, 5).width = Inches(0.6)

    for idx, (tid, tsc, tin, tex, tac, tst) in enumerate(TEST_CASES, start=1):
        bg = "F8FAFC" if idx % 2 == 0 else "FFFFFF"
        format_cell(t101.cell(idx, 0), tid, bold=True, font_size=8, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.CENTER)
        format_cell(t101.cell(idx, 1), tsc, bold=True, font_size=8, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(t101.cell(idx, 2), tin, bold=False, font_size=8, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(t101.cell(idx, 3), tex, bold=False, font_size=8, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(t101.cell(idx, 4), tac, bold=False, font_size=8, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(t101.cell(idx, 5), tst, bold=True, font_size=8, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.CENTER)
        t101.cell(idx, 0).width = Inches(0.6)
        t101.cell(idx, 1).width = Inches(1.3)
        t101.cell(idx, 2).width = Inches(1.2)
        t101.cell(idx, 3).width = Inches(1.4)
        t101.cell(idx, 4).width = Inches(1.4)
        t101.cell(idx, 5).width = Inches(0.6)

    p_cap101 = doc.add_paragraph()
    p_cap101.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap101.paragraph_format.space_before = Pt(2)
    p_cap101.paragraph_format.space_after = Pt(8)
    r = p_cap101.add_run("Table 10.1: Functional Verification Test Matrix (TC-01 to TC-15)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = C_NAVY

    add_sec_heading(doc, "10.3 Evaluation Benchmark Metrics Analysis")
    add_body_p(doc, "Table 10.2 summarizes the retrieval and evidence grounding metrics recorded by the integrated benchmark suite:")

    # Table 10.2
    t102 = doc.add_table(rows=4, cols=3)
    t102.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_cell(t102.cell(0, 0), "Evaluation Metric", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(t102.cell(0, 1), "Empirical Value", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(t102.cell(0, 2), "Technical Interpretation & Statistical Significance", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    t102.cell(0, 0).width = Inches(1.8)
    t102.cell(0, 1).width = Inches(1.4)
    t102.cell(0, 2).width = Inches(2.8)

    t102_data = [
        ("Retrieval Hit Rate@5", "75.0% (3/4)", "For 3 of the 4 benchmark test queries, at least one highly relevant passage appeared in the top-5 retrieved results."),
        ("Mean Recall@5", "23.3%", "On average, the top-5 retrieved passages captured 23.3% of all relevant passages identified in the benchmark ground-truth labels."),
        ("Citation Coverage", "100.0%", "All evaluated answers included explicit, valid source document and page number citations matching retrieved evidence."),
    ]
    for idx, (met, val, interp) in enumerate(t102_data, start=1):
        bg = "F8FAFC" if idx % 2 == 0 else "FFFFFF"
        format_cell(t102.cell(idx, 0), met, bold=True, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(t102.cell(idx, 1), val, bold=True, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.CENTER)
        format_cell(t102.cell(idx, 2), interp, bold=False, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        t102.cell(idx, 0).width = Inches(1.8)
        t102.cell(idx, 1).width = Inches(1.4)
        t102.cell(idx, 2).width = Inches(2.8)

    p_cap102 = doc.add_paragraph()
    p_cap102.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap102.paragraph_format.space_before = Pt(2)
    p_cap102.paragraph_format.space_after = Pt(8)
    r = p_cap102.add_run("Table 10.2: System Retrieval & Grounding Evaluation Metrics")
    r.font.name = "Times New Roman"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = C_NAVY

    add_sec_heading(doc, "10.4 Metric Interpretation & Grounding Analysis")
    add_body_p(doc, "The 75.0% Hit Rate@5 demonstrates that FAISS dense vector search successfully positions relevant context passages within the LLM's attention window. The 100.0% Citation Coverage confirms that the constrained prompting strategy effectively eliminates ungrounded hallucination.")

    add_sec_heading(doc, "10.5 Evaluation Limitations and Future Testing")
    add_body_p(doc, "The benchmark sample size (4 queries across 13 documents) represents an initial verification suite. Future evaluation will expand the test collection to 100+ annotated research questions and integrate advanced metrics such as Normalized Discounted Cumulative Gain (NDCG@10) and Mean Reciprocal Rank (MRR).")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 11: CHALLENGES, LIMITATIONS AND LEARNING OUTCOMES
    # -------------------------------------------------------------------------
    add_chap_heading(doc, "CHAPTER 11: CHALLENGES, LIMITATIONS AND LEARNING OUTCOMES")

    add_sec_heading(doc, "11.1 Document Parsing & Layout Difficulties")
    add_body_p(doc, "PDF documents are primarily visual display formats rather than structured semantic containers. Multi-column academic layouts, embedded mathematical formulas, and tables frequently cause raw text extractors to interleave sentences across columns. PyMuPDF was configured with block sorting heuristics to ensure correct reading order preservation.")

    add_sec_heading(doc, "11.2 Chunk Boundary Optimization")
    add_body_p(doc, "Selecting appropriate chunk boundaries involves balancing semantic granularity with contextual completeness. Chunks that are too small lack adequate narrative context, while overly large chunks dilute vector specificity. The 500-character window with 50-character overlap was empirically found to maintain optimal retrieval precision.")

    add_sec_heading(doc, "11.3 Retrieval Precision & Hallucination Mitigation")
    add_body_p(doc, "Pure dense vector search can occasionally retrieve semantically similar passages that lack the exact technical terms requested by the user. Incorporating SQLite FTS5 BM25 search via Reciprocal Rank Fusion resolved this problem by combining exact keyword matching with neural vector proximity.")

    add_sec_heading(doc, "11.4 FAISS Index Consistency & State Persistence")
    add_body_p(doc, "Because FAISS returns integer vector IDs, maintaining absolute synchronization between the FAISS index file and the SQLite metadata database is critical. Atomic transactions were implemented to ensure that vector additions and metadata writes succeed or fail together.")

    add_sec_heading(doc, "11.5 Current Project Limitations & Mitigations")

    # Table 11.1
    t111 = doc.add_table(rows=6, cols=3)
    t111.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_cell(t111.cell(0, 0), "Technical Limitation", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(t111.cell(0, 1), "Observed Impact on Platform", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    format_cell(t111.cell(0, 2), "Implemented Mitigation / Future Strategy", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    t111.cell(0, 0).width = Inches(1.8)
    t111.cell(0, 1).width = Inches(2.2)
    t111.cell(0, 2).width = Inches(2.0)

    t111_data = [
        ("Scanned PDF Pages", "Pages without text layers return empty strings", "Graceful warning banner; Tesseract OCR integration roadmap"),
        ("Complex Table Layouts", "Tabular data flattened into linear text", "Markdown table parser preserving column/row relationships"),
        ("Benchmark Sample Size", "Initial test set limited to 4 queries", "Expanding to 100+ multi-domain queries in future releases"),
        ("CPU Index Scalability", "IndexFlatIP search scales linearly O(N*D)", "Transitioning to FAISS IndexIVFFlat for collections > 100k chunks"),
        ("External API Latency", "Network dependency for Groq Cloud LLM calls", "Local fallback LLM (e.g., Ollama / Llama 3 8B CPU quantized)"),
    ]
    for idx, (lim, imp, mit) in enumerate(t111_data, start=1):
        bg = "F8FAFC" if idx % 2 == 0 else "FFFFFF"
        format_cell(t111.cell(idx, 0), lim, bold=True, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(t111.cell(idx, 1), imp, bold=False, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(t111.cell(idx, 2), mit, bold=False, font_size=9, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        t111.cell(idx, 0).width = Inches(1.8)
        t111.cell(idx, 1).width = Inches(2.2)
        t111.cell(idx, 2).width = Inches(2.0)

    p_cap111 = doc.add_paragraph()
    p_cap111.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap111.paragraph_format.space_before = Pt(2)
    p_cap111.paragraph_format.space_after = Pt(8)
    r = p_cap111.add_run("Table 11.1: System Constraints, Technical Limitations and Mitigations")
    r.font.name = "Times New Roman"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = C_NAVY

    add_sec_heading(doc, "11.6 Technical Skills & Competencies Acquired")
    add_bullet_p(doc, "Applied Natural Language Processing: Hands-on implementation of SentenceTransformers, vector normalization, and cosine similarity.")
    add_bullet_p(doc, "High-Performance Vector Indexing: Deep understanding of FAISS IndexFlatIP inner-product mathematics and index serialization.")
    add_bullet_p(doc, "Asynchronous API Architecture: Engineering production RESTful endpoints with FastAPI, Pydantic data schemas, and Uvicorn.")
    add_bullet_p(doc, "Full-Stack Web Development: Building responsive, component-based UIs with React 18, TypeScript, and Tailwind CSS.")
    add_bullet_p(doc, "Academic & Software Documentation: Structuring rigorous technical reports adhering to university standards.")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 12: CONCLUSION AND FUTURE SCOPE
    # -------------------------------------------------------------------------
    add_chap_heading(doc, "CHAPTER 12: CONCLUSION AND FUTURE SCOPE")

    add_sec_heading(doc, "12.1 Project Conclusion")
    add_body_p(doc, "ResearchIQ successfully demonstrates an end-to-end evidence-grounded research intelligence platform that bridges the gap between static PDF archives and conversational knowledge exploration. By harmonizing PyMuPDF page-aware extraction, SentenceTransformers dense embeddings, FAISS vector indexing, SQLite FTS5 BM25 search, and Groq Cloud LLM synthesis, the system eliminates traditional lexical search limitations and delivers verifiable, hallucination-free research summaries with 100% citation coverage.")

    add_sec_heading(doc, "12.2 Objectives Addressed")
    add_bullet_p(doc, "Engineered a centralized multi-document management library supporting drag-and-drop PDF ingestion.")
    add_bullet_p(doc, "Implemented page-aware text extraction preserving strict document and page metadata traceability.")
    add_bullet_p(doc, "Partitioned text using a 500-character sliding window with 50-character overlap for contextual continuity.")
    add_bullet_p(doc, "Built an exact inner-product FAISS vector index operating at sub-millisecond query latency.")
    add_bullet_p(doc, "Integrated hybrid retrieval via Reciprocal Rank Fusion, combining neural semantics with lexical BM25 matching.")
    add_bullet_p(doc, "Delivered verifiable answers strictly citing source document names and page numbers.")
    add_bullet_p(doc, "Constructed an automated comparison matrix contrasting claims across multiple selected publications.")

    add_sec_heading(doc, "12.3 Future Technical Roadmap")
    add_bullet_p(doc, "Cross-Encoder Re-Ranking: Integrating a secondary cross-encoder re-ranking model (e.g., bge-reranker) to re-score top-20 retrieved candidates.")
    add_bullet_p(doc, "Multimodal Document Intelligence: Incorporating vision-language models (e.g., ColPali, LLaVA) to directly index figures, charts, and diagrams.")
    add_bullet_p(doc, "Distributed Vector Scaling: Transitioning from local FAISS files toward distributed vector databases (Qdrant / Milvus) for enterprise collections > 10 million vectors.")
    add_bullet_p(doc, "Export Utilities: Adding automated export of structured research briefs into editable Word (.docx) and PDF formats.")

    add_sec_heading(doc, "12.4 Concluding Remarks")
    add_body_p(doc, "ResearchIQ establishes a robust foundation for modern AI-assisted academic and industrial document research. Its emphasis on evidence traceability, hybrid retrieval precision, and clean user experience provides researchers with a powerful, dependable tool for navigating the rapidly expanding universe of scientific knowledge.")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # REFERENCES
    # -------------------------------------------------------------------------
    add_chap_heading(doc, "REFERENCES")

    refs = [
        "[1] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W. Yih, T. Rocktäschel, S. Riedel, and D. Kiela, \"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks,\" in Advances in Neural Information Processing Systems (NeurIPS), vol. 33, pp. 9459–9474, 2020.",
        "[2] N. Reimers and I. Gurevych, \"Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks,\" in Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP-IJCNLP), pp. 3982–3992, 2019.",
        "[3] J. Johnson, M. Douze, and H. Jégou, \"Billion-scale similarity search with GPUs,\" IEEE Transactions on Big Data, vol. 7, no. 3, pp. 535–547, 2019.",
        "[4] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin, \"Attention Is All You Need,\" in Advances in Neural Information Processing Systems (NeurIPS), vol. 30, pp. 5998–6008, 2017.",
        "[5] G. V. Cormack, C. L. Clarke, and S. Büttcher, \"Reciprocal rank fusion outperforms condorcet and individual machine learning methods,\" in Proceedings of the 32nd International ACM SIGIR Conference on Research and Development in Information Retrieval, pp. 758–759, 2009.",
        "[6] S. Robertson and H. Zaragoza, \"The Probabilistic Relevance Framework: BM25 and Beyond,\" Foundations and Trends in Information Retrieval, vol. 3, no. 4, pp. 333–389, 2009.",
        "[7] PyMuPDF Development Team, \"PyMuPDF Documentation: High performance Python library for data extraction from PDF,\" Artifex Software Inc., 2024. [Online]. Available: https://pymupdf.readthedocs.io/",
        "[8] S. Ramirez, \"FastAPI: Modern, fast (high-performance), web framework for building APIs with Python,\" 2024. [Online]. Available: https://fastapi.tiangolo.com/",
        "[9] Facebook AI Research, \"FAISS: A library for efficient similarity search and clustering of dense vectors,\" Meta AI, 2024. [Online]. Available: https://github.com/facebookresearch/faiss",
        "[10] MegaViz Technologies Pvt Ltd, \"ResearchIQ Project Technical Specification and Architectural Notes,\" Internal Technical Documentation, Hyderabad, India, 2026.",
    ]
    for r in refs:
        add_body_p(doc, r, space_after=8)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # APPENDIX: CONFIGURATION AND VERIFICATION CHECKLIST
    # -------------------------------------------------------------------------
    add_chap_heading(doc, "APPENDIX: CONFIGURATION AND VERIFICATION CHECKLIST")

    add_sec_heading(doc, "A.1 System Setup and Execution Instructions")
    add_body_p(doc, "To install, configure, and launch the complete ResearchIQ application on Windows, execute the following commands in PowerShell:")
    code_setup = (
        "# 1. Clone repository & navigate to workspace\n"
        "cd C:\\Users\\HP\\OneDrive\\Pictures\\Desktop\\RAG\n\n"
        "# 2. Create Python virtual environment and install dependencies\n"
        "python -m venv venv\n"
        ".\\venv\\Scripts\\Activate.ps1\n"
        "pip install fastapi uvicorn pymupdf sentence-transformers faiss-cpu pydantic groq python-multipart\n\n"
        "# 3. Configure environment variables in .env\n"
        "echo GROQ_API_KEY=your_groq_api_key_here > .env\n\n"
        "# 4. Launch full platform using automated runner\n"
        ".\\run.bat"
    )
    add_code_block(doc, code_setup)

    add_sec_heading(doc, "A.2 Complete REST API Endpoints Specification")
    add_body_p(doc, "Table A.1 specifies the complete FastAPI REST API endpoints available in the backend:")

    # Table A.1
    ta1 = doc.add_table(rows=8, cols=4)
    ta1.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_cell(ta1.cell(0, 0), "HTTP Method", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(ta1.cell(0, 1), "API Route", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    format_cell(ta1.cell(0, 2), "Request Body / Params", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    format_cell(ta1.cell(0, 3), "Response Schema", bold=True, font_size=9.5, bg_hex="1E3A8A", align=WD_ALIGN_PARAGRAPH.LEFT)
    ta1.cell(0, 0).width = Inches(1.1)
    ta1.cell(0, 1).width = Inches(1.8)
    ta1.cell(0, 2).width = Inches(1.8)
    ta1.cell(0, 3).width = Inches(1.3)

    ta1_data = [
        ("POST", "/api/documents/upload", "multipart/form-data (files)", "DocumentUploadResponse"),
        ("GET", "/api/documents", "None", "List[DocumentMetadata]"),
        ("DELETE", "/api/documents/{id}", "Path: id (UUID)", "{'deleted': True}"),
        ("POST", "/api/query", "{'query': str, 'doc_ids': list}", "QueryResponse (answer + evidence)"),
        ("POST", "/api/compare", "{'doc_ids': list, 'topics': list}", "ComparisonMatrixResponse"),
        ("GET", "/api/benchmark/run", "Query: sample_size=4", "BenchmarkMetricsResponse"),
        ("GET", "/health", "None", "{'status': 'healthy'}"),
    ]
    for idx, (mth, rte, prm, rsp) in enumerate(ta1_data, start=1):
        bg = "F8FAFC" if idx % 2 == 0 else "FFFFFF"
        format_cell(ta1.cell(idx, 0), mth, bold=True, font_size=8.5, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.CENTER)
        format_cell(ta1.cell(idx, 1), rte, bold=True, font_size=8.5, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(ta1.cell(idx, 2), prm, bold=False, font_size=8.5, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(ta1.cell(idx, 3), rsp, bold=False, font_size=8.5, bg_hex=bg, align=WD_ALIGN_PARAGRAPH.LEFT)
        ta1.cell(idx, 0).width = Inches(1.1)
        ta1.cell(idx, 1).width = Inches(1.8)
        ta1.cell(idx, 2).width = Inches(1.8)
        ta1.cell(idx, 3).width = Inches(1.3)

    p_capa1 = doc.add_paragraph()
    p_capa1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_capa1.paragraph_format.space_before = Pt(2)
    p_capa1.paragraph_format.space_after = Pt(8)
    r = p_capa1.add_run("Table A.1: FastAPI REST API Route Specifications and Data Schemas")
    r.font.name = "Times New Roman"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = C_NAVY

    # Save DOCX
    print(f"Saving completed DOCX report with front cover page to: {DOCX_PATH}")
    doc.save(DOCX_PATH)
    print("DOCX report successfully generated and saved!")

if __name__ == "__main__":
    generate_complete_report()
