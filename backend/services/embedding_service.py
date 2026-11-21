import numpy as np
from typing import List
from backend.config import settings

class EmbeddingService:
    _model = None

    @classmethod
    def get_model(cls):
        """Lazy load SentenceTransformers model."""
        if cls._model is None:
            from sentence_transformers import SentenceTransformer
            # Load lightweight 384-dimensional model
            cls._model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
        return cls._model

    @classmethod
    def generate_embeddings(cls, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """
        Generate normalized embeddings for a list of texts.
        Returns a float32 2D numpy array of shape (len(texts), 384).
        """
        if not texts:
            return np.empty((0, settings.EMBEDDING_DIM), dtype="float32")

        model = cls.get_model()
        embeddings = model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        return embeddings.astype("float32")

    @classmethod
    def embed_query(cls, query: str) -> np.ndarray:
        """Generate normalized 1D embedding for a single query."""
        model = cls.get_model()
        vec = model.encode(
            [query],
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        return vec.astype("float32")[0]
