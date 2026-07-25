"""
Main FastAPI Application Entry Point
Initializes the FastAPI application and registers all routes
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.config import settings
from app.routes import (
    documents,
    search,
    qa,
    comparison,
    summarization,
    classification,
    analytics
)
from app.exceptions import setup_exception_handlers

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """
    Factory function to create and configure the FastAPI application
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    
    # Create FastAPI instance
    app = FastAPI(
        title=settings.API_TITLE,
        description=settings.API_DESCRIPTION,
        version=settings.API_VERSION,
        debug=settings.DEBUG
    )
    
    # ========== MIDDLEWARE CONFIGURATION ==========
    
    # CORS Middleware - Allow cross-origin requests
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # ========== EXCEPTION HANDLERS ==========
    setup_exception_handlers(app)
    
    # ========== ROUTE REGISTRATION ==========
    
    # Register all route modules
    app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
    app.include_router(search.router, prefix="/api/search", tags=["Search"])
    app.include_router(qa.router, prefix="/api/qa", tags=["Q&A"])
    app.include_router(comparison.router, prefix="/api/compare", tags=["Comparison"])
    app.include_router(summarization.router, prefix="/api/summarize", tags=["Summarization"])
    app.include_router(classification.router, prefix="/api/classify", tags=["Classification"])
    app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
    
    # ========== HEALTH CHECK ENDPOINT ==========
    @app.get("/health", tags=["Health"])
    async def health_check():
        """
        Health check endpoint to verify the application is running
        
        Returns:
            dict: Status and timestamp
        """
        return {
            "status": "healthy",
            "version": settings.API_VERSION,
            "environment": settings.ENVIRONMENT
        }
    
    # ========== ROOT ENDPOINT ==========
    @app.get("/", tags=["Root"])
    async def root():
        """
        Root endpoint providing API information
        
        Returns:
            dict: API information and available endpoints
        """
        return {
            "message": "AI Research & Knowledge Assistant API",
            "version": settings.API_VERSION,
            "docs": "/docs",
            "openapi_schema": "/openapi.json"
        }
    
    # Create necessary directories
    settings.create_directories()
    
    logger.info("✅ FastAPI Application initialized successfully")
    return app

# Create the application instance
app = create_app()

# If running directly
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )