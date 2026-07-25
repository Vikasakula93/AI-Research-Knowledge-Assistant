"""
Search-related Pydantic models
"""

from pydantic import BaseModel, Field
from typing import Optional

class SearchRequest(BaseModel):
    """
    Request model for searching documents
    """
    query: str = Field(..., min_length=1, description="Search query")
    document_ids: Optional[list[str]] = Field(
        None, 
        description="Specific documents to search in (if None, search all)"
    )
    search_mode: str = Field(
        default="semantic",
        description="Search mode: 'keyword', 'semantic', or 'hybrid'"
    )
    top_k: int = Field(default=5, ge=1, le=50, description="Number of results to return")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What are neural networks?",
                "document_ids": None,
                "search_mode": "semantic",
                "top_k": 5
            }
        }

class SearchResult(BaseModel):
    """
    Single search result item
    """
    document_id: str = Field(..., description="Document ID")
    document_name: str = Field(..., description="Document name")
    chunk_id: str = Field(..., description="Chunk ID within the document")
    page_number: int = Field(..., description="Page number in the document")
    content: str = Field(..., description="Retrieved text chunk")
    relevance_score: float = Field(..., ge=0, le=1, description="Relevance score (0-1)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "document_id": "doc_123",
                "document_name": "ML_Basics.pdf",
                "chunk_id": "chunk_456",
                "page_number": 5,
                "content": "Neural networks are computational models...",
                "relevance_score": 0.95
            }
        }

class SearchResponse(BaseModel):
    """
    Response model for search results
    """
    query: str = Field(..., description="The search query")
    search_mode: str = Field(..., description="Search mode used")
    total_results: int = Field(..., description="Total number of results found")
    results: list[SearchResult] = Field(..., description="List of search results")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "neural networks",
                "search_mode": "semantic",
                "total_results": 5,
                "results": []
            }
        }