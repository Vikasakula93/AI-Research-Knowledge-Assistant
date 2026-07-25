"""
Document Service
Handles document upload, storage, and metadata management
"""

import os
import uuid
from datetime import datetime
from typing import List, Optional
import PyPDF2
import logging

from app.config import settings
from app.exceptions import (
    InvalidFileTypeError,
    FileTooLargeError,
    ProcessingError,
    DocumentNotFoundError
)

logger = logging.getLogger(__name__)

class DocumentService:
    """
    Service for handling document operations
    Manages upload, storage, retrieval, and deletion
    """
    
    def __init__(self):
        """Initialize the document service"""
        self.upload_dir = settings.UPLOAD_DIRECTORY
        self.supported_types = settings.SUPPORTED_FILE_TYPES
        self.max_size = settings.MAX_UPLOAD_SIZE
        # In-memory storage (replace with database in production)
        self.documents_metadata = {}
    
    def validate_file(self, filename: str, file_size: int) -> bool:
        """
        Validate uploaded file
        
        Args:
            filename (str): Name of the file
            file_size (int): Size of the file in bytes
            
        Returns:
            bool: True if valid
            
        Raises:
            InvalidFileTypeError: If file type not supported
            FileTooLargeError: If file exceeds max size
        """
        # Check file extension
        file_extension = filename.split('.')[-1].lower()
        if file_extension not in self.supported_types:
            raise InvalidFileTypeError(
                f"File type '.{file_extension}' not supported. "
                f"Supported types: {', '.join(self.supported_types)}"
            )
        
        # Check file size
        if file_size > self.max_size:
            raise FileTooLargeError(
                f"File size {file_size / 1024 / 1024:.2f}MB exceeds "
                f"maximum {self.max_size / 1024 / 1024:.2f}MB"
            )
        
        return True
    
    def extract_pdf_info(self, file_path: str) -> dict:
        """
        Extract information from PDF file
        
        Args:
            file_path (str): Path to the PDF file
            
        Returns:
            dict: Contains page count and basic info
            
        Raises:
            ProcessingError: If PDF extraction fails
        """
        try:
            with open(file_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                total_pages = len(pdf_reader.pages)
                
                # Extract text from first page for validation
                first_page_text = pdf_reader.pages[0].extract_text()
                
                return {
                    "total_pages": total_pages,
                    "is_valid": True,
                    "first_page_preview": first_page_text[:200]
                }
        except Exception as e:
            logger.error(f"Error extracting PDF info: {str(e)}")
            raise ProcessingError(f"Failed to extract PDF information: {str(e)}")
    
    def save_document_metadata(
        self,
        document_id: str,
        filename: str,
        file_path: str,
        file_size: int,
        pdf_info: dict
    ) -> dict:
        """
        Save document metadata
        
        Args:
            document_id (str): Unique document ID
            filename (str): Original filename
            file_path (str): Path where file is stored
            file_size (int): Size in bytes
            pdf_info (dict): PDF information
            
        Returns:
            dict: Saved metadata
        """
        metadata = {
            "document_id": document_id,
            "document_name": filename,
            "file_name": filename,
            "file_path": file_path,
            "file_size": file_size,
            "upload_timestamp": datetime.now().isoformat(),
            "total_pages": pdf_info.get("total_pages", 0),
            "total_chunks": 0,
            "processing_status": "pending",
            "document_type": "research_paper",
            "classification": None
        }
        
        # Store in memory (replace with database)
        self.documents_metadata[document_id] = metadata
        logger.info(f"✅ Document metadata saved: {document_id}")
        
        return metadata
    
    def upload_document(self, file, filename: str) -> dict:
        """
        Upload a document
        
        Args:
            file: File object from request
            filename (str): Original filename
            
        Returns:
            dict: Upload result with document ID and metadata
        """
        # Read file content
        file_content = file.file.read()
        file_size = len(file_content)
        
        # Validate file
        self.validate_file(filename, file_size)
        
        # Generate unique document ID
        document_id = f"doc_{uuid.uuid4().hex[:8]}"
        
        # Save file to disk
        file_path = os.path.join(self.upload_dir, f"{document_id}_{filename}")
        os.makedirs(self.upload_dir, exist_ok=True)
        
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        logger.info(f"📄 File saved: {file_path}")
        
        # Extract PDF info
        pdf_info = self.extract_pdf_info(file_path)
        
        # Save metadata
        metadata = self.save_document_metadata(
            document_id,
            filename,
            file_path,
            file_size,
            pdf_info
        )
        
        return {
            "document_id": document_id,
            "metadata": metadata,
            "message": "Document uploaded successfully"
        }
    
    def get_document_metadata(self, document_id: str) -> dict:
        """
        Get metadata for a specific document
        
        Args:
            document_id (str): Document ID
            
        Returns:
            dict: Document metadata
            
        Raises:
            DocumentNotFoundError: If document not found
        """
        if document_id not in self.documents_metadata:
            raise DocumentNotFoundError(f"Document {document_id} not found")
        
        return self.documents_metadata[document_id]
    
    def list_documents(self) -> List[dict]:
        """
        List all uploaded documents
        
        Returns:
            List[dict]: List of all document metadata
        """
        return list(self.documents_metadata.values())
    
    def delete_document(self, document_id: str) -> bool:
        """
        Delete a document
        
        Args:
            document_id (str): Document ID to delete
            
        Returns:
            bool: True if deleted successfully
            
        Raises:
            DocumentNotFoundError: If document not found
        """
        if document_id not in self.documents_metadata:
            raise DocumentNotFoundError(f"Document {document_id} not found")
        
        metadata = self.documents_metadata[document_id]
        file_path = metadata.get("file_path")
        
        # Delete file from disk
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"🗑️ File deleted: {file_path}")
        
        # Delete metadata
        del self.documents_metadata[document_id]
        logger.info(f"✅ Document deleted: {document_id}")
        
        return True
    
    def update_processing_status(self, document_id: str, status: str, chunks_count: int = 0):
        """
        Update document processing status
        
        Args:
            document_id (str): Document ID
            status (str): New processing status
            chunks_count (int): Number of chunks created
        """
        if document_id in self.documents_metadata:
            self.documents_metadata[document_id]["processing_status"] = status
            if chunks_count > 0:
                self.documents_metadata[document_id]["total_chunks"] = chunks_count
            logger.info(f"📊 Document status updated: {document_id} -> {status}")