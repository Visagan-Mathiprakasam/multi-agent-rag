import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Output directory for generated diagram images
IMG_DIR = r"C:\Users\visag\.gemini\antigravity\brain\16632dba-7765-414e-bb84-677366a2f22c\scratch\images"
os.makedirs(IMG_DIR, exist_ok=True)

# Common styling parameters
FONT_FAMILY = 'DejaVu Sans'
plt.rcParams['font.family'] = FONT_FAMILY
plt.rcParams['font.size'] = 9

def draw_fig_5_1():
    """Figure 5.1: Architecture of the Self-Adaptive Multi-Agent RAG Framework"""
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis('off')

    # Background canvas card
    bg = patches.FancyBboxPatch((0.5, 0.5), 99, 49, boxstyle="round,pad=0.2",
                                facecolor="#F8FAFC", edgecolor="#CBD5E1", lw=1.2)
    ax.add_patch(bg)

    # Layer 1: Presentation Layer
    p_box = patches.FancyBboxPatch((3, 6), 18, 38, boxstyle="round,pad=0.5",
                                   facecolor="#EFF6FF", edgecolor="#3B82F6", lw=1.5)
    ax.add_patch(p_box)
    ax.text(12, 40, "PRESENTATION\nLAYER", ha='center', va='center', weight='bold', color="#1E3A8A", fontsize=9)
    ax.text(12, 28, "Streamlit Web UI\n\n- Chat Dialogue\n- Model Select\n- Agent Traces\n- Triad Metrics",
            ha='center', va='center', color="#1E293B", fontsize=8)

    # Layer 2: Orchestration Layer (LangGraph)
    o_box = patches.FancyBboxPatch((25, 6), 46, 38, boxstyle="round,pad=0.5",
                                   facecolor="#F0FDF4", edgecolor="#10B981", lw=1.5)
    ax.add_patch(o_box)
    ax.text(48, 41, "ORCHESTRATION & AGENT ENSEMBLE (LangGraph StateGraph)", ha='center', va='center', weight='bold', color="#065F46", fontsize=9.5)

    # Sub-agents inside Orchestration
    agents = [
        ("Query Router\nAgent", 30, 26, "#DCFCE7", "#15803D"),
        ("Semantic\nRetriever", 42, 26, "#DCFCE7", "#15803D"),
        ("Live Web\nSearcher", 54, 26, "#DCFCE7", "#15803D"),
        ("Multi-Source\nSynthesizer", 36, 12, "#FEF3C7", "#D97706"),
        ("RAG Triad\nEvaluator", 50, 12, "#F3E8FF", "#7E22CE")
    ]
    for label, x, y, fc, ec in agents:
        abox = patches.FancyBboxPatch((x-4.5, y-4), 9, 8, boxstyle="round,pad=0.3",
                                      facecolor=fc, edgecolor=ec, lw=1.2)
        ax.add_patch(abox)
        ax.text(x, y, label, ha='center', va='center', weight='bold', color="#0F172A", fontsize=7.5)

    # Internal Agent Arrows
    ax.annotate('', xy=(37.5, 26), xytext=(34.5, 26), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.2))
    ax.annotate('', xy=(49.5, 26), xytext=(46.5, 26), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.2))
    ax.annotate('', xy=(36, 16), xytext=(36, 22), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.2))
    ax.annotate('', xy=(50, 16), xytext=(50, 22), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.2))
    ax.annotate('', xy=(45.5, 12), xytext=(40.5, 12), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.2))

    # Layer 3: Knowledge & Inference Services
    k_box = patches.FancyBboxPatch((75, 26), 22, 18, boxstyle="round,pad=0.5",
                                   facecolor="#FFFBEB", edgecolor="#F59E0B", lw=1.5)
    ax.add_patch(k_box)
    ax.text(86, 40, "KNOWLEDGE STORES", ha='center', va='center', weight='bold', color="#92400E", fontsize=8.5)
    ax.text(86, 31, "ChromaDB (Local)\nDense Vector Store\n(384-dim MiniLM)\n----\nDuckDuckGo Search",
            ha='center', va='center', color="#0F172A", fontsize=7.5)

    inf_box = patches.FancyBboxPatch((75, 6), 22, 17, boxstyle="round,pad=0.5",
                                     facecolor="#FAF5FF", edgecolor="#8B5CF6", lw=1.5)
    ax.add_patch(inf_box)
    ax.text(86, 19, "INFERENCE GATEWAY", ha='center', va='center', weight='bold', color="#5B21B6", fontsize=8.5)
    ax.text(86, 11, "OpenRouter API\n- Meta Llama 3.3\n- Mistral Nemo\n- Deterministic Fallback",
            ha='center', va='center', color="#0F172A", fontsize=7.5)

    # Inter-layer connecting arrows
    ax.annotate('Query', xy=(25, 28), xytext=(21, 28),
                arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.5), fontsize=7.5, color="#2563EB", weight='bold')
    ax.annotate('Answer + Triad', xy=(21, 14), xytext=(25, 14),
                arrowprops=dict(arrowstyle="<-", color="#059669", lw=1.5), fontsize=7.5, color="#059669", weight='bold')

    ax.annotate('Top-k Chunks', xy=(63.5, 30), xytext=(75, 30),
                arrowprops=dict(arrowstyle="->", color="#D97706", lw=1.3), fontsize=7.5, color="#D97706")
    ax.annotate('Prompt / Comp', xy=(75, 12), xytext=(54.5, 12),
                arrowprops=dict(arrowstyle="<->", color="#7C3AED", lw=1.3), fontsize=7.5, color="#7C3AED")

    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, "fig_5_1_architecture.png")
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    print("Saved:", out_path)

def draw_fig_5_2():
    """Figure 5.2: Context Diagram of the Proposed System"""
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis('off')

    # Center process
    center = patches.Circle((50, 25), 11, facecolor="#DBEAFE", edgecolor="#1D4ED8", lw=2)
    ax.add_patch(center)
    ax.text(50, 26.5, "0.0\nMulti-Agent RAG\nFramework", ha='center', va='center', weight='bold', color="#1E3A8A", fontsize=9)
    ax.text(50, 18, "(Central System)", ha='center', va='center', fontstyle='italic', color="#3B82F6", fontsize=7.5)

    # External entities
    # 1. User (Left)
    u_box = patches.FancyBboxPatch((3, 20), 16, 12, boxstyle="round,pad=0.3",
                                   facecolor="#F1F5F9", edgecolor="#475569", lw=1.5)
    ax.add_patch(u_box)
    ax.text(11, 26, "End User /\nKnowledge Worker", ha='center', va='center', weight='bold', color="#0F172A", fontsize=8.5)

    # 2. ChromaDB (Top Right)
    c_box = patches.FancyBboxPatch((78, 33), 18, 12, boxstyle="round,pad=0.3",
                                   facecolor="#FEF3C7", edgecolor="#D97706", lw=1.5)
    ax.add_patch(c_box)
    ax.text(87, 39, "ChromaDB\nVector Store", ha='center', va='center', weight='bold', color="#92400E", fontsize=8.5)

    # 3. DuckDuckGo (Right Middle)
    d_box = patches.FancyBboxPatch((78, 18), 18, 12, boxstyle="round,pad=0.3",
                                   facecolor="#DCFCE7", edgecolor="#16A34A", lw=1.5)
    ax.add_patch(d_box)
    ax.text(87, 24, "DuckDuckGo\nSearch Engine", ha='center', va='center', weight='bold', color="#14532D", fontsize=8.5)

    # 4. OpenRouter API (Bottom Right)
    o_box = patches.FancyBboxPatch((78, 3), 18, 12, boxstyle="round,pad=0.3",
                                   facecolor="#F3E8FF", edgecolor="#9333EA", lw=1.5)
    ax.add_patch(o_box)
    ax.text(87, 9, "OpenRouter\nAPI Gateway", ha='center', va='center', weight='bold', color="#581C87", fontsize=8.5)

    # Connecting labeled arrows
    # User -> System
    ax.annotate('Query & Filters', xy=(39, 27), xytext=(19, 27),
                arrowprops=dict(arrowstyle="->", color="#1E293B", lw=1.3), fontsize=7.5)
    # System -> User
    ax.annotate('Answer + Citations', xy=(19, 23), xytext=(39, 23),
                arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.3), fontsize=7.5, color="#2563EB")

    # System <-> ChromaDB
    ax.annotate('Dense Embedding Query', xy=(78, 41), xytext=(60, 32),
                arrowprops=dict(arrowstyle="->", color="#D97706", lw=1.3), fontsize=7)
    ax.annotate('Top-K Matching Chunks', xy=(58, 30), xytext=(78, 37),
                arrowprops=dict(arrowstyle="->", color="#D97706", lw=1.3), fontsize=7)

    # System <-> DuckDuckGo
    ax.annotate('Keyword Search Query', xy=(78, 25), xytext=(61, 26),
                arrowprops=dict(arrowstyle="->", color="#16A34A", lw=1.3), fontsize=7)
    ax.annotate('Scraped Web Snippets', xy=(61, 23), xytext=(78, 22),
                arrowprops=dict(arrowstyle="->", color="#16A34A", lw=1.3), fontsize=7)

    # System <-> OpenRouter
    ax.annotate('Prompt with Evidence', xy=(78, 10), xytext=(60, 18),
                arrowprops=dict(arrowstyle="->", color="#9333EA", lw=1.3), fontsize=7)
    ax.annotate('Synthesized Completion', xy=(58, 16), xytext=(78, 6),
                arrowprops=dict(arrowstyle="->", color="#9333EA", lw=1.3), fontsize=7)

    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, "fig_5_2_context.png")
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    print("Saved:", out_path)

def draw_fig_5_3():
    """Figure 5.3: Use Case Diagram of the Proposed System"""
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis('off')

    # System Boundary Box
    b_box = patches.Rectangle((22, 2), 56, 46, facecolor="#F8FAFC", edgecolor="#64748B", lw=1.5, linestyle="--")
    ax.add_patch(b_box)
    ax.text(50, 45.5, "Self-Adaptive Multi-Agent RAG System Boundary", ha='center', va='center', weight='bold', color="#334155", fontsize=9)

    # Left Actor: End User
    ax.plot([10, 10], [26, 31], color="#0F172A", lw=2) # body
    ax.plot([10], [33], marker='o', markersize=9, color="#0F172A") # head
    ax.plot([6, 14], [29, 29], color="#0F172A", lw=2) # arms
    ax.plot([6, 10, 14], [22, 26, 22], color="#0F172A", lw=2) # legs
    ax.text(10, 18, "End User", ha='center', va='center', weight='bold', color="#0F172A", fontsize=8.5)

    # Right Actor: Admin & Cloud
    ax.plot([90, 90], [35, 40], color="#0F172A", lw=2)
    ax.plot([90], [42], marker='o', markersize=8, color="#0F172A")
    ax.plot([87, 93], [38, 38], color="#0F172A", lw=2)
    ax.plot([87, 90, 93], [31, 35, 31], color="#0F172A", lw=2)
    ax.text(90, 27, "System\nAdministrator", ha='center', va='center', weight='bold', color="#0F172A", fontsize=8)

    # Use Cases (Ellipses)
    ucs = [
        ("Submit Natural\nLanguage Query", 35, 38, "#EFF6FF", "#3B82F6"),
        ("Classify Intent\n& Route Strategy", 63, 38, "#ECFDF5", "#10B981"),
        ("Semantic Vector\nSearch (ChromaDB)", 35, 27, "#FEF3C7", "#D97706"),
        ("Live Web Search\n(DuckDuckGo)", 63, 27, "#ECFDF5", "#10B981"),
        ("Synthesize Answer\nwith Citations", 35, 16, "#EFF6FF", "#3B82F6"),
        ("Compute Automated\nRAG Triad Scores", 63, 16, "#FAF5FF", "#8B5CF6"),
        ("Ingest Documents\n& Build Embeddings", 49, 6, "#FFF1F2", "#E11D48")
    ]
    for label, x, y, fc, ec in ucs:
        ell = patches.Ellipse((x, y), 22, 7.5, facecolor=fc, edgecolor=ec, lw=1.2)
        ax.add_patch(ell)
        ax.text(x, y, label, ha='center', va='center', weight='bold', color="#0F172A", fontsize=7.2)

    # Association Lines
    ax.plot([14, 24], [27, 38], color="#64748B", lw=1.2)
    ax.plot([14, 24], [26, 27], color="#64748B", lw=1.2)
    ax.plot([14, 24], [24, 16], color="#64748B", lw=1.2)

    ax.plot([85, 60], [33, 6], color="#64748B", lw=1.2) # Admin to Ingest
    ax.plot([85, 74], [35, 38], color="#64748B", lw=1.2) # Admin to Route

    # Include / Extend relations
    ax.annotate('<<include>>', xy=(52, 38), xytext=(46, 38),
                arrowprops=dict(arrowstyle="->", color="#94A3B8", linestyle="--"), fontsize=6.5, color="#64748B")
    ax.annotate('<<include>>', xy=(35, 20), xytext=(35, 23.5),
                arrowprops=dict(arrowstyle="->", color="#94A3B8", linestyle="--"), fontsize=6.5, color="#64748B")
    ax.annotate('<<extend>>', xy=(63, 20), xytext=(63, 23.5),
                arrowprops=dict(arrowstyle="->", color="#94A3B8", linestyle="--"), fontsize=6.5, color="#64748B")

    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, "fig_5_3_use_case.png")
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    print("Saved:", out_path)

def draw_fig_5_4():
    """Figure 5.4: Activity Diagram for Query Processing and Adaptive RAG"""
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis('off')

    # Initial state
    init_dot = patches.Circle((6, 25), 2.2, facecolor="#0F172A", edgecolor="#0F172A")
    ax.add_patch(init_dot)
    ax.text(6, 19, "Start", ha='center', va='center', weight='bold', fontsize=7.5)

    # Activity 1: Receive Query
    a1 = patches.FancyBboxPatch((12, 21), 11, 8, boxstyle="round,pad=0.2", facecolor="#EFF6FF", edgecolor="#3B82F6", lw=1.2)
    ax.add_patch(a1)
    ax.text(17.5, 25, "Receive\nUser Prompt", ha='center', va='center', weight='bold', fontsize=7.5)
    ax.annotate('', xy=(12, 25), xytext=(8.5, 25), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.2))

    # Activity 2: Classify Intent
    a2 = patches.FancyBboxPatch((27, 21), 11, 8, boxstyle="round,pad=0.2", facecolor="#EFF6FF", edgecolor="#3B82F6", lw=1.2)
    ax.add_patch(a2)
    ax.text(32.5, 25, "Router:\nClassify Intent", ha='center', va='center', weight='bold', fontsize=7.5)
    ax.annotate('', xy=(27, 25), xytext=(23, 25), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.2))

    # Decision Diamond
    diamond = patches.Polygon([[42, 25], [45.5, 29], [49, 25], [45.5, 21]], closed=True,
                              facecolor="#FEF3C7", edgecolor="#D97706", lw=1.2)
    ax.add_patch(diamond)
    ax.text(45.5, 25, "Route?", ha='center', va='center', weight='bold', fontsize=7)
    ax.annotate('', xy=(42, 25), xytext=(38, 25), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.2))

    # Branch 1: Vector RAG (Top)
    v_box = patches.FancyBboxPatch((53, 36), 12, 7.5, boxstyle="round,pad=0.2", facecolor="#DCFCE7", edgecolor="#16A34A", lw=1.2)
    ax.add_patch(v_box)
    ax.text(59, 39.7, "ChromaDB\nVector Retrieval", ha='center', va='center', weight='bold', fontsize=7.2)

    # Branch 2: Web Search (Middle)
    w_box = patches.FancyBboxPatch((53, 21), 12, 7.5, boxstyle="round,pad=0.2", facecolor="#DCFCE7", edgecolor="#16A34A", lw=1.2)
    ax.add_patch(w_box)
    ax.text(59, 24.7, "DuckDuckGo\nWeb Search", ha='center', va='center', weight='bold', fontsize=7.2)

    # Branch 3: Direct LLM (Bottom)
    d_box = patches.FancyBboxPatch((53, 7), 12, 7.5, boxstyle="round,pad=0.2", facecolor="#F3E8FF", edgecolor="#9333EA", lw=1.2)
    ax.add_patch(d_box)
    ax.text(59, 10.7, "Direct LLM\nBypass Retrieval", ha='center', va='center', weight='bold', fontsize=7.2)

    # Arrows from diamond to branches
    ax.annotate('', xy=(53, 39.7), xytext=(45.5, 29), arrowprops=dict(arrowstyle="->", color="#16A34A", lw=1.2))
    ax.text(47, 36, "[Vector]", fontsize=6.8, color="#16A34A", weight='bold')

    ax.annotate('', xy=(53, 25), xytext=(49, 25), arrowprops=dict(arrowstyle="->", color="#16A34A", lw=1.2))
    ax.text(49.5, 26.5, "[Web/Hybrid]", fontsize=6.8, color="#16A34A", weight='bold')

    ax.annotate('', xy=(53, 11), xytext=(45.5, 21), arrowprops=dict(arrowstyle="->", color="#9333EA", lw=1.2))
    ax.text(47, 14, "[Direct]", fontsize=6.8, color="#9333EA", weight='bold')

    # Synchronization Bar / Join
    join_bar = patches.Rectangle((69, 5), 1.5, 40, facecolor="#0F172A", edgecolor="#0F172A")
    ax.add_patch(join_bar)

    ax.annotate('', xy=(69, 39.7), xytext=(65, 39.7), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.2))
    ax.annotate('', xy=(69, 25), xytext=(65, 25), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.2))
    ax.annotate('', xy=(69, 11), xytext=(65, 11), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.2))

    # Activity: Synthesize
    s_box = patches.FancyBboxPatch((74, 28), 12, 8, boxstyle="round,pad=0.2", facecolor="#FEF3C7", edgecolor="#D97706", lw=1.2)
    ax.add_patch(s_box)
    ax.text(80, 32, "Synthesizer:\nAnswer & Cites", ha='center', va='center', weight='bold', fontsize=7.2)
    ax.annotate('', xy=(74, 32), xytext=(70.5, 32), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.2))

    # Activity: Evaluate
    e_box = patches.FancyBboxPatch((74, 14), 12, 8, boxstyle="round,pad=0.2", facecolor="#F3E8FF", edgecolor="#7E22CE", lw=1.2)
    ax.add_patch(e_box)
    ax.text(80, 18, "Evaluator:\nRAG Triad Scores", ha='center', va='center', weight='bold', fontsize=7.2)
    ax.annotate('', xy=(80, 22), xytext=(80, 28), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.2))

    # Final State
    ax.annotate('', xy=(90, 18), xytext=(86, 18), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.2))
    f_out = patches.Circle((93, 18), 2.5, facecolor="white", edgecolor="#0F172A", lw=1.5)
    f_in = patches.Circle((93, 18), 1.4, facecolor="#0F172A", edgecolor="#0F172A")
    ax.add_patch(f_out)
    ax.add_patch(f_in)
    ax.text(93, 12.5, "End UI Display", ha='center', va='center', weight='bold', fontsize=7.2)

    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, "fig_5_4_activity.png")
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    print("Saved:", out_path)

def draw_fig_5_5():
    """Figure 5.5: Data Flow Diagram (Level 1) of the Proposed System"""
    fig, ax = plt.subplots(figsize=(10, 4.1), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis('off')

    # Entity: User
    u_ent = patches.Rectangle((3, 29), 13, 14, facecolor="#F1F5F9", edgecolor="#475569", lw=1.5)
    ax.add_patch(u_ent)
    ax.text(9.5, 36, "USER\n(Browser)", ha='center', va='center', weight='bold', color="#0F172A", fontsize=8)

    # Process 2.0: Query Classification
    p2 = patches.Circle((30, 36), 6.5, facecolor="#EFF6FF", edgecolor="#2563EB", lw=1.5)
    ax.add_patch(p2)
    ax.text(30, 37, "2.0\nQuery Intent\nRouting", ha='center', va='center', weight='bold', color="#1E3A8A", fontsize=7.2)

    # Process 3.0: Vector Retrieval
    p3 = patches.Circle((55, 36), 6.5, facecolor="#EFF6FF", edgecolor="#2563EB", lw=1.5)
    ax.add_patch(p3)
    ax.text(55, 37, "3.0\nSemantic\nVector Search", ha='center', va='center', weight='bold', color="#1E3A8A", fontsize=7.2)

    # Process 4.0: Web Scraping
    p4 = patches.Circle((55, 14), 6.5, facecolor="#EFF6FF", edgecolor="#2563EB", lw=1.5)
    ax.add_patch(p4)
    ax.text(55, 15, "4.0\nLive Web\nScraping", ha='center', va='center', weight='bold', color="#1E3A8A", fontsize=7.2)

    # Process 5.0: Synthesis & Eval
    p5 = patches.Circle((80, 25), 7.5, facecolor="#EFF6FF", edgecolor="#2563EB", lw=1.5)
    ax.add_patch(p5)
    ax.text(80, 26, "5.0\nMulti-Source\nSynthesis &\nEvaluation", ha='center', va='center', weight='bold', color="#1E3A8A", fontsize=7.2)

    # Data Store D1: ChromaDB
    d1_top = patches.Rectangle((23, 10), 16, 8, facecolor="#FFFBEB", edgecolor="#D97706", lw=1.2)
    ax.add_patch(d1_top)
    ax.text(31, 14, "D1: ChromaDB\nVector Collections", ha='center', va='center', weight='bold', color="#92400E", fontsize=7.2)

    # Flow arrows
    # User -> P2.0
    ax.annotate('Query String', xy=(23.5, 36), xytext=(16, 36),
                arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.2), fontsize=7)

    # P2.0 -> P3.0
    ax.annotate('Vector Route', xy=(48.5, 37.5), xytext=(36.5, 37.5),
                arrowprops=dict(arrowstyle="->", color="#16A34A", lw=1.2), fontsize=7, color="#16A34A")

    # P2.0 -> P4.0
    ax.annotate('Web Route', xy=(49, 18), xytext=(34, 30),
                arrowprops=dict(arrowstyle="->", color="#16A34A", lw=1.2), fontsize=7, color="#16A34A")

    # P3.0 <-> D1
    ax.annotate('Query Vector', xy=(33, 18), xytext=(50, 31),
                arrowprops=dict(arrowstyle="->", color="#D97706", lw=1.2), fontsize=6.8)
    ax.annotate('Top Chunks', xy=(52, 30), xytext=(36, 18),
                arrowprops=dict(arrowstyle="->", color="#D97706", lw=1.2), fontsize=6.8)

    # P3.0 -> P5.0
    ax.annotate('Context Chunks', xy=(73, 29), xytext=(61.5, 36),
                arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.2), fontsize=7)

    # P4.0 -> P5.0
    ax.annotate('Web Snippets', xy=(73, 21), xytext=(61.5, 14),
                arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.2), fontsize=7)

    # P5.0 -> User
    ax.plot([80, 80, 10, 10], [17.5, 4, 4, 29], color="#2563EB", lw=1.3, linestyle="-")
    ax.text(48, 5.5, "Synthesized Answer, Evidence Citations & RAG Triad Scores",
            ha='center', va='center', weight='bold', color="#2563EB", fontsize=7.5)

    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, "fig_5_5_dfd.png")
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    print("Saved:", out_path)

def draw_fig_8_2():
    """Figure 8.2: RAG Triad Evaluation Metrics Radar and Distribution Chart"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.8), dpi=300)

    # Left: Radar Chart
    categories = ['Context\nRelevance', 'Groundedness\n(Faithfulness)', 'Answer\nRelevance', 'Query\nRouting Acc']
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    # Convert ax1 to polar projection
    ax1.remove()
    ax1 = fig.add_subplot(1, 2, 1, polar=True)

    scores_proposed = [0.91, 0.94, 0.93, 0.96]
    scores_proposed += scores_proposed[:1]

    scores_baseline = [0.68, 0.76, 0.74, 0.50]
    scores_baseline += scores_baseline[:1]

    ax1.set_theta_offset(np.pi / 2)
    ax1.set_theta_direction(-1)
    ax1.set_xticks(angles[:-1])
    ax1.set_xticklabels(categories, fontsize=8, weight='bold')
    ax1.set_ylim(0, 1.0)
    ax1.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax1.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=7, color="#64748B")

    ax1.plot(angles, scores_proposed, color="#2563EB", linewidth=2, linestyle='solid', label='Multi-Agent RAG (0.926)')
    ax1.fill(angles, scores_proposed, color="#3B82F6", alpha=0.25)

    ax1.plot(angles, scores_baseline, color="#94A3B8", linewidth=1.5, linestyle='dashed', label='Naive RAG (0.725)')
    ax1.fill(angles, scores_baseline, color="#CBD5E1", alpha=0.15)
    ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.22), fontsize=7.5, frameon=True)
    ax1.set_title("RAG Triad Metric Fidelity", fontsize=9.5, weight='bold', pad=12)

    # Right: Grouped Bar Chart
    labels = ['Context Rel', 'Groundedness', 'Answer Rel', 'Composite']
    x = np.arange(len(labels))
    width = 0.35

    naive_vals = [0.68, 0.76, 0.74, 0.725]
    prop_vals = [0.91, 0.94, 0.93, 0.926]

    rects1 = ax2.bar(x - width/2, naive_vals, width, label='Naive RAG Baseline', color='#94A3B8')
    rects2 = ax2.bar(x + width/2, prop_vals, width, label='Proposed Multi-Agent', color='#2563EB')

    ax2.set_ylabel('Score (0.0 to 1.0)', fontsize=8, weight='bold')
    ax2.set_title('Empirical Metric Benchmark Comparison', fontsize=9.5, weight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, fontsize=8, weight='bold')
    ax2.set_ylim(0, 1.15)
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    ax2.legend(fontsize=7.5, loc='upper left')

    # Add bar values
    for r in rects1:
        h = r.get_height()
        ax2.annotate(f'{h:.2f}', xy=(r.get_x() + r.get_width() / 2, h),
                     xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=7)
    for r in rects2:
        h = r.get_height()
        ax2.annotate(f'{h:.2f}', xy=(r.get_x() + r.get_width() / 2, h),
                     xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=7, weight='bold')

    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, "fig_8_2_radar.png")
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    print("Saved:", out_path)

def draw_fig_8_3():
    """Figure 8.3: Execution Latency Comparison Across Query Modes"""
    fig, ax = plt.subplots(figsize=(10, 3.6), dpi=300)

    modes = [
        'Naive RAG Pipeline\n(Static Vector for all queries)',
        'Hybrid Multi-Agent Path\n(ChromaDB + Web + Synthesis + Triad)',
        'Live Web Search Mode\n(DuckDuckGo API + Synthesizer)',
        'Vector RAG Mode\n(ChromaDB Top-4 + Synthesizer)',
        'Direct LLM Mode\n(Conversational / Greeting bypass)'
    ]
    latencies = [3.40, 2.65, 1.85, 1.45, 0.62]
    colors_list = ['#EF4444', '#F59E0B', '#10B981', '#3B82F6', '#6366F1']

    y_pos = np.arange(len(modes))
    bars = ax.barh(y_pos, latencies, color=colors_list, height=0.55, edgecolor='#1E293B', lw=0.8)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(modes, fontsize=8, weight='bold')
    ax.invert_yaxis()
    ax.set_xlabel('End-to-End Query Execution Latency (seconds)', fontsize=8.5, weight='bold')
    ax.set_title('Latency Comparison Across Dynamic Agent Pathways', fontsize=9.5, weight='bold', pad=10)
    ax.set_xlim(0, 4.0)
    ax.grid(axis='x', linestyle='--', alpha=0.6)

    # Reference threshold line (Acceptable interactive UX < 3.0s)
    ax.axvline(x=3.0, color='#DC2626', linestyle=':', lw=1.5)
    ax.text(3.02, 0.2, 'Interactive UX Limit (3.0s)', color='#DC2626', fontsize=7.5, weight='bold')

    # Data value labels
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.08, bar.get_y() + bar.get_height()/2, f'{w:.2f} s',
                ha='left', va='center', fontsize=8, weight='bold', color="#0F172A")

    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, "fig_8_3_latency.png")
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    print("Saved:", out_path)

if __name__ == "__main__":
    print("Generating all 7 architectural and benchmark figures...")
    draw_fig_5_1()
    draw_fig_5_2()
    draw_fig_5_3()
    draw_fig_5_4()
    draw_fig_5_5()
    draw_fig_8_2()
    draw_fig_8_3()
    print("All diagrams generated successfully!")
