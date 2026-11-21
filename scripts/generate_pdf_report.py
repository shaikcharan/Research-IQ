"""
generate_pdf_report.py
======================
Compiles the university-standard B.Tech Project Report PDF for CT University:
- Official University Front Cover Page with CT University Logo, Title, Submitted By, Under Guidance Of.
- Preliminary pages start with Candidate's Declaration on page i, Acknowledgement (ii), Abstract (iii), TOC (iv), LOF (vi), LOT (vii).
- Running header: "RESEARCHIQ – PROJECT REPORT" | "CT UNIVERSITY" (NO MegaViz in header).
- Running footer: "SHAIK CHARAN | REG. NO: 72311068" | "Page X" (or Roman numerals for prelims).
- Four-sided 1 pt black border on EVERY SINGLE PAGE.
- Embedded figures: CT University Logo, Figures 6.1 to 6.6, and Figures 9.1 to 9.5 (12 images total).
- No blank or empty pages anywhere.
"""

import os
import re
import html
import docx
from docx.oxml.ns import qn

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image,
    PageBreak, KeepTogether, Flowable, HRFlowable
)
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCX_PATH = os.path.join(BASE_DIR, "ResearchIQ_Internship_Report", "ResearchIQ_Internship_Report.docx")
PDF_PATH = os.path.join(BASE_DIR, "ResearchIQ_Internship_Report", "ResearchIQ_Internship_Report.pdf")
FIG_DIR = os.path.join(BASE_DIR, "ResearchIQ_Internship_Report", "figures")

FIGURE_FILES = [
    "ct_university_logo.png",
    "fig_6_1_architecture.png",
    "fig_6_2_doc_processing.png",
    "fig_6_3_chunking_embedding.png",
    "fig_6_4_faiss_indexing.png",
    "fig_6_5_rag_architecture.png",
    "fig_6_6_complete_workflow.png",
    "fig_9_1_app_launch.png",
    "fig_9_2_pdf_upload.png",
    "fig_9_3_text_extraction.png",
    "fig_9_4_text_preprocessing.png",
    "fig_9_5_chunking.png",
]

class SectionMarker(Flowable):
    def __init__(self, section_name):
        super().__init__()
        self.section_name = section_name

    def draw(self):
        self.canv._current_section = self.section_name

class UniversityCanvas(canvas.Canvas):
    """
    Two-pass canvas that renders:
    1. Four-sided 1 pt black page border on EVERY SINGLE PAGE.
    2. Cover page: unnumbered, clean borders, no running header.
    3. Preliminary pages: Roman numerals (i, ii, iii...).
    4. Main body: Running header (RESEARCHIQ – PROJECT REPORT | CT UNIVERSITY) and Arabic numerals.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []
        self._current_section = "cover"

    def showPage(self):
        self.pages.append((dict(self.__dict__), self._current_section))
        self._startPage()

    def save(self):
        num_pages = len(self.pages)
        main_page_counter = 0
        prelim_page_counter = 0

        def to_roman(n):
            val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
            syb = ["m", "cm", "d", "cd", "c", "xc", "l", "xl", "x", "ix", "v", "iv", "i"]
            res = ""
            for v, s in zip(val, syb):
                while n >= v:
                    res += s
                    n -= v
            return res

        for idx, (state, sec) in enumerate(self.pages):
            self.__dict__.update(state)
            w, h = A4

            # 1. Four-sided black border on EVERY SINGLE PAGE (24 pt = 0.33 in margin)
            self.saveState()
            self.setStrokeColor(colors.black)
            self.setLineWidth(1.0)
            self.rect(24, 24, w - 48, h - 48)

            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#334155"))

            if sec == "cover":
                # Cover page has NO headers or footers
                pass
            elif sec == "main":
                main_page_counter += 1
                # Running Header (NO MEGAVIZ!)
                self.drawString(36, h - 38, "RESEARCHIQ – PROJECT REPORT")
                self.setFont("Helvetica", 8)
                self.drawRightString(w - 36, h - 38, "CT UNIVERSITY")
                self.setStrokeColor(colors.HexColor("#94A3B8"))
                self.setLineWidth(0.5)
                self.line(36, h - 42, w - 36, h - 42)

                # Running Footer
                self.line(36, 42, w - 36, 42)
                self.drawString(36, 30, "SHAIK CHARAN | REG. NO: 72311068")
                self.drawRightString(w - 36, 30, f"Page {main_page_counter}")
            else:
                prelim_page_counter += 1
                # Running Footer for Preliminaries
                self.setStrokeColor(colors.HexColor("#94A3B8"))
                self.setLineWidth(0.5)
                self.line(36, 42, w - 36, 42)
                self.drawString(36, 30, "SHAIK CHARAN | REG. NO: 72311068")
                self.drawRightString(w - 36, 30, to_roman(prelim_page_counter))

            self.restoreState()
            super().showPage()
        super().save()


def build_pdf():
    print(f"Reading DOCX from: {DOCX_PATH}")
    doc = docx.Document(DOCX_PATH)

    styles = getSampleStyleSheet()

    # Cover Page Specific Styles
    style_cover_univ = ParagraphStyle(
        "CoverUniv",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1E3A8A"),
        alignment=TA_CENTER,
        spaceAfter=3,
    )
    style_cover_school = ParagraphStyle(
        "CoverSchool",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#0F172A"),
        alignment=TA_CENTER,
        spaceAfter=2,
    )
    style_cover_dept = ParagraphStyle(
        "CoverDept",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=13.5,
        textColor=colors.HexColor("#1E3A8A"),
        alignment=TA_CENTER,
        spaceAfter=2,
    )
    style_cover_loc = ParagraphStyle(
        "CoverLoc",
        parent=styles["Normal"],
        fontName="Times-Italic",
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor("#475569"),
        alignment=TA_CENTER,
        spaceAfter=6,
    )
    style_cover_banner = ParagraphStyle(
        "CoverBanner",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#0F172A"),
        alignment=TA_CENTER,
        spaceBefore=4,
        spaceAfter=3,
    )
    style_cover_on = ParagraphStyle(
        "CoverOn",
        parent=styles["Normal"],
        fontName="Times-Italic",
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor("#475569"),
        alignment=TA_CENTER,
        spaceAfter=3,
    )
    style_cover_title = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#1E3A8A"),
        alignment=TA_CENTER,
        spaceAfter=3,
    )
    style_cover_sub = ParagraphStyle(
        "CoverSub",
        parent=styles["Normal"],
        fontName="Times-Italic",
        fontSize=9.5,
        leading=12.5,
        textColor=colors.HexColor("#0F172A"),
        alignment=TA_CENTER,
        spaceAfter=8,
    )
    style_cover_deg = ParagraphStyle(
        "CoverDeg",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#0F172A"),
        alignment=TA_CENTER,
        spaceAfter=8,
    )
    style_cover_bot = ParagraphStyle(
        "CoverBot",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#1E3A8A"),
        alignment=TA_CENTER,
        spaceBefore=10,
    )

    # General Report Styles
    style_prelim_title = ParagraphStyle(
        "PrelimTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=13.5,
        leading=17,
        textColor=colors.HexColor("#0F172A"),
        alignment=TA_CENTER,
        spaceBefore=8,
        spaceAfter=10,
        keepWithNext=True,
    )
    style_chap_title = ParagraphStyle(
        "ChapterTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=17.5,
        textColor=colors.HexColor("#1E3A8A"),
        alignment=TA_CENTER,
        spaceBefore=10,
        spaceAfter=8,
        keepWithNext=True,
    )
    style_h2 = ParagraphStyle(
        "ReportH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14.5,
        textColor=colors.HexColor("#1E3A8A"),
        alignment=TA_LEFT,
        spaceBefore=9,
        spaceAfter=3,
        keepWithNext=True,
    )
    style_h3 = ParagraphStyle(
        "ReportH3",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#0F172A"),
        alignment=TA_LEFT,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True,
    )
    style_body = ParagraphStyle(
        "ReportBody",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=9.5,
        leading=12.5,
        textColor=colors.HexColor("#1E293B"),
        alignment=TA_JUSTIFY,
        spaceAfter=4.5,
    )
    style_bullet = ParagraphStyle(
        "ReportBullet",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=9.5,
        leading=12.5,
        textColor=colors.HexColor("#1E293B"),
        alignment=TA_LEFT,
        leftIndent=14,
        firstLineIndent=-8,
        spaceAfter=2.5,
    )
    style_caption = ParagraphStyle(
        "ReportCaption",
        parent=styles["Italic"],
        fontName="Times-Italic",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#334155"),
        alignment=TA_CENTER,
        spaceBefore=2,
        spaceAfter=5,
    )
    style_code = ParagraphStyle(
        "ReportCode",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#0F172A"),
        alignment=TA_LEFT,
    )
    style_th = ParagraphStyle(
        "ReportTH",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=10,
        textColor=colors.white,
        alignment=TA_CENTER,
    )
    style_td = ParagraphStyle(
        "ReportTD",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#0F172A"),
        alignment=TA_LEFT,
    )
    style_td_center = ParagraphStyle(
        "ReportTDCenter",
        parent=style_td,
        alignment=TA_CENTER,
    )
    style_td_right = ParagraphStyle(
        "ReportTDRight",
        parent=style_td,
        alignment=TA_RIGHT,
    )

    story = []
    current_section = "cover"
    image_counter = 0

    body_elements = list(doc.element.body)
    print(f"Total DOCX body elements to compile: {len(body_elements)}")

    for elem in body_elements:
        tag = elem.tag.split("}")[-1]

        if tag == "sectPr":
            if current_section == "cover":
                current_section = "prelim"
                story.append(SectionMarker("prelim"))
                story.append(PageBreak())
            elif current_section == "prelim":
                current_section = "main"
                story.append(SectionMarker("main"))
                story.append(PageBreak())
            continue

        elif tag == "tbl":
            tbl = docx.table.Table(elem, doc)
            rows = tbl.rows
            if not rows:
                continue

            num_cols = len(rows[0].cells)

            # 0. Cover Page Two-Column Table (Submitted By & Under Guidance Of)
            if current_section == "cover" and num_cols == 2 and len(rows) == 1:
                c_left = rows[0].cells[0].text.strip()
                c_right = rows[0].cells[1].text.strip()
                p_l = Paragraph(c_left.replace("\n", "<br/>").replace("SUBMITTED BY:", "<b><font color='#1E3A8A'>SUBMITTED BY:</font></b><br/>"), style_body)
                p_r = Paragraph(c_right.replace("\n", "<br/>").replace("UNDER THE GUIDANCE OF:", "<b><font color='#1E3A8A'>UNDER THE GUIDANCE OF:</font></b><br/>"), style_td_right)
                t_sub = Table([[p_l, p_r]], colWidths=[245, 250])
                t_sub.setStyle(TableStyle([
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, 0), (-1, -1), 2),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ]))
                story.append(Spacer(1, 4))
                story.append(t_sub)
                continue

            # 1. Code blocks (1 col, 1 row)
            if num_cols == 1 and len(rows) == 1:
                code_text = rows[0].cells[0].text
                escaped = html.escape(code_text).replace("\n", "<br/>")
                p = Paragraph(escaped, style_code)
                t = Table([[p]], colWidths=[495])
                t.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
                    ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E1")),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ]))
                story.append(Spacer(1, 3))
                story.append(t)
                story.append(Spacer(1, 4))
                continue

            # 2. Table of Contents (2 cols: Title, Page)
            if num_cols == 2 and len(rows) > 10:
                table_data = []
                for r in rows:
                    title_text = r.cells[0].text.strip()
                    page_text = r.cells[1].text.strip()
                    is_main_h = title_text.startswith("CHAPTER") or title_text in [
                        "Candidate's Declaration", "Acknowledgement", "Abstract",
                        "List of Figures", "List of Tables", "REFERENCES", "APPENDIX"
                    ]
                    p_title = Paragraph(f"<b>{html.escape(title_text)}</b>" if is_main_h else html.escape(title_text), style_td)
                    p_page = Paragraph(f"<b>{page_text}</b>" if is_main_h else page_text, style_td_right)
                    table_data.append([p_title, p_page])
                t = Table(table_data, colWidths=[435, 60])
                t.setStyle(TableStyle([
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("TOPPADDING", (0, 0), (-1, -1), 1.5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
                    ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.HexColor("#F1F5F9")),
                ]))
                story.append(t)
                continue

            # 3. List of Figures / List of Tables (3 cols)
            if num_cols == 3 and rows[0].cells[0].text.strip() in ["Figure No.", "Table No."]:
                table_data = []
                for idx_r, r in enumerate(rows):
                    row_data = []
                    for idx_c, c in enumerate(r.cells):
                        txt = html.escape(c.text.strip())
                        if idx_r == 0:
                            row_data.append(Paragraph(f"<b>{txt}</b>", style_th))
                        elif idx_c in [0, 2]:
                            row_data.append(Paragraph(txt, style_td_center))
                        else:
                            row_data.append(Paragraph(txt, style_td))
                    table_data.append(row_data)
                t = Table(table_data, colWidths=[70, 365, 60], repeatRows=1)
                t.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                    ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                ]))
                story.append(t)
                continue

            # 4. Functional Requirements Table (4 cols: ID, Name, Description, Priority)
            if num_cols == 4 and rows[0].cells[0].text.strip() == "Req. ID":
                table_data = []
                for idx_r, r in enumerate(rows):
                    row_data = []
                    for idx_c, c in enumerate(r.cells):
                        txt = html.escape(c.text.strip()).replace("\n", "<br/>")
                        if idx_r == 0:
                            row_data.append(Paragraph(f"<b>{txt}</b>", style_th))
                        elif idx_c in [0, 3]:
                            row_data.append(Paragraph(f"<b>{txt}</b>" if idx_c == 3 else txt, style_td_center))
                        else:
                            row_data.append(Paragraph(txt, style_td))
                    table_data.append(row_data)
                t = Table(table_data, colWidths=[50, 110, 280, 55], repeatRows=1)
                ts = [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                    ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                    ("LEFTPADDING", (0, 0), (-1, -1), 3),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ]
                for r_i in range(1, len(rows)):
                    if r_i % 2 == 0:
                        ts.append(("BACKGROUND", (0, r_i), (-1, r_i), colors.HexColor("#F8FAFC")))
                t.setStyle(TableStyle(ts))
                story.append(Spacer(1, 3))
                story.append(t)
                story.append(Spacer(1, 4))
                continue

            # 5. Non-Functional Requirements Table (4 cols: NFR ID, Category, Spec, Target)
            if num_cols == 4 and rows[0].cells[0].text.strip() == "NFR ID":
                table_data = []
                for idx_r, r in enumerate(rows):
                    row_data = []
                    for idx_c, c in enumerate(r.cells):
                        txt = html.escape(c.text.strip()).replace("\n", "<br/>")
                        if idx_r == 0:
                            row_data.append(Paragraph(f"<b>{txt}</b>", style_th))
                        elif idx_c in [0, 3]:
                            row_data.append(Paragraph(f"<b>{txt}</b>" if idx_c == 3 else txt, style_td_center))
                        else:
                            row_data.append(Paragraph(txt, style_td))
                    table_data.append(row_data)
                t = Table(table_data, colWidths=[50, 110, 255, 80], repeatRows=1)
                ts = [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                    ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                    ("LEFTPADDING", (0, 0), (-1, -1), 3),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ]
                for r_i in range(1, len(rows)):
                    if r_i % 2 == 0:
                        ts.append(("BACKGROUND", (0, r_i), (-1, r_i), colors.HexColor("#F8FAFC")))
                t.setStyle(TableStyle(ts))
                story.append(Spacer(1, 3))
                story.append(t)
                story.append(Spacer(1, 4))
                continue

            # 6. Test Cases Table (6 cols: ID, Description, Input, Expected, Actual, Status)
            if num_cols == 6 and rows[0].cells[0].text.strip() == "Test ID":
                table_data = []
                for idx_r, r in enumerate(rows):
                    row_data = []
                    for idx_c, c in enumerate(r.cells):
                        txt = html.escape(c.text.strip()).replace("\n", "<br/>")
                        if idx_r == 0:
                            row_data.append(Paragraph(f"<b>{txt}</b>", style_th))
                        elif idx_c == 0:
                            row_data.append(Paragraph(f"<b>{txt}</b>", style_td_center))
                        elif idx_c == 5:
                            color_tag = '<font color="#16A34A"><b>PASS</b></font>' if "PASS" in txt else txt
                            row_data.append(Paragraph(color_tag, style_td_center))
                        else:
                            row_data.append(Paragraph(txt, style_td))
                    table_data.append(row_data)
                t = Table(table_data, colWidths=[45, 95, 85, 110, 110, 50], repeatRows=1)
                ts = [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                    ("TOPPADDING", (0, 0), (-1, -1), 2),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                    ("LEFTPADDING", (0, 0), (-1, -1), 3),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ]
                for r_i in range(1, len(rows)):
                    if r_i % 2 == 0:
                        ts.append(("BACKGROUND", (0, r_i), (-1, r_i), colors.HexColor("#F8FAFC")))
                t.setStyle(TableStyle(ts))
                story.append(Spacer(1, 3))
                story.append(t)
                story.append(Spacer(1, 4))
                continue

            # General Tables
            col_w = int(495 / num_cols)
            remainder = 495 - (col_w * num_cols)
            widths = [col_w] * num_cols
            widths[-1] += remainder

            table_data = []
            for idx_r, r in enumerate(rows):
                row_data = []
                for idx_c, c in enumerate(r.cells):
                    txt = html.escape(c.text.strip()).replace("\n", "<br/>")
                    if idx_r == 0:
                        row_data.append(Paragraph(f"<b>{txt}</b>", style_th))
                    else:
                        row_data.append(Paragraph(txt, style_td))
                table_data.append(row_data)
            t = Table(table_data, colWidths=widths, repeatRows=1)
            ts = [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]
            for r_i in range(1, len(rows)):
                if r_i % 2 == 0:
                    ts.append(("BACKGROUND", (0, r_i), (-1, r_i), colors.HexColor("#F8FAFC")))
            t.setStyle(TableStyle(ts))
            story.append(Spacer(1, 3))
            story.append(t)
            story.append(Spacer(1, 4))
            continue

        elif tag == "p":
            p = docx.text.paragraph.Paragraph(elem, doc)
            text = p.text.strip()

            has_page_break = bool(p._p.xpath('.//w:br[@w:type="page"]'))

            # Check for image
            blips = p._p.xpath('.//a:blip')
            if blips:
                if image_counter < len(FIGURE_FILES):
                    fig_fname = FIGURE_FILES[image_counter]
                    fig_path = os.path.join(FIG_DIR, fig_fname)
                    image_counter += 1
                    if os.path.exists(fig_path):
                        if "ct_university_logo" in fig_fname:
                            img_flowable = Image(fig_path, width=130, height=130)
                            story.append(Spacer(1, 2))
                            story.append(img_flowable)
                            story.append(Spacer(1, 4))
                        else:
                            img_flowable = Image(fig_path, width=450, height=210)
                            story.append(Spacer(1, 3))
                            story.append(img_flowable)
                            story.append(Spacer(1, 2))
                continue

            if not text:
                if has_page_break:
                    story.append(PageBreak())
                continue

            # Switch sections when headings appear
            if text == "CANDIDATE'S DECLARATION":
                if current_section == "cover":
                    current_section = "prelim"
                    story.append(SectionMarker("prelim"))
                    story.append(PageBreak())

            if text.startswith("CHAPTER 1"):
                if current_section == "prelim":
                    current_section = "main"
                    story.append(SectionMarker("main"))
                    story.append(PageBreak())

            # Cover Page Paragraph Mappings
            if current_section == "cover":
                if text == "CT UNIVERSITY":
                    story.append(Paragraph(html.escape(text), style_cover_univ))
                    continue
                if text == "SCHOOL OF ENGINEERING & TECHNOLOGY":
                    story.append(Paragraph(html.escape(text), style_cover_school))
                    continue
                if text == "DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING":
                    story.append(Paragraph(html.escape(text), style_cover_dept))
                    continue
                if "Ludhiana, Punjab" in text and "Specialization" in text:
                    story.append(Paragraph(html.escape(text).replace("\n", "<br/>"), style_cover_loc))
                    continue
                if text == "INDUSTRIAL TRAINING & PROJECT REPORT":
                    story.append(Paragraph(html.escape(text), style_cover_banner))
                    continue
                if text == "ON":
                    story.append(Paragraph(html.escape(text), style_cover_on))
                    continue
                if "RESEARCHIQ: ACADEMIC & INDUSTRIAL" in text:
                    story.append(Paragraph(html.escape(text).replace("\n", "<br/>"), style_cover_title))
                    continue
                if "An Evidence-Grounded Multi-Document RAG" in text:
                    story.append(Paragraph(html.escape(text), style_cover_sub))
                    continue
                if "Submitted in partial fulfillment" in text:
                    story.append(Paragraph(html.escape(text).replace("\n", "<br/>"), style_cover_deg))
                    continue
                if "ACADEMIC YEAR" in text:
                    story.append(Paragraph(html.escape(text).replace("\n", "<br/>"), style_cover_bot))
                    continue

            # Main Report Headings
            if text.startswith("CHAPTER ") or text in [
                "REFERENCES", "APPENDIX: CONFIGURATION AND VERIFICATION CHECKLIST"
            ]:
                if not text.startswith("CHAPTER 1") and story and not isinstance(story[-1], PageBreak):
                    story.append(PageBreak())
                p_flow = Paragraph(html.escape(text), style_chap_title)
                story.append(p_flow)
                story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
                continue

            if text in [
                "CANDIDATE'S DECLARATION", "ACKNOWLEDGEMENT", "ABSTRACT",
                "TABLE OF CONTENTS", "LIST OF FIGURES", "LIST OF TABLES"
            ]:
                if story and not isinstance(story[-1], PageBreak):
                    story.append(PageBreak())
                story.append(Paragraph(html.escape(text), style_prelim_title))
                story.append(HRFlowable(width="50%", thickness=1, color=colors.HexColor("#0F172A"), spaceBefore=2, spaceAfter=8))
                continue

            # Level 2 heading
            if re.match(r"^\d+\.\d+\s+[A-Za-z]", text) or re.match(r"^[A-Z]\.\d+\s+[A-Za-z]", text):
                p_flow = Paragraph(html.escape(text), style_h2)
                story.append(p_flow)
                continue

            # Level 3 heading
            if re.match(r"^\d+\.\d+\.\d+\s+[A-Za-z]", text):
                p_flow = Paragraph(html.escape(text), style_h3)
                story.append(p_flow)
                continue

            # Figure Caption
            if text.startswith("Figure ") and ":" in text[:15]:
                story.append(Paragraph(html.escape(text), style_caption))
                continue

            # Table Caption
            if text.startswith("Table ") and ":" in text[:15]:
                story.append(Spacer(1, 4))
                story.append(Paragraph(f"<b>{html.escape(text)}</b>", style_h3))
                continue

            # Bullet points
            if p.style.name == "List Bullet" or text.startswith("• ") or text.startswith("- "):
                cleaned_text = re.sub(r"^[•\-]\s*", "", text)
                bullet_html = f"&bull; {html.escape(cleaned_text)}"
                story.append(Paragraph(bullet_html, style_bullet))
                continue

            # Formatted body paragraph
            run_parts = []
            for r in p.runs:
                r_txt = html.escape(r.text)
                if r.bold:
                    r_txt = f"<b>{r_txt}</b>"
                if r.italic:
                    r_txt = f"<i>{r_txt}</i>"
                run_parts.append(r_txt)
            formatted_text = "".join(run_parts).replace("\n", "<br/>")

            # Signature lines
            if "_______________________________" in formatted_text:
                story.append(Spacer(1, 8))
                story.append(Paragraph(formatted_text, style_body))
                continue

            story.append(Paragraph(formatted_text, style_body))

            if has_page_break:
                story.append(PageBreak())

    print(f"Total flowables in PDF story: {len(story)}")
    print(f"Total images embedded: {image_counter}")

    pdf_doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=48,
        rightMargin=48,
        topMargin=46,
        bottomMargin=46
    )

    print(f"Building updated PDF at: {PDF_PATH}")
    pdf_doc.build(story, canvasmaker=UniversityCanvas)
    print("PDF compilation completed successfully!")

if __name__ == "__main__":
    build_pdf()
