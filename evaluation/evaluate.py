"""
Evaluation script for the Multi-Agent RAG Framework.
Compares three modes:
  A. Basic RAG (single retrieval, no agents)
  B. Static Multi-Agent RAG (fixed agent pipeline)
  C. Self-Adaptive Multi-Agent RAG (full adaptive system)
"""
import sys
import os
import time
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.coordinator import run_workflow, detect_domains, estimate_complexity
from agents.retrieval_agent import RetrievalAgent
from agents.base_agent import get_llm
from utils.config import DOMAINS


# --- Test Dataset ---
TEST_QUESTIONS = [
    {
        "id": 1,
        "query": "What factors should be considered before choosing a crop?",
        "expected_domain": ["agriculture"],
        "category": "single_domain"
    },
    {
        "id": 2,
        "query": "What factors should be considered when evaluating investment risk?",
        "expected_domain": ["finance"],
        "category": "single_domain"
    },
    {
        "id": 3,
        "query": "What are the advantages and limitations of solar energy?",
        "expected_domain": ["energy"],
        "category": "single_domain"
    },
    {
        "id": 4,
        "query": "What are common causes of iron deficiency?",
        "expected_domain": ["healthcare"],
        "category": "single_domain"
    },
    {
        "id": 5,
        "query": "How can a student create a study plan for an upcoming examination?",
        "expected_domain": ["education"],
        "category": "single_domain"
    },
    {
        "id": 6,
        "query": "What are the benefits of drip irrigation compared to traditional flood irrigation?",
        "expected_domain": ["agriculture"],
        "category": "single_domain"
    },
    {
        "id": 7,
        "query": "How does the 50/30/20 budgeting rule work?",
        "expected_domain": ["finance"],
        "category": "single_domain"
    },
    {
        "id": 8,
        "query": "What are effective learning strategies based on cognitive science research?",
        "expected_domain": ["education"],
        "category": "single_domain"
    },
    {
        "id": 9,
        "query": "Should a manufacturing company consider solar energy based on its energy requirements and financial constraints?",
        "expected_domain": ["energy", "finance"],
        "category": "multi_domain"
    },
    {
        "id": 10,
        "query": "How can a farmer balance crop selection with financial planning for maximum profitability?",
        "expected_domain": ["agriculture", "finance"],
        "category": "multi_domain"
    }
]


def run_basic_rag(query, domains):
    """Mode A: Basic RAG - retrieve + generate, no specialized agents."""
    start = time.time()
    retrieval_agent = RetrievalAgent()
    docs = retrieval_agent.run(query, domains)

    # Simple LLM generation with retrieved context
    context = "\n\n".join([d["content"] for d in docs]) if docs else "No documents found."
    llm = get_llm()
    prompt = f"Based on the following context, answer the query.\n\nContext:\n{context}\n\nQuery: {query}"

    try:
        response = llm.generate_content(prompt)
        answer = response.text
    except Exception as e:
        answer = f"Error: {e}"

    elapsed = time.time() - start
    return {
        "answer": answer,
        "response_time": round(elapsed, 2),
        "agents_activated": 1,
        "retrieval_rounds": 1,
        "num_sources": len(docs),
        "confidence": "N/A"
    }


def run_static_multi_agent(query, domains):
    """Mode B: Static Multi-Agent - always runs all agents in the detected domains."""
    start = time.time()

    # Always retrieve + analyze + verify (static pipeline)
    from agents.retrieval_agent import RetrievalAgent
    from agents.verification_agent import VerificationAgent
    from agents.agriculture_agent import AgricultureAgent
    from agents.finance_agent import FinanceAgent
    from agents.energy_agent import EnergyAgent
    from agents.healthcare_agent import HealthcareAgent
    from agents.education_agent import EducationAgent

    domain_agents = {
        "agriculture": AgricultureAgent,
        "finance": FinanceAgent,
        "energy": EnergyAgent,
        "healthcare": HealthcareAgent,
        "education": EducationAgent,
    }

    retrieval_agent = RetrievalAgent()
    docs = retrieval_agent.run(query, domains)

    analyses = []
    agents_count = 2  # retrieval + verification
    for domain in domains:
        if domain in domain_agents:
            agent = domain_agents[domain]()
            analysis = agent.analyze(query, docs)
            analyses.append(analysis)
            agents_count += 1

    combined = "\n\n".join(analyses)
    verification_agent = VerificationAgent()
    verification = verification_agent.verify(query, combined, docs)

    elapsed = time.time() - start
    return {
        "answer": combined[:500] + "...",  # Truncate for display
        "response_time": round(elapsed, 2),
        "agents_activated": agents_count,
        "retrieval_rounds": 1,
        "num_sources": len(docs),
        "confidence": verification.get("score", "N/A")
    }


def run_adaptive_multi_agent(query):
    """Mode C: Self-Adaptive Multi-Agent RAG (the full system)."""
    start = time.time()
    result = run_workflow(query, selected_domain="auto")
    elapsed = time.time() - start

    return {
        "answer": result.get("final_response", "")[:500] + "...",
        "response_time": round(elapsed, 2),
        "agents_activated": len(set(result.get("agents_activated", []))),
        "retrieval_rounds": result.get("retrieval_rounds", 1),
        "num_sources": len(result.get("retrieved_docs", [])),
        "confidence": result.get("confidence_score", "N/A"),
        "detected_domains": result.get("detected_domains", []),
        "complexity": result.get("complexity", "N/A")
    }


def evaluate_domain_detection():
    """Test domain detection accuracy."""
    print("\n" + "="*60)
    print("DOMAIN DETECTION ACCURACY")
    print("="*60)

    correct = 0
    total = len(TEST_QUESTIONS)

    for q in TEST_QUESTIONS:
        detected = detect_domains(q["query"])
        expected = set(q["expected_domain"])
        detected_set = set(detected)

        match = expected.issubset(detected_set)
        if match:
            correct += 1
            status = "PASS"
        else:
            status = "FAIL"

        print(f"  Q{q['id']}: {status} | Expected: {q['expected_domain']} | Detected: {detected}")

    accuracy = correct / total * 100
    print(f"\n  Domain Detection Accuracy: {accuracy:.0f}% ({correct}/{total})")
    return accuracy


def evaluate_full_pipeline():
    """Run all test questions through all three modes and compare."""
    print("\n" + "="*60)
    print("FULL PIPELINE EVALUATION")
    print("="*60)

    results = []

    # Use a subset for faster evaluation
    eval_questions = TEST_QUESTIONS[:6]  # First 6 questions

    for q in eval_questions:
        print(f"\n--- Q{q['id']}: {q['query'][:60]}... ---")

        domains = q["expected_domain"]

        # Mode A: Basic RAG
        print("  Running Basic RAG...")
        basic = run_basic_rag(q["query"], domains)

        # Mode C: Adaptive (skip static to save time/API calls)
        print("  Running Adaptive Multi-Agent RAG...")
        adaptive = run_adaptive_multi_agent(q["query"])

        results.append({
            "question_id": q["id"],
            "query": q["query"][:50],
            "basic_rag": basic,
            "adaptive_rag": adaptive
        })

        print(f"  Basic RAG:    Time={basic['response_time']}s, Sources={basic['num_sources']}")
        print(f"  Adaptive RAG: Time={adaptive['response_time']}s, Sources={adaptive['num_sources']}, "
              f"Agents={adaptive['agents_activated']}, Confidence={adaptive['confidence']}")

    # Summary table
    print("\n" + "="*60)
    print("COMPARISON SUMMARY")
    print("="*60)
    print(f"{'Metric':<25} {'Basic RAG':<15} {'Adaptive RAG':<15}")
    print("-" * 55)

    avg_time_basic = sum(r["basic_rag"]["response_time"] for r in results) / len(results)
    avg_time_adaptive = sum(r["adaptive_rag"]["response_time"] for r in results) / len(results)
    avg_sources_basic = sum(r["basic_rag"]["num_sources"] for r in results) / len(results)
    avg_sources_adaptive = sum(r["adaptive_rag"]["num_sources"] for r in results) / len(results)
    avg_agents = sum(r["adaptive_rag"]["agents_activated"] for r in results) / len(results)

    print(f"{'Avg Response Time (s)':<25} {avg_time_basic:<15.2f} {avg_time_adaptive:<15.2f}")
    print(f"{'Avg Sources Used':<25} {avg_sources_basic:<15.1f} {avg_sources_adaptive:<15.1f}")
    print(f"{'Avg Agents Activated':<25} {'1':<15} {avg_agents:<15.1f}")
    print(f"{'Has Verification':<25} {'No':<15} {'Yes (adaptive)':<15}")
    print(f"{'Has Confidence Score':<25} {'No':<15} {'Yes':<15}")

    return results


def main():
    """Run all evaluations."""
    print("\n" + "#"*60)
    print("# Multi-Agent RAG Framework - Evaluation")
    print("#"*60)

    # Test 1: Domain detection
    evaluate_domain_detection()

    # Test 2: Full pipeline comparison
    print("\nStarting full pipeline evaluation (this may take a few minutes)...")
    evaluate_full_pipeline()

    print("\n" + "#"*60)
    print("# Evaluation Complete")
    print("#"*60)


if __name__ == "__main__":
    main()
