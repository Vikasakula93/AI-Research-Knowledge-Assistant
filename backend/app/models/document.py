"""
Document-related Pydantic models
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class DocumentCreate(BaseModel):
    """
    Request model for creating/uploading a document
    """
    file_name: str = Field(..., description="Original file name")
    document_type: str = Field(default="research_paper", description="Type of document")
    
    class Config:
        json_schema_extra = {
            "example": {
                "file_name": "research_paper.pdf",
                "document_type": "research_paper"
            }
        }

class DocumentResponse(BaseModel):
    """
    Response model for a single document
    """
    document_id: str = Field(..., description="Unique document identifier")
    document_name: str = Field(..., description="Display name of the document")
    file_name: str = Field(..., description="Original file name")
    upload_timestamp: datetime = Field(..., description="When the document was uploaded")
    total_pages: int = Field(..., description="Number of pages in the PDF")
    total_chunks: int = Field(..., description="Number of chunks created from the document")
    processing_status: str = Field(..., description="Current processing status")
    document_type: str = Field(..., description="Type of document")
    file_size: int = Field(..., description="File size in bytes")
    classification: Optional[str] = Field(None, description="Classified category")
    
    class Config:
        json_schema_extra = {
            "example": {
                "document_id": "doc_123abc",
                "document_name": "ResearchPaper.pdf",
                "file_name": "ResearchPaper.pdf",
                "upload_timestamp": "2024-01-15T10:30:00",
                "total_pages": 25,
                "total_chunks": 120,
                "processing_status": "completed",
                "document_type": "research_paper",
                "file_size": 5242880,
                "classification": "Machine Learning"
            }
        }

class DocumentListResponse(BaseModel):
    """
    Response model for listing documents
    """
    total_documents: int = Field(..., description="Total number of documents")
    documents: list[DocumentResponse] = Field(..., description="List of documents")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_documents": 2,
                "documents": []
            }
        }