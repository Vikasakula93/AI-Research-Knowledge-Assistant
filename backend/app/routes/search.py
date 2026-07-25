"""
Semantic Search Routes
Endpoints for searching across documents
"""

from fastapi import APIRouter, HTTPException
import logging
from typing import List, Optional

from app.services.search_service import SearchService
from app.services.embedding_service import EmbeddingService
from app.services.vector_db_service import VectorDatabaseService
from app.models.search import SearchRequest, SearchResponse

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
embedding_service = EmbeddingService()
vector_db_service = VectorDatabaseService(embedding_service.get_embedding_dimension())
search_service = SearchService(embedding_service, vector_db_service)

@router.post("/", response_model=SearchResponse)
async def search_documents(request: SearchRequest):
    """
    Search documents using semantic or keyword search
    
    - **query**: Search query
    - **search_mode**: 'semantic', 'keyword', or 'hybrid'
    - **top_k**: Number of results to return
    - **document_ids**: Optional list of specific document IDs to search
    
    Returns:
        - List of relevant search results with relevance scores
    """
    try:
        logger.info(f"🔍 Searching: {request.query} (mode: {request.search_mode})")
        
        if request.search_mode == "semantic":
            results = search_service.semantic_search(
                request.query,
                request.top_k,
                request.document_ids
            )
        elif request.search_mode == "keyword":
            results = search_service.keyword_search(
                request.query,
                request.top_k,
                request.document_ids
            )
        elif request.search_mode == "hybrid":
            results = search_service.hybrid_search(
                request.query,
                request.top_k,
                request.document_ids
            )
        else:
            raise ValueError(f"Invalid search mode: {request.search_mode}")
        
        return {
            "query": request.query,
            "search_mode": request.search_mode,
            "total_results": len(results),
            "results": results
        }
    except Exception as e:
        logger.error(f"Error searching documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))