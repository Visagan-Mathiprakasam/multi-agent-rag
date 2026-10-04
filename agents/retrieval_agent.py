"""
Retrieval Agent: Searches the vector database and returns relevant documents.
"""
from rag.retriever import retrieve
from utils.config import TOP_K


class RetrievalAgent:
    """Agent responsible for retrieving relevant documents from the vector store."""

    def __init__(self):
        self.name = "Retrieval Agent"

    def run(self, query, domains, top_k=None):
        """
        Retrieve relevant documents for the query.

        Args:
            query: User query string.
            domains: List of domain names to search.
            top_k: Number of results to return.

        Returns:
            List of retrieved document dicts.
        """
        if top_k is None:
            top_k = TOP_K

        try:
            results = retrieve(query, domains, top_k)
            return results
        except Exception as e:
            print(f"Retrieval error: {e}")
            return []
