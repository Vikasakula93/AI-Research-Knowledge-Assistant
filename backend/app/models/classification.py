"""
Document Classification related Pydantic models
"""

from pydantic import BaseModel, Field
from typing import Optional

class ClassificationResponse(BaseModel):
    """
    Response model for document classification
    """
    document_id: str = Field(..., description="Document ID")
    document_name: str = Field(..., description="Document name")
    predicted_category: str = Field(..., description="Predicted document category")
    confidence: float = Field(..., ge=0, le=1, description="Classification confidence")
    all_predictions: dict = Field(..., description="All category predictions with scores")
    
    class Config:
        json_schema_extra = {
            "example": {
                "document_id": "doc_123",
                "document_name": "Research.pdf",
                "predicted_category": "Machine Learning",
                "confidence": 0.92,
                "all_predictions": {
                    "Machine Learning": 0.92,
                    "AI": 0.05,
                    "Computer Vision": 0.03
                }
            }
        }