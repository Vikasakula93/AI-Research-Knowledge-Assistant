"""
Question Answering Routes
Endpoints for Q&A with documents
"""

from fastapi import APIRouter, HTTPException
import logging
from typing import Optional
import uuid

from app.services.qa_service import QAService
from app.services.search_service import SearchService
from app.services.embedding_service import EmbeddingService
from app.services.vector_db_service import VectorDatabaseService
from app.services.llm_service import LLMService
from app.models.qa import QuestionRequest, QuestionResponse

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
embedding_service = EmbeddingService()
vector_db_service = VectorDatabaseService(embedding_service.get_embedding_dimension())
search_service = SearchService(embedding_service, vector_db_service)
llm_service = LLMService()
qa_service = QAService(search_service, llm_service)

@router.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question about the documents
    
    - **question**: User's question
    - **document_ids**: Optional specific documents to search
    - **conversation_context**: Optional previous messages for context
    
    Returns:
        - Answer with source documents, pages, and confidence score
    """
    try:
        # Generate session ID if not provided
        session_id = str(uuid.uuid4())
        
        logger.info(f"❓ Question asked: {request.question}")
        
        result = qa_service.answer_question(
            request.question,
            session_id,
            request.document_ids,
            search_mode="semantic"
        )
        
        return result
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/context/{session_id}")
async def get_conversation_context(session_id: str):
    """
    Get conversation context for a session
    
    - **session_id**: Session ID
    
    Returns:
        - Conversation history
    """
    try:
        context = qa_service.get_conversation_context(session_id)
        
        return {
            "session_id": session_id,
            "conversation_length": len(context),
            "context": context
        }
    except Exception as e:
        logger.error(f"Error retrieving context: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))