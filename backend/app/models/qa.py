"""
Question Answering related Pydantic models
"""

from pydantic import BaseModel, Field
from typing import Optional

class QuestionRequest(BaseModel):
    """
    Request model for asking questions
    """
    question: str = Field(..., min_length=1, description="User's question")
    document_ids: Optional[list[str]] = Field(
        None,
        description="Specific documents to reference (if None, use all)"
    )
    conversation_context: Optional[list[dict]] = Field(
        None,
        description="Previous conversation messages for context"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What are the main findings of this research?",
                "document_ids": None,
                "conversation_context": None
            }
        }

class QuestionResponse(BaseModel):
    """
    Response model for Q&A
    """
    question: str = Field(..., description="The asked question")
    answer: str = Field(..., description="Generated answer")
    source_documents: list[str] = Field(..., description="Document IDs referenced")
    source_pages: list[int] = Field(..., description="Page numbers referenced")
    confidence_score: float = Field(..., ge=0, le=1, description="Confidence in the answer")
    retrieved_context: list[str] = Field(..., description="Retrieved context chunks")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What are neural networks?",
                "answer": "Neural networks are computational models inspired by biological networks...",
                "source_documents": ["doc_123"],
                "source_pages": [5, 6],
                "confidence_score": 0.92,
                "retrieved_context": ["Neural networks are..."]
            }
        }