"""
Coordinator Agent: Orchestrates the entire multi-agent RAG workflow.
Uses LangGraph StateGraph for structured agent orchestration.
Handles domain detection, complexity estimation, and adaptive agent selection.
"""
import time
from typing import TypedDict, Any
from langgraph.graph import StateGraph, END

from agents.base_agent import get_llm
from agents.retrieval_agent import RetrievalAgent
from agents.verification_agent import VerificationAgent
from agents.agriculture_agent import AgricultureAgent
from agents.finance_agent import FinanceAgent
from agents.energy_agent import EnergyAgent
from agents.healthcare_agent import HealthcareAgent
from agents.education_agent import EducationAgent
from utils.config import (
    DOMAIN_KEYWORDS, DOMAINS, CONFIDENCE_THRESHOLD,
    MAX_RETRIEVAL_ROUNDS, TOP_K,
    COMPLEXITY_WORD_THRESHOLD_MEDIUM, COMPLEXITY_WORD_THRESHOLD_HIGH
)
from utils.confidence import calculate_confidence, get_confidence_label, get_confidence_details


# --- Workflow State Schema ---
class WorkflowState(TypedDict):
    """State that flows through the LangGraph workflow."""
    query: str
    selected_domain: str          # User's domain choice or "auto"
    detected_domains: list        # Detected domain(s)
    complexity: str               # LOW / MEDIUM / HIGH
    agents_activated: list        # Names of agents that ran
    retrieved_docs: list          # Retrieved document chunks
    agent_analyses: dict          # domain_name -> analysis text
    verification_result: dict     # Verification output
    confidence_score: float       # Overall confidence
    confidence_details: dict      # Breakdown of confidence
    retrieval_rounds: int         # Number of retrieval passes
    final_response: str           # Final synthesized response
    workflow_log: list            # Log of workflow steps
    error: str                    # Error message if any
    start_time: float             # For response time tracking
    response_mode: str            # Mode for final output formatting


# --- Domain Detection ---
def detect_domains(query, selected_domain="auto"):
    """
    Detect relevant domains from the query using keyword matching.
    Falls back to LLM classification if no keywords match.
    """
    if selected_domain != "auto" and selected_domain in DOMAINS:
        return [selected_domain]

    query_lower = query.lower()
    domain_scores = {}

    # Score each domain by keyword matches
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in query_lower)
        if score > 0:
            domain_scores[domain] = score

    if not domain_scores:
        # Fallback: use LLM for domain classification
        try:
            llm = get_llm()
            prompt = (
                f"Classify this query into one or more of these domains: "
                f"{', '.join(DOMAINS)}.\n\n"
                f"Query: \"{query}\"\n\n"
                f"Return ONLY the domain name(s), comma-separated. "
                f"Choose the single most relevant domain if unsure."
            )
            response = llm.generate_content(prompt)
            detected = [d.strip().lower() for d in response.text.strip().split(",")]
            detected = [d for d in detected if d in DOMAINS]
            if detected:
                return detected
        except Exception as e:
            print(f"LLM domain detection failed: {e}")
        # Ultimate fallback
        return ["education"]

    # Return domains sorted by score
    sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)

    # Include domains with at least 50% of the top score
    top_score = sorted_domains[0][1]
    relevant = [d for d, s in sorted_domains if s >= top_score * 0.5]

    return relevant


# --- Complexity Estimation ---
def estimate_complexity(query, num_domains):
    """
    Estimate query complexity based on length, keywords, and domain count.
    """
    # Multi-domain queries are automatically HIGH
    if num_domains >= 2:
        return "HIGH"

    word_count = len(query.split())

    # Check for complexity-indicating phrases
    complex_indicators = [
        "should", "compare", "versus", "trade-off", "considering",
        "evaluate", "analyze", "impact", "effect", "relationship",
        "advantages and disadvantages", "pros and cons", "factors",
        "how does", "what are the implications", "recommend",
        "advantages", "limitations", "challenges", "benefits",
        "strategies", "considered", "planning"
    ]
    complexity_hits = sum(1 for ind in complex_indicators if ind in query.lower())

    if word_count > COMPLEXITY_WORD_THRESHOLD_HIGH or complexity_hits >= 2:
        return "HIGH"
    elif word_count > COMPLEXITY_WORD_THRESHOLD_MEDIUM or complexity_hits >= 1:
        return "MEDIUM"
    else:
        return "LOW"


# --- Domain Agent Registry ---
DOMAIN_AGENTS = {
    "agriculture": AgricultureAgent,
    "finance": FinanceAgent,
    "energy": EnergyAgent,
    "healthcare": HealthcareAgent,
    "education": EducationAgent,
}


# --- LangGraph Node Functions ---

def classify_node(state: WorkflowState) -> dict:
    """Node 1: Detect domain and estimate complexity."""
    query = state["query"]
    selected = state.get("selected_domain", "auto")

    detected = detect_domains(query, selected)
    complexity = estimate_complexity(query, len(detected))

    log = [
        f"Domain Detection: {', '.join(detected)}",
        f"Complexity Level: {complexity}"
    ]

    return {
        "detected_domains": detected,
        "complexity": complexity,
        "workflow_log": state.get("workflow_log", []) + log,
        "agents_activated": ["Coordinator Agent"]
    }


def retrieve_node(state: WorkflowState) -> dict:
    """Node 2: Retrieve relevant documents from vector store."""
    retrieval_agent = RetrievalAgent()
    docs = retrieval_agent.run(
        state["query"],
        state["detected_domains"],
        top_k=TOP_K
    )

    rounds = state.get("retrieval_rounds", 0) + 1
    agents = state.get("agents_activated", []) + ["Retrieval Agent"]
    log_entry = f"Retrieval Round {rounds}: Found {len(docs)} relevant chunks"

    return {
        "retrieved_docs": docs,
        "retrieval_rounds": rounds,
        "agents_activated": agents,
        "workflow_log": state.get("workflow_log", []) + [log_entry]
    }


def analyze_node(state: WorkflowState) -> dict:
    """Node 3: Run domain-specific agent(s) on retrieved evidence."""
    analyses = {}
    agents = list(state.get("agents_activated", []))
    log_entries = []

    for domain in state["detected_domains"]:
        if domain in DOMAIN_AGENTS:
            agent = DOMAIN_AGENTS[domain]()
            analysis = agent.analyze(state["query"], state["retrieved_docs"])
            analyses[domain] = analysis
            agent_name = f"{domain.title()} Agent"
            agents.append(agent_name)
            log_entries.append(f"Activated {agent_name}")

    return {
        "agent_analyses": analyses,
        "agents_activated": agents,
        "workflow_log": state.get("workflow_log", []) + log_entries
    }


def verify_node(state: WorkflowState) -> dict:
    """Node 4: Verify analysis claims against evidence."""
    verification_agent = VerificationAgent()

    # Combine all analyses for verification
    combined_analysis = "\n\n".join(
        f"--- {domain.title()} Analysis ---\n{text}"
        for domain, text in state.get("agent_analyses", {}).items()
    )

    result = verification_agent.verify(
        state["query"],
        combined_analysis,
        state["retrieved_docs"]
    )

    agents = list(state.get("agents_activated", [])) + ["Verification Agent"]
    log_entry = f"Verification: {result.get('status', 'Unknown')} (Score: {result.get('score', 0)})"

    return {
        "verification_result": result,
        "agents_activated": agents,
        "workflow_log": state.get("workflow_log", []) + [log_entry]
    }


def evaluate_confidence_node(state: WorkflowState) -> dict:
    """Node 5: Calculate confidence and decide whether to loop."""
    # Gather retrieval scores
    retrieval_scores = [doc.get("score", 0) for doc in state.get("retrieved_docs", [])]
    source_count = len(state.get("retrieved_docs", []))

    # Agent agreement: 1.0 for single agent, check overlap for multiple
    analyses = state.get("agent_analyses", {})
    if len(analyses) <= 1:
        agent_agreement = 1.0
    else:
        # Simple heuristic: check if analyses are roughly the same length
        # and share key terms (simplified for college project)
        agent_agreement = 0.8  # Default reasonable agreement for multi-agent

    verification_score = state.get("verification_result", {}).get("score", 0.5)

    confidence = calculate_confidence(
        retrieval_scores, source_count, agent_agreement, verification_score
    )
    details = get_confidence_details(
        retrieval_scores, source_count, agent_agreement, verification_score
    )
    label = get_confidence_label(confidence)

    log_entry = f"Confidence: {confidence} ({label})"

    return {
        "confidence_score": confidence,
        "confidence_details": details,
        "workflow_log": state.get("workflow_log", []) + [log_entry]
    }


def finalize_node(state: WorkflowState) -> dict:
    """Node 6: Generate the final structured response."""
    llm = get_llm()

    # Combine analyses
    analyses_text = "\n\n".join(
        f"### {domain.title()} Analysis:\n{text}"
        for domain, text in state.get("agent_analyses", {}).items()
    )

    # Format sources
    sources = []
    seen = set()
    for doc in state.get("retrieved_docs", []):
        src = doc.get("source", "Unknown")
        if src not in seen:
            sources.append(src)
            seen.add(src)

    verification = state.get("verification_result", {})
    confidence_label = get_confidence_label(state.get("confidence_score", 0))

    prompt = f"""Based on the following domain-specific analyses, generate a final comprehensive response for the user.

USER QUERY: {state['query']}
RESPONSE MODE: {state.get('response_mode', 'Learn From Basics')}
DETECTED DOMAINS: {', '.join(state.get('detected_domains', []))}

DOMAIN ANALYSES:
{analyses_text}

VERIFICATION STATUS: {verification.get('status', 'Not performed')}

INSTRUCTIONS:
You MUST structure your response exactly based on the RESPONSE MODE below. Use markdown formatting with exact headers (e.g., ### ANSWER). Do not output anything outside these sections.

If RESPONSE MODE is 'Quick Answer':
### ANSWER
(A short, 1-2 sentence direct answer)
### KEY POINTS
(2-5 concise bullet points)
### YOU MAY ALSO WANT TO KNOW
(Generate 3-4 related follow-up questions)

If RESPONSE MODE is 'Learn From Basics' (Default) or 'Detailed Analysis':
### ANSWER
(A direct, prominent answer to the user's question. Clear and concise.)
### UNDERSTAND IT SIMPLY
(Explain the topic in simple language as if the user is learning it for the first time. Explain technical terms inline if needed.)
### HOW IT WORKS
(A simple visual sequence using arrows, e.g., Soil -> Water -> Climate -> Crop Selection)
### KEY POINTS
(The most important points in a clean bulleted list.)
### DECISION GUIDE
(Practical factors the person should consider before making a decision. Numbered list.)
### ADVANTAGES
(Evidence-supported benefits. If none, write 'N/A')
### LIMITATIONS / RISKS
(Important limitations, uncertainties, or risks. Do not fabricate.)
### KEY TERMS
(Explain 2-3 important terminologies relevant to the query. e.g., Term: Definition)
### WHY THESE AGENTS
(Briefly explain why the specific agents were chosen for this query.)
### YOU MAY ALSO WANT TO KNOW
(Generate 3-4 related follow-up questions starting with arrows ->)

Rules for all modes:
- Base your answer ONLY on the provided domain analyses and retrieved evidence.
- If this involves healthcare, include a medical disclaimer at the very end of DECISION GUIDE.
- Be clear, practical, and actionable. Do not use placeholder text.
"""

    try:
        response = llm.generate_content(prompt)
        final = response.text
    except Exception as e:
        final = f"Error generating final response: {str(e)}\n\nRaw analyses:\n{analyses_text}"

    elapsed = time.time() - state.get("start_time", time.time())
    log_entry = f"Final response generated in {elapsed:.1f}s"

    return {
        "final_response": final,
        "workflow_log": state.get("workflow_log", []) + [log_entry]
    }


# --- Routing Functions ---

def route_after_analyze(state: WorkflowState) -> str:
    """Decide whether to verify or skip to finalize based on complexity."""
    complexity = state.get("complexity", "LOW")
    if complexity in ("MEDIUM", "HIGH"):
        return "verify"
    else:
        return "finalize"


def route_after_confidence(state: WorkflowState) -> str:
    """Decide whether to re-retrieve or finalize based on confidence."""
    confidence = state.get("confidence_score", 1.0)
    rounds = state.get("retrieval_rounds", 1)

    if confidence < CONFIDENCE_THRESHOLD and rounds < MAX_RETRIEVAL_ROUNDS:
        return "re_retrieve"
    else:
        return "finalize"


# --- Build LangGraph Workflow ---

def build_workflow():
    """Construct the LangGraph StateGraph for the multi-agent workflow."""
    workflow = StateGraph(WorkflowState)

    # Add nodes
    workflow.add_node("classify", classify_node)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("verify", verify_node)
    workflow.add_node("evaluate_confidence", evaluate_confidence_node)
    workflow.add_node("re_retrieve", retrieve_node)  # Reuses retrieve logic
    workflow.add_node("finalize", finalize_node)

    # Define edges
    workflow.set_entry_point("classify")
    workflow.add_edge("classify", "retrieve")
    workflow.add_edge("retrieve", "analyze")

    # After analyze: verify if MEDIUM/HIGH, else finalize
    workflow.add_conditional_edges(
        "analyze",
        route_after_analyze,
        {"verify": "verify", "finalize": "finalize"}
    )

    # After verify: evaluate confidence
    workflow.add_edge("verify", "evaluate_confidence")

    # After confidence check: re-retrieve if low, else finalize
    workflow.add_conditional_edges(
        "evaluate_confidence",
        route_after_confidence,
        {"re_retrieve": "re_retrieve", "finalize": "finalize"}
    )

    # After re-retrieve: go back to analyze
    workflow.add_edge("re_retrieve", "analyze")

    # Finalize ends the workflow
    workflow.add_edge("finalize", END)

    return workflow.compile()


# --- Main Entry Point ---

def run_workflow(query, selected_domain="auto", response_mode="Learn From Basics"):
    """
    Run the complete multi-agent RAG workflow.

    Args:
        query: User's natural language query.
        selected_domain: User's domain choice or 'auto' for detection.
        response_mode: Desired detail level for output.

    Returns:
        Final WorkflowState dict with all results.
    """
    # Initialize state
    initial_state = {
        "query": query,
        "selected_domain": selected_domain,
        "detected_domains": [],
        "complexity": "LOW",
        "agents_activated": [],
        "retrieved_docs": [],
        "agent_analyses": {},
        "verification_result": {},
        "confidence_score": 0.0,
        "confidence_details": {},
        "retrieval_rounds": 0,
        "final_response": "",
        "workflow_log": [],
        "error": "",
        "start_time": time.time(),
        "response_mode": response_mode
    }

    try:
        app = build_workflow()
        result = app.invoke(initial_state)
        return result
    except Exception as e:
        initial_state["error"] = str(e)
        initial_state["final_response"] = f"An error occurred: {str(e)}"
        initial_state["workflow_log"].append(f"ERROR: {str(e)}")
        return initial_state
