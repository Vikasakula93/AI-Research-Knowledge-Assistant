"""
Document Summarization Routes
Endpoints for generating document summaries
"""

from fastapi import APIRouter, HTTPException
import logging

from app.services.llm_service import LLMService
from app.models.summarization import SummarizationRequest, SummarizationResponse

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize LLM service
llm_service = LLMService()

@router.post("/", response_model=SummarizationResponse)
async def summarize_document(request: SummarizationRequest):
    """
    Generate summaries for a document
    
    - **document_id**: ID of the document to summarize
    - **summary_type**: Type of summary ('executive', 'technical', 'bullet_points', or 'comprehensive')
    
    Returns:
        - Executive, technical, and key takeaway summaries
    """
    try:
        logger.info(f"📝 Summarizing document: {request.document_id}")
        
        # In production, retrieve actual document content from database
        sample_text = """
        This is a sample research paper about machine learning and artificial intelligence.
        The paper discusses various deep learning architectures, their applications,
        and the future challenges in the field...
        """
        
        summaries = llm_service.summarize_document(sample_text, request.summary_type)
        
        return {
            "document_id": request.document_id,
            "document_name": f"Document_{request.document_id}.pdf",
            "summary_type": request.summary_type,
            "executive_summary": summaries.get("executive", ""),
            "technical_summary": summaries.get("technical", ""),
            "key_takeaways": [
                "Key point 1",
                "Key point 2",
                "Key point 3"
            ]
        }
    except Exception as e:
        logger.error(f"Error summarizing document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))