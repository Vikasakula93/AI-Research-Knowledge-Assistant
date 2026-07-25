"""
Configuration Management
Loads environment variables and provides application configuration
"""

import os
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """
    Application Settings Class
    Centralizes all configuration from environment variables
    """
    
    # ========== ENVIRONMENT & DEBUG ==========
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # ========== API CONFIGURATION ==========
    API_TITLE: str = os.getenv("API_TITLE", "AI Research & Knowledge Assistant")
    API_VERSION: str = os.getenv("API_VERSION", "1.0.0")
    API_DESCRIPTION: str = os.getenv("API_DESCRIPTION", "An intelligent assistant")
    
    # ========== SERVER CONFIGURATION ==========
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    
    # ========== DATABASE CONFIGURATION ==========
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./research_assistant.db"
    )
    SQLALCHEMY_ECHO: bool = DEBUG
    
    # ========== LLM CONFIGURATION ==========
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", 0.7))
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", 1000))
    
    # ========== EMBEDDINGS CONFIGURATION ==========
    EMBEDDINGS_MODEL: str = os.getenv(
        "EMBEDDINGS_MODEL", 
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    EMBEDDING_DIMENSION: int = int(os.getenv("EMBEDDING_DIMENSION", 384))
    
    # ========== VECTOR DATABASE CONFIGURATION ==========
    VECTOR_DB_TYPE: str = os.getenv("VECTOR_DB_TYPE", "faiss")
    PINECONE_API_KEY: Optional[str] = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT: Optional[str] = os.getenv("PINECONE_ENVIRONMENT")
    PINECONE_INDEX_NAME: Optional[str] = os.getenv("PINECONE_INDEX_NAME")
    
    # ========== DOCUMENT PROCESSING CONFIGURATION ==========
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", 50000000))  # 50MB
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", 500))  # Characters per chunk
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", 50))  # Overlap between chunks
    SUPPORTED_FILE_TYPES: List[str] = os.getenv("SUPPORTED_FILE_TYPES", "pdf,txt,docx").split(",")
    
    # ========== TENSORFLOW MODEL CONFIGURATION ==========
    TF_MODEL_PATH: str = os.getenv("TF_MODEL_PATH", "./ml_models/document_classifier.h5")
    CLASSIFICATION_CATEGORIES: List[str] = os.getenv(
        "CLASSIFICATION_CATEGORIES", 
        "AI,ML,CV,NLP,Robotics,CyberSecurity,CloudComputing"
    ).split(",")
    
    # ========== REDIS CONFIGURATION ==========
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    REDIS_DB: int = int(os.getenv("REDIS_DB", 0))
    
    # ========== LOGGING CONFIGURATION ==========
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "json")
    
    # ========== CORS CONFIGURATION ==========
    CORS_ORIGINS: List[str] = os.getenv(
        "CORS_ORIGINS", 
        "http://localhost:3000,http://localhost:8000"
    ).split(",")
    
    # ========== FILE STORAGE CONFIGURATION ==========
    UPLOAD_DIRECTORY: str = os.getenv("UPLOAD_DIRECTORY", "./uploads")
    CHUNK_STORAGE_DIRECTORY: str = os.getenv("CHUNK_STORAGE_DIRECTORY", "./data/chunks")
    
    # Create directories if they don't exist
    @classmethod
    def create_directories(cls):
        """Create necessary directories for the application"""
        for directory in [cls.UPLOAD_DIRECTORY, cls.CHUNK_STORAGE_DIRECTORY]:
            os.makedirs(directory, exist_ok=True)

# Create a global settings instance
settings = Settings()