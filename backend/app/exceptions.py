"""
Custom Exception Classes and Exception Handlers
Defines application-specific exceptions and their handling
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

class ApplicationException(Exception):
    """Base exception class for all application exceptions"""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: str = "INTERNAL_ERROR"
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)

class DocumentNotFoundError(ApplicationException):
    """Raised when a document is not found"""
    
    def __init__(self, message: str = "Document not found"):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="DOCUMENT_NOT_FOUND"
        )

class InvalidFileTypeError(ApplicationException):
    """Raised when an unsupported file type is uploaded"""
    
    def __init__(self, message: str = "Invalid file type"):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="INVALID_FILE_TYPE"
        )

class FileTooLargeError(ApplicationException):
    """Raised when uploaded file exceeds maximum size"""
    
    def __init__(self, message: str = "File size exceeds maximum limit"):
        super().__init__(
            message=message,
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            error_code="FILE_TOO_LARGE"
        )

class ProcessingError(ApplicationException):
    """Raised when document processing fails"""
    
    def __init__(self, message: str = "Error processing document"):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="PROCESSING_ERROR"
        )

class VectorDatabaseError(ApplicationException):
    """Raised when vector database operations fail"""
    
    def __init__(self, message: str = "Vector database error"):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="VECTOR_DB_ERROR"
        )

class LLMError(ApplicationException):
    """Raised when LLM operations fail"""
    
    def __init__(self, message: str = "LLM error"):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="LLM_ERROR"
        )

def setup_exception_handlers(app: FastAPI):
    """
    Register all exception handlers with the FastAPI application
    
    Args:
        app (FastAPI): The FastAPI application instance
    """
    
    @app.exception_handler(ApplicationException)
    async def application_exception_handler(request: Request, exc: ApplicationException):
        """Handle application exceptions"""
        
        logger.error(f"Application Exception: {exc.error_code} - {exc.message}")
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.error_code,
                    "message": exc.message,
                    "path": str(request.url)
                }
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle unexpected exceptions"""
        
        logger.error(f"Unexpected Exception: {str(exc)}")
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred",
                    "path": str(request.url)
                }
            }
        )