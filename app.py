"""
Streamlit UI for the Self-Adaptive Multi-Agent RAG Framework.
Provides an interactive interface for querying the decision support system.
"""
import streamlit as st
import time
import os
import sys

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.coordinator import run_workflow
from rag.vector_store import ingest_all, get_collection_stats
from utils.config import DOMAINS, CONFIDENCE_THRESHOLD, DATA_DIR, AVAILABLE_MODELS
from utils.confidence import get_confidence_label
from rag.vector_store import ingest_domain


# --- Page Configuration ---
st.set_page_config(
    page_title="Multi-Agent RAG Decision Support",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


def init_session_state():
    """Initialize Streamlit session state variables."""
    if "result" not in st.session_state:
        st.session_state.result = None
    if "ingested" not in st.session_state:
        st.session_state.ingested = False
    if "api_key_valid" not in st.session_state:
        st.session_state["api_key_valid"] = None   # None = not yet tested
    if "api_key_error" not in st.session_state:
        st.session_state["api_key_error"] = ""


def render_sidebar():
    """Render the sidebar with project info and controls."""
    with st.sidebar:
        st.title("⚙️ Settings")

        # --- OpenRouter API Key ---
        st.markdown("**🔑 OpenRouter API Key**")
        st.caption("Free models available. Get your key at [openrouter.ai](https://openrouter.ai/keys)")
        or_key = st.text_input(
            "API Key",
            type="password",
            value=os.getenv("OPENROUTER_API_KEY", ""),
            key="or_key_input",
            placeholder="sk-or-v1-...",
            label_visibility="collapsed"
        )
        if or_key:
            os.environ["OPENROUTER_API_KEY"] = or_key

        if st.button("✅ Validate & Connect", use_container_width=True, key="or_validate"):
            if not or_key:
                st.error("Enter your OpenRouter key first.")
            else:
                # Always validate against openrouter/free — never a paid model
                # This ensures the key check works regardless of which model is selected
                with st.spinner("Validating key with openrouter/free..."):
                    try:
                        from openai import OpenAI as _OAI
                        _c = _OAI(api_key=or_key, base_url="https://openrouter.ai/api/v1")
                        _r = _c.chat.completions.create(
                            model="openrouter/free",
                            messages=[{"role": "user", "content": "Reply with just: OK"}],
                            extra_headers={"HTTP-Referer": "http://localhost:8501", "X-Title": "Multi-Agent RAG"}
                        )
                        if _r.choices:
                            st.session_state["api_key_valid"] = True
                            active = os.getenv("ACTIVE_LLM_MODEL", "openrouter/free")
                            st.success(f"✅ Key valid! Using model: {active}")
                        else:
                            st.session_state["api_key_valid"] = False
                            st.error("No response received.")
                    except Exception as _e:
                        st.session_state["api_key_valid"] = False
                        err = str(_e)
                        if "401" in err or "User not found" in err or "invalid" in err.lower():
                            st.error("❌ Invalid API key — please get a fresh key from openrouter.ai/keys")
                        else:
                            st.error(f"❌ {err[:200]}")

        # Status badge
        if st.session_state.get("api_key_valid"):
            active_model = os.getenv("ACTIVE_LLM_MODEL", "openrouter/free")
            st.success(f"⚡ Connected — {active_model}")
        elif or_key and st.session_state.get("api_key_valid") is False:
            st.error("⚠️ Key invalid or model unavailable")
        elif or_key:
            st.info("🔶 Key entered — click Validate & Connect")

        st.divider()

        # --- Model selector ---
        st.markdown("**🧠 Model**")
        current_model = os.getenv("ACTIVE_LLM_MODEL", "openrouter/free")
        model_index = AVAILABLE_MODELS.index(current_model) if current_model in AVAILABLE_MODELS else 0
        selected_model = st.selectbox(
            "Select model",
            AVAILABLE_MODELS,
            index=model_index,
            label_visibility="collapsed"
        )
        os.environ["ACTIVE_LLM_MODEL"] = selected_model

        model_descriptions = {
            "openrouter/free":                        "🆓 Free Router — auto-picks best free model (recommended)",
            "google/gemma-4-31b-it:free":             "🆓 Gemma 4 31B — Google's latest open model (free)",
            "qwen/qwen3.8-27b:free":                  "🆓 Qwen 3.8 27B — Alibaba's flagship open model (free)",
            "nvidia/nemotron-3.5-lightning:free":     "🆓 Nemotron 3.5 Lightning — NVIDIA fast model (free)",
            "z-ai/glm-5.2:free":                      "🆓 GLM 5.2 — High performance open model (free)",
            "openai/gpt-4o-mini":                     "⚡ GPT-4o Mini — Fast & affordable (paid key required)",
            "openai/gpt-4o":                          "🏆 GPT-4o — Most capable flagship (paid key required)",
            "google/gemma-3-27b-it":                  "💎 Gemma 3 27B Paid — Full rate limit (paid key required)",
        }
        st.caption(model_descriptions.get(selected_model, ""))

        st.divider()

        # Domain selector
        domain_options = ["Auto Detect"] + [d.title() for d in DOMAINS]
        selected = st.selectbox("Domain", domain_options, index=0)
        selected_domain = "auto" if selected == "Auto Detect" else selected.lower()

        st.divider()

        # Knowledge base management
        st.subheader("📚 Knowledge Base")
        stats = get_collection_stats()
        for domain, count in stats.items():
            status = "✅" if count > 0 else "❌"
            st.text(f"{status} {domain.title()}: {count} chunks")

        if st.button("🔄 Ingest/Refresh Documents", use_container_width=True):
            with st.spinner("Ingesting documents from data/ folder..."):
                total = ingest_all()
                st.session_state.ingested = True
                st.success(f"Ingested {total} total chunks!")
                st.rerun()

        st.divider()

        # Custom Document Upload
        st.subheader("📄 Upload Document")
        upload_domain = st.selectbox("Assign to Domain:", [d.title() for d in DOMAINS], index=0)
        uploaded_file = st.file_uploader("Upload PDF or TXT", type=['pdf', 'txt'])
        
        if uploaded_file is not None:
            if st.button("Upload and Ingest", type="primary", use_container_width=True):
                with st.spinner(f"Ingesting into {upload_domain}..."):
                    domain_lower = upload_domain.lower()
                    save_path = os.path.join(DATA_DIR, domain_lower, uploaded_file.name)
                    
                    with open(save_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Re-ingest the targeted domain to include the new file
                    ingest_domain(domain_lower)
                    
                    st.success(f"Successfully added '{uploaded_file.name}' to {upload_domain}!")
                    time.sleep(1.5)
                    st.rerun()

        st.divider()

        # Response Mode selector
        st.subheader("🎛️ Response Mode")
        response_mode = st.radio(
            "Detail Level:",
            ["Quick Answer", "Learn From Basics", "Detailed Analysis"],
            index=1,
            label_visibility="collapsed"
        )
        st.divider()

        # Project info
        st.subheader("ℹ️ About")
        st.markdown("""
        **Self-Adaptive Multi-Agent RAG Framework**

        An intelligent decision support system using:
        - 🔍 RAG (Retrieval-Augmented Generation)
        - 🤖 Multiple Specialized AI Agents
        - 🧠 Adaptive Coordination
        - ✅ Evidence Verification

        **Domains:** Agriculture, Finance, Energy, Healthcare, Education
        """)

        st.divider()
        st.caption("Confidence Threshold: " + str(CONFIDENCE_THRESHOLD))

    return selected_domain, response_mode


import re

def parse_response(response_text):
    """
    Robustly parse LLM markdown response into structured sections.
    Handles: ### HEADER, ## HEADER, **HEADER**, HEADER: patterns from any LLM.
    Falls back to returning the full text under ANSWER if no sections detected.
    """
    if not response_text or not response_text.strip():
        return {}

    sections = {}
    # Try splitting on any heading level (##, ###, ####)
    parts = re.split(r'\n(?=#{1,4}\s)', response_text.strip())

    if len(parts) > 1:
        for part in parts:
            part = part.strip()
            if not part:
                continue
            # Extract heading and body
            m = re.match(r'^#{1,4}\s+(.+?)$', part, re.MULTILINE)
            if m:
                title = m.group(1).strip().rstrip(':').upper()
                body = part[m.end():].strip()
                sections[title] = body
        if sections:
            return sections

    # Fallback: split on **BOLD HEADER** lines
    parts = re.split(r'\n(?=\*\*[A-Z][A-Z /]+\*\*)', response_text.strip())
    if len(parts) > 1:
        for part in parts:
            part = part.strip()
            m = re.match(r'^\*\*([A-Z][A-Z /]+)\*\*', part)
            if m:
                title = m.group(1).strip().rstrip(':').upper()
                body = part[m.end():].strip().lstrip(':').strip()
                sections[title] = body
        if sections:
            return sections

    # Last resort: put entire text under ANSWER
    sections["ANSWER"] = response_text.strip()
    return sections


def render_results(result):
    """Render results in Google AI Overview style — answer-first, rich and readable."""
    if not result:
        return
    if result.get("error"):
        st.error(f"Error: {result['error']}")
        return

    raw_response = result.get("final_response", "")
    sections = parse_response(raw_response)
    domains = result.get("detected_domains", [])
    docs    = result.get("retrieved_docs", [])

    # ── CSS ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    .ai-overview-box {
        background: linear-gradient(135deg, #f0f7ff 0%, #e8f4fd 100%);
        border: 1px solid #bfdbfe;
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow: 0 2px 12px rgba(59,130,246,0.08);
    }
    .ai-overview-label {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.78rem;
        font-weight: 700;
        color: #1d4ed8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 14px;
    }
    .ai-overview-answer {
        font-size: 1.15rem;
        line-height: 1.75;
        color: #1e293b;
    }
    .section-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 22px 26px;
        margin-bottom: 18px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .section-label {
        font-size: 0.72rem;
        font-weight: 800;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 12px;
    }
    .green-card {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 18px;
    }
    .red-card {
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 18px;
    }
    .source-pill {
        display: inline-block;
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 20px;
        padding: 3px 10px;
        font-size: 0.72rem;
        color: #1d4ed8;
        margin: 2px 4px 2px 0;
    }
    .source-receipt {
        border-left: 3px solid #f59e0b;
        background: #fffbeb;
        padding: 12px 16px;
        border-radius: 0 10px 10px 0;
        margin-bottom: 10px;
        font-size: 0.88rem;
        color: #374151;
    }
    .query-title {
        font-family: Google Sans, Roboto, sans-serif;
        font-size: 1.9rem;
        font-weight: 600;
        color: #111827;
        line-height: 1.25;
        margin-bottom: 6px;
    }
    .domain-chip {
        display: inline-block;
        background: #dbeafe;
        color: #1e40af;
        border-radius: 20px;
        padding: 2px 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Query title ──────────────────────────────────────────────────────────
    query = st.session_state.get("current_query", "Analysis")
    for d in domains:
        st.markdown(f"<span class='domain-chip'>🏷 {d.title()}</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='query-title'>{query}</div>", unsafe_allow_html=True)
    st.write("")

    # ── 1. AI OVERVIEW BOX (main answer) ─────────────────────────────────────
    # Try multiple possible section names GPT-4o or other LLMs may use
    answer_text = (
        sections.get("ANSWER")
        or sections.get("DIRECT ANSWER")
        or sections.get("OVERVIEW")
        or sections.get("SUMMARY")
        or sections.get("RESPONSE")
        or ""
    )

    if not answer_text and raw_response:
        # If no sections parsed at all, show the raw response directly
        answer_text = raw_response

    if answer_text:
        st.markdown(f"""
        <div class="ai-overview-box">
            <div class="ai-overview-label">🤖 AI Overview</div>
            <div class="ai-overview-answer">{answer_text.replace(chr(10), '<br>')}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── 2. UNDERSTAND IT SIMPLY ──────────────────────────────────────────────
    simple = (sections.get("UNDERSTAND IT SIMPLY")
              or sections.get("SIMPLE EXPLANATION")
              or sections.get("IN SIMPLE TERMS"))
    if simple:
        st.markdown("""<div class="section-card">
            <div class="section-label">💡 Understand It Simply</div>""", unsafe_allow_html=True)
        st.markdown(simple)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── 3. HOW IT WORKS ──────────────────────────────────────────────────────
    how = sections.get("HOW IT WORKS") or sections.get("HOW THIS WORKS")
    if how:
        st.info(f"**⚙️ How It Works**\n\n{how}")

    # ── 4. KEY POINTS + DECISION GUIDE side-by-side ─────────────────────────
    key_pts = sections.get("KEY POINTS") or sections.get("KEY TAKEAWAYS") or sections.get("MAIN POINTS")
    dec_guide = sections.get("DECISION GUIDE") or sections.get("WHAT TO CONSIDER") or sections.get("CONSIDERATIONS")

    if key_pts or dec_guide:
        col_a, col_b = st.columns(2, gap="large")
        with col_a:
            if key_pts:
                st.markdown("<div class='section-card'><div class='section-label'>📌 Key Points</div>", unsafe_allow_html=True)
                st.markdown(key_pts)
                st.markdown("</div>", unsafe_allow_html=True)
        with col_b:
            if dec_guide:
                st.markdown("<div class='section-card'><div class='section-label'>🧭 Decision Guide</div>", unsafe_allow_html=True)
                st.markdown(dec_guide)
                st.markdown("</div>", unsafe_allow_html=True)

    # ── 5. ADVANTAGES + LIMITATIONS ─────────────────────────────────────────
    adv  = sections.get("ADVANTAGES") or sections.get("BENEFITS") or sections.get("PROS")
    lim  = (sections.get("LIMITATIONS / RISKS")
            or sections.get("LIMITATIONS")
            or sections.get("RISKS")
            or sections.get("CONS")
            or sections.get("DISADVANTAGES"))

    if adv or lim:
        col_c, col_d = st.columns(2, gap="large")
        with col_c:
            if adv:
                st.markdown(f"""
                <div class="green-card">
                    <div class="section-label" style="color:#166534;">✅ Advantages</div>
                    {adv.replace(chr(10), '<br>')}
                </div>""", unsafe_allow_html=True)
        with col_d:
            if lim:
                st.markdown(f"""
                <div class="red-card">
                    <div class="section-label" style="color:#991b1b;">⚠️ Limitations / Risks</div>
                    {lim.replace(chr(10), '<br>')}
                </div>""", unsafe_allow_html=True)

    # ── 6. Render ALL remaining sections we haven't shown yet ─────────────────
    shown_keys = {
        "ANSWER","DIRECT ANSWER","OVERVIEW","SUMMARY","RESPONSE",
        "UNDERSTAND IT SIMPLY","SIMPLE EXPLANATION","IN SIMPLE TERMS",
        "HOW IT WORKS","HOW THIS WORKS",
        "KEY POINTS","KEY TAKEAWAYS","MAIN POINTS",
        "DECISION GUIDE","WHAT TO CONSIDER","CONSIDERATIONS",
        "ADVANTAGES","BENEFITS","PROS",
        "LIMITATIONS / RISKS","LIMITATIONS","RISKS","CONS","DISADVANTAGES",
        "YOU MAY ALSO WANT TO KNOW","WHY THESE AGENTS"
    }
    extra = {k: v for k, v in sections.items() if k not in shown_keys and v.strip()}
    if extra:
        for title, content in extra.items():
            with st.expander(f"📖 {title.title()}", expanded=False):
                st.markdown(content)

    # ── 7. SOURCES (receipt style) ────────────────────────────────────────────
    st.divider()
    st.markdown("<div class='section-label'>📚 Sources & Evidence</div>", unsafe_allow_html=True)
    if docs:
        for doc in docs[:4]:
            src     = doc.get("source", "Unknown")
            domain  = doc.get("domain", "")
            page    = doc.get("page", "N/A")
            snippet = doc.get("content", "")[:220].replace('\n', ' ') + "…"
            score   = doc.get("score", 0)
            st.markdown(f"""
            <div class="source-receipt">
                <b>📄 {src}</b> &nbsp;
                <span class="source-pill">Page {page}</span>
                <span class="source-pill">{domain.title()}</span>
                <span class="source-pill">Relevance {score:.0%}</span><br>
                <span style="font-style:italic;color:#4b5563;">"{snippet}"</span>
            </div>""", unsafe_allow_html=True)
        if len(docs) > 4:
            with st.expander(f"Show all {len(docs)} sources"):
                for doc in docs[4:]:
                    st.markdown(f"- **{doc.get('source')}** (p.{doc.get('page')}) — {doc.get('content','')[:120]}…")
    else:
        st.info("No local documents retrieved. Answer generated from model knowledge.")

    # ── 8. CONFIDENCE bar ────────────────────────────────────────────────────
    confidence = result.get("confidence_score", 0)
    if confidence:
        pct = int(confidence * 100)
        label = get_confidence_label(confidence)
        col_conf, col_ver = st.columns(2)
        with col_conf:
            st.markdown(f"**Evidence Confidence:** {pct}% — {label}")
            st.progress(confidence)
        with col_ver:
            vr = result.get("verification_result", {})
            st.markdown(f"**Verification:** {vr.get('status', 'N/A')}")
            if vr.get("summary"):
                st.caption(vr["summary"])

    # ── 9. Technical details (collapsed) ─────────────────────────────────────
    with st.expander("🔧 How the AI handled this query", expanded=False):
        st.markdown(f"- **Domain(s):** {', '.join([d.title() for d in domains])}")
        st.markdown(f"- **Complexity:** {result.get('complexity','N/A')}")
        st.markdown(f"- **Agents:** {', '.join(set(result.get('agents_activated',[])))}")
        st.markdown(f"- **Retrieval rounds:** {result.get('retrieval_rounds',0)}")
        model_used = os.getenv("ACTIVE_LLM_MODEL","openrouter/free")
        st.markdown(f"- **Model:** {model_used}")
        why = sections.get("WHY THESE AGENTS")
        if why:
            st.markdown(f"- **Why these agents:** {why[:300]}")

    # ── 10. Follow-up questions ──────────────────────────────────────────────
    st.divider()
    follow_section = sections.get("YOU MAY ALSO WANT TO KNOW") or ""
    follow_lines = [l.strip().lstrip("->→•- ").strip()
                    for l in follow_section.split('\n')
                    if l.strip() and len(l.strip()) > 10]

    quick_follows = ["Explain this simply", "Give me an example",
                     "What are the risks?", "Compare alternatives"]
    all_follows = (follow_lines[:4] if follow_lines else quick_follows)

    st.markdown("<div class='section-label'>💬 You may also want to know</div>", unsafe_allow_html=True)
    cols = st.columns(len(all_follows))
    for text, col in zip(all_follows, cols):
        with col:
            if st.button(f"→ {text[:45]}", use_container_width=True, key=f"fu_{hash(text)}"):
                st.session_state["current_query"] = f"Regarding '{query}': {text}"
                st.session_state["result"] = None
                st.rerun()

    st.write("")
    follow_up = st.text_input("Ask a follow-up question:", placeholder="Type here and press Enter…", key="follow_input")
    if follow_up:
        st.session_state["current_query"] = f"Regarding '{query}': {follow_up}"
        st.session_state["result"] = None
        st.rerun()




def main():
    """Main Streamlit application."""
    init_session_state()

    # --- Header ---
    st.title("🤖 Self-Adaptive Multi-Agent RAG Framework")
    st.markdown(
        "*Intelligent Decision Support Across Agriculture, Finance, "
        "Energy, Healthcare, and Education*"
    )
    st.markdown(
        "Enter a question below. The system will automatically detect the domain, "
        "assess complexity, select appropriate AI agents, retrieve relevant evidence, "
        "verify claims, and provide an evidence-grounded response."
    )

    # --- Sidebar ---
    selected_domain, response_mode = render_sidebar()

    # --- Check if documents are ingested ---
    stats = get_collection_stats()
    total_docs = sum(stats.values())
    if total_docs == 0:
        st.warning(
            "⚠️ No documents found in the knowledge base. "
            "Click **'Ingest/Refresh Documents'** in the sidebar to load documents from the `data/` folder."
        )

    # --- Demo Examples ---
    with st.expander("📝 Try a Demo Query", expanded=False):
        demo_queries = [
            "What factors should be considered before choosing a crop?",
            "What factors should be considered when evaluating investment risk?",
            "What are the advantages and limitations of solar energy?",
            "What are common causes of iron deficiency?",
            "How can a student create a study plan for an upcoming examination?",
            "Should a manufacturing company consider solar energy based on its energy requirements and financial constraints?"
        ]
        for dq in demo_queries:
            if st.button(dq, key=f"demo_{hash(dq)}", use_container_width=True):
                st.session_state["current_query"] = dq
                st.rerun()

    # --- Query Input ---
    st.subheader("💬 Your Query")
    default_query = st.session_state.get("current_query", "")
    query = st.text_area(
        "Enter your question:",
        value=default_query,
        placeholder="e.g., What factors should be considered before choosing a crop?",
        height=100,
        label_visibility="collapsed"
    )
    # Sync back to session state
    if query != default_query:
        st.session_state["current_query"] = query

    # --- Analyze Button ---
    col1, col2 = st.columns([1, 5])
    with col1:
        analyze_clicked = st.button("🔍 Analyze", type="primary", use_container_width=True)

    if analyze_clicked and query.strip():
        # Warn if no API key has been validated
        if not st.session_state.get("api_key_valid") and not os.getenv("OPENROUTER_API_KEY"):
            st.warning(
                "⚠️ **No OpenRouter API key detected.** Running in local knowledge synthesis mode. "
                "To get live AI-powered answers, enter your key in the sidebar and click **Validate & Connect**. "
                "Get a key at [openrouter.ai](https://openrouter.ai/keys)."
            )

        with st.spinner("🤖 Analyzing your query... This may take a moment."):
            start_time = time.time()
            try:
                result = run_workflow(query.strip(), selected_domain, response_mode)
                elapsed = time.time() - start_time
                st.session_state.result = result
                st.success(f"Analysis complete in {elapsed:.1f} seconds!")
            except RuntimeError as e:
                err_msg = str(e)
                if "LLM_API_KEY_INVALID" in err_msg:
                    st.session_state["api_key_valid"] = False
                    st.error(
                        "❌ **Invalid OpenRouter API Key.**\n\n"
                        "Your key was rejected by OpenRouter. Please:\n"
                        "1. Open the **⚙️ Settings** sidebar\n"
                        "2. Enter a working key from [openrouter.ai/keys](https://openrouter.ai/keys)\n"
                        "3. Click **Validate & Connect** to verify it\n"
                        "4. Run your query again"
                    )
                elif "LLM_QUOTA_EXCEEDED" in err_msg:
                    st.error("⚠️ **Quota / Rate Limit Exceeded.** Try switching models or wait a moment.")
                elif "LLM_MODEL_NOT_FOUND" in err_msg:
                    st.error(
                        f"❌ **Model Not Found.**\n\n{err_msg.split(':', 1)[-1].strip()}"
                    )
                else:
                    st.error(f"❌ Error: {err_msg}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")

    elif analyze_clicked and not query.strip():
        st.warning("Please enter a query first.")

    # --- Display Results ---
    if st.session_state.result:
        st.divider()
        render_results(st.session_state.result)


if __name__ == "__main__":
    main()
