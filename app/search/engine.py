"""
Main search orchestrator
"""
import asyncio
import logging
from typing import List
from app.core.schemas import Paper
from app.core.config import settings
from app.search.ss_client import search_ss
from app.search.normaliser import normalise_papers
from app.search.ranker import rank_papers

logger = logging.getLogger(__name__)

async def search_papers(query: str, top_k: int, use_embeddings: bool = True) -> List[Paper]:
    """
    Search for papers across multiple sources and return ranked results
    
    Args:
        query: Search query string
        top_k: Number of top results to return

    Returns:
        List of top ranked papers
    """
    if top_k is None:
        top_k = settings.default_top_k
    
    logger.info(f"Starting search for query: '{query}' with top_k={top_k}")

    ss_task = search_ss(query, top_k * 2, settings.semantic_scholar_key)

    ss_results = await ss_task

    logger.info(f"Retrieved {len(ss_results)} total papers from sources")

    normalised_papers = normalise_papers(ss_results)
    ranked_papers = rank_papers(normalised_papers, query, use_embeddings)

    result = ranked_papers[:top_k]
    logger.info(f"Returning top {len(result)} papers")
    return result