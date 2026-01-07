"""
Pydantic models for API requests and responses
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Paper(BaseModel):
    """Normalised paper model"""

    title: str
    authors: List[str]
    abstract: str
    published_date: Optional[datetime] = None
    arxiv_id: Optional[str] = None
    doi: Optional[str] = None
    pdf_url: Optional[str] = None
    source: str
    score: float = Field(default=0.0, description="Relevance score")
    citation_count: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "LSTM Networks for Stock Price Prediction",
                "authors": ["John Doe", "Nicholas Tan"],
                "abstract": "This paper explores...",
                "published_date": "2026-01-07T00:00:00",
                "arxiv_id": "1234.56789",
                "doi": "10.1000/sampledoi",
                "pdf_url": "http://arxiv.org/pdf/1234.56789.pdf",
                "source": "arXiv",
                "citation_count": 42,
                "score": 0.95
            }
        }

class SearchRequest(BaseModel):
    """Search request model"""

    query: str = Field(..., min_length=1, description="Search query")
    top_k: Optional[int] = Field(None, gt=0, le=100, description="Number of top results to return")
    use_embeddings: Optional[bool] = Field(True, description="Whether to use embedding-based search")

    class Config:
        json_schema_extra = {
            "example": {
                "query": "lstm networks for stock prediction",
                "top_k": 20,
                "use_embeddings": True
            }
        }