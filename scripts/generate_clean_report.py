"""
generate_clean_report.py
========================
Builds the polished, university-standard B.Tech Project Report for CT University:
- Page i Certificate removed completely.
- Preliminary pages: Declaration (i), Acknowledgement (ii), Abstract (iii), TOC (iv), LOF (v), LOT (vi).
- No training or daily diary logs.
- Functional & Non-Functional Requirements in explicit academic tables.
- Running header: "RESEARCHIQ – PROJECT REPORT" | "CT UNIVERSITY" (NO MegaViz in header).
- No blank or empty pages anywhere.
- Screenshots: Figures 9.1 to 9.5 ONLY (Figures 9.6 to 9.12 removed).
- 1 pt Four-Sided Black Border on EVERY SINGLE PAGE (both DOCX and PDF).
- Accurate, synchronized page numbers and Table of Contents.
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_DIR = os.path.join(BASE_DIR, "ResearchIQ_Internship_Report")
FIG_DIR = os.path.join(REPORT_DIR, "figures")
DOCX_PATH = os.path.join(REPORT_DIR, "ResearchIQ_Internship_Report.docx")

C_BLACK = RGBColor(0, 0, 0)
C_NAVY = RGBColor(30, 58, 138)
C_DARK = RGBColor(15, 23, 42)
C_GRAY = RGBColor(71, 85, 105)

def apply_page_border(section):
    sectPr = section._sectPr
    for existing in sectPr.findall(qn('w:pgBorders')):
        sectPr.remove(existing)
    borders_elm = parse_xml(
        '<w:pgBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'w:offsetFrom="page" w:z-order="front">\n'
        '  <w:top w:val="single" w:sz="8" w:space="24" w:color="000000"/>\n'
        '  <w:left w:val="single" w:sz="8" w:space="24" w:color="000000"/>\n'
        '  <w:bottom w:val="single" w:sz="8" w:space="24" w:color="000000"/>\n'
        '  <w:right w:val="single" w:sz="8" w:space="24" w:color="000000"/>\n'
        '</w:pgBorders>'
    )
    sectPr.append(borders_elm)

def setup_header_footer(section, is_roman=False):
    section.header_distance = Inches(0.4)
    section.footer_distance = Inches(0.4)

    # Header
    header = section.header
    header.is_linked_to_previous = False
    p_hdr = header.paragraphs[0]
    p_hdr.text = ""
    p_hdr.paragraph_format.space_before = Pt(0)
    p_hdr.paragraph_format.space_after = Pt(4)
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    r_left = p_hdr.add_run("RESEARCHIQ – PROJECT REPORT\t\tCT UNIVERSITY")
    r_left.font.name = "Times New Roman"
    r_left.font.size = Pt(8.5)
    r_left.font.bold = True
    r_left.font.color.rgb = RGBColor(71, 85, 105)

    # Footer
    footer = section.footer
    footer.is_linked_to_previous = False
    p_ftr = footer.paragraphs[0]
    p_ftr.text = ""
    p_ftr.paragraph_format.space_before = Pt(4)
    p_ftr.paragraph_format.space_after = Pt(0)
    p_ftr.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    r_f_left = p_ftr.add_run("SHAIK CHARAN | REG. NO: 72311068\t\tPage ")
    r_f_left.font.name = "Times New Roman"
    r_f_left.font.size = Pt(8.5)
    r_f_left.font.color.rgb = RGBColor(71, 85, 105)

    # Dynamic page number
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    p_ftr._p.append(fldSimple)

def add_body_p(doc, text, bold_prefix="", space_after=6, italic_prefix=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    if bold_prefix:
        r_bold = p.add_run(bold_prefix)
        r_bold.font.name = "Times New Roman"
        r_bold.font.size = Pt(11)
        r_bold.font.bold = True
        r_bold.font.italic = italic_prefix
        r_bold.font.color.rgb = C_BLACK

    r_text = p.add_run(text)
    r_text.font.name = "Times New Roman"
    r_text.font.size = Pt(11)
    r_text.font.color.rgb = C_BLACK
    return p

def add_bullet_p(doc, text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    if bold_prefix:
        r_bold = p.add_run(bold_prefix)
        r_bold.font.name = "Times New Roman"
        r_bold.font.size = Pt(11)
        r_bold.font.bold = True
        r_bold.font.color.rgb = C_BLACK

    r_text = p.add_run(text)
    r_text.font.name = "Times New Roman"
    r_text.font.size = Pt(11)
    r_text.font.color.rgb = C_BLACK
    return p

def add_chap_heading(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(12)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.color.rgb = C_NAVY
    return p

def add_sec_heading(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = C_NAVY
    return p

def add_subsec_heading(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(11.5)
    run.font.bold = True
    run.font.color.rgb = C_DARK
    return p

def add_figure(doc, img_name, fig_num, caption):
    img_path = os.path.join(FIG_DIR, img_name)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(3)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(5.7))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(8)
        r_num = p_cap.add_run(f"Figure {fig_num}: ")
        r_num.font.name = "Times New Roman"
        r_num.font.size = Pt(9.5)
        r_num.font.bold = True
        r_num.font.color.rgb = C_NAVY
        r_cap = p_cap.add_run(caption)
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(9.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = C_BLACK

def format_cell(cell, text, bold=False, italic=False, font_size=9, bg_hex=None, align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.text = text
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.1
    for r in p.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(font_size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = RGBColor(255, 255, 255) if bg_hex == "1E3A8A" else C_BLACK
    if bg_hex:
        shading = parse_xml(f'<w:shd xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:val="clear" w:color="auto" w:fill="{bg_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

def add_code_block(doc, code_str):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.0)
    shading = parse_xml('<w:shd xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:val="clear" w:color="auto" w:fill="F8FAFC"/>')
    cell._tc.get_or_add_tcPr().append(shading)
    borders = parse_xml(
        '<w:tcBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">\n'
        '  <w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>\n'
        '  <w:left w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>\n'
        '  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>\n'
        '  <w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>\n'
        '</w:tcBorders>'
    )
    cell._tc.get_or_add_tcPr().append(borders)
    cell.text = code_str
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.05
    for r in p.runs:
        r.font.name = "Consolas"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
