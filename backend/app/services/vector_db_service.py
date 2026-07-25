"""
Vector Database Service
Handles storing and retrieving embeddings from vector database
"""

import logging
import json
from typing import List, Dict, Tuple
import faiss
import numpy as np

from app.config import settings

logger = logging.getLogger(__name__)

class VectorDatabaseService:
    """
    Service for managing vector database operations
    Currently implements FAISS for local vector search
    """
    
    def __init__(self, embedding_dimension: int):
        """
        Initialize vector database service
        
        Args:
            embedding_dimension (int): Dimension of embeddings
        """
        self.embedding_dimension = embedding_dimension
        self.db_type = settings.VECTOR_DB_TYPE
        self.index = None
        self.metadata_store = {}  # Store metadata for each vector
        self.vector_count = 0
        
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize the vector database based on configuration"""
        
        if self.db_type == "faiss":
            logger.info("Initializing FAISS vector database")
            # Create FAISS index for similarity search
            self.index = faiss.IndexFlatL2(self.embedding_dimension)
            logger.info("✅ FAISS index initialized")
        else:
            logger.warning(f"Vector DB type '{self.db_type}' not fully implemented, using FAISS")
            self.index = faiss.IndexFlatL2(self.embedding_dimension)
    
    def add_vectors(
        self,
        vectors: List[List[float]],
        metadata: List[Dict]
    ) -> bool:
        """
        Add vectors to the database
        
        Args:
            vectors (List[List[float]]): List of embedding vectors
            metadata (List[Dict]): Metadata for each vector (document_id, chunk_id, etc.)
            
        Returns:
            bool: True if successful
        """
        try:
            if len(vectors) == 0:
                logger.warning("No vectors to add")
                return False
            
            # Convert to numpy array
            vectors_array = np.array(vectors, dtype=np.float32)
            
            # Add to FAISS index
            self.index.add(vectors_array)
            
            # Store metadata
            for i, meta in enumerate(metadata):
                vector_id = self.vector_count + i
                self.metadata_store[vector_id] = meta
            
            self.vector_count += len(vectors)
            logger.info(f"✅ Added {len(vectors)} vectors to database. Total: {self.vector_count}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding vectors: {str(e)}")
            return False
    
    def search(self, query_vector: List[float], k: int = 5) -> List[Tuple[int, float, Dict]]:
        """
        Search for similar vectors
        
        Args:
            query_vector (List[float]): Query embedding vector
            k (int): Number of results to return
            
        Returns:
            List[Tuple[int, float, Dict]]: List of (vector_id, distance, metadata)
        """
        try:
            # Convert to numpy array
            query_array = np.array([query_vector], dtype=np.float32)
            
            # Search in FAISS
            distances, indices = self.index.search(query_array, k)
            
            results = []
            for idx, distance in zip(indices[0], distances[0]):
                if idx >= 0 and idx < len(self.metadata_store):
                    metadata = self.metadata_store.get(idx, {})
                    # Convert distance to similarity score (0-1)
                    similarity = 1 / (1 + distance)
                    results.append((idx, similarity, metadata))
            
            logger.info(f"🔍 Search returned {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Error searching vectors: {str(e)}")
            return []
    
    def delete_document_vectors(self, document_id: str) -> int:
        """
        Delete all vectors for a specific document
        
        Args:
            document_id (str): Document ID
            
        Returns:
            int: Number of vectors deleted
        """
        # Note: FAISS doesn't support deletion directly
        # In production, consider using a more advanced index
        deleted_count = 0
        to_delete = [
            vid for vid, meta in self.metadata_store.items()
            if meta.get("document_id") == document_id
        ]
        
        for vid in to_delete:
            del self.metadata_store[vid]
            deleted_count += 1
        
        logger.info(f"🗑️ Deleted {deleted_count} vectors for document {document_id}")
        return deleted_count
    
    def get_database_stats(self) -> Dict:
        """
        Get statistics about the vector database
        
        Returns:
            Dict: Database statistics
        """
        return {
            "type": self.db_type,
            "total_vectors": self.vector_count,
            "embedding_dimension": self.embedding_dimension,
            "metadata_store_size": len(self.metadata_store)
        }