"""
Embedding model wrapper using Sentence Transformers.
Uses a singleton pattern to avoid reloading the model.
"""
from sentence_transformers import SentenceTransformer
from utils.config import EMBEDDING_MODEL


class EmbeddingFunction:
    """Singleton embedding function compatible with ChromaDB."""
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _get_model(self):
        if EmbeddingFunction._model is None:
            EmbeddingFunction._model = SentenceTransformer(EMBEDDING_MODEL)
        return EmbeddingFunction._model

    def __call__(self, input):
        """ChromaDB-compatible call interface."""
        model = self._get_model()
        return model.encode(input, show_progress_bar=False).tolist()

    def embed_documents(self, texts):
        """Embed a list of document texts."""
        model = self._get_model()
        return model.encode(texts, show_progress_bar=False).tolist()

    def embed_query(self, text):
        """Embed a single query text."""
        model = self._get_model()
        return model.encode([text], show_progress_bar=False)[0].tolist()


def get_embedding_function():
    """Get the singleton embedding function."""
    return EmbeddingFunction()
