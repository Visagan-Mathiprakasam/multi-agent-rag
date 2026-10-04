"""
Document loading and chunking for the RAG pipeline.
Supports both PDF and TXT files.
"""
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.config import CHUNK_SIZE, CHUNK_OVERLAP, DATA_DIR


def load_documents(domain):
    """
    Load all documents from a domain's data folder.

    Args:
        domain: Domain name (e.g., 'agriculture', 'finance').

    Returns:
        List of LangChain Document objects.
    """
    domain_path = os.path.join(DATA_DIR, domain)
    if not os.path.exists(domain_path):
        print(f"Data directory not found: {domain_path}")
        return []

    documents = []
    for filename in os.listdir(domain_path):
        filepath = os.path.join(domain_path, filename)
        try:
            if filename.lower().endswith(".pdf"):
                loader = PyPDFLoader(filepath)
                docs = loader.load()
            elif filename.lower().endswith(".txt"):
                loader = TextLoader(filepath, encoding="utf-8")
                docs = loader.load()
            else:
                continue  # Skip unsupported file types

            # Enrich metadata with source info
            for doc in docs:
                doc.metadata["source"] = filename
                doc.metadata["domain"] = domain
                if "page" not in doc.metadata:
                    doc.metadata["page"] = 0

            documents.extend(docs)
            print(f"  Loaded: {filename} ({len(docs)} pages/sections)")

        except Exception as e:
            print(f"  Error loading {filepath}: {e}")

    return documents


def split_documents(documents):
    """
    Split documents into smaller chunks for embedding.

    Args:
        documents: List of LangChain Document objects.

    Returns:
        List of chunked Document objects.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    return splitter.split_documents(documents)
