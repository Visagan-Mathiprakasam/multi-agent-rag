"""
Confidence calculation for the Multi-Agent RAG Framework.
Uses a simple weighted formula combining retrieval quality, source count,
agent agreement, and verification results.
"""

# Weights for confidence components
W_RETRIEVAL = 0.4    # Retrieval relevance
W_SOURCES = 0.2      # Number of supporting sources
W_AGREEMENT = 0.2    # Agreement between agents
W_VERIFICATION = 0.2 # Verification result


def calculate_confidence(retrieval_scores, source_count, agent_agreement, verification_score):
    """
    Calculate overall confidence score.

    Args:
        retrieval_scores: List of similarity scores from retrieved documents (0-1).
        source_count: Number of relevant sources found.
        agent_agreement: Agreement score between agents (0-1). 
                         1.0 for single agent, calculated for multi-agent.
        verification_score: Score from verification agent (0-1).

    Returns:
        Confidence score between 0 and 1.
    """
    # Average retrieval similarity
    avg_retrieval = sum(retrieval_scores) / len(retrieval_scores) if retrieval_scores else 0.0

    # Normalize source count (cap at 5 sources)
    source_score = min(source_count / 5.0, 1.0)

    # Compute weighted confidence
    confidence = (
        W_RETRIEVAL * avg_retrieval +
        W_SOURCES * source_score +
        W_AGREEMENT * agent_agreement +
        W_VERIFICATION * verification_score
    )

    return round(min(confidence, 1.0), 3)


def get_confidence_label(score):
    """Convert numeric confidence to human-readable label."""
    if score >= 0.8:
        return "High"
    elif score >= 0.6:
        return "Medium"
    elif score >= 0.4:
        return "Low"
    else:
        return "Very Low"


def get_confidence_details(retrieval_scores, source_count, agent_agreement, verification_score):
    """
    Return a breakdown of confidence components for transparency.
    """
    avg_retrieval = sum(retrieval_scores) / len(retrieval_scores) if retrieval_scores else 0.0
    source_score = min(source_count / 5.0, 1.0)

    return {
        "retrieval_relevance": round(avg_retrieval, 3),
        "source_coverage": round(source_score, 3),
        "agent_agreement": round(agent_agreement, 3),
        "verification_score": round(verification_score, 3),
        "weights": {
            "retrieval": W_RETRIEVAL,
            "sources": W_SOURCES,
            "agreement": W_AGREEMENT,
            "verification": W_VERIFICATION
        }
    }
