"""
Document Management Routes
Endpoints for uploading, listing, and deleting documents
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
import logging

from app.services.document_service import DocumentService
from app.models.document import DocumentResponse, DocumentListResponse

logger = logging.getLogger(__name__)
router = APIRouter()

# Create service instance (in production, use dependency injection)
document_service = DocumentService()

@router.post("/upload", response_model=dict)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document
    
    - **file**: PDF or text document to upload
    
    Returns:
        - Document ID and metadata
    """
    try:
        logger.info(f"📤 Uploading document: {file.filename}")
        
        result = document_service.upload_document(file, file.filename)
        
        return {
            "status": "success",
            "document_id": result["document_id"],
            "metadata": result["metadata"],
            "message": result["message"]
        }
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/list", response_model=DocumentListResponse)
async def list_documents():
    """
    List all uploaded documents
    
    Returns:
        - List of all documents with metadata
    """
    try:
        documents = document_service.list_documents()
        
        return {
            "total_documents": len(documents),
            "documents": documents
        }
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str):
    """
    Get metadata for a specific document
    
    - **document_id**: ID of the document
    
    Returns:
        - Document metadata
    """
    try:
        metadata = document_service.get_document_metadata(document_id)
        
        return metadata
    except Exception as e:
        logger.error(f"Error getting document: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """
    Delete a document
    
    - **document_id**: ID of the document to delete
    
    Returns:
        - Success message
    """
    try:
        document_service.delete_document(document_id)
        
        return {
            "status": "success",
            "message": f"Document {document_id} deleted successfully"
        }
    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))