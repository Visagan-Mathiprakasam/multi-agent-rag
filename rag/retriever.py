"""
Retrieval module for querying the vector store.
Returns ranked document chunks with metadata and similarity scores.
"""
from rag.vector_store import get_or_create_collection
from rag.embeddings import get_embedding_function
from utils.config import TOP_K


def retrieve(query, domains, top_k=None):
    """
    Retrieve relevant document chunks from one or more domain collections.

    Args:
        query: User query string.
        domains: List of domain names to search.
        top_k: Number of results to return (default from config).

    Returns:
        List of result dicts with keys: content, source, page, domain, score.
    """
    if top_k is None:
        top_k = TOP_K

    embedding_fn = get_embedding_function()
    query_embedding = embedding_fn.embed_query(query)

    all_results = []

    for domain in domains:
        try:
            collection = get_or_create_collection(domain)

            # Skip empty collections
            if collection.count() == 0:
                continue

            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=min(top_k, collection.count()),
                include=["documents", "metadatas", "distances"]
            )

            if results and results["documents"] and results["documents"][0]:
                for i, (doc, meta, dist) in enumerate(zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0]
                )):
                    # With cosine distance: similarity = 1 - distance
                    similarity = round(max(0.0, 1.0 - dist), 4)
                    all_results.append({
                        "content": doc,
                        "source": meta.get("source", "Unknown"),
                        "page": meta.get("page", "N/A"),
                        "domain": domain,
                        "score": similarity
                    })

        except Exception as e:
            print(f"Error retrieving from {domain}: {e}")

    # Sort by similarity score descending and return top_k
    all_results.sort(key=lambda x: x["score"], reverse=True)
    return all_results[:top_k]
