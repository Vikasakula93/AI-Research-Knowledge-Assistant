"""
Embedding Service
Handles generation of embeddings for text chunks
"""

import logging
from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import settings

logger = logging.getLogger(__name__)

class EmbeddingService:
    """
    Service for generating embeddings
    Uses sentence-transformers for semantic embeddings
    """
    
    def __init__(self):
        """Initialize the embedding service with pre-trained model"""
        try:
            logger.info(f"Loading embedding model: {settings.EMBEDDINGS_MODEL}")
            self.model = SentenceTransformer(settings.EMBEDDINGS_MODEL)
            self.embedding_dimension = settings.EMBEDDING_DIMENSION
            logger.info(f"✅ Embedding model loaded. Dimension: {self.embedding_dimension}")
        except Exception as e:
            logger.error(f"❌ Failed to load embedding model: {str(e)}")
            raise
    
    def embed_text(self, text: str) -> Union[List[float], np.ndarray]:
        """
        Generate embedding for a single text
        
        Args:
            text (str): Text to embed
            
        Returns:
            Union[List[float], np.ndarray]: Embedding vector
        """
        try:
            embedding = self.model.encode(text, convert_to_tensor=False)
            return embedding.tolist() if isinstance(embedding, np.ndarray) else embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise
    
    def embed_texts(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts (List[str]): List of texts to embed
            batch_size (int): Batch size for processing
            
        Returns:
            List[List[float]]: List of embedding vectors
        """
        try:
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                show_progress_bar=True,
                convert_to_tensor=False
            )
            
            if isinstance(embeddings, np.ndarray):
                embeddings = embeddings.tolist()
            
            logger.info(f"✅ Generated embeddings for {len(texts)} texts")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {str(e)}")
            raise
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of embeddings
        
        Returns:
            int: Embedding dimension
        """
        return self.embedding_dimension