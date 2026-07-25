"""
Document Comparison related Pydantic models
"""

from pydantic import BaseModel, Field
from typing import Optional

class ComparisonRequest(BaseModel):
    """
    Request model for comparing documents
    """
    document_ids: list[str] = Field(..., min_items=2, description="IDs of documents to compare")
    comparison_aspects: Optional[list[str]] = Field(
        None,
        description="Specific aspects to compare (e.g., 'methodology', 'findings')"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "document_ids": ["doc_123", "doc_456"],
                "comparison_aspects": ["methodology", "conclusions"]
            }
        }

class ComparisonResponse(BaseModel):
    """
    Response model for document comparison
    """
    compared_documents: list[str] = Field(..., description="Document names compared")
    similarities: str = Field(..., description="Identified similarities")
    differences: str = Field(..., description="Identified differences")
    detailed_comparison: dict = Field(..., description="Aspect-by-aspect comparison")
    
    class Config:
        json_schema_extra = {
            "example": {
                "compared_documents": ["Paper1.pdf", "Paper2.pdf"],
                "similarities": "Both papers use deep learning...",
                "differences": "Paper 1 focuses on CNN while Paper 2 focuses on RNN...",
                "detailed_comparison": {
                    "methodology": "...",
                    "conclusions": "..."
                }
            }
        }