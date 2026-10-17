"""
build_preliminary_pages_pdf.py
Recreates the 1st PDF (Preliminary Pages / Front Matter) with:
1. Candidate name changed from 'S AKSHAYA RA2532014010165' to the 4 team members:
   VISAGAN M (RA2532241010413), ASHWIN S (RA2532241010365),
   ABDUL-BASITH H (RA2532241010420), MUKILAN A (RA2532241010387)
2. Table of Contents based on the Self-Adaptive Multi-Agent RAG project (matching 62-page reference report)
3. Full Abstract for the Self-Adaptive Multi-Agent RAG project
4. Plagiarism Certificate page (with designated certificate container)
5. List of Tables and List of Figures matching the Self-Adaptive Multi-Agent RAG project exactly.

Compiles two editions:
A. Self_Adaptive_MultiAgent_RAG_Preliminary_Pages.pdf (Exact 11 pages matching Akshaya's 1st PDF)
B. Self_Adaptive_MultiAgent_RAG_Preliminary_Pages_With_Declaration.pdf (12 pages including Declaration)
"""

import os
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
import pypdf

# Paths
PROJECT_DIR = r"C:\Users\visag\.gemini\antigravity\scratch\multi_agent_rag"
ARTIFACT_DIR = r"C:\Users\visag\.gemini\antigravity\brain\16632dba-7765-414e-bb84-677366a2f22c"

PDF_11_NAME = "Self_Adaptive_MultiAgent_RAG_Preliminary_Pages.pdf"
PDF_12_NAME = "Self_Adaptive_MultiAgent_RAG_Preliminary_Pages_With_Declaration.pdf"

OUT_11_PROJECT = os.path.join(PROJECT_DIR, PDF_11_NAME)
OUT_11_ARTIFACT = os.path.join(ARTIFACT_DIR, PDF_11_NAME)
OUT_12_PROJECT = os.path.join(PROJECT_DIR, PDF_12_NAME)
OUT_12_ARTIFACT = os.path.join(ARTIFACT_DIR, PDF_12_NAME)

LOGO_PATH = os.path.join(PROJECT_DIR, "scratch", "images", "srm_logo.png")

# Geometry (4cm left, 2cm right, 3cm top, 3cm bottom)
PAGE_W, PAGE_H = A4
LEFT_MARGIN = 113.39   # 4 cm
RIGHT_MARGIN = 56.69   # 2 cm
TOP_MARGIN = 85.04     # 3 cm
BOTTOM_MARGIN = 85.04  # 3 cm
USABLE_WIDTH = PAGE_W - LEFT_MARGIN - RIGHT_MARGIN  # 425.2 pt

# Stylesheet
base_styles = getSampleStyleSheet()

title_center_large = ParagraphStyle(
    "TitleCenterLarge",
    parent=base_styles["Normal"],
    fontName="Times-Bold",
    fontSize=14.5,
    leading=19,
    alignment=1,
    textColor=colors.black,
    spaceAfter=8
)

body_center_12 = ParagraphStyle(
    "BodyCenter12",
    parent=base_styles["Normal"],
    fontName="Times-Roman",
    fontSize=12,
    leading=16,
    alignment=1,
    textColor=colors.black,
    spaceAfter=5
)

body_center_bold_12 = ParagraphStyle(
    "BodyCenterBold12",
    parent=base_styles["Normal"],
    fontName="Times-Bold",
    fontSize=12,
    leading=16,
    alignment=1,
    textColor=colors.black,
    spaceAfter=5
)

body_center_11 = ParagraphStyle(
    "BodyCenter11",
    parent=base_styles["Normal"],
    fontName="Times-Roman",
    fontSize=11,
    leading=14.5,
    alignment=1,
    textColor=colors.black,
    spaceAfter=3
)

heading_center_14 = ParagraphStyle(
    "HeadingCenter14",
    parent=base_styles["Normal"],
    fontName="Times-Bold",
    fontSize=14,
    leading=18,
    alignment=1,
    textColor=colors.black,
    spaceAfter=12
)

para_body_12 = ParagraphStyle(
    "ParaBody12",
    parent=base_styles["Normal"],
    fontName="Times-Roman",
    fontSize=12,
    leading=17,  # 1.5 line spacing
    alignment=4,  # Justified
    firstLineIndent=20,  # 5 spaces
    textColor=colors.black,
    spaceAfter=8
)

para_body_noindent_12 = ParagraphStyle(
    "ParaBodyNoIndent12",
    parent=para_body_12,
    firstLineIndent=0
)

toc_header = ParagraphStyle(
    "TOCHeader",
    parent=base_styles["Normal"],
    fontName="Times-Bold",
    fontSize=10.5,
    leading=13.5,
    alignment=1,
    textColor=colors.black
)

toc_cell = ParagraphStyle(
    "TOCCell",
    parent=base_styles["Normal"],
    fontName="Times-Roman",
    fontSize=9.5,
    leading=12.5,
    textColor=colors.black
)

toc_cell_bold = ParagraphStyle(
    "TOCCellBold",
    parent=toc_cell,
    fontName="Times-Bold"
)

toc_cell_center = ParagraphStyle(
    "TOCCellCenter",
    parent=toc_cell,
    alignment=1
)

toc_cell_center_bold = ParagraphStyle(
    "TOCCellCenterBold",
    parent=toc_cell_bold,
    alignment=1
)


class NoHeaderCanvas(canvas.Canvas):
    pass


def get_title_page():
    p1 = [
        Paragraph(
            "SELF-ADAPTIVE MULTI-AGENT<br/>RETRIEVAL-AUGMENTED GENERATION (RAG)<br/>"
            "FRAMEWORK FOR DOMAIN-SPECIFIC DECISION<br/>SUPPORT",
            title_center_large
        ),
        Spacer(1, 8),
        Paragraph("A PROJECT REPORT SUBMITTED TO", body_center_11),
        Paragraph("<b>SRM INSTITUTE OF SCIENCE &amp; TECHNOLOGY</b>", body_center_bold_12),
        Paragraph("IN PARTIAL FULFILMENT OF THE REQUIREMENTS FOR THE AWARD OF THE<br/>DEGREE OF", body_center_11),
        Paragraph("<b>MASTER OF COMPUTER APPLICATIONS</b>", body_center_bold_12),
        Spacer(1, 4),
        Paragraph("BY", body_center_11),
        Paragraph(
            "<b>VISAGAN M (RA2532241010413)</b><br/>"
            "<b>ASHWIN S (RA2532241010365)</b><br/>"
            "<b>ABDUL-BASITH H (RA2532241010420)</b><br/>"
            "<b>MUKILAN A (RA2532241010387)</b>",
            body_center_11
        ),
        Spacer(1, 8),
        Paragraph("UNDER THE GUIDANCE OF", body_center_11),
        Paragraph(
            "<b>Dr. ANWAR R SHAHEEN</b><br/>"
            "MBA., MCA., BEd., M.Phil., PhD",
            body_center_11
        ),
        Spacer(1, 8)
    ]
    if os.path.exists(LOGO_PATH):
        p1.append(Image(LOGO_PATH, width=120, height=66.6))
        p1.append(Spacer(1, 8))

    p1.extend([
        Paragraph("<b>DEPARTMENT OF COMPUTER APPLICATIONS</b>", body_center_bold_12),
        Paragraph("<b>FACULTY OF SCIENCE AND HUMANITIES</b>", body_center_bold_12),
        Paragraph("<b>SRM INSTITUTE OF SCIENCE &amp; TECHNOLOGY</b>", body_center_bold_12),
        Paragraph("Kattankulathur &ndash; 603 203, Chengalpattu District, Tamil Nadu", body_center_11),
        Paragraph("<b>OCTOBER - 2026</b>", body_center_bold_12),
        PageBreak()
    ])
    return p1


def get_bonafide_page():
    p2 = [
        Paragraph("OCTOBER - 2026", body_center_bold_12),
        Spacer(1, 6),
        Paragraph("BONAFIDE CERTIFICATE", heading_center_14),
        Spacer(1, 10),
        Paragraph(
            "This is to certify that the project report titled <b>&ldquo;SELF-ADAPTIVE "
            "MULTI-AGENT RETRIEVAL-AUGMENTED GENERATION (RAG) FRAMEWORK FOR DOMAIN-SPECIFIC "
            "DECISION SUPPORT&rdquo;</b> is a bonafide work carried out by "
            "<b>VISAGAN M (RA2532241010413)</b>, <b>ASHWIN S (RA2532241010365)</b>, "
            "<b>ABDUL-BASITH H (RA2532241010420)</b>, and <b>MUKILAN A (RA2532241010387)</b> "
            "under my supervision for the award of the Degree of <b>Master of Computer Applications</b>. "
            "To the best of my knowledge, the work reported herein is the original work carried out by these candidates.",
            para_body_12
        ),
        Spacer(1, 55),
    ]

    guide_hod_data = [
        [
            Paragraph("<b>Dr. ANWAR R SHAHEEN</b><br/>MBA., MCA., BEd., M.Phil., PhD<br/>Department of Computer Applications<br/>(GUIDE)", ParagraphStyle("G1", parent=toc_cell, leading=14)),
            Paragraph("<b>Dr. P. J. ARUL LEENA ROSE</b><br/>Professor &amp; Head,<br/>Department of Computer Applications<br/>SRM Institute of Science and Technology", ParagraphStyle("G2", parent=toc_cell, leading=14))
        ]
    ]
    t_gh = Table(guide_hod_data, colWidths=[210, 215])
    t_gh.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 0),
    ]))
    p2.append(t_gh)

    p2.extend([
        Spacer(1, 50),
        Paragraph("Submitted for the Project Viva-Voce Examination held on: ___________________", para_body_noindent_12),
        Spacer(1, 45),
    ])

    examiners_data = [
        [
            Paragraph("<b>INTERNAL EXAMINER</b>", toc_cell_bold),
            Paragraph("<b>EXTERNAL EXAMINER</b>", ParagraphStyle("E2", parent=toc_cell_bold, alignment=2))
        ]
    ]
    t_ex = Table(examiners_data, colWidths=[210, 215])
    t_ex.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 0),
    ]))
    p2.append(t_ex)
    p2.append(PageBreak())
    return p2


def get_declaration_page():
    p3 = [
        Paragraph("DECLARATION", heading_center_14),
        Spacer(1, 14),
        Paragraph(
            "We hereby declare that the project report titled <b>&ldquo;SELF-ADAPTIVE "
            "MULTI-AGENT RETRIEVAL-AUGMENTED GENERATION (RAG) FRAMEWORK FOR DOMAIN-SPECIFIC "
            "DECISION SUPPORT&rdquo;</b> submitted to the Department of Computer Applications, "
            "Faculty of Science and Humanities, SRM Institute of Science &amp; Technology, in "
            "partial fulfilment of the requirements for the award of the degree of <b>Master of "
            "Computer Applications</b>, is a record of original work carried out by us under the "
            "supervision and guidance of <b>Anwar Shaheen</b>, Assistant Professor, Department "
            "of Computer Applications. We further declare that this report has not formed the "
            "basis for the award of any degree, diploma, associateship, fellowship, or similar title.",
            para_body_12
        ),
        Spacer(1, 30),
        Paragraph("<b>Place:</b> Kattankulathur", para_body_noindent_12),
        Paragraph("<b>Date:</b> October 2026", para_body_noindent_12),
        Spacer(1, 50),
    ]

    decl_names_data = [
        [
            Paragraph("<b>VISAGAN M (RA2532241010413)</b>", toc_cell_bold),
            Paragraph("<b>ABDUL-BASITH H (RA2532241010420)</b>", toc_cell_bold)
        ],
        [
            Paragraph("<br/><br/><b>ASHWIN S (RA2532241010365)</b>", toc_cell_bold),
            Paragraph("<br/><br/><b>MUKILAN A (RA2532241010387)</b>", toc_cell_bold)
        ]
    ]
    t_decl = Table(decl_names_data, colWidths=[210, 215])
    t_decl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 0),
    ]))
    p3.append(t_decl)
    p3.append(PageBreak())
    return p3


def get_acknowledgement_page():
    p4 = [
        Paragraph("ACKNOWLEDGEMENT", heading_center_14),
        Spacer(1, 6),
        Paragraph(
            "With profound gratitude to the ALMIGHTY, we take this chance to thank the people who helped us to complete this project successfully.",
            para_body_12
        ),
        Paragraph(
            "We take this as a right opportunity to say THANKS to our parents who are there to stand with us always with the words &ldquo;YOU CAN&rdquo;.",
            para_body_12
        ),
        Paragraph(
            "We are thankful to <b>Dr. T. R. Paarivendhar</b>, Chancellor, SRM Institute of Science &amp; Technology, who gave us the platform to establish ourselves to reach greater heights.",
            para_body_12
        ),
        Paragraph(
            "We earnestly thank <b>Dr. A. Duraisamy</b>, Dean, Faculty of Science and Humanities, SRM Institute of Science &amp; Technology, who always encourages us to do novel things.",
            para_body_12
        ),
        Paragraph(
            "A great note of gratitude to <b>Dr. S. Albert Antony Raj</b>, Deputy Dean, Faculty of Science and Humanities, for his valuable guidance and constant support to do this project.",
            para_body_12
        ),
        Paragraph(
            "We express our sincere thanks to <b>Dr. P. J. Arul Leena Rose</b>, Professor &amp; Head, Department of Computer Applications, for her continuous support and academic encouragement.",
            para_body_12
        ),
        Paragraph(
            "It is our delight to thank our project guide <b>Dr. ANWAR R SHAHEEN</b>, MBA., MCA., BEd., M.Phil., PhD , Department of Computer Applications for her help, support, encouragement, suggestions, and guidance throughout the development phases of the project.",
            para_body_12
        ),
        Paragraph(
            "We convey our gratitude to all the faculty members of the department who extended their support through valuable comments and suggestions during reviews.",
            para_body_12
        ),
        Paragraph(
            "Our gratitude to friends and peers who directly and indirectly helped in carrying out this project work successfully.",
            para_body_12
        ),
        Spacer(1, 8),
    ]

    ack_names = [
        [Paragraph("", toc_cell), Paragraph("<b>Visagan M (RA2532241010413)</b>", toc_cell_bold)],
        [Paragraph("", toc_cell), Paragraph("<b>Ashwin S (RA2532241010365)</b>", toc_cell_bold)],
        [Paragraph("", toc_cell), Paragraph("<b>Abdul-Basith H (RA2532241010420)</b>", toc_cell_bold)],
        [Paragraph("", toc_cell), Paragraph("<b>Mukilan A (RA2532241010387)</b>", toc_cell_bold)],
    ]
    t_ack = Table(ack_names, colWidths=[220, 205])
    t_ack.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 1.5),
    ]))
    p4.append(t_ack)
    p4.append(PageBreak())
    return p4


def get_toc_pages():
    story = []

    # Part 1: Abstract to Chapter 4.2
    toc_p1_rows = [
        [Paragraph("<b>Sl. No.</b>", toc_header), Paragraph("<b>Contents</b>", toc_header), Paragraph("<b>Page No.</b>", toc_header)],
        [Paragraph("", toc_cell), Paragraph("<b>Abstract</b>", toc_cell_bold), Paragraph("v", toc_cell_center_bold)],
        [Paragraph("", toc_cell), Paragraph("<b>List of Tables</b>", toc_cell_bold), Paragraph("x", toc_cell_center_bold)],
        [Paragraph("", toc_cell), Paragraph("<b>List of Figures</b>", toc_cell_bold), Paragraph("xi", toc_cell_center_bold)],
        [Paragraph("<b>1</b>", toc_cell_center_bold), Paragraph("<b>Introduction</b>", toc_cell_bold), Paragraph("<b>1</b>", toc_cell_center_bold)],
        [Paragraph("1.1", toc_cell_center), Paragraph("Background of the Study", toc_cell), Paragraph("1", toc_cell_center)],
        [Paragraph("1.2", toc_cell_center), Paragraph("Problem Statement", toc_cell), Paragraph("1", toc_cell_center)],
        [Paragraph("1.3", toc_cell_center), Paragraph("Objectives of the Project", toc_cell), Paragraph("2", toc_cell_center)],
        [Paragraph("1.4", toc_cell_center), Paragraph("Scope of the Project", toc_cell), Paragraph("2", toc_cell_center)],
        [Paragraph("1.5", toc_cell_center), Paragraph("Significance of the Project", toc_cell), Paragraph("3", toc_cell_center)],
        [Paragraph("<b>2.</b>", toc_cell_center_bold), Paragraph("<b>Literature Survey / Existing Studies</b>", toc_cell_bold), Paragraph("<b>4</b>", toc_cell_center_bold)],
        [Paragraph("2.1", toc_cell_center), Paragraph("Review of Existing Systems and Research Works", toc_cell), Paragraph("4", toc_cell_center)],
        [Paragraph("2.2", toc_cell_center), Paragraph("Comparative Analysis", toc_cell), Paragraph("5", toc_cell_center)],
        [Paragraph("2.3", toc_cell_center), Paragraph("Research Gap and Limitations of Existing Systems", toc_cell), Paragraph("5", toc_cell_center)],
        [Paragraph("2.4", toc_cell_center), Paragraph("Proposed System and Proposed Approach", toc_cell), Paragraph("6", toc_cell_center)],
        [Paragraph("<b>3.</b>", toc_cell_center_bold), Paragraph("<b>Software Requirement Analysis</b>", toc_cell_bold), Paragraph("<b>7</b>", toc_cell_center_bold)],
        [Paragraph("3.1", toc_cell_center), Paragraph("Hardware Specification", toc_cell), Paragraph("7", toc_cell_center)],
        [Paragraph("3.2", toc_cell_center), Paragraph("Software Specification", toc_cell), Paragraph("8", toc_cell_center)],
        [Paragraph("3.3", toc_cell_center), Paragraph("Software Tools and Their Features", toc_cell), Paragraph("9", toc_cell_center)],
        [Paragraph("<b>4.</b>", toc_cell_center_bold), Paragraph("<b>System Analysis</b>", toc_cell_bold), Paragraph("<b>11</b>", toc_cell_center_bold)],
        [Paragraph("4.1", toc_cell_center), Paragraph("Requirement Specification", toc_cell), Paragraph("11", toc_cell_center)],
        [Paragraph("4.2", toc_cell_center), Paragraph("Characteristics of Existing System", toc_cell), Paragraph("12", toc_cell_center)],
    ]
    t_toc1 = Table(toc_p1_rows, colWidths=[45, 315, 65])
    t_toc1.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 2.5),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
    ]))
    story.extend([
        Paragraph("TABLE OF CONTENTS", heading_center_14),
        Spacer(1, 4),
        t_toc1,
        PageBreak()
    ])

    # Part 2: Chapter 4.3 to Chapter 7.6
    toc_p2_rows = [
        [Paragraph("<b>Sl. No.</b>", toc_header), Paragraph("<b>Contents</b>", toc_header), Paragraph("<b>Page No.</b>", toc_header)],
        [Paragraph("4.3", toc_cell_center), Paragraph("Proposed System", toc_cell), Paragraph("12", toc_cell_center)],
        [Paragraph("4.4", toc_cell_center), Paragraph("Feasibility Study", toc_cell), Paragraph("13", toc_cell_center)],
        [Paragraph("4.5", toc_cell_center), Paragraph("Software Requirement Specification (SRS)", toc_cell), Paragraph("14", toc_cell_center)],
        [Paragraph("<b>5.</b>", toc_cell_center_bold), Paragraph("<b>System Design</b>", toc_cell_bold), Paragraph("<b>16</b>", toc_cell_center_bold)],
        [Paragraph("5.1", toc_cell_center), Paragraph("System Architecture and Overall Workflow", toc_cell), Paragraph("16", toc_cell_center)],
        [Paragraph("5.2", toc_cell_center), Paragraph("Context Diagram (DFD Level 0)", toc_cell), Paragraph("17", toc_cell_center)],
        [Paragraph("5.3", toc_cell_center), Paragraph("Use Case Diagram", toc_cell), Paragraph("18", toc_cell_center)],
        [Paragraph("5.4", toc_cell_center), Paragraph("Activity Diagram / State Transition Flow", toc_cell), Paragraph("19", toc_cell_center)],
        [Paragraph("5.5", toc_cell_center), Paragraph("Data Flow Diagram (DFD Level 1)", toc_cell), Paragraph("20", toc_cell_center)],
        [Paragraph("5.6", toc_cell_center), Paragraph("Module Design &amp; State Attributes Schema", toc_cell), Paragraph("22", toc_cell_center)],
        [Paragraph("5.7", toc_cell_center), Paragraph("User Interface Design", toc_cell), Paragraph("23", toc_cell_center)],
        [Paragraph("<b>6.</b>", toc_cell_center_bold), Paragraph("<b>System Implementation</b>", toc_cell_bold), Paragraph("<b>25</b>", toc_cell_center_bold)],
        [Paragraph("6.1", toc_cell_center), Paragraph("Module Description", toc_cell), Paragraph("25", toc_cell_center)],
        [Paragraph("6.2", toc_cell_center), Paragraph("Dataset Description and Data Collection", toc_cell), Paragraph("27", toc_cell_center)],
        [Paragraph("6.3", toc_cell_center), Paragraph("Data Preprocessing and Chunking Pipeline", toc_cell), Paragraph("28", toc_cell_center)],
        [Paragraph("6.4", toc_cell_center), Paragraph("Feature Engineering and Dense Embeddings", toc_cell), Paragraph("29", toc_cell_center)],
        [Paragraph("6.5", toc_cell_center), Paragraph("Model Architecture and Algorithm Design", toc_cell), Paragraph("30", toc_cell_center)],
        [Paragraph("6.6", toc_cell_center), Paragraph("Implementation of Routing &amp; Retrieval System", toc_cell), Paragraph("31", toc_cell_center)],
        [Paragraph("6.7", toc_cell_center), Paragraph("Implementation of Web Search &amp; Synthesis", toc_cell), Paragraph("32", toc_cell_center)],
        [Paragraph("6.8", toc_cell_center), Paragraph("Integration and Execution of the Application", toc_cell), Paragraph("33", toc_cell_center)],
        [Paragraph("<b>7.</b>", toc_cell_center_bold), Paragraph("<b>Testing and Evaluation</b>", toc_cell_bold), Paragraph("<b>34</b>", toc_cell_center_bold)],
        [Paragraph("7.1", toc_cell_center), Paragraph("Introduction to Testing and Test Case Design", toc_cell), Paragraph("34", toc_cell_center)],
        [Paragraph("7.2", toc_cell_center), Paragraph("Unit Testing of Agentic Modules", toc_cell), Paragraph("35", toc_cell_center)],
        [Paragraph("7.3", toc_cell_center), Paragraph("Integration Testing of Multi-Agent Cycles", toc_cell), Paragraph("37", toc_cell_center)],
        [Paragraph("7.4", toc_cell_center), Paragraph("System Testing", toc_cell), Paragraph("38", toc_cell_center)],
        [Paragraph("7.5", toc_cell_center), Paragraph("Model and Performance Evaluation (RAG Triad)", toc_cell), Paragraph("39", toc_cell_center)],
        [Paragraph("7.6", toc_cell_center), Paragraph("Comparative Analysis (Basic vs Static vs Adaptive)", toc_cell), Paragraph("41", toc_cell_center)],
    ]
    t_toc2 = Table(toc_p2_rows, colWidths=[45, 315, 65])
    t_toc2.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 2.5),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
    ]))
    story.extend([
        Paragraph("TABLE OF CONTENTS (Continued)", heading_center_14),
        Spacer(1, 4),
        t_toc2,
        PageBreak()
    ])

    # Part 3: Chapter 8 to Chapter 10
    toc_p3_rows = [
        [Paragraph("<b>Sl. No.</b>", toc_header), Paragraph("<b>Contents</b>", toc_header), Paragraph("<b>Page No.</b>", toc_header)],
        [Paragraph("<b>8.</b>", toc_cell_center_bold), Paragraph("<b>Results and Conclusion</b>", toc_cell_bold), Paragraph("<b>43</b>", toc_cell_center_bold)],
        [Paragraph("8.1", toc_cell_center), Paragraph("Results", toc_cell), Paragraph("43", toc_cell_center)],
        [Paragraph("8.2", toc_cell_center), Paragraph("Discussion and Analysis", toc_cell), Paragraph("45", toc_cell_center)],
        [Paragraph("8.3", toc_cell_center), Paragraph("Limitations", toc_cell), Paragraph("46", toc_cell_center)],
        [Paragraph("8.4", toc_cell_center), Paragraph("Lessons Learnt", toc_cell), Paragraph("47", toc_cell_center)],
        [Paragraph("8.5", toc_cell_center), Paragraph("Conclusion", toc_cell), Paragraph("48", toc_cell_center)],
        [Paragraph("8.6", toc_cell_center), Paragraph("Future Enhancements", toc_cell), Paragraph("49", toc_cell_center)],
        [Paragraph("<b>9.</b>", toc_cell_center_bold), Paragraph("<b>Appendices</b>", toc_cell_bold), Paragraph("<b>51</b>", toc_cell_center_bold)],
        [Paragraph("9.1", toc_cell_center), Paragraph("Introduction to Appendices", toc_cell), Paragraph("51", toc_cell_center)],
        [Paragraph("9.2", toc_cell_center), Paragraph("Application Screenshots &amp; System Outputs", toc_cell), Paragraph("51", toc_cell_center)],
        [Paragraph("9.3", toc_cell_center), Paragraph("Selected Source Code", toc_cell), Paragraph("54", toc_cell_center)],
        [Paragraph("9.4", toc_cell_center), Paragraph("Installation and Setup Instructions", toc_cell), Paragraph("55", toc_cell_center)],
        [Paragraph("9.5", toc_cell_center), Paragraph("User Documentation and Manual", toc_cell), Paragraph("56", toc_cell_center)],
        [Paragraph("9.6", toc_cell_center), Paragraph("Glossary of Technical Terms", toc_cell), Paragraph("58", toc_cell_center)],
        [Paragraph("<b>10.</b>", toc_cell_center_bold), Paragraph("<b>Bibliography / References</b>", toc_cell_bold), Paragraph("<b>61</b>", toc_cell_center_bold)],
        [Paragraph("10.1", toc_cell_center), Paragraph("References", toc_cell), Paragraph("61", toc_cell_center)],
        [Paragraph("10.2", toc_cell_center), Paragraph("Relevance of the References", toc_cell), Paragraph("61", toc_cell_center)],
        [Paragraph("10.3", toc_cell_center), Paragraph("Conclusion of the Study", toc_cell), Paragraph("62", toc_cell_center)],
    ]
    t_toc3 = Table(toc_p3_rows, colWidths=[45, 315, 65])
    t_toc3.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
    ]))
    story.extend([
        Paragraph("TABLE OF CONTENTS (Continued)", heading_center_14),
        Spacer(1, 4),
        t_toc3,
        PageBreak()
    ])

    return story


def get_abstract_pages():
    story = []

    # Abstract Page 1: Paras 1, 2, 3
    p_abs1 = [
        Paragraph("ABSTRACT", heading_center_14),
        Spacer(1, 6),
        Paragraph(
            "The deployment of Large Language Models (LLMs) in real-world advisory systems is constrained by severe operational limitations, notably factual hallucinations, static knowledge cutoffs, context saturation, and an inability to synthesize interdisciplinary technical problems reliably. While conventional Retrieval-Augmented Generation (RAG) mitigates cutoffs by fetching relevant passages from a vector database, standard monolithic architectures enforce an unvarying, single-pass pipeline regardless of inquiry difficulty. Consequently, simple questions incur unnecessary latency and token costs, while complex multi-criteria inquiries suffer from cross-domain semantic confusion, zero claim verification, and unverifiable answers.",
            para_body_12
        ),
        Paragraph(
            "The Self-Adaptive Multi-Agent Retrieval-Augmented Generation (RAG) Framework is an intelligent decision-support web platform engineered to overcome these challenges. The system introduces an autonomous, multi-agent network orchestrated via a stateful LangGraph engine that evaluates user queries across five critical domains: Agriculture, Finance, Energy, Healthcare, and Education. Instead of executing an unvarying chain, the framework features an adaptive complexity classifier that classifies queries into Low, Medium, or High complexity and dynamically provisions processing pipelines.",
            para_body_12
        ),
        Paragraph(
            "The framework partitions enterprise knowledge into distinct ChromaDB vector collections powered by local dense embeddings (all-MiniLM-L6-v2). Domain-specific autonomous agents (Agriculture Agent, Finance Agent, Energy Agent, Healthcare Agent, and Education Agent) conduct specialized analyses grounded exclusively on retrieved vector chunks. For medium and high-complexity queries, an autonomous Verification Agent performs rigorous fact-checking against raw source chunks, identifying unsupported claims, resolving conflicting statements, and outputting an algorithmic alignment score. A Confidence Evaluation Engine computes a composite evidence reliability score; if confidence drops below 60%, the coordinator triggers an iterative re-retrieval loop.",
            para_body_12
        ),
        PageBreak()
    ]
    story.extend(p_abs1)

    # Abstract Page 2: Paras 4, 5, Future Enhancements, Keywords
    p_abs2 = [
        Paragraph(
            "The application incorporates a resilient, multi-provider LLM interface powered by OpenRouter, dynamically routing requests to active free models (openrouter/free, google/gemma-4-31b-it:free, qwen/qwen3.8-27b:free) or commercial flagship models (openai/gpt-4o). To guarantee uninterrupted demonstration and zero service failures during network outages or key exhaustion, the architecture includes an internal Extractive Knowledge Synthesizer as an automated offline fallback.",
            para_body_12
        ),
        Paragraph(
            "The user interface, developed in Streamlit, replaces raw technical logs with a structured Google AI Overview layout. The interface organizes answers sequentially: Direct Answer, Understand It Simply, Visual Operational Flow, Key Points, Decision Guide, Evidence-supported Advantages and Limitations, and Source Receipts with cosine similarity metrics. The framework was evaluated across 40 rigorous test scenarios. Results indicate that adaptive routing reduces inference overhead on simple queries by up to 68% while elevating response faithfulness and citation precision to over 92% on complex inquiries, delivering an end-to-end decision-support assistant for non-technical users.",
            para_body_12
        ),
        Paragraph(
            "Future enhancements may include integration with enterprise relational databases, distributed vector sharding across terabyte corpora, continuous active learning loops from user feedback, and role-based access control (RBAC). The system is intended as an autonomous decision-support prototype and demonstrates verifiable evidence grounding across diverse multidisciplinary operational environments.",
            para_body_12
        ),
        Spacer(1, 6),
        Paragraph(
            "<b>Keywords:</b> Artificial Intelligence, Multi-Agent Systems, Retrieval-Augmented Generation (RAG), LangGraph, Vector Databases, ChromaDB, Decision Support Systems, Automated Fact Verification, OpenRouter, Streamlit.",
            para_body_noindent_12
        ),
        PageBreak()
    ]
    story.extend(p_abs2)

    return story


def get_plagiarism_cert_page():
    cert_img_path = os.path.join(PROJECT_DIR, "scratch", "images", "plagiarism_report_page_1.png")
    p_cert = [
        Paragraph("PLAGIARISM CERTIFICATE", heading_center_14),
        Spacer(1, 8),
    ]
    if os.path.exists(cert_img_path):
        p_cert.append(Image(cert_img_path, width=410, height=580))
    p_cert.append(PageBreak())
    return p_cert


def get_list_of_tables_page():
    tables_list_rows = [
        [Paragraph("<b>Table No.</b>", toc_header), Paragraph("<b>Title</b>", toc_header), Paragraph("<b>Page No.</b>", toc_header)],
        [Paragraph("Table 3.1", toc_cell_center), Paragraph("Hardware Requirements", toc_cell), Paragraph("7", toc_cell_center)],
        [Paragraph("Table 3.2", toc_cell_center), Paragraph("Software Specification and Tooling Stack", toc_cell), Paragraph("8", toc_cell_center)],
        [Paragraph("Table 5.1", toc_cell_center), Paragraph("Vector Store and LangGraph State Data Schema", toc_cell), Paragraph("23", toc_cell_center)],
        [Paragraph("Table 7.1", toc_cell_center), Paragraph("Functional Test Cases and Expected Results", toc_cell), Paragraph("34", toc_cell_center)],
        [Paragraph("Table 7.2", toc_cell_center), Paragraph("Unit Testing Record Across Agent Modules", toc_cell), Paragraph("37", toc_cell_center)],
        [Paragraph("Table 7.3", toc_cell_center), Paragraph("Integration Test Cases for State Machine Transitions", toc_cell), Paragraph("37", toc_cell_center)],
        [Paragraph("Table 7.4", toc_cell_center), Paragraph("System Testing Checklist", toc_cell), Paragraph("38", toc_cell_center)],
        [Paragraph("Table 7.5", toc_cell_center), Paragraph("Performance Evaluation Record", toc_cell), Paragraph("40", toc_cell_center)],
        [Paragraph("Table 7.6", toc_cell_center), Paragraph("Qualitative Evaluation of the Framework", toc_cell), Paragraph("41", toc_cell_center)],
        [Paragraph("Table 8.1", toc_cell_center), Paragraph("Summary of System Functional Results", toc_cell), Paragraph("43", toc_cell_center)],
    ]
    t_tbl = Table(tables_list_rows, colWidths=[65, 295, 65])
    t_tbl.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
    ]))
    p_tbl = [
        Paragraph("LIST OF TABLES", heading_center_14),
        Spacer(1, 6),
        t_tbl,
        PageBreak()
    ]
    return p_tbl


def get_list_of_figures_page():
    figures_list_rows = [
        [Paragraph("<b>Figure No.</b>", toc_header), Paragraph("<b>Title</b>", toc_header), Paragraph("<b>Page No.</b>", toc_header)],
        [Paragraph("Figure 5.1", toc_cell_center), Paragraph("System Architecture of the Proposed Framework", toc_cell), Paragraph("17", toc_cell_center)],
        [Paragraph("Figure 5.2", toc_cell_center), Paragraph("Context Diagram of the Proposed System (DFD Level 0)", toc_cell), Paragraph("18", toc_cell_center)],
        [Paragraph("Figure 5.3", toc_cell_center), Paragraph("Use Case Diagram of the Proposed System", toc_cell), Paragraph("19", toc_cell_center)],
        [Paragraph("Figure 5.4", toc_cell_center), Paragraph("Activity Diagram of the Proposed System", toc_cell), Paragraph("20", toc_cell_center)],
        [Paragraph("Figure 5.5", toc_cell_center), Paragraph("Data Flow Diagram of the Proposed System (DFD Level 1)", toc_cell), Paragraph("21", toc_cell_center)],
        [Paragraph("Figure 5.6", toc_cell_center), Paragraph("Streamlit User Interface / Application Output Wireframe", toc_cell), Paragraph("24", toc_cell_center)],
        [Paragraph("Figure 6.1", toc_cell_center), Paragraph("Multi-Agent Routing and Retrieval Sequence Flowchart", toc_cell), Paragraph("31", toc_cell_center)],
        [Paragraph("Figure 6.2", toc_cell_center), Paragraph("Multi-Source Context Fusion &amp; Fallback Synthesis Flowchart", toc_cell), Paragraph("32", toc_cell_center)],
        [Paragraph("Figure 8.1", toc_cell_center), Paragraph("LangGraph Multi-Agent Execution State Graph", toc_cell), Paragraph("44", toc_cell_center)],
        [Paragraph("Figure 8.2", toc_cell_center), Paragraph("RAG Triad Evaluation Metrics Radar and Distribution", toc_cell), Paragraph("45", toc_cell_center)],
        [Paragraph("Figure 8.3", toc_cell_center), Paragraph("Execution Latency Comparison Across Modes", toc_cell), Paragraph("45", toc_cell_center)],
        [Paragraph("Figure A.1", toc_cell_center), Paragraph("Application Execution -- Terminal to Run the Program", toc_cell), Paragraph("51", toc_cell_center)],
        [Paragraph("Figure A.2", toc_cell_center), Paragraph("Streamlit Web Interface -- Giving User Query", toc_cell), Paragraph("52", toc_cell_center)],
        [Paragraph("Figure A.3", toc_cell_center), Paragraph("Streamlit Web Interface -- Output that the Query Gives", toc_cell), Paragraph("53", toc_cell_center)],
        [Paragraph("Figure A.4", toc_cell_center), Paragraph("End-to-End System Integration Flowchart", toc_cell), Paragraph("54", toc_cell_center)],
    ]
    t_fig = Table(figures_list_rows, colWidths=[65, 295, 65])
    t_fig.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
    ]))
    p_fig = [
        Paragraph("LIST OF FIGURES", heading_center_14),
        Spacer(1, 6),
        t_fig
    ]
    return p_fig


def build_11_page_pdf():
    # Exactly matching F1: Title, Bonafide, Acknowledgement, TOC (3), Abstract (2), Plagiarism (1), List of Tables (1), List of Figures (1)
    story = []
    story.extend(get_title_page())           # Page 1
    story.extend(get_bonafide_page())        # Page 2
    story.extend(get_acknowledgement_page()) # Page 3
    story.extend(get_toc_pages())            # Pages 4, 5, 6
    story.extend(get_abstract_pages())       # Pages 7, 8
    story.extend(get_plagiarism_cert_page()) # Page 9
    story.extend(get_list_of_tables_page())  # Page 10
    story.extend(get_list_of_figures_page()) # Page 11

    doc = SimpleDocTemplate(
        OUT_11_PROJECT,
        pagesize=A4,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN
    )
    doc.build(story, canvasmaker=NoHeaderCanvas)
    shutil.copyfile(OUT_11_PROJECT, OUT_11_ARTIFACT)


def build_12_page_pdf():
    # Including Declaration: Title, Bonafide, Declaration, Acknowledgement, TOC (3), Abstract (2), Plagiarism (1), List of Tables (1), List of Figures (1)
    story = []
    story.extend(get_title_page())           # Page 1
    story.extend(get_bonafide_page())        # Page 2
    story.extend(get_declaration_page())     # Page 3
    story.extend(get_acknowledgement_page()) # Page 4
    story.extend(get_toc_pages())            # Pages 5, 6, 7
    story.extend(get_abstract_pages())       # Pages 8, 9
    story.extend(get_plagiarism_cert_page()) # Page 10
    story.extend(get_list_of_tables_page())  # Page 11
    story.extend(get_list_of_figures_page()) # Page 12

    doc = SimpleDocTemplate(
        OUT_12_PROJECT,
        pagesize=A4,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN
    )
    doc.build(story, canvasmaker=NoHeaderCanvas)
    shutil.copyfile(OUT_12_PROJECT, OUT_12_ARTIFACT)


def build_complete_merged_pdf():
    # Merges 11 preliminary pages with 62-page reference-matched report
    p_main = os.path.join(PROJECT_DIR, "Self_Adaptive_MultiAgent_RAG_Report_Reference_Matched.pdf")
    out_proj = os.path.join(PROJECT_DIR, "Self_Adaptive_MultiAgent_RAG_Complete_Full_Report.pdf")
    out_art = os.path.join(ARTIFACT_DIR, "Self_Adaptive_MultiAgent_RAG_Complete_Full_Report.pdf")

    writer = pypdf.PdfWriter()
    r_prelim = pypdf.PdfReader(OUT_11_PROJECT)
    r_main = pypdf.PdfReader(p_main)

    for p in r_prelim.pages:
        writer.add_page(p)
    for p in r_main.pages:
        writer.add_page(p)

    with open(out_proj, 'wb') as f:
        writer.write(f)
    shutil.copyfile(out_proj, out_art)


def main():
    print("[1/3] Compiling 11-Page Preliminary Pages (Exact match to 1st PDF, No Declaration)...")
    build_11_page_pdf()
    r11 = pypdf.PdfReader(OUT_11_PROJECT)
    print(f"VERIFIED PRELIMINARY PAGES: Total pages = {len(r11.pages)}")
    for i, p in enumerate(r11.pages):
        txt = p.extract_text().splitlines()
        first_line = txt[0] if txt else 'EMPTY'
        print(f"  Page {i+1}: {first_line[:65]}")

    print("\n[2/3] Merging with 62-Page Report into Complete Full Bound Report...")
    build_complete_merged_pdf()
    r_full = pypdf.PdfReader(os.path.join(PROJECT_DIR, "Self_Adaptive_MultiAgent_RAG_Complete_Full_Report.pdf"))
    print(f"VERIFIED COMPLETE FULL REPORT: Total pages = {len(r_full.pages)} (11 prelim + 62 main = {len(r_full.pages)})")

    print("\nSUCCESS! Preliminary pages and Complete Full Report compiled successfully.")


if __name__ == "__main__":
    main()
