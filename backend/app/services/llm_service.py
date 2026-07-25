"""
LLM Service
Handles interactions with Large Language Models (OpenAI)
"""

import logging
from typing import List, Optional
import openai

from app.config import settings

logger = logging.getLogger(__name__)

class LLMService:
    """
    Service for interacting with LLMs
    Currently implements OpenAI API
    """
    
    def __init__(self):
        """Initialize LLM service"""
        if not settings.OPENAI_API_KEY:
            logger.warning("⚠️ OpenAI API key not configured")
            raise ValueError("OPENAI_API_KEY not set in environment")
        
        openai.api_key = settings.OPENAI_API_KEY
        self.model = settings.LLM_MODEL
        self.temperature = settings.LLM_TEMPERATURE
        self.max_tokens = settings.LLM_MAX_TOKENS
        logger.info(f"✅ LLM Service initialized with model: {self.model}")
    
    def generate_response(
        self,
        messages: List[dict],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate a response from LLM
        
        Args:
            messages (List[dict]): Conversation messages in OpenAI format
            temperature (Optional[float]): Temperature for response generation
            max_tokens (Optional[int]): Maximum tokens in response
            
        Returns:
            str: Generated response text
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens
            )
            
            answer = response.choices[0].message.content
            logger.info("✅ LLM response generated successfully")
            return answer
            
        except Exception as e:
            logger.error(f"Error generating LLM response: {str(e)}")
            raise
    
    def answer_question(
        self,
        question: str,
        context: List[str],
        document_names: List[str]
    ) -> dict:
        """
        Answer a question based on provided context
        
        Args:
            question (str): User's question
            context (List[str]): Retrieved context chunks
            document_names (List[str]): Names of source documents
            
        Returns:
            dict: Contains answer, confidence, and metadata
        """
        try:
            # Prepare context string
            context_str = "\n\n".join([f"[Context {i+1}]\n{chunk}" for i, chunk in enumerate(context)])
            
            # Create prompt for Q&A
            system_prompt = """You are an expert research assistant. 
            Answer the user's question based ONLY on the provided context. 
            If the answer cannot be found in the context, clearly state that.
            Keep your answer concise and well-structured."""
            
            user_prompt = f"""Context from research documents:
{context_str}

Question: {question}

Answer based only on the above context. If the information is not available, say so clearly."""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            # Generate response
            answer = self.generate_response(messages)
            
            # Calculate confidence based on context relevance
            confidence = min(len(context) * 0.3, 1.0)
            
            return {
                "answer": answer,
                "confidence": confidence,
                "source_documents": document_names,
                "context_used": len(context)
            }
            
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            raise
    
    def summarize_document(
        self,
        text: str,
        summary_type: str = "comprehensive"
    ) -> dict:
        """
        Summarize a document
        
        Args:
            text (str): Document text to summarize
            summary_type (str): Type of summary (executive, technical, bullet_points)
            
        Returns:
            dict: Contains different types of summaries
        """
        try:
            # Create summarization prompts
            prompts = {
                "executive": "Provide a 2-3 sentence executive summary of this text.",
                "technical": "Provide a detailed technical summary of this text covering methodology and findings.",
                "bullet_points": "Provide key points as a bullet-point summary (5-7 points)."
            }
            
            summaries = {}
            
            for summary_type_name, prompt in prompts.items():
                user_prompt = f"{prompt}\n\nText:\n{text[:3000]}"  # Limit text length
                
                messages = [
                    {"role": "system", "content": "You are an expert at summarizing documents."},
                    {"role": "user", "content": user_prompt}
                ]
                
                summary = self.generate_response(messages, max_tokens=500)
                summaries[summary_type_name] = summary
            
            logger.info(f"✅ Document summaries generated")
            return summaries
            
        except Exception as e:
            logger.error(f"Error summarizing document: {str(e)}")
            raise
    
    def compare_documents(
        self,
        documents_content: dict,
        comparison_aspects: Optional[List[str]] = None
    ) -> dict:
        """
        Compare multiple documents
        
        Args:
            documents_content (dict): {doc_name: content}
            comparison_aspects (Optional[List[str]]): Aspects to compare
            
        Returns:
            dict: Comparison results
        """
        try:
            doc_summaries = "\n\n".join([
                f"Document: {name}\nContent: {content[:1000]}"
                for name, content in documents_content.items()
            ])
            
            prompt = f"""Compare the following documents:

{doc_summaries}

Provide:
1. Similarities between the documents
2. Key differences
3. Comparison of methodologies (if applicable)
4. Comparison of conclusions (if applicable)
"""
            
            messages = [
                {"role": "system", "content": "You are an expert at comparing research documents."},
                {"role": "user", "content": prompt}
            ]
            
            comparison = self.generate_response(messages, max_tokens=1000)
            
            logger.info("✅ Document comparison generated")
            return {
                "comparison": comparison,
                "documents_compared": list(documents_content.keys())
            }
            
        except Exception as e:
            logger.error(f"Error comparing documents: {str(e)}")
            raise