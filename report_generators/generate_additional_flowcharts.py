import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

IMG_DIR = r"C:\Users\visag\.gemini\antigravity\brain\16632dba-7765-414e-bb84-677366a2f22c\scratch\images"
os.makedirs(IMG_DIR, exist_ok=True)

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 9

def draw_fig_5_6():
    """Figure 5.6: Streamlit User Interface Architecture and Wireframe Layout"""
    fig, ax = plt.subplots(figsize=(10, 4.4), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis('off')

    # Browser Outer Window
    window = patches.FancyBboxPatch((1, 1), 98, 48, boxstyle="round,pad=0.3",
                                    facecolor="#FFFFFF", edgecolor="#334155", lw=1.5)
    ax.add_patch(window)

    # Browser title bar
    bar = patches.Rectangle((1, 45.5), 98, 3.5, facecolor="#F1F5F9", edgecolor="#334155", lw=1)
    ax.add_patch(bar)
    for i, col in enumerate(["#EF4444", "#F59E0B", "#10B981"]):
        dot = patches.Circle((3 + i * 2.2, 47.2), 0.8, facecolor=col, edgecolor="none")
        ax.add_patch(dot)
    ax.text(50, 47.2, "http://localhost:8501 - Self-Adaptive Multi-Agent RAG Dashboard",
            ha='center', va='center', fontsize=7.5, color="#475569", weight='bold')

    # Left Sidebar (Streamlit Controls)
    sb = patches.Rectangle((2, 2), 26, 43.5, facecolor="#F8FAFC", edgecolor="#CBD5E1", lw=1)
    ax.add_patch(sb)
    ax.text(15, 42.5, "SYSTEM CONTROLS", ha='center', va='center', weight='bold', color="#1E293B", fontsize=8)

    # Sidebar inputs
    m_box = patches.FancyBboxPatch((3.5, 33), 23, 7, boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor="#94A3B8")
    ax.add_patch(m_box)
    ax.text(15, 37.5, "Model Selector [Dropdown]", ha='center', va='center', fontsize=7, weight='bold')
    ax.text(15, 34.5, "meta-llama/llama-3.3-70b-instruct", ha='center', va='center', fontsize=6, color="#2563EB")

    api_box = patches.FancyBboxPatch((3.5, 23.5), 23, 7, boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor="#94A3B8")
    ax.add_patch(api_box)
    ax.text(15, 28, "OpenRouter API Key [Field]", ha='center', va='center', fontsize=7, weight='bold')
    ax.text(15, 25, "sk-or-v1-****************", ha='center', va='center', fontsize=6.5, color="#64748B")

    sl_box = patches.FancyBboxPatch((3.5, 14), 23, 7.5, boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor="#94A3B8")
    ax.add_patch(sl_box)
    ax.text(15, 19, "Similarity Cutoff Slider", ha='center', va='center', fontsize=7, weight='bold')
    ax.text(15, 16, "Cosine Distance <= 0.45", ha='center', va='center', fontsize=6.5, color="#16A34A")

    status_box = patches.FancyBboxPatch((3.5, 4.5), 23, 7.5, boxstyle="round,pad=0.2", facecolor="#EFF6FF", edgecolor="#3B82F6")
    ax.add_patch(status_box)
    ax.text(15, 9.5, "Status: ChromaDB Ready", ha='center', va='center', fontsize=7, weight='bold', color="#1D4ED8")
    ax.text(15, 6.5, "600+ Chunks Loaded", ha='center', va='center', fontsize=6.5, color="#3B82F6")

    # Main Content Area (Right)
    # Header Banner
    h_box = patches.FancyBboxPatch((30, 39.5), 67.5, 5, boxstyle="round,pad=0.2", facecolor="#EFF6FF", edgecolor="#93C5FD")
    ax.add_patch(h_box)
    ax.text(63.75, 42, "Self-Adaptive Multi-Agent RAG Framework (OpenRouter + LangGraph)",
            ha='center', va='center', weight='bold', color="#1E3A8A", fontsize=8.5)

    # Chat Dialogue: User Query Card
    uq_box = patches.FancyBboxPatch((30, 31.5), 67.5, 6.5, boxstyle="round,pad=0.2", facecolor="#F1F5F9", edgecolor="#CBD5E1")
    ax.add_patch(uq_box)
    ax.text(32, 35.8, "USER QUERY:", weight='bold', fontsize=7, color="#0F172A")
    ax.text(32, 33.2, "\"Explain how LangGraph state machines coordinate multi-agent RAG with web fallback.\"", fontsize=7, color="#1E293B")

    # Agent Route Badge
    badge = patches.FancyBboxPatch((85, 35), 11, 2.5, boxstyle="round,pad=0.1", facecolor="#DCFCE7", edgecolor="#16A34A")
    ax.add_patch(badge)
    ax.text(90.5, 36.2, "Route: HYBRID", ha='center', va='center', weight='bold', fontsize=6, color="#14532D")

    # Synthesized Answer Card
    ans_box = patches.FancyBboxPatch((30, 15.5), 67.5, 14.5, boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor="#3B82F6", lw=1.2)
    ax.add_patch(ans_box)
    ax.text(32, 27.5, "SYNTHESIZED GROUNDED RESPONSE [Agent Synthesizer]:", weight='bold', fontsize=7, color="#1E40AF")
    ax.text(32, 24.5, "1. LangGraph defines cyclic state graphs passing typed AgentState dictionaries across nodes.", fontsize=6.8, color="#0F172A")
    ax.text(32, 21.8, "2. Query Router classifies intent and triggers semantic ChromaDB vector retrieval [Source 1].", fontsize=6.8, color="#0F172A")
    ax.text(32, 19.1, "3. When similarity distance exceeds 0.45, DuckDuckGo executes live web search [Source 2].", fontsize=6.8, color="#0F172A")
    ax.text(32, 16.5, "4. The Evaluator verifies Context Relevance (0.91) and Groundedness (0.94) before final output.", fontsize=6.8, color="#0F172A")

    # Evidence Chunks Accordion (Bottom Left of Main)
    acc1 = patches.FancyBboxPatch((30, 3), 32.5, 11, boxstyle="round,pad=0.2", facecolor="#FFFBEB", edgecolor="#F59E0B")
    ax.add_patch(acc1)
    ax.text(46.25, 11.5, "Retrieved Chunks [ChromaDB]", ha='center', va='center', weight='bold', fontsize=7, color="#92400E")
    ax.text(32, 8.5, "- Chunk ID #104 (dist: 0.28)\n- Chunk ID #219 (dist: 0.34)", fontsize=6.5, color="#78350F")
    ax.text(32, 5, "[Click to expand full passages]", fontsize=6, color="#B45309", fontstyle='italic')

    # RAG Triad Scorecard (Bottom Right of Main)
    acc2 = patches.FancyBboxPatch((65, 3), 32.5, 11, boxstyle="round,pad=0.2", facecolor="#FAF5FF", edgecolor="#8B5CF6")
    ax.add_patch(acc2)
    ax.text(81.25, 11.5, "Automated RAG Triad Scorecard", ha='center', va='center', weight='bold', fontsize=7, color="#5B21B6")
    ax.text(67, 8.5, "Context Rel: 0.91 | Faithfulness: 0.94\nAnswer Rel: 0.93 | Harmonic: 0.926", fontsize=6.5, color="#4C1D95")
    ax.text(67, 5, "Status: PASSED (Zero Hallucination)", fontsize=6, color="#059669", weight='bold')

    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, "fig_5_6_wireframe.png")
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    print("Saved:", out_path)

def draw_fig_6_1():
    """Figure 6.1: Multi-Agent Routing and Retrieval Sequence Flowchart"""
    fig, ax = plt.subplots(figsize=(10, 4.0), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis('off')

    # Sequence lifelines
    lifelines = [
        ("User / UI", 12),
        ("Query Router", 34),
        ("ChromaDB Vector Store", 58),
        ("DuckDuckGo Web Engine", 86)
    ]
    for name, x in lifelines:
        box = patches.FancyBboxPatch((x-9, 43), 18, 5.5, boxstyle="round,pad=0.2", facecolor="#EFF6FF", edgecolor="#2563EB", lw=1.2)
        ax.add_patch(box)
        ax.text(x, 45.7, name, ha='center', va='center', weight='bold', fontsize=7.5, color="#1E3A8A")
        ax.plot([x, x], [4, 43], color="#94A3B8", linestyle="--", lw=1)

    # Messages / interactions
    # 1. User -> Router
    ax.annotate('1. Submit Query String', xy=(34, 38), xytext=(12, 38),
                arrowprops=dict(arrowstyle="->", color="#1E293B", lw=1.2), fontsize=7, color="#0F172A")

    # 2. Router self-classification
    r_act = patches.Rectangle((33, 30), 2, 8, facecolor="#93C5FD", edgecolor="#2563EB")
    ax.add_patch(r_act)
    ax.text(34, 34, "2. Classify Intent:\nVector / Web / Hybrid", ha='center', va='center', fontsize=6.5, color="#1E40AF", weight='bold')

    # 3. Router -> ChromaDB
    ax.annotate('3. Dense Embedding Search (Cosine)', xy=(58, 28), xytext=(35, 28),
                arrowprops=dict(arrowstyle="->", color="#16A34A", lw=1.2), fontsize=7, color="#16A34A")

    # 4. ChromaDB self search
    c_act = patches.Rectangle((57, 21), 2, 7, facecolor="#86EFAC", edgecolor="#16A34A")
    ax.add_patch(c_act)
    ax.text(58, 24.5, "4. Compute Top-4\nCosine Distances", ha='center', va='center', fontsize=6.5, color="#14532D", weight='bold')

    # 5. ChromaDB -> Router
    ax.annotate('5. Return Chunks (dist = 0.28)', xy=(35, 20), xytext=(57, 20),
                arrowprops=dict(arrowstyle="->", color="#16A34A", linestyle="--", lw=1.2), fontsize=7, color="#16A34A")

    # 6. Fallback / Web condition check
    ax.annotate('6. Distance Check: If dist > 0.45 or Temporal -> Trigger Web Search', xy=(86, 14), xytext=(35, 14),
                arrowprops=dict(arrowstyle="->", color="#D97706", lw=1.2), fontsize=7, color="#D97706")

    # 7. DuckDuckGo -> Router
    w_act = patches.Rectangle((85, 8), 2, 6, facecolor="#FDE68A", edgecolor="#D97706")
    ax.add_patch(w_act)
    ax.annotate('7. Return 5 Clean Web Snippets & URLs', xy=(35, 8), xytext=(85, 8),
                arrowprops=dict(arrowstyle="->", color="#D97706", linestyle="--", lw=1.2), fontsize=7, color="#D97706")

    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, "fig_6_1_routing_seq.png")
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    print("Saved:", out_path)

def draw_fig_6_2():
    """Figure 6.2: Multi-Source Context Fusion and Fallback Synthesis Flowchart"""
    fig, ax = plt.subplots(figsize=(10, 4.0), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis('off')

    # Stream A: Vector Chunks
    v_in = patches.FancyBboxPatch((3, 34), 22, 11, boxstyle="round,pad=0.2", facecolor="#EFF6FF", edgecolor="#3B82F6", lw=1.2)
    ax.add_patch(v_in)
    ax.text(14, 41, "ChromaDB Stream", weight='bold', color="#1E3A8A", fontsize=7.5, ha='center')
    ax.text(14, 36.5, "- Dense top-k passages\n- Document ID metadata\n- Similarity distance score", fontsize=6.5, color="#1E293B", ha='center')

    # Stream B: Web Snippets
    w_in = patches.FancyBboxPatch((3, 17), 22, 11, boxstyle="round,pad=0.2", facecolor="#FEF3C7", edgecolor="#D97706", lw=1.2)
    ax.add_patch(w_in)
    ax.text(14, 24, "DuckDuckGo Stream", weight='bold', color="#92400E", fontsize=7.5, ha='center')
    ax.text(14, 19.5, "- Top-5 live web snippets\n- Scraped webpage text\n- Verified source URL links", fontsize=6.5, color="#78350F", ha='center')

    # Merge / Context Harmonization Box
    m_box = patches.FancyBboxPatch((31, 23), 20, 16, boxstyle="round,pad=0.3", facecolor="#F0FDF4", edgecolor="#10B981", lw=1.5)
    ax.add_patch(m_box)
    ax.text(41, 35, "Context Harmonizer", weight='bold', color="#065F46", fontsize=8, ha='center')
    ax.text(41, 30, "- Deduplicate content\n- Map [Doc-X] & [Web-X]\n- Strip boilerplate HTML\n- Truncate to context limit", fontsize=6.5, color="#0F172A", ha='center')

    ax.annotate('', xy=(31, 36), xytext=(25, 39), arrowprops=dict(arrowstyle="->", color="#3B82F6", lw=1.3))
    ax.annotate('', xy=(31, 26), xytext=(25, 23), arrowprops=dict(arrowstyle="->", color="#D97706", lw=1.3))

    # Inference Decision Box
    inf_box = patches.FancyBboxPatch((56, 23), 20, 16, boxstyle="round,pad=0.3", facecolor="#FAF5FF", edgecolor="#8B5CF6", lw=1.5)
    ax.add_patch(inf_box)
    ax.text(66, 35, "Synthesizer Engine", weight='bold', color="#5B21B6", fontsize=8, ha='center')
    ax.text(66, 29, "OpenRouter LLM Prompt\n(System instructions:\nstrict context grounding,\nnumbered in-line citations)", fontsize=6.5, color="#0F172A", ha='center')

    ax.annotate('', xy=(56, 31), xytext=(51, 31), arrowprops=dict(arrowstyle="->", color="#10B981", lw=1.3))

    # Offline Fallback Branch (Bottom)
    fb_box = patches.FancyBboxPatch((56, 4), 20, 12, boxstyle="round,pad=0.2", facecolor="#FFF1F2", edgecolor="#E11D48", lw=1.2, linestyle="--")
    ax.add_patch(fb_box)
    ax.text(66, 12.5, "Deterministic Fallback", weight='bold', color="#9F1239", fontsize=7.5, ha='center')
    ax.text(66, 8, "- Extractive text summarizer\n- Triggered on API timeout\n- Guarantees 100% uptime", fontsize=6.2, color="#881337", ha='center')

    ax.annotate('API Error?', xy=(66, 16), xytext=(66, 23),
                arrowprops=dict(arrowstyle="->", color="#E11D48", linestyle=":", lw=1.2), fontsize=6.5, color="#E11D48", weight='bold', ha='center')

    # Final Output Box
    out_b = patches.FancyBboxPatch((81, 23), 16, 16, boxstyle="round,pad=0.2", facecolor="#EFF6FF", edgecolor="#2563EB", lw=1.5)
    ax.add_patch(out_b)
    ax.text(89, 35, "Grounded Output", weight='bold', color="#1E3A8A", fontsize=7.8, ha='center')
    ax.text(89, 29, "Synthesized markdown\nwith traceable citations:\n[Source 1], [Source 2]", fontsize=6.5, color="#1E293B", ha='center')

    ax.annotate('', xy=(81, 31), xytext=(76, 31), arrowprops=dict(arrowstyle="->", color="#8B5CF6", lw=1.3))
    ax.annotate('', xy=(86, 23), xytext=(76, 10), arrowprops=dict(arrowstyle="->", color="#E11D48", lw=1.2))

    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, "fig_6_2_fusion_flow.png")
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    print("Saved:", out_path)

def draw_fig_8_1():
    """Figure 8.1: LangGraph Multi-Agent Execution State Graph and Decision Flow"""
    fig, ax = plt.subplots(figsize=(10, 4.4), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis('off')

    # Title box
    ax.text(50, 47, "LangGraph StateGraph Multi-Agent Orchestration Flow", ha='center', va='center', weight='bold', color="#1E293B", fontsize=9.5)

    # Start Node
    s_node = patches.Circle((8, 25), 3.5, facecolor="#0F172A", edgecolor="#0F172A")
    ax.add_patch(s_node)
    ax.text(8, 25, "START", ha='center', va='center', weight='bold', color="white", fontsize=6.5)

    # Router Node
    r_node = patches.FancyBboxPatch((18, 19), 14, 12, boxstyle="round,pad=0.2", facecolor="#EFF6FF", edgecolor="#3B82F6", lw=1.5)
    ax.add_patch(r_node)
    ax.text(25, 27, "Router Agent", weight='bold', color="#1E3A8A", fontsize=7.5, ha='center')
    ax.text(25, 22.5, "Evaluate intent\n& complexity", color="#1E293B", fontsize=6.5, ha='center')
    ax.annotate('', xy=(18, 25), xytext=(11.5, 25), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.3))

    # Conditional branching diamonds
    # Branch 1: Retriever (Top)
    ret_node = patches.FancyBboxPatch((42, 34), 16, 11, boxstyle="round,pad=0.2", facecolor="#DCFCE7", edgecolor="#16A34A", lw=1.3)
    ax.add_patch(ret_node)
    ax.text(50, 41, "Retriever Agent", weight='bold', color="#14532D", fontsize=7.5, ha='center')
    ax.text(50, 37, "ChromaDB search\nTop-4 chunks", color="#14532D", fontsize=6.5, ha='center')

    # Branch 2: Web Search (Bottom)
    web_node = patches.FancyBboxPatch((42, 5), 16, 11, boxstyle="round,pad=0.2", facecolor="#FEF3C7", edgecolor="#D97706", lw=1.3)
    ax.add_patch(web_node)
    ax.text(50, 12, "Web Search Agent", weight='bold', color="#92400E", fontsize=7.5, ha='center')
    ax.text(50, 8, "DuckDuckGo scrape\nTop-5 snippets", color="#92400E", fontsize=6.5, ha='center')

    # Connecting arrows from Router
    ax.annotate('', xy=(42, 39.5), xytext=(32, 28), arrowprops=dict(arrowstyle="->", color="#16A34A", lw=1.2))
    ax.text(32, 37, "route == 'vector'", fontsize=6.5, color="#16A34A", weight='bold')

    ax.annotate('', xy=(42, 10.5), xytext=(32, 22), arrowprops=dict(arrowstyle="->", color="#D97706", lw=1.2))
    ax.text(32, 14, "route == 'web'", fontsize=6.5, color="#D97706", weight='bold')

    # Direct LLM bypass arrow (Middle)
    ax.annotate('', xy=(66, 25), xytext=(32, 25), arrowprops=dict(arrowstyle="->", color="#6366F1", lw=1.2, linestyle="--"))
    ax.text(45, 26.5, "route == 'direct'", fontsize=6.5, color="#6366F1", weight='bold')

    # Dynamic promotion / Fallback from Retriever to Web
    ax.annotate('distance > 0.45\n(Low Conf Fallback)', xy=(50, 16), xytext=(50, 34),
                arrowprops=dict(arrowstyle="->", color="#DC2626", linestyle=":", lw=1.3),
                fontsize=6.2, color="#DC2626", weight='bold', ha='center')

    # Synthesizer Node
    syn_node = patches.FancyBboxPatch((66, 19), 15, 12, boxstyle="round,pad=0.2", facecolor="#FAF5FF", edgecolor="#8B5CF6", lw=1.5)
    ax.add_patch(syn_node)
    ax.text(73.5, 27, "Synthesizer Agent", weight='bold', color="#5B21B6", fontsize=7.5, ha='center')
    ax.text(73.5, 22.5, "Fuse multi-source\ncontext & citations", color="#4C1D95", fontsize=6.5, ha='center')

    ax.annotate('', xy=(66, 28), xytext=(58, 39.5), arrowprops=dict(arrowstyle="->", color="#16A34A", lw=1.2))
    ax.annotate('', xy=(66, 22), xytext=(58, 10.5), arrowprops=dict(arrowstyle="->", color="#D97706", lw=1.2))

    # Evaluator Node
    eval_node = patches.FancyBboxPatch((85, 19), 13, 12, boxstyle="round,pad=0.2", facecolor="#EFF6FF", edgecolor="#2563EB", lw=1.5)
    ax.add_patch(eval_node)
    ax.text(91.5, 27, "Triad Evaluator", weight='bold', color="#1E3A8A", fontsize=7.5, ha='center')
    ax.text(91.5, 22.5, "Grade CR, Faith,\nAnswer Relevance", color="#1E3A8A", fontsize=6.5, ha='center')
    ax.annotate('', xy=(85, 25), xytext=(81, 25), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.3))

    # Terminal End Node
    end_node = patches.Circle((95, 8), 3.2, facecolor="white", edgecolor="#0F172A", lw=1.5)
    end_in = patches.Circle((95, 8), 1.8, facecolor="#0F172A", edgecolor="#0F172A")
    ax.add_patch(end_node)
    ax.add_patch(end_in)
    ax.text(95, 3.2, "TERMINAL UI", ha='center', va='center', weight='bold', fontsize=6.5)
    ax.annotate('', xy=(95, 11.2), xytext=(91.5, 19), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.2))

    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, "fig_8_1_stategraph.png")
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    print("Saved:", out_path)

def draw_fig_a_4():
    """Figure A.4: End-to-End System Integration and Deployment Pipeline Flowchart"""
    fig, ax = plt.subplots(figsize=(10, 3.8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis('off')

    steps = [
        ("Step 1: Setup", "Python 3.10+ virtualenv\npip install dependencies\nSetup .env API keys", 11, "#EFF6FF", "#3B82F6"),
        ("Step 2: Ingestion", "Parse PDF / Markdown docs\nRecursive 500-char chunking\nDense MiniLM embeddings", 33, "#ECFDF5", "#10B981"),
        ("Step 3: Vector Store", "Persistent ChromaDB index\nHNSW cosine search cache\nCosine cutoff <= 0.45", 55, "#FEF3C7", "#D97706"),
        ("Step 4: Orchestration", "LangGraph StateGraph engine\nDuckDuckGo web scraper\nOpenRouter multi-model LLM", 77, "#FAF5FF", "#8B5CF6"),
        ("Step 5: Frontend", "Streamlit reactive UI\nReal-time agent badges\nTriad metric scorecards", 94, "#EFF6FF", "#2563EB")
    ]
    for title, desc, x, fc, ec in steps:
        box = patches.FancyBboxPatch((x-6.5, 10), 13, 30, boxstyle="round,pad=0.2", facecolor=fc, edgecolor=ec, lw=1.3)
        ax.add_patch(box)
        ax.text(x, 36, title, weight='bold', color="#0F172A", fontsize=7.5, ha='center')
        ax.text(x, 24, desc, color="#334155", fontsize=6.5, ha='center')

    for i in range(len(steps)-1):
        x1 = steps[i][2] + 6.5
        x2 = steps[i+1][2] - 6.5
        ax.annotate('', xy=(x2, 25), xytext=(x1, 25), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.3))

    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, "fig_a_4_integration.png")
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    print("Saved:", out_path)

if __name__ == "__main__":
    print("Generating additional flowcharts...")
    draw_fig_5_6()
    draw_fig_6_1()
    draw_fig_6_2()
    draw_fig_8_1()
    draw_fig_a_4()
    print("All additional flowcharts generated successfully!")
