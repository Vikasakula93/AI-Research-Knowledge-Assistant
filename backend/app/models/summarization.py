"""
Summarization related Pydantic models
"""

from pydantic import BaseModel, Field

class SummarizationRequest(BaseModel):
    """
    Request model for document summarization
    """
    document_id: str = Field(..., description="ID of document to summarize")
    summary_type: str = Field(
        default="comprehensive",
        description="Type: 'executive', 'technical', 'bullet_points', or 'comprehensive'"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "document_id": "doc_123",
                "summary_type": "comprehensive"
            }
        }

class SummarizationResponse(BaseModel):
    """
    Response model for summarization
    """
    document_id: str = Field(..., description="Document ID")
    document_name: str = Field(..., description="Document name")
    summary_type: str = Field(..., description="Type of summary generated")
    executive_summary: str = Field(..., description="Executive summary")
    technical_summary: str = Field(..., description="Technical summary")
    key_takeaways: list[str] = Field(..., description="Key takeaways as bullet points")
    
    class Config:
        json_schema_extra = {
            "example": {
                "document_id": "doc_123",
                "document_name": "ResearchPaper.pdf",
                "summary_type": "comprehensive",
                "executive_summary": "This paper presents...",
                "technical_summary": "The authors use...",
                "key_takeaways": ["Finding 1", "Finding 2"]
            }
        }