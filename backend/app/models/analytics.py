"""
Analytics related Pydantic models
"""

from pydantic import BaseModel, Field

class AnalyticsResponse(BaseModel):
    """
    Response model for analytics
    """
    total_documents: int = Field(..., description="Total number of uploaded documents")
    total_chunks: int = Field(..., description="Total number of chunks created")
    total_embeddings: int = Field(..., description="Total embeddings generated")
    total_questions_answered: int = Field(..., description="Total Q&A interactions")
    most_queried_documents: list[dict] = Field(..., description="Top queried documents")
    average_processing_time: float = Field(..., description="Average doc processing time in seconds")
    storage_used: dict = Field(..., description="Storage usage breakdown")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_documents": 15,
                "total_chunks": 3500,
                "total_embeddings": 3500,
                "total_questions_answered": 250,
                "most_queried_documents": [
                    {"document": "Paper1.pdf", "queries": 45},
                    {"document": "Paper2.pdf", "queries": 38}
                ],
                "average_processing_time": 2.5,
                "storage_used": {
                    "documents": "150MB",
                    "embeddings": "45MB"
                }
            }
        }