"""
FastAPI application entry point
"""
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from typing import List

from app.core.schemas import SearchRequest, Paper
from app.core.config import settings
from app.search.engine import search_papers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Academic Paper Search engine",
    description="Search and rank academic papers from arXiv and Semantic Scholar",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "service": "paper-search-engine"}

@app.post("/api/search", response_model=List[Paper])
async def search_endpoint(request: SearchRequest) -> List[Paper]:
    """
    Search academic papers across multiple sources

    Args:
        request: SearchRequest with query and optional top_k

    Returns:
        List of ranked Paper objects
    """
    try:
        if not request.query or len(request.query.strip()) < 3:
            raise HTTPException(status_code=400, detail="query too short (min 3 chars)")
        
        top_k = request.top_k or settings.default_top_k
        use_embeddings = request.use_embeddings if request.use_embeddings is not None else settings.use_embeddings
        logger.info(f"Search request: query='{request.query}', top_k={top_k}, use_embeddings={use_embeddings}")

        results = await search_papers(request.query, top_k, use_embeddings)
        logger.info(f"Returning {len(results)} results")
        return results
    
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Search failed: {e}, exc_info=True")
        raise HTTPException(status_code=500, detail="Internal search error")
    
@app.get("/test/search", response_model=List[Paper])
async def test_search(query: str, top_k: int = None, use_embeddings: bool = True) -> List[Paper]:
    """
    Test endpoint with GET method

    Args:
        query: Search query string
        top_k: Number of top results to return
        use_embeddings: Whether to use embedding-based search
    
    Returns:
        List of ranked Paper objects
    """
    request = SearchRequest(query=query, top_k=top_k, use_embeddings=use_embeddings)
    return await search_endpoint(request)
