"""
Document Comparison Routes
Endpoints for comparing multiple documents
"""

from fastapi import APIRouter, HTTPException
import logging

from app.services.llm_service import LLMService
from app.models.comparison import ComparisonRequest, ComparisonResponse

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize LLM service
llm_service = LLMService()

@router.post("/", response_model=ComparisonResponse)
async def compare_documents(request: ComparisonRequest):
    """
    Compare two or more documents
    
    - **document_ids**: List of document IDs to compare (minimum 2)
    - **comparison_aspects**: Optional specific aspects to focus on
    
    Returns:
        - Comparison analysis including similarities and differences
    """
    try:
        if len(request.document_ids) < 2:
            raise ValueError("At least 2 documents required for comparison")
        
        logger.info(f"📊 Comparing documents: {request.document_ids}")
        
        # In production, retrieve actual document content from database
        documents_content = {
            doc_id: f"Sample content for {doc_id}"  # Placeholder
            for doc_id in request.document_ids
        }
        
        comparison_result = llm_service.compare_documents(
            documents_content,
            request.comparison_aspects
        )
        
        return {
            "compared_documents": list(documents_content.keys()),
            "similarities": "Similarities identified",
            "differences": "Differences identified",
            "detailed_comparison": {
                "comparison": comparison_result.get("comparison", "")
            }
        }
    except Exception as e:
        logger.error(f"Error comparing documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))