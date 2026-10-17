import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle, Spacer

# Page Geometry matching SRMIST MCA format and reference doc
PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT_MARGIN = 4.0 * 28.3465    # 4 cm = 113.39 pt
RIGHT_MARGIN = 2.0 * 28.3465   # 2 cm = 56.69 pt
TOP_MARGIN = 3.0 * 28.3465     # 3 cm = 85.04 pt
BOTTOM_MARGIN = 3.0 * 28.3465  # 3 cm = 85.04 pt
USABLE_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN   # 425.20 pt
USABLE_HEIGHT = PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN # 671.81 pt

class ReferenceDocCanvas(canvas.Canvas):
    """
    Two-pass canvas to number pages bottom-middle: 1, 2, 3 ... 62
    Matching the reference document style exactly.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Times-Roman", 11)
        page_num_str = str(self._pageNumber)
        # Bottom-center placement
        center_x = (LEFT_MARGIN + (PAGE_WIDTH - RIGHT_MARGIN)) / 2.0
        center_y = 1.3 * 28.3465  # approx 1.3 cm from bottom edge
        self.drawCentredString(center_x, center_y, page_num_str)
        self.restoreState()

styles = getSampleStyleSheet()

# Strict SRMIST & Reference PDF Typography: Times New Roman
title_style = ParagraphStyle(
    'RefChapterTitle',
    parent=styles['Normal'],
    fontName='Times-Bold',
    fontSize=14,
    leading=18,
    alignment=TA_LEFT,
    spaceBefore=0,
    spaceAfter=10,
    keepWithNext=True
)

h1_style = ParagraphStyle(
    'RefSectionH1',
    parent=styles['Normal'],
    fontName='Times-Bold',
    fontSize=13,
    leading=17,
    alignment=TA_LEFT,
    spaceBefore=10,
    spaceAfter=6,
    keepWithNext=True
)

h2_style = ParagraphStyle(
    'RefSectionH2',
    parent=styles['Normal'],
    fontName='Times-Bold',
    fontSize=12,
    leading=16,
    alignment=TA_LEFT,
    spaceBefore=8,
    spaceAfter=4,
    keepWithNext=True
)

body_style = ParagraphStyle(
    'RefBodyText',
    parent=styles['Normal'],
    fontName='Times-Roman',
    fontSize=12,
    leading=18,
    alignment=TA_JUSTIFY,
    firstLineIndent=20, # 5 spaces indent as per guideline
    spaceAfter=6
)

body_noindent_style = ParagraphStyle(
    'RefBodyNoIndent',
    parent=styles['Normal'],
    fontName='Times-Roman',
    fontSize=12,
    leading=18,
    alignment=TA_JUSTIFY,
    firstLineIndent=0,
    spaceAfter=6
)

bullet_style = ParagraphStyle(
    'RefBulletText',
    parent=styles['Normal'],
    fontName='Times-Roman',
    fontSize=12,
    leading=18,
    alignment=TA_JUSTIFY,
    leftIndent=24,
    firstLineIndent=-14,
    spaceAfter=4
)

caption_style = ParagraphStyle(
    'RefCaption',
    parent=styles['Normal'],
    fontName='Times-BoldItalic',
    fontSize=11,
    leading=14,
    alignment=TA_CENTER,
    spaceBefore=6,
    spaceAfter=8
)

# Placeholder box inner styles
box_tag_style = ParagraphStyle(
    'BoxTag',
    fontName='Helvetica-Bold',
    fontSize=10,
    leading=13,
    textColor=colors.HexColor('#FBBF24'), # Amber gold
    alignment=TA_CENTER,
    spaceAfter=3
)

box_title_style = ParagraphStyle(
    'BoxTitle',
    fontName='Helvetica-Bold',
    fontSize=10,
    leading=13,
    textColor=colors.white,
    alignment=TA_CENTER,
    spaceAfter=3
)

box_desc_style = ParagraphStyle(
    'BoxDesc',
    fontName='Helvetica',
    fontSize=8.5,
    leading=11.5,
    textColor=colors.HexColor('#E5E7EB'), # Light grey
    alignment=TA_CENTER,
    spaceAfter=2
)

box_dim_style = ParagraphStyle(
    'BoxDim',
    fontName='Helvetica-Oblique',
    fontSize=8,
    leading=10,
    textColor=colors.HexColor('#9CA3AF'), # Muted grey
    alignment=TA_CENTER
)

def make_placeholder_box(fig_no, fig_title, image_desc, dimensions="1200 x 650 px (PNG / JPEG)", height=155):
    """
    Creates an exact black-box placeholder table with formatted instructions inside.
    """
    inner_flowables = [
        Paragraph(f"<b>[IMAGE PLACEHOLDER -- {fig_no}]</b>", box_tag_style),
        Paragraph(f"<b>Image to be added:</b> {fig_title}", box_title_style),
        Paragraph(f"<b>Visual Content:</b> {image_desc}", box_desc_style),
        Paragraph(f"<b>Recommended Resolution:</b> {dimensions}", box_dim_style)
    ]
    t = Table([[inner_flowables]], colWidths=[USABLE_WIDTH], rowHeights=[height])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#111827')), # Deep black-slate box
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#374151')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t
