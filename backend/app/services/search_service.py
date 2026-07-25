"""
Search Service
Handles semantic, keyword, and hybrid search
"""

import logging
import re
from typing import List, Dict
from app.services.embedding_service import EmbeddingService
from app.services.vector_db_service import VectorDatabaseService

logger = logging.getLogger(__name__)

class SearchService:
    """
    Service for different search modes
    """
    
    def __init__(self, embedding_service: EmbeddingService, vector_db_service: VectorDatabaseService):
        """
        Initialize search service
        
        Args:
            embedding_service: Service for generating embeddings
            vector_db_service: Service for vector search
        """
        self.embedding_service = embedding_service
        self.vector_db_service = vector_db_service
        self.chunks_storage = {}  # Store chunks in memory
    
    def semantic_search(
        self,
        query: str,
        top_k: int = 5,
        document_ids: List[str] = None
    ) -> List[Dict]:
        """
        Perform semantic search
        
        Args:
            query (str): Search query
            top_k (int): Number of results
            document_ids (List[str]): Filter by specific documents
            
        Returns:
            List[Dict]: Search results with relevance scores
        """
        try:
            # Generate embedding for query
            query_embedding = self.embedding_service.embed_text(query)
            
            # Search vector database
            results = self.vector_db_service.search(query_embedding, k=top_k)
            
            # Format results
            search_results = []
            for vector_id, similarity, metadata in results:
                # Filter by document if specified
                if document_ids and metadata.get("document_id") not in document_ids:
                    continue
                
                result = {
                    "document_id": metadata.get("document_id"),
                    "document_name": metadata.get("document_name"),
                    "chunk_id": metadata.get("chunk_id"),
                    "page_number": metadata.get("page_number", 0),
                    "content": metadata.get("content", ""),
                    "relevance_score": float(similarity)
                }
                search_results.append(result)
            
            logger.info(f"🔍 Semantic search: Found {len(search_results)} results")
            return search_results[:top_k]
            
        except Exception as e:
            logger.error(f"Error in semantic search: {str(e)}")
            return []
    
    def keyword_search(
        self,
        query: str,
        top_k: int = 5,
        document_ids: List[str] = None
    ) -> List[Dict]:
        """
        Perform keyword-based search
        
        Args:
            query (str): Search query
            top_k (int): Number of results
            document_ids (List[str]): Filter by specific documents
            
        Returns:
            List[Dict]: Search results
        """
        try:
            keywords = query.lower().split()
            all_results = []
            
            # Search through stored chunks
            for chunk_id, chunk_data in self.chunks_storage.items():
                # Filter by document if specified
                if document_ids and chunk_data.get("document_id") not in document_ids:
                    continue
                
                content = chunk_data.get("content", "").lower()
                
                # Count keyword matches
                match_count = sum(1 for keyword in keywords if keyword in content)
                
                if match_count > 0:
                    relevance = match_count / len(keywords)
                    all_results.append({
                        "document_id": chunk_data.get("document_id"),
                        "document_name": chunk_data.get("document_name"),
                        "chunk_id": chunk_id,
                        "page_number": chunk_data.get("page_number", 0),
                        "content": chunk_data.get("content"),
                        "relevance_score": relevance
                    })
            
            # Sort by relevance and return top_k
            sorted_results = sorted(all_results, key=lambda x: x["relevance_score"], reverse=True)
            logger.info(f"🔍 Keyword search: Found {len(sorted_results)} results")
            return sorted_results[:top_k]
            
        except Exception as e:
            logger.error(f"Error in keyword search: {str(e)}")
            return []
    
    def hybrid_search(
        self,
        query: str,
        top_k: int = 5,
        document_ids: List[str] = None
    ) -> List[Dict]:
        """
        Perform hybrid search (semantic + keyword)
        
        Args:
            query (str): Search query
            top_k (int): Number of results
            document_ids (List[str]): Filter by specific documents
            
        Returns:
            List[Dict]: Combined search results
        """
        try:
            # Get semantic results
            semantic_results = self.semantic_search(query, top_k * 2, document_ids)
            
            # Get keyword results
            keyword_results = self.keyword_search(query, top_k * 2, document_ids)
            
            # Combine and deduplicate
            combined = {}
            for result in semantic_results:
                chunk_id = result["chunk_id"]
                combined[chunk_id] = result
                combined[chunk_id]["semantic_score"] = result["relevance_score"]
            
            for result in keyword_results:
                chunk_id = result["chunk_id"]
                if chunk_id in combined:
                    combined[chunk_id]["keyword_score"] = result["relevance_score"]
                else:
                    result["semantic_score"] = 0
                    combined[chunk_id] = result
            
            # Calculate hybrid score
            for chunk_id in combined:
                semantic = combined[chunk_id].get("semantic_score", 0)
                keyword = combined[chunk_id].get("keyword_score", 0)
                combined[chunk_id]["relevance_score"] = (semantic + keyword) / 2
            
            # Sort and return
            results = sorted(combined.values(), key=lambda x: x["relevance_score"], reverse=True)
            logger.info(f"🔍 Hybrid search: Found {len(results)} results")
            return results[:top_k]
            
        except Exception as e:
            logger.error(f"Error in hybrid search: {str(e)}")
            return []
    
    def store_chunk(self, chunk_data: Dict):
        """
        Store a document chunk
        
        Args:
            chunk_data (Dict): Chunk information including content, document_id, etc.
        """
        chunk_id = chunk_data.get("chunk_id")
        self.chunks_storage[chunk_id] = chunk_data