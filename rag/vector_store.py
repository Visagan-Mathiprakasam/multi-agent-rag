"""
Vector store management using ChromaDB.
Handles collection creation, document ingestion, and persistence.
"""
import os
import chromadb
from rag.document_loader import load_documents, split_documents
from rag.embeddings import get_embedding_function
from utils.config import CHROMA_PERSIST_DIR, DOMAINS


def get_chroma_client():
    """Get or create the ChromaDB persistent client."""
    os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
    return chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)


def get_or_create_collection(domain):
    """Get or create a ChromaDB collection for a domain."""
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=f"rag_{domain}",
        metadata={"hnsw:space": "cosine"}  # Use cosine similarity
    )


def ingest_domain(domain):
    """
    Load documents from a domain folder and ingest into ChromaDB.

    Args:
        domain: Domain name string.

    Returns:
        Number of chunks ingested.
    """
    print(f"\nIngesting documents for domain: {domain}")
    documents = load_documents(domain)
    if not documents:
        print(f"  No documents found for domain: {domain}")
        return 0

    chunks = split_documents(documents)
    if not chunks:
        print(f"  No chunks created for domain: {domain}")
        return 0

    collection = get_or_create_collection(domain)
    embedding_fn = get_embedding_function()

    # Prepare data for ChromaDB
    texts = [chunk.page_content for chunk in chunks]
    metadatas = []
    for chunk in chunks:
        # Ensure all metadata values are strings (ChromaDB requirement)
        meta = {}
        for k, v in chunk.metadata.items():
            meta[k] = str(v) if not isinstance(v, str) else v
        metadatas.append(meta)
    ids = [f"{domain}_{i}" for i in range(len(chunks))]
    embeddings = embedding_fn.embed_documents(texts)

    # Batch upsert to handle large document sets
    batch_size = 100
    for i in range(0, len(texts), batch_size):
        end = min(i + batch_size, len(texts))
        collection.upsert(
            ids=ids[i:end],
            documents=texts[i:end],
            metadatas=metadatas[i:end],
            embeddings=embeddings[i:end]
        )

    print(f"  Ingested {len(chunks)} chunks for domain: {domain}")
    return len(chunks)


def ingest_all():
    """Ingest documents for all domains."""
    total = 0
    for domain in DOMAINS:
        count = ingest_domain(domain)
        total += count
    print(f"\nTotal chunks ingested across all domains: {total}")
    return total


def get_collection_stats():
    """Get document count for each domain collection."""
    stats = {}
    for domain in DOMAINS:
        try:
            collection = get_or_create_collection(domain)
            stats[domain] = collection.count()
        except Exception:
            stats[domain] = 0
    return stats
