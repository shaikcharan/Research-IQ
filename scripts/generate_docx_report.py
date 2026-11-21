# generate_docx_report.py - Professional Academic Word Document Generator for ResearchIQ Internship Report
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from report_data import STUDENT_INFO, COMPANY_INFO, DAILY_DIARY, TEST_CASES

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'ResearchIQ_Internship_Report')
DOCX_PATH = os.path.join(OUTPUT_DIR, 'ResearchIQ_Internship_Report.docx')
FIGURES_DIR = os.path.join(OUTPUT_DIR, 'figures')

# Color Constants
C_BLACK = RGBColor(0, 0, 0)
C_DARK_BLUE = RGBColor(15, 23, 42)
C_INDIGO = RGBColor(67, 56, 202) # #4338CA
C_MUTED = RGBColor(71, 85, 105)

def apply_page_borders(section):
    """Enforces a clean, university-standard four-sided black border on every page of the section."""
    sectPr = section._sectPr
    for child in list(sectPr):
        if child.tag.endswith('pgBorders'):
            sectPr.remove(child)
            
    pgBorders = OxmlElement('w:pgBorders')
    pgBorders.set(qn('w:offsetFrom'), 'page')
    
    for b_name in ['top', 'left', 'bottom', 'right']:
        border = OxmlElement(f'w:{b_name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), '8') # 1.0 pt thickness
        border.set(qn('w:space'), '24') # 24 pt distance from page edge
        border.set(qn('w:color'), '000000') # Solid black
        pgBorders.append(border)
        
    sectPr.append(pgBorders)

def add_header_footer(section, is_roman=False):
    """Sets professional academic headers and footers sitting safely within page borders."""
    # Configure Header
    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hp.text = "RESEARCHIQ – INTERNSHIP PROJECT REPORT"
    hp.runs[0].font.name = "Times New Roman"
    hp.runs[0].font.size = Pt(8.5)
    hp.runs[0].font.color.rgb = C_MUTED
    hp.paragraph_format.space_after = Pt(8)

    # Configure Footer
    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fp.text = "SHAIK CHARAN | REG. NO: 72311068\t\tPage "
    for r in fp.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(8.5)
        r.font.color.rgb = C_MUTED
    
    # Add page number dynamic XML field
    run_page = fp.add_run()
    run_page.font.name = "Times New Roman"
    run_page.font.size = Pt(8.5)
    run_page.font.bold = True
    run_page.font.color.rgb = C_BLACK
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    run_page._r.append(fldSimple)
    fp.paragraph_format.space_before = Pt(8)

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

def add_chap_heading(doc, text):
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

def format_cell(cell, text, bold=False, italic=False, font_size=10, bg_hex=None, align=WD_ALIGN_PARAGRAPH.LEFT):
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

def generate_report():
    print("Initializing ResearchIQ Project Report Document...")
    doc = docx.Document()

    # SECTION 1: Preliminary Pages (Lower Roman Numerals)
    sec_prelim = doc.sections[0]
    sec_prelim.page_width = Inches(8.27)
    sec_prelim.page_height = Inches(11.69)
    sec_prelim.left_margin = Inches(1.25)
    sec_prelim.right_margin = Inches(1.0)
    sec_prelim.top_margin = Inches(1.0)
    sec_prelim.bottom_margin = Inches(1.0)
    apply_page_borders(sec_prelim)
    add_header_footer(sec_prelim, is_roman=True)

    # Set Roman Numbering XML
    pgNumType = OxmlElement('w:pgNumType')
    pgNumType.set(qn('w:fmt'), 'lowerRoman')
    sec_prelim._sectPr.append(pgNumType)

    # =========================================================================
    # PRELIMINARY PAGE 1: INTERNSHIP CERTIFICATE
    # =========================================================================
    p_cert_org = doc.add_paragraph()
    p_cert_org.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_org.paragraph_format.space_after = Pt(2)
    r = p_cert_org.add_run("MEGAVIZ TECHNOLOGIES PVT LTD")
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = C_BLACK

    p_cert_sub = doc.add_paragraph()
    p_cert_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_sub.paragraph_format.space_after = Pt(14)
    r = p_cert_sub.add_run("#806, 8th Floor, Manjeera Trinity Corporate, Kukatpally Housing Board Colony, Hyderabad – 500072\nEmail: info@megaviztech.com | Phone: +91 91541-83243 | Website: www.megaviztech.com")
    r.font.name = "Times New Roman"
    r.font.size = Pt(9.5)
    r.font.color.rgb = C_MUTED

    p_cert_title = doc.add_paragraph()
    p_cert_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_title.paragraph_format.space_before = Pt(8)
    p_cert_title.paragraph_format.space_after = Pt(18)
    r = p_cert_title.add_run("CERTIFICATE OF INTERNSHIP COMPLETION")
    r.font.name = "Times New Roman"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.underline = True

    add_body_p(doc, f"This is to formally certify that Mr. Shaik Charan, bearing Registration Number 72311068, a bona fide undergraduate student pursuing Bachelor of Technology (B.Tech) in Computer Science and Engineering with specialization in Artificial Intelligence and Data Science at CT University, Ludhiana, Punjab, has successfully completed a comprehensive 45 DAYS industrial internship at MegaViz Technologies Pvt Ltd, Hyderabad, from 20 June 2026 to 04 August 2026.")
    
    add_body_p(doc, f"During this intensive tenure, he operated in the capacity of AI & ML Developer and executed the research and technical development of the engineering project entitled \"ResearchIQ – Academic & Industrial Research Intelligence\". His role encompassed designing document ingestion workflows, evaluating sentence chunking algorithms, implementing vector embeddings with Sentence-Transformers, configuring Facebook AI Similarity Search (FAISS) vector indexes, engineering SQLite FTS5 hybrid retrieval pipelines, and integrating Groq Cloud LLMs for citation-grounded research synthesis.")

    add_body_p(doc, "Throughout the internship duration, Mr. Shaik Charan demonstrated exemplary technical proficiency, analytical rigor, disciplined work ethics, and sincere professional dedication. His performance, initiative, and project deliverables have been evaluated and rated as Outstanding.")

    p_sig_intro = doc.add_paragraph()
    p_sig_intro.paragraph_format.space_before = Pt(28)
    p_sig_intro.paragraph_format.space_after = Pt(18)

    # 4-Column Signature Table (Company Guide, Seal, Faculty Guide, HOD)
    sig_table = doc.add_table(rows=2, cols=4)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_table.autofit = False
    
    col_widths = [Inches(1.6), Inches(1.2), Inches(1.5), Inches(1.5)]
    for row in sig_table.rows:
        for i, w in enumerate(col_widths):
            row.cells[i].width = w

    format_cell(sig_table.cell(0, 0), "____________________\nMs. Kolla Geetha Madhuri\nChief Executive Officer (CEO)\nIndustry Guide & Supervisor\nMegaViz Technologies Pvt Ltd", bold=True, font_size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(sig_table.cell(0, 1), "\n[ COMPANY SEAL ]\nMegaViz Technologies\nHyderabad, India\n", bold=True, italic=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(sig_table.cell(0, 2), "____________________\n[ Faculty Guide Name ]\nAssistant Professor\nDept. of Computer Science & Eng.\nCT University, Punjab", bold=True, font_size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(sig_table.cell(0, 3), "____________________\nHead of Department (HOD)\nDept. of Computer Science & Eng.\nCT University, Ludhiana\nPunjab, India", bold=True, font_size=9, align=WD_ALIGN_PARAGRAPH.CENTER)

    format_cell(sig_table.cell(1, 0), "Date: 04 August 2026", font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(sig_table.cell(1, 1), "", font_size=8.5)
    format_cell(sig_table.cell(1, 2), "Date: ______________", font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(sig_table.cell(1, 3), "Date: ______________", font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)

    # =========================================================================
    # PRELIMINARY PAGE 2: STUDENT DECLARATION
    # =========================================================================
    doc.add_page_break()
    add_chap_heading(doc, "CANDIDATE'S DECLARATION")
    
    add_body_p(doc, f"I, Shaik Charan, bearing Registration Number 72311068, hereby declare that the industrial internship training and subsequent project report entitled \"ResearchIQ – Academic & Industrial Research Intelligence\" is an authentic record of independent work carried out by me during the academic year 2026–2027 in partial fulfillment of the requirements for the award of the degree of Bachelor of Technology (B.Tech) in Computer Science and Engineering with specialization in Artificial Intelligence and Data Science at CT University, Ludhiana, Punjab, India.")

    add_body_p(doc, f"I further declare that this internship was formally undertaken at MegaViz Technologies Pvt Ltd, located at #806, 8th Floor, Manjeera Trinity Corporate, Kukatpally, Hyderabad, Telangana, over a scheduled period of 45 DAYS from 20 June 2026 to 04 August 2026, under the direct industry mentorship and executive guidance of Ms. Kolla Geetha Madhuri, Chief Executive Officer (CEO).")

    add_body_p(doc, "The technical matter, algorithmic workflows, architectural diagrams, software code snippets, and experimental benchmarks embodied in this report have been developed, executed, and validated by me and have not been submitted in part or full for the award of any other degree, diploma, fellowship, or professional certification at this or any other university or academic institution.")

    add_body_p(doc, "All literature, documentation sources, research papers, software packages, and corporate references cited herein have been rigorously acknowledged in accordance with standard academic citation ethics and IEEE reference formats.")

    p_sig_dec = doc.add_paragraph()
    p_sig_dec.paragraph_format.space_before = Pt(45)
    p_sig_dec.paragraph_format.space_after = Pt(4)
    p_sig_dec.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p_sig_dec.add_run("_______________________________\nSHAIK CHARAN\nRegistration Number: 72311068\nB.Tech (CSE – AI & Data Science)\nCT University, Ludhiana, Punjab\nPlace: Hyderabad / Ludhiana\nDate: 04 August 2026")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    # =========================================================================
    # PRELIMINARY PAGE 3: ACKNOWLEDGEMENT
    # =========================================================================
    doc.add_page_break()
    add_chap_heading(doc, "ACKNOWLEDGEMENT")

    add_body_p(doc, "The successful conceptualization, engineering execution, and documentation of this industrial internship project report would not have been achievable without the invaluable guidance, academic encouragement, and professional mentorship extended by esteemed individuals and organizations.")

    add_body_p(doc, "First and foremost, I express my profound gratitude and highest regards to CT University, Ludhiana, Punjab, for conferring upon me the academic curriculum, computational resources, and administrative encouragement to undertake an advanced industrial internship in Artificial Intelligence and Machine Learning.")

    add_body_p(doc, "I extend my deepest gratitude and sincere appreciation to MegaViz Technologies Pvt Ltd, Hyderabad, for providing me with an exceptional corporate training ecosystem. In particular, I am immensely indebted to my Project Supervisor and Industry Guide, Ms. Kolla Geetha Madhuri, Chief Executive Officer (CEO), MegaViz Technologies Pvt Ltd, for her extraordinary technical mentorship, strategic vision, unwavering encouragement, and regular constructive feedback throughout the 45 DAYS of intensive internship from 20 June 2026 to 04 August 2026. Her deep insights into document intelligence, software scalability, and enterprise AI architectures provided the vital compass that steered the ResearchIQ project to completion.")

    add_body_p(doc, "I convey my heartfelt thanks to the Head of Department, Department of Computer Science and Engineering, CT University, and my Faculty Guide for their systematic academic oversight, structural advice, and meticulous evaluation during all review stages of the internship curriculum.")

    add_body_p(doc, "I also express my appreciation to the engineering team and developer colleagues at MegaViz Technologies Pvt Ltd for fostering a collaborative, technically stimulating, and innovative workplace atmosphere.")

    add_body_p(doc, "Finally, I owe my deepest debt of affection and gratitude to my family and friends for their unconditional patience, moral reinforcement, and belief in my endeavors throughout my academic journey.")

    p_ack_name = doc.add_paragraph()
    p_ack_name.paragraph_format.space_before = Pt(25)
    p_ack_name.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p_ack_name.add_run("SHAIK CHARAN\nReg. No: 72311068\nCT University, Punjab")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    # =========================================================================
    # PRELIMINARY PAGE 4: ABSTRACT
    # =========================================================================
    doc.add_page_break()
    add_chap_heading(doc, "ABSTRACT")

    add_body_p(doc, "The exponential expansion of scientific publications and technical industrial reports has created a profound research bottleneck: academic scholars, R&D engineers, and enterprise analysts spend an excessive proportion of their time manually reading, cross-referencing, and synthesizing multi-page PDF documents. While general-purpose Large Language Models (LLMs) offer promising summarization capabilities, their direct enterprise deployment suffers from context window saturation, high inference latency, parametric hallucinations, inability to detect subtle empirical contradictions between competing papers, and an absence of verifiable, page-level citation audit trails.")

    add_body_p(doc, "This internship project report presents ResearchIQ – Academic & Industrial Research Intelligence, a production-grade, local-first multi-document research assistant engineered during a 45 DAYS industrial internship at MegaViz Technologies Pvt Ltd, Hyderabad, under the guidance of CEO Ms. Kolla Geetha Madhuri. ResearchIQ implements a robust end-to-end Retrieval-Augmented Generation (RAG) architecture tailored for complex, multi-source scientific analysis.")

    add_body_p(doc, "The system pipeline begins with per-page text extraction and SHA-256 duplicate validation using PyMuPDF (fitz), strictly preserving original 1-indexed page boundaries while rejecting unreadable scanned PDFs. Extracted text is processed via sentence-boundary-aware chunking (750-character window with 150-character sliding overlap) and encoded into 384-dimensional dense vectors using the lightweight transformer sentence-transformers/all-MiniLM-L6-v2. For retrieval, ResearchIQ introduces a hybrid search engine fusing dense vector similarity via Facebook AI Similarity Search (FAISS IndexFlatIP) and sparse lexical matching via SQLite FTS5 BM25 utilizing Reciprocal Rank Fusion (RRF with constant k=60), while enforcing user-selected document isolation.")

    add_body_p(doc, "The grounded generation layer leverages Groq Cloud's ultra-low-latency Llama-3.3-70b-versatile LLM constrained by strict academic grounding prompts requiring mandatory [Document Title, p. X] citations, with automated fallback for insufficient evidence. Crucially, the platform incorporates an automated Cross-Document Contradiction Analysis Engine that aligns entities across papers to categorize claims as Agreement, Difference, or Potential Contradiction, alongside a 13-section Executive Research Brief generator with 1-click export to Markdown and styled ReportLab PDF. Empirical benchmarking on an academic battery technology corpus demonstrated a 100% Retrieval Hit Rate@5, 87.5% Mean Recall@5, and 100% Citation Coverage Rate, confirming ResearchIQ as an authoritative, transparent, and reproducible software platform for accelerated research synthesis.")

    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_before = Pt(12)
    r_kwh = p_kw.add_run("Keywords: ")
    r_kwh.font.name = "Times New Roman"
    r_kwh.font.bold = True
    r_kwt = p_kw.add_run("Retrieval-Augmented Generation (RAG), Natural Language Processing, Hybrid Retrieval, Reciprocal Rank Fusion, FAISS, SQLite FTS5, Contradiction Detection, Document Intelligence, PyMuPDF, Executive Brief Synthesis.")
    r_kwt.font.name = "Times New Roman"
    r_kwt.font.italic = True

    # =========================================================================
    # PRELIMINARY PAGE 5: TABLE OF CONTENTS
    # =========================================================================
    doc.add_page_break()
    add_chap_heading(doc, "TABLE OF CONTENTS")

    toc_items = [
        ("Candidate's Declaration", "ii"),
        ("Certificate of Internship Completion", "iii"),
        ("Acknowledgement", "iv"),
        ("Abstract", "v"),
        ("List of Figures", "viii"),
        ("List of Tables", "ix"),
        ("CHAPTER 1: INTRODUCTION", "1"),
        ("    1.1 Introduction", "1"),
        ("    1.2 Introduction to Artificial Intelligence", "1"),
        ("    1.3 Introduction to Machine Learning", "2"),
        ("    1.4 Internship Background", "3"),
        ("    1.5 Project Background", "3"),
        ("    1.6 Problem Statement", "4"),
        ("    1.7 Purpose of the Project", "4"),
        ("    1.8 Project Objectives", "5"),
        ("    1.9 Scope of the Project", "5"),
        ("    1.10 Proposed Solution", "6"),
        ("    1.11 Organization of the Report", "6"),
        ("CHAPTER 2: COMPANY PROFILE", "8"),
        ("    2.1 Introduction to MegaViz Technologies Pvt Ltd", "8"),
        ("    2.2 Company Background", "8"),
        ("    2.3 Company Vision and Mission", "9"),
        ("    2.4 Company Services and Products", "9"),
        ("    2.5 Software Development Services", "10"),
        ("    2.6 Website Design and Development", "10"),
        ("    2.7 Mobile Application Development", "11"),
        ("    2.8 Digital Marketing and SEO", "11"),
        ("    2.9 Company Technology Domain", "12"),
        ("    2.10 Organizational Overview", "12"),
        ("    2.11 Relevance to the Internship", "13"),
        ("CHAPTER 3: INTERNSHIP AND TRAINING DETAILS", "14"),
        ("    3.1 Introduction to Industrial Training", "14"),
        ("    3.2 Internship Objectives", "14"),
        ("    3.3 Internship Duration (45 DAYS)", "15"),
        ("    3.4 Internship Position – AI & ML Developer", "15"),
        ("    3.5 Project Supervisor and Industry Guide", "16"),
        ("    3.6 Training Methodology", "16"),
        ("    3.7 Training Environment", "17"),
        ("    3.8 Tools and Technologies Learned", "17"),
        ("    3.9 Roles and Responsibilities", "18"),
        ("    3.10 Daily Training Activities (39 Working Days Diary)", "19"),
        ("    3.11 Skills Acquired", "26"),
        ("    3.12 Learning Outcomes", "26"),
        ("CHAPTER 4: PROBLEM IDENTIFICATION AND SCOPE", "28"),
        ("    4.1 Project Introduction", "28"),
        ("    4.2 Existing System", "28"),
        ("    4.3 Limitations of Existing System", "29"),
        ("    4.4 Problem Identification", "30"),
        ("    4.5 Proposed System", "30"),
        ("    4.6 Advantages of Proposed System", "31"),
        ("    4.7 Functional Requirements", "32"),
        ("    4.8 Non-Functional Requirements", "33"),
        ("    4.9 Project Applications", "34"),
        ("    4.10 Project Scope", "34"),
        ("CHAPTER 5: SYSTEM REQUIREMENTS", "36"),
        ("    5.1 Introduction", "36"),
        ("    5.2 Hardware Requirements", "36"),
        ("    5.3 Software Requirements", "37"),
        ("    5.4 Programming Languages", "38"),
        ("    5.5 Frameworks and Libraries", "38"),
        ("    5.6 Database and Storage Requirements", "39"),
        ("    5.7 Development Environment", "40"),
        ("    5.8 System Configuration", "40"),
        ("CHAPTER 6: SYSTEM ARCHITECTURE AND DESIGN", "42"),
        ("    6.1 Introduction", "42"),
        ("    6.2 Overall System Architecture", "42"),
        ("    6.3 Document Upload Module", "44"),
        ("    6.4 PDF Text Extraction Module", "45"),
        ("    6.5 Text Preprocessing Module", "46"),
        ("    6.6 Text Chunking Module", "46"),
        ("    6.7 Embedding Generation Module", "48"),
        ("    6.8 FAISS Vector Indexing Module", "49"),
        ("    6.9 Semantic Retrieval Module", "50"),
        ("    6.10 RAG Processing Module", "51"),
        ("    6.11 Research Analysis Module", "52"),
        ("    6.12 Multi-Document Comparison", "53"),
        ("    6.13 Evidence and Reference Generation", "54"),
        ("    6.14 Complete System Workflow", "55"),
        ("CHAPTER 7: METHODOLOGY AND TOOLS", "57"),
        ("    7.1 Introduction", "57"),
        ("    7.2 Artificial Intelligence", "57"),
        ("    7.3 Machine Learning", "58"),
        ("    7.4 Natural Language Processing", "59"),
        ("    7.5 PDF Text Extraction", "60"),
        ("    7.6 Text Preprocessing", "60"),
        ("    7.7 Text Chunking", "61"),
        ("    7.8 Embedding Models", "62"),
        ("    7.9 FAISS Vector Search", "63"),
        ("    7.10 Semantic Retrieval", "64"),
        ("    7.11 Retrieval-Augmented Generation", "64"),
        ("    7.12 Backend Technologies", "65"),
        ("    7.13 Frontend Technologies", "66"),
        ("    7.14 Database and Storage", "67"),
        ("    7.15 Technology Integration", "68"),
        ("CHAPTER 8: IMPLEMENTATION DETAILS", "69"),
        ("    8.1 Introduction", "69"),
        ("    8.2 Development Environment Setup", "69"),
        ("    8.3 Project Directory Structure", "70"),
        ("    8.4 Document Upload Implementation", "71"),
        ("    8.5 PDF Text Extraction", "72"),
        ("    8.6 Text Cleaning and Preprocessing", "73"),
        ("    8.7 Text Chunking Implementation", "74"),
        ("    8.8 Embedding Generation", "75"),
        ("    8.9 FAISS Index Creation", "76"),
        ("    8.10 Semantic Search Implementation", "77"),
        ("    8.11 Document Retrieval", "78"),
        ("    8.12 RAG Pipeline Implementation", "79"),
        ("    8.13 Multi-Document Comparison", "80"),
        ("    8.14 Research Analysis", "81"),
        ("    8.15 Evidence Generation", "82"),
        ("    8.16 Frontend Implementation", "83"),
        ("    8.17 Backend Implementation", "84"),
        ("    8.18 Complete Application Execution", "85"),
        ("CHAPTER 9: TESTING AND EVALUATION", "87"),
        ("    9.1 Introduction to Software Testing", "87"),
        ("    9.2 Testing Objectives", "87"),
        ("    9.3 Testing Methodology", "88"),
        ("    9.4 Unit Testing", "88"),
        ("    9.5 Integration Testing", "89"),
        ("    9.6 Functional Testing", "90"),
        ("    9.7 System Testing", "90"),
        ("    9.8 Performance Testing", "91"),
        ("    9.9 Test Case Design", "91"),
        ("    9.10 Testing Results (Test Cases Table TC-01 to TC-15)", "92"),
        ("    9.11 Result Analysis", "95"),
        ("    9.12 Discussion and Screenshot Artifacts", "96"),
        ("CHAPTER 10: CHALLENGES, LEARNINGS AND PROBLEM SOLVING", "104"),
        ("    10.1 Technical Challenges", "104"),
        ("    10.2 PDF Processing Challenges", "104"),
        ("    10.3 Text Extraction Challenges", "105"),
        ("    10.4 Chunking and Embedding Challenges", "106"),
        ("    10.5 Vector Indexing Challenges", "107"),
        ("    10.6 Retrieval Accuracy Challenges", "107"),
        ("    10.7 Performance Challenges", "108"),
        ("    10.8 Solutions Implemented", "109"),
        ("    10.9 Technical Knowledge Acquired", "110"),
        ("    10.10 Professional Skills Developed", "110"),
        ("CHAPTER 11: CONCLUSION AND FUTURE ENHANCEMENTS", "112"),
        ("    11.1 Conclusion", "112"),
        ("    11.2 Project Objectives Achieved", "112"),
        ("    11.3 Project Outcomes", "113"),
        ("    11.4 Current Limitations", "114"),
        ("    11.5 Future Enhancements", "115"),
        ("    11.6 Practical Applications", "116"),
        ("REFERENCES", "118"),
        ("APPENDIX A: INTERNSHIP CERTIFICATE GUIDELINES", "121"),
        ("APPENDIX B: APPLICATION INSTALLATION & EXECUTION MANUAL", "123")
    ]

    toc_table = doc.add_table(rows=len(toc_items), cols=2)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    toc_table.autofit = False
    for i, (title, page) in enumerate(toc_items):
        is_chap = title.startswith("CHAPTER") or title in ["Candidate's Declaration", "Certificate of Internship Completion", "Acknowledgement", "Abstract", "List of Figures", "List of Tables", "REFERENCES", "APPENDIX A", "APPENDIX B"]
        format_cell(toc_table.cell(i, 0), title, bold=is_chap, font_size=10)
        format_cell(toc_table.cell(i, 1), page, bold=is_chap, font_size=10, align=WD_ALIGN_PARAGRAPH.RIGHT)
        toc_table.cell(i, 0).width = Inches(5.2)
        toc_table.cell(i, 1).width = Inches(0.8)

    # =========================================================================
    # PRELIMINARY PAGE 6: LIST OF FIGURES
    # =========================================================================
    doc.add_page_break()
    add_chap_heading(doc, "LIST OF FIGURES")

    figures_list = [
        ("Figure 6.1", "Overall ResearchIQ System Architecture", "43"),
        ("Figure 6.2", "Document Processing Workflow Pipeline", "45"),
        ("Figure 6.3", "Sentence-Boundary Chunking and Embedding Workflow", "47"),
        ("Figure 6.4", "FAISS Vector Indexing & ID Mapping Architecture", "49"),
        ("Figure 6.5", "Retrieval-Augmented Generation & Fusion Architecture", "52"),
        ("Figure 6.6", "Complete ResearchIQ End-to-End System Workflow", "56"),
        ("Figure 9.1", "Application Launch & Dashboard Interface Test", "97"),
        ("Figure 9.2", "PDF Document Upload & Validation Test", "97"),
        ("Figure 9.3", "PyMuPDF Text & Page Metadata Extraction Test", "98"),
        ("Figure 9.4", "Text Preprocessing & Sanitization Test", "98"),
        ("Figure 9.5", "Sentence-Aware Overlapping Text Chunking Test", "99"),
        ("Figure 9.6", "Embedding Vector Generation Test", "99"),
        ("Figure 9.7", "FAISS Vector Indexing & Storage Test", "100"),
        ("Figure 9.8", "Hybrid Semantic & Keyword Document Retrieval Test", "100"),
        ("Figure 9.9", "Evidence-Grounded RAG Question Answering Test", "101"),
        ("Figure 9.10", "Cross-Document Claim Comparison & Contradiction Test", "101"),
        ("Figure 9.11", "Evidence Explorer & Interactive Citation Navigation Test", "102"),
        ("Figure 9.12", "Final 13-Section Research Brief PDF & Markdown Export Test", "102")
    ]

    fig_table = doc.add_table(rows=len(figures_list) + 1, cols=3)
    fig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    fig_table.autofit = False
    format_cell(fig_table.cell(0, 0), "Figure No.", bold=True, font_size=10, bg_hex="F1F5F9")
    format_cell(fig_table.cell(0, 1), "Figure Caption / Title", bold=True, font_size=10, bg_hex="F1F5F9")
    format_cell(fig_table.cell(0, 2), "Page", bold=True, font_size=10, bg_hex="F1F5F9", align=WD_ALIGN_PARAGRAPH.RIGHT)
    fig_table.cell(0, 0).width = Inches(1.2)
    fig_table.cell(0, 1).width = Inches(4.1)
    fig_table.cell(0, 2).width = Inches(0.7)

    for i, (num, cap, page) in enumerate(figures_list):
        format_cell(fig_table.cell(i+1, 0), num, bold=True, font_size=9.5)
        format_cell(fig_table.cell(i+1, 1), cap, font_size=9.5)
        format_cell(fig_table.cell(i+1, 2), page, font_size=9.5, align=WD_ALIGN_PARAGRAPH.RIGHT)
        fig_table.cell(i+1, 0).width = Inches(1.2)
        fig_table.cell(i+1, 1).width = Inches(4.1)
        fig_table.cell(i+1, 2).width = Inches(0.7)

    # =========================================================================
    # PRELIMINARY PAGE 7: LIST OF TABLES
    # =========================================================================
    doc.add_page_break()
    add_chap_heading(doc, "LIST OF TABLES")

    tables_list = [
        ("Table 3.1", "Daily Training Activities Log (39 Working Days / 45 DAYS Period)", "19"),
        ("Table 5.1", "Hardware Environment Specifications", "37"),
        ("Table 5.2", "Software & Operating System Specifications", "37"),
        ("Table 5.3", "Programming Languages and Core Runtime Versions", "38"),
        ("Table 5.4", "Primary Python Libraries & Frameworks", "39"),
        ("Table 5.5", "Database Schema & Entity Specifications", "39"),
        ("Table 9.1", "Complete ResearchIQ Software Verification Test Cases (TC-01 to TC-15)", "92"),
        ("Table 9.2", "Empirical RAG Benchmark Evaluation Metrics", "95")
    ]

    tbl_table = doc.add_table(rows=len(tables_list) + 1, cols=3)
    tbl_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_table.autofit = False
    format_cell(tbl_table.cell(0, 0), "Table No.", bold=True, font_size=10, bg_hex="F1F5F9")
    format_cell(tbl_table.cell(0, 1), "Table Title / Description", bold=True, font_size=10, bg_hex="F1F5F9")
    format_cell(tbl_table.cell(0, 2), "Page", bold=True, font_size=10, bg_hex="F1F5F9", align=WD_ALIGN_PARAGRAPH.RIGHT)
    tbl_table.cell(0, 0).width = Inches(1.2)
    tbl_table.cell(0, 1).width = Inches(4.1)
    tbl_table.cell(0, 2).width = Inches(0.7)

    for i, (num, cap, page) in enumerate(tables_list):
        format_cell(tbl_table.cell(i+1, 0), num, bold=True, font_size=9.5)
        format_cell(tbl_table.cell(i+1, 1), cap, font_size=9.5)
        format_cell(tbl_table.cell(i+1, 2), page, font_size=9.5, align=WD_ALIGN_PARAGRAPH.RIGHT)
        tbl_table.cell(i+1, 0).width = Inches(1.2)
        tbl_table.cell(i+1, 1).width = Inches(4.1)
        tbl_table.cell(i+1, 2).width = Inches(0.7)

    # =========================================================================
    # SECTION 2: CHAPTER 1 ONWARD (Arabic Numerals: 1, 2, 3...)
    # =========================================================================
    sec_body = doc.add_section(WD_SECTION.NEW_PAGE)
    sec_body.page_width = Inches(8.27)
    sec_body.page_height = Inches(11.69)
    sec_body.left_margin = Inches(1.25)
    sec_body.right_margin = Inches(1.0)
    sec_body.top_margin = Inches(1.0)
    sec_body.bottom_margin = Inches(1.0)
    apply_page_borders(sec_body)
    add_header_footer(sec_body, is_roman=False)

    # Set Decimal Arabic Numbering starting at 1
    pgNumTypeBody = OxmlElement('w:pgNumType')
    pgNumTypeBody.set(qn('w:fmt'), 'decimal')
    pgNumTypeBody.set(qn('w:start'), '1')
    sec_body._sectPr.append(pgNumTypeBody)

    # -------------------------------------------------------------------------
    # CHAPTER 1: INTRODUCTION
    # -------------------------------------------------------------------------
    add_chap_heading(doc, "CHAPTER 1\nINTRODUCTION")

    add_sec_heading(doc, "1.1 Introduction")
    add_body_p(doc, "In the modern digital economy, the volume of published technical literature, scientific research papers, patent filings, and corporate analytical reports has expanded exponentially. Researchers, data scientists, academic scholars, and corporate decision-makers are inundated with hundreds of pages of complex, domain-specific text formatted primarily as Portable Document Format (PDF) files. The conventional paradigm of conducting literature reviews, competitive technology evaluations, and cross-source evidentiary analysis requires individuals to manually read dozens of multi-page documents, mentally track disparate claims, identify contradictions, and write syntheses. This manual approach is inherently labor-intensive, error-prone, cognitively exhausting, and unscalable.")

    add_sec_heading(doc, "1.2 Introduction to Artificial Intelligence")
    add_body_p(doc, "Artificial Intelligence (AI) constitutes a subfield of computer science dedicated to the development of computational systems capable of executing cognitive tasks traditionally associated with human intelligence. These tasks encompass visual perception, speech recognition, decision-making, and natural language understanding. In the context of enterprise document intelligence, modern AI harnesses advanced representation learning and neural architectures to convert unstructured human-authored prose into high-dimensional semantic spaces, enabling machines to understand thematic context, intent, and complex relational logic across vast textual corpora.")

    add_sec_heading(doc, "1.3 Introduction to Machine Learning")
    add_body_p(doc, "Machine Learning (ML), as the foundational operational branch of AI, provides systems with the computational ability to automatically learn patterns and infer relationships from empirical data without being explicitly programmed with deterministic heuristic rules. Deep learning, driven by multi-layered transformer neural networks, has fundamentally redefined Natural Language Processing (NLP). Large language models (LLMs) and transformer encoders now achieve unprecedented proficiency in semantic extraction, contextual embedding generation, and grammatical synthesis, providing the algorithmic backbone for automated information retrieval.")

    add_sec_heading(doc, "1.4 Internship Background")
    add_body_p(doc, f"This industrial internship was undertaken at MegaViz Technologies Pvt Ltd, located in Hyderabad, Telangana, India, for a designated curriculum duration of 45 DAYS from 20 June 2026 to 04 August 2026. Working under the executive guidance and technical mentorship of Ms. Kolla Geetha Madhuri, Chief Executive Officer (CEO), the author operated as an AI & ML Developer within the company's software intelligence division. The objective was to immerse in cutting-edge industrial AI development and engineer a scalable, robust, and reproducible enterprise research intelligence application.")

    add_sec_heading(doc, "1.5 Project Background")
    add_body_p(doc, "The project, designated \"ResearchIQ – Academic & Industrial Research Intelligence\", emerged from a tangible industrial and academic challenge: how to empower researchers to ingest collections of specialized PDFs, query across them simultaneously, detect subtle empirical disagreements between authors, and generate executive briefs backed by exact, auditable page citations. Rather than relying on generic black-box cloud chat wrappers, ResearchIQ was architected as a complete full-stack solution running locally on commodity hardware.")

    add_sec_heading(doc, "1.6 Problem Statement")
    add_body_p(doc, "Enterprise analysts and academic scholars encounter severe bottlenecks when analyzing multi-document corpora. First, feeding full 50+ page PDFs directly into LLM prompts exceeds token limits, generates massive latency, and costs significant funds. Second, generative LLMs suffer from parametric hallucinations, frequently generating fabricated metrics, dates, and non-existent citations. Third, existing single-document RAG tools cannot cross-compare multiple documents or detect when Paper A and Paper B present contradictory findings under identical experimental conditions. Finally, prevailing summarization tools fail to provide exact 1-indexed page citations, rendering responses unverified and academically untrustworthy.")

    add_sec_heading(doc, "1.7 Purpose of the Project")
    add_body_p(doc, "The fundamental purpose of ResearchIQ is to engineer an open, verifiable, and highly accurate multi-document research assistant that guarantees strict evidence grounding. By isolating user-selected documents, employing hybrid vector-keyword retrieval via Reciprocal Rank Fusion, verifying page numbers, and classifying contradictions, ResearchIQ transforms dense scientific literature into structured, actionable intelligence.")

    add_sec_heading(doc, "1.8 Project Objectives")
    add_bullet_p(doc, "1. Multi-Document Ingestion:", "Support drag-and-drop ingestion of multiple research PDFs up to 20MB with SHA-256 duplicate validation.")
    add_bullet_p(doc, "2. Page-Preserving Text Parsing:", "Extract raw textual passages using PyMuPDF (fitz) while strictly preserving 1-indexed page boundaries.")
    add_bullet_p(doc, "3. Sentence-Aware Chunking:", "Implement overlapping text chunking (750 chars, 150 overlap) respecting sentence syntax.")
    add_bullet_p(doc, "4. Dense Vector Indexing:", "Generate 384-dimensional normalized vector embeddings and index them locally via FAISS IndexFlatIP.")
    add_bullet_p(doc, "5. Hybrid Retrieval Architecture:", "Combine FAISS semantic search and SQLite FTS5 BM25 keyword matching using Reciprocal Rank Fusion.")
    add_bullet_p(doc, "6. Contradiction Detection Engine:", "Extract claims across papers to classify agreements, differences, and potential empirical contradictions.")
    add_bullet_p(doc, "7. Executive Brief Synthesis:", "Generate 13-section academic research briefs with 1-click export to Markdown and styled ReportLab PDF.")
    add_bullet_p(doc, "8. Interactive Citation Explorer:", "Provide clickable citation tags in the UI that smoothly scroll to and highlight exact retrieved passages.")

    add_sec_heading(doc, "1.9 Scope of the Project")
    add_body_p(doc, "The project scope encompasses local processing on Windows development machines, complete offline vector search, deterministic prompt engineering with Groq Cloud LLM APIs, relational SQLite storage, a modular FastAPI backend, and an interactive React/TypeScript frontend. It intentionally focuses on text-based scientific PDFs, leaving multi-modal optical character recognition (OCR) for scanned image documents as documented future scope.")

    add_sec_heading(doc, "1.10 Proposed Solution")
    add_body_p(doc, "ResearchIQ addresses the identified problems through a four-stage architecture: (A) Page-Level Ingestion & Text Sanitization; (B) Local Embedding & Hybrid Vector/FTS5 Indexing; (C) Reciprocal Rank Fusion Retrieval with Document Isolation; and (D) Citation-Grounded LLM Generation and Cross-Document Matrix Alignment. This guarantees that every statement made by the AI cites verifiable evidence [Document Title, p. X].")

    add_sec_heading(doc, "1.11 Organization of the Report")
    add_body_p(doc, "This internship report is systematically structured into 11 chapters. Chapter 2 presents the corporate profile of MegaViz Technologies Pvt Ltd. Chapter 3 details the industrial internship training, supervision, and daily diary. Chapter 4 explores problem formulation and requirements. Chapter 5 details hardware, software, and library requirements. Chapter 6 presents system architecture and workflow diagrams. Chapter 7 analyzes foundational methodologies and algorithms. Chapter 8 provides implementation details and code snippets. Chapter 9 presents software testing methodologies and test case results. Chapter 10 examines technical challenges, solutions, and acquired skills. Chapter 11 concludes the report and highlights future enhancements, followed by academic references and technical appendices.")

    # -------------------------------------------------------------------------
    # CHAPTER 2: COMPANY PROFILE
    # -------------------------------------------------------------------------
    doc.add_page_break()
    add_chap_heading(doc, "CHAPTER 2\nCOMPANY PROFILE")

    add_sec_heading(doc, "2.1 Introduction to MegaViz Technologies Pvt Ltd")
    add_body_p(doc, "MegaViz Technologies Pvt Ltd is a premier software development, digital engineering, and technology consulting firm headquartered in Hyderabad, Telangana, India. Operating from its corporate headquarters at #806, 8th Floor, Manjeera Trinity Corporate in Kukatpally, the organization delivers high-impact digital transformation solutions, bespoke software applications, enterprise mobile platforms, advanced digital marketing services, and artificial intelligence development for global and regional enterprises.")

    add_sec_heading(doc, "2.2 Company Background")
    add_body_p(doc, "Established with a focus on modern software craftsmanship, MegaViz Technologies has cultivated specialized expertise across end-to-end full-stack software development, responsive web architectures, cross-platform mobile computing (Android & iOS), cloud database administration, search engine optimization (SEO), and applied machine learning. The firm operates with a strong commitment to quality standards, modern software engineering methodologies, and client-centric development models.")

    add_sec_heading(doc, "2.3 Company Vision and Mission")
    add_bullet_p(doc, "Corporate Vision:", "To be a globally recognized technology partner that empowers businesses to innovate, transform, and scale through cutting-edge digital engineering, intelligent software solutions, and data-driven artificial intelligence systems.")
    add_bullet_p(doc, "Corporate Mission:", "To deliver robust, scalable, and secure software applications through continuous innovation, ethical engineering standards, and technical excellence, while nurturing talent through high-impact industrial internships and research development.")

    add_sec_heading(doc, "2.4 Company Services and Products")
    add_body_p(doc, "MegaViz Technologies provides a diversified suite of professional IT services designed to support enterprise digital presence, workflow automation, and operational efficiency:")
    add_bullet_p(doc, "• Custom Software Development:", "Engineering tailored enterprise applications, inventory management, CRM, and workflow tools.")
    add_bullet_p(doc, "• Website Design & Web Applications:", "Responsive, secure corporate web platforms utilizing modern JavaScript/TypeScript ecosystems.")
    add_bullet_p(doc, "• Mobile Application Development:", "Native and cross-platform mobile apps for Android and iOS using modern mobile SDKs.")
    add_bullet_p(doc, "• Digital Marketing & SEO Services:", "Comprehensive digital branding, organic SEO, technical auditing, and search marketing.")
    add_bullet_p(doc, "• UI/UX & Graphic Design:", "Human-centric interface design, wireframing, component libraries, and interactive prototyping.")
    add_bullet_p(doc, "• Emerging AI & Data Intelligence:", "Data analysis, retrieval systems, and machine learning integration for automated business workflows.")

    add_sec_heading(doc, "2.5 Software Development Services")
    add_body_p(doc, "The software engineering division at MegaViz Technologies builds custom enterprise software using modern asynchronous backends (Python, FastAPI, Node.js), robust relational and NoSQL databases, and modular microservices. Applications adhere to strict security protocols, parameter validation, REST architectural principles, and automated testing.")

    add_sec_heading(doc, "2.6 Website Design and Development")
    add_body_p(doc, "MegaViz Technologies crafts high-performance web applications using modern front-end frameworks such as React, Vue.js, and TypeScript, styled with Tailwind CSS. Development emphasizes mobile responsiveness, accessibility standards (WCAG), fast core web vitals, and clean API integration.")

    add_sec_heading(doc, "2.7 Mobile Application Development")
    add_body_p(doc, "The company's mobile development team creates performant, cross-platform mobile solutions using Flutter and React Native. The applications feature smooth touch interactions, local offline data synchronization, secure payment gateway integrations, and robust RESTful API connectivity.")

    add_sec_heading(doc, "2.8 Digital Marketing and SEO")
    add_body_p(doc, "MegaViz Technologies delivers data-driven digital marketing solutions covering search engine optimization (SEO), search engine marketing (SEM), social media marketing (SMM), and digital analytics. The team utilizes keyword intelligence, backlink profiling, and performance auditing to drive verified organic visibility for commercial partners.")

    add_sec_heading(doc, "2.9 Company Technology Domain")
    add_body_p(doc, "The core technological competencies of MegaViz Technologies span Python, TypeScript, React, Node.js, FastAPI, PostgreSQL, SQLite, FAISS vector indexing, Flutter, Tailwind CSS, Docker, and REST API development. The organization actively evaluates emerging AI paradigms such as Retrieval-Augmented Generation, vector embeddings, and language model integration for document automation.")

    add_sec_heading(doc, "2.10 Organizational Overview")
    add_body_p(doc, "MegaViz Technologies operates under the executive leadership of Chief Executive Officer Ms. Kolla Geetha Madhuri. The organizational hierarchy comprises Project Management, Software Engineering, Mobile Development, Quality Assurance & Testing, Digital Marketing, and AI Research & Development. The firm maintains an open, engineering-first culture that encourages research exploration, rapid prototyping, and rigorous software verification.")

    add_sec_heading(doc, "2.11 Relevance to the Internship")
    add_body_p(doc, "The software engineering, data architecture, and AI exploration capabilities of MegaViz Technologies provided the ideal industrial environment for the author's internship as an AI & ML Developer. Mentorship from CEO Ms. Kolla Geetha Madhuri provided critical guidance on software design, modular API architecture, vector database scalability, and practical user interface design, culminating in the development of the ResearchIQ platform.")

    # -------------------------------------------------------------------------
    # CHAPTER 3: INTERNSHIP AND TRAINING DETAILS
    # -------------------------------------------------------------------------
    doc.add_page_break()
    add_chap_heading(doc, "CHAPTER 3\nINTERNSHIP AND TRAINING DETAILS")

    add_sec_heading(doc, "3.1 Introduction to Industrial Training")
    add_body_p(doc, "Industrial training is a mandatory pedagogical requirement of the Bachelor of Technology (B.Tech) curriculum at CT University. It bridges theoretical computer science education with real-world enterprise engineering practices. During industrial training, students gain firsthand exposure to production software architectures, agile methodologies, code review standards, and enterprise problem-solving under professional mentorship.")

    add_sec_heading(doc, "3.2 Internship Objectives")
    add_bullet_p(doc, "• Technical Immersion:", "Acquire deep practical skills in Natural Language Processing, vector embeddings, and full-stack software development.")
    add_bullet_p(doc, "• Software Engineering Rigor:", "Apply professional development practices, including modular design, git version control, API standardization, and automated unit testing.")
    add_bullet_p(doc, "• Problem Formulation:", "Identify gaps in existing scientific document summarization tools and architect a working, reproducible RAG solution.")
    add_bullet_p(doc, "• Industry Mentorship:", "Work closely under executive technical guidance to understand corporate software development standards and timelines.")

    add_sec_heading(doc, "3.3 Internship Duration (45 DAYS)")
    add_body_p(doc, "The industrial internship was formally scheduled and executed for a designated duration of 45 DAYS, commencing on 20 June 2026 and concluding on 04 August 2026. Across this comprehensive 45 DAYS timeframe, 39 intensive working days were conducted on-site at MegaViz Technologies Pvt Ltd, with all 7 intervening Sundays strictly excluded from formal office diary entries.")

    add_sec_heading(doc, "3.4 Internship Position – AI & ML Developer")
    add_body_p(doc, "The author was appointed to the position of AI & ML Developer within the Software and AI Research Division of MegaViz Technologies Pvt Ltd. The primary responsibilities encompassed architectural design, backend algorithm implementation, vector search optimization, prompt engineering, and UI development for the ResearchIQ platform.")

    add_sec_heading(doc, "3.5 Project Supervisor and Industry Guide")
    add_body_p(doc, "The internship was conducted under the direct supervision and industry guidance of Ms. Kolla Geetha Madhuri, Chief Executive Officer (CEO), MegaViz Technologies Pvt Ltd. Ms. Kolla Geetha Madhuri provided continuous technical mentoring, architectural direction, review of daily milestone achievements, and formal evaluation of project deliverables.")

    add_sec_heading(doc, "3.6 Training Methodology")
    add_body_p(doc, "The training followed an iterative, agile engineering methodology comprising five distinct phases: (1) Technical Exploration & Requirements Definition; (2) Data Ingestion & Chunking Algorithm Development; (3) Vector Search & RRF Hybrid Retrieval Implementation; (4) Full-Stack User Interface & API Integration; and (5) Automated Verification, Benchmarking, and Final Project Review.")

    add_sec_heading(doc, "3.7 Training Environment")
    add_body_p(doc, "The development workstation operated on Windows 11 Enterprise (64-bit), utilizing Python 3.11 for asynchronous backend engineering and Node.js 24 for frontend development. Visual Studio Code was employed as the primary integrated development environment, supported by Git for version management and PowerShell for local automation scripting.")

    add_sec_heading(doc, "3.8 Tools and Technologies Learned")
    add_body_p(doc, "During the internship, the author achieved practical proficiency in: (1) PyMuPDF (fitz) for PDF text and metadata extraction; (2) Sentence-Transformers for generating high-dimensional dense text embeddings; (3) Facebook AI Similarity Search (FAISS) for inner-product vector indexing; (4) SQLite FTS5 for native BM25 full-text indexing; (5) FastAPI and Uvicorn for asynchronous REST API development; (6) React 19, TypeScript, and Vite for modern user interface engineering; (7) Tailwind CSS for commercial SaaS styling; and (8) ReportLab for programmatic PDF report generation.")

    add_sec_heading(doc, "3.9 Roles and Responsibilities")
    add_bullet_p(doc, "• Algorithmic Design:", "Design sentence-boundary text chunking and Reciprocal Rank Fusion ranking pipelines.")
    add_bullet_p(doc, "• Service Engineering:", "Implement modular Python backend services for extraction, embedding, retrieval, and LLM orchestration.")
    add_bullet_p(doc, "• Frontend Construction:", "Develop reusable React/TypeScript components, interactive workspace panels, and citation explorers.")
    add_bullet_p(doc, "• Quality Assurance:", "Write automated pytest test suites, perform manual user scenario testing, and measure retrieval benchmarks.")
    add_bullet_p(doc, "• Progress Reporting:", "Maintain structured daily engineering logs and present technical progress during weekly review sessions with CEO Ms. Kolla Geetha Madhuri.")

    add_sec_heading(doc, "3.10 Daily Training Activities (39 Working Days Diary)")
    add_body_p(doc, "The table below documents the comprehensive daily training activities, work performed, and learning outcomes across the 45 DAYS internship tenure from 20 June 2026 to 04 August 2026. All Sundays have been strictly excluded in accordance with industrial documentation guidelines.")

    # Table 3.1: Daily Training Activities
    p_t_cap = doc.add_paragraph()
    p_t_cap.paragraph_format.space_before = Pt(8)
    p_t_cap.paragraph_format.space_after = Pt(4)
    r = p_t_cap.add_run("Table 3.1: Daily Training Activities Log (39 Working Days / 45 DAYS Curriculum Period)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.bold = True

    diary_table = doc.add_table(rows=len(DAILY_DIARY) + 1, cols=5)
    diary_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    diary_table.autofit = False

    col_widths = [Inches(0.9), Inches(0.9), Inches(1.3), Inches(1.7), Inches(1.4)]
    headers = ["Date", "Day", "Training Activity", "Work Performed", "Learning Outcome"]
    
    for c_idx, h_text in enumerate(headers):
        format_cell(diary_table.cell(0, c_idx), h_text, bold=True, font_size=9, bg_hex="E2E8F0", align=WD_ALIGN_PARAGRAPH.CENTER)
        diary_table.cell(0, c_idx).width = col_widths[c_idx]

    for r_idx, entry in enumerate(DAILY_DIARY):
        row_cells = diary_table.rows[r_idx + 1].cells
        format_cell(row_cells[0], entry["date"], font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)
        format_cell(row_cells[1], entry["day"], font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)
        format_cell(row_cells[2], entry["activity"], bold=True, font_size=8.5)
        format_cell(row_cells[3], entry["work"], font_size=8.5)
        format_cell(row_cells[4], entry["outcome"], font_size=8.5)
        for c_idx, w in enumerate(col_widths):
            row_cells[c_idx].width = w

    add_sec_heading(doc, "3.11 Skills Acquired")
    add_body_p(doc, "The internship facilitated substantial technical and professional skill growth. Technical competencies acquired include vector embedding mathematical foundations, dense/sparse search hybrid fusion, asynchronous API design in FastAPI, TypeScript type safety, and local vector index management. Professional skills developed include agile project structuring, technical writing, software testing, time management, and direct communication with executive leadership.")

    add_sec_heading(doc, "3.12 Learning Outcomes")
    add_body_p(doc, "Upon completion of the 45 DAYS industrial internship, the author successfully: (1) Formulated and executed an industrial-grade AI document intelligence platform from concept to deployment; (2) Mastered the design of verifiable RAG architectures that prevent LLM hallucinations; (3) Gained hands-on experience in building commercial-grade responsive web user interfaces; and (4) Demonstrated full-stack software testing, automated benchmarking, and technical presentation skills.")

    # Save initial progress
    doc.save(DOCX_PATH)
    print("Preliminary Pages & Chapters 1-3 written.")

if __name__ == "__main__":
    generate_report()
