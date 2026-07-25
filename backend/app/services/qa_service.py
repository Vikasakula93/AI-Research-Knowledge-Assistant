"""
Q&A Service
Handles question answering with conversation context
"""

import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class QAService:
    """
    Service for question answering operations
    """
    
    def __init__(self, search_service, llm_service):
        """
        Initialize Q&A service
        
        Args:
            search_service: Search service for retrieving context
            llm_service: LLM service for generating answers
        """
        self.search_service = search_service
        self.llm_service = llm_service
        self.conversation_history = {}  # Store conversation context
    
    def answer_question(
        self,
        question: str,
        session_id: str,
        document_ids: Optional[List[str]] = None,
        search_mode: str = "semantic"
    ) -> dict:
        """
        Answer a user's question
        
        Args:
            question (str): User's question
            session_id (str): Session ID for conversation context
            document_ids (Optional[List[str]]): Specific documents to search
            search_mode (str): Search strategy (semantic, keyword, hybrid)
            
        Returns:
            dict: Answer with sources and confidence
        """
        try:
            # Retrieve relevant context
            if search_mode == "semantic":
                results = self.search_service.semantic_search(question, top_k=5, document_ids=document_ids)
            elif search_mode == "keyword":
                results = self.search_service.keyword_search(question, top_k=5, document_ids=document_ids)
            else:  # hybrid
                results = self.search_service.hybrid_search(question, top_k=5, document_ids=document_ids)
            
            if not results:
                return {
                    "question": question,
                    "answer": "Sorry, I couldn't find relevant information in the documents to answer your question.",
                    "source_documents": [],
                    "source_pages": [],
                    "confidence_score": 0.0,
                    "retrieved_context": []
                }
            
            # Extract context and metadata
            context = [result["content"] for result in results]
            source_docs = list(set([result["document_id"] for result in results]))
            source_pages = list(set([result["page_number"] for result in results]))
            document_names = list(set([result["document_name"] for result in results]))
            
            # Generate answer using LLM
            llm_response = self.llm_service.answer_question(question, context, document_names)
            
            # Store in conversation history
            if session_id not in self.conversation_history:
                self.conversation_history[session_id] = []
            
            self.conversation_history[session_id].append({
                "question": question,
                "answer": llm_response["answer"],
                "sources": source_docs
            })
            
            logger.info(f"✅ Answer generated for session {session_id}")
            
            return {
                "question": question,
                "answer": llm_response["answer"],
                "source_documents": source_docs,
                "source_pages": sorted(source_pages),
                "confidence_score": llm_response["confidence"],
                "retrieved_context": context[:3]  # Top 3 chunks
            }
            
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            raise
    
    def get_conversation_context(self, session_id: str) -> List[dict]:
        """
        Get conversation history for a session
        
        Args:
            session_id (str): Session ID
            
        Returns:
            List[dict]: Conversation history
        """
        return self.conversation_history.get(session_id, [])