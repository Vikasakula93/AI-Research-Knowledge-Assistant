"""
Analytics Routes
Endpoints for system analytics and statistics
"""

from fastapi import APIRouter, HTTPException
import logging

from app.models.analytics import AnalyticsResponse

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=AnalyticsResponse)
async def get_analytics():
    """
    Get system analytics and statistics
    
    Returns:
        - Analytics about documents, embeddings, and interactions
    """
    try:
        logger.info("📊 Fetching analytics")
        
        # In production, gather real statistics from database
        analytics = {
            "total_documents": 15,
            "total_chunks": 3500,
            "total_embeddings": 3500,
            "total_questions_answered": 250,
            "most_queried_documents": [
                {"document": "ResearchPaper1.pdf", "queries": 45},
                {"document": "ResearchPaper2.pdf", "queries": 38}
            ],
            "average_processing_time": 2.5,
            "storage_used": {
                "documents": "150MB",
                "embeddings": "45MB",
                "total": "195MB"
            }
        }
        
        return analytics
    except Exception as e:
        logger.error(f"Error fetching analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))