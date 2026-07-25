"""
Pydantic models for request/response validation
"""

from .document import (
    DocumentCreate,
    DocumentResponse,
    DocumentListResponse
)
from .search import (
    SearchRequest,
    SearchResult,
    SearchResponse
)
from .qa import (
    QuestionRequest,
    QuestionResponse
)
from .comparison import (
    ComparisonRequest,
    ComparisonResponse
)
from .summarization import (
    SummarizationRequest,
    SummarizationResponse
)
from .classification import (
    ClassificationResponse
)
from .analytics import (
    AnalyticsResponse
)

__all__ = [
    "DocumentCreate",
    "DocumentResponse",
    "DocumentListResponse",
    "SearchRequest",
    "SearchResult",
    "SearchResponse",
    "QuestionRequest",
    "QuestionResponse",
    "ComparisonRequest",
    "ComparisonResponse",
    "SummarizationRequest",
    "SummarizationResponse",
    "ClassificationResponse",
    "AnalyticsResponse"
]