"""
Verification Agent: Checks whether generated analysis is supported by evidence.
Produces verification status and a score.
"""
from agents.base_agent import get_llm


class VerificationAgent:
    """Agent that verifies analysis claims against retrieved evidence."""

    def __init__(self):
        self.name = "Verification Agent"
        self.llm = get_llm()

    def verify(self, query, analysis, retrieved_docs):
        """
        Verify that analysis claims are supported by retrieved documents.

        Args:
            query: Original user query.
            analysis: Generated analysis text (may be combined from multiple agents).
            retrieved_docs: List of retrieved document dicts.

        Returns:
            Dict with keys: status, unsupported_claims, contradictions, score, summary.
        """
        context = self._format_docs(retrieved_docs)

        prompt = f"""You are a Verification Agent. Your task is to check whether the analysis
is properly supported by the retrieved evidence.

QUERY: {query}

RETRIEVED EVIDENCE:
{context}

ANALYSIS TO VERIFY:
{analysis}

Evaluate the following:
1. Are the key claims in the analysis supported by the evidence? (Yes/Partially/No)
2. List any specific claims NOT supported by the evidence.
3. Are there contradictions between the analysis and the evidence?
4. Provide an overall verification score (0.0 to 1.0, where 1.0 = fully verified).

Respond in EXACTLY this format (one item per line):
VERIFICATION_STATUS: [Verified/Partially Verified/Not Verified]
UNSUPPORTED_CLAIMS: [comma-separated list, or None]
CONTRADICTIONS: [comma-separated list, or None]
VERIFICATION_SCORE: [number between 0.0 and 1.0]
SUMMARY: [one-line summary of verification result]"""

        try:
            response = self.llm.generate_content(prompt)
            return self._parse_verification(response.text)
        except Exception as e:
            return {
                "status": "Error",
                "unsupported_claims": [],
                "contradictions": [],
                "score": 0.5,
                "summary": f"Verification failed: {str(e)}"
            }

    def _parse_verification(self, text):
        """Parse the structured verification response from the LLM."""
        result = {
            "status": "Partially Verified",
            "unsupported_claims": [],
            "contradictions": [],
            "score": 0.5,
            "summary": "Could not parse verification result."
        }

        for line in text.strip().split("\n"):
            line = line.strip()
            if line.startswith("VERIFICATION_STATUS:"):
                result["status"] = line.split(":", 1)[1].strip()
            elif line.startswith("UNSUPPORTED_CLAIMS:"):
                claims_text = line.split(":", 1)[1].strip()
                if claims_text.lower() not in ("none", "n/a", ""):
                    result["unsupported_claims"] = [
                        c.strip() for c in claims_text.split(",") if c.strip()
                    ]
            elif line.startswith("CONTRADICTIONS:"):
                contra_text = line.split(":", 1)[1].strip()
                if contra_text.lower() not in ("none", "n/a", ""):
                    result["contradictions"] = [
                        c.strip() for c in contra_text.split(",") if c.strip()
                    ]
            elif line.startswith("VERIFICATION_SCORE:"):
                try:
                    score = float(line.split(":", 1)[1].strip())
                    result["score"] = max(0.0, min(1.0, score))
                except ValueError:
                    result["score"] = 0.5
            elif line.startswith("SUMMARY:"):
                result["summary"] = line.split(":", 1)[1].strip()

        return result

    def _format_docs(self, docs):
        """Format retrieved documents for the verification prompt."""
        if not docs:
            return "No evidence documents available."
        formatted = []
        for i, doc in enumerate(docs, 1):
            source = doc.get("source", "Unknown")
            content = doc.get("content", "")
            formatted.append(f"[Evidence {i} - {source}]\n{content}")
        return "\n\n".join(formatted)
