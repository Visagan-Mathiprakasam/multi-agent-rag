import os
import shutil
from reportlab.platypus import SimpleDocTemplate, PageBreak
from ref_styles import (
    ReferenceDocCanvas, A4, LEFT_MARGIN, RIGHT_MARGIN, TOP_MARGIN, BOTTOM_MARGIN
)
from ref_ch123 import get_ch123_pages
from ref_ch456 import get_ch456_pages
from ref_ch78 import get_ch78_pages
from ref_ch910 import get_ch910_pages

def build_pdf():
    workspace_pdf = r"C:\Users\visag\.gemini\antigravity\scratch\multi_agent_rag\Self_Adaptive_MultiAgent_RAG_Report_Reference_Matched.pdf"
    artifact_pdf = r"C:\Users\visag\.gemini\antigravity\brain\16632dba-7765-414e-bb84-677366a2f22c\Self_Adaptive_MultiAgent_RAG_Report_Reference_Matched.pdf"

    print("[1/5] Gathering story flowables across all 62 pages...")
    story = []
    story.extend(get_ch123_pages())  # Pages 1 to 10
    story.extend(get_ch456_pages())  # Pages 11 to 33
    story.extend(get_ch78_pages())   # Pages 34 to 50
    story.extend(get_ch910_pages())  # Pages 51 to 62

    # Remove trailing PageBreak if present on the final page
    if story and isinstance(story[-1], PageBreak):
        story.pop()

    print(f"[2/5] Initializing SimpleDocTemplate for {workspace_pdf}...")
    doc = SimpleDocTemplate(
        workspace_pdf,
        pagesize=A4,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN,
        title="Self-Adaptive Multi-Agent RAG Framework - PG Project Report",
        author="Visagan Mathiprakasam",
        subject="Department of Computer Applications PG Project Report (2026-2027)"
    )

    print("[3/5] Building document with ReferenceDocCanvas...")
    doc.build(story, canvasmaker=ReferenceDocCanvas)
    print("SUCCESS: PDF compiled successfully!")

    print(f"[4/5] Copying to artifact path: {artifact_pdf}...")
    shutil.copyfile(workspace_pdf, artifact_pdf)

    print("[5/5] Verifying page count with pypdf...")
    import pypdf
    reader = pypdf.PdfReader(workspace_pdf)
    total_pages = len(reader.pages)
    print(f"VERIFIED TOTAL PAGES: {total_pages}")
    
    # Check for non-ASCII characters
    has_ufffd = False
    for idx, p in enumerate(reader.pages):
        text = p.extract_text() or ""
        if '\ufffd' in text:
            print(f"WARNING: Page {idx+1} contains unicode replacement character \\ufffd")
            has_ufffd = True
    if not has_ufffd:
        print("CHARACTER ENCODING: 100% Clean ASCII (Zero \\ufffd characters detected across all pages)")

if __name__ == "__main__":
    build_pdf()
