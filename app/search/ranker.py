"""
Paper ranking using embeddings or heuristics
"""
import logging
from typing import List
from sentence_transformers import SentenceTransformer, util
from app.core.schemas import Paper
from app.core.config import settings

logger = logging.getLogger(__name__)

_model = None

def get_model() -> SentenceTransformer:
    """
    Load and return the sentence transformer model
    """
    global _model
    if _model is None:
        logger.info(f"Loading embedding model: {settings.embedding_model}")
        _model = SentenceTransformer(settings.embedding_model)
    return _model

def create_paper_text(paper: Paper) -> str:
    """
    Create searchable text from paper for embedding

    Args:
        paper: Paper object

    Returns:
        Concatenated text string
    """
    abstract_snippet = paper.abstract[:500] if paper.abstract else ""
    return f"{paper.title} {abstract_snippet}"

def rank_with_embeddings(papers: List[Paper], query: str) -> List[Paper]:
    """
    Rank papers using semantic embeddings

    Args:
        papers: List of Paper objects
        query: Search query string

    Returns:
        List of ranked Paper objects with scores
    """
    try:
        model = get_model()
        query_embedding = model.encode(query, convert_to_tensor=True)
        paper_texts = [create_paper_text(paper) for paper in papers]
        paper_embeddings = model.encode(paper_texts, convert_to_tensor=True)

        scores = util.cos_sim(query_embedding, paper_embeddings)[0]

        for i, paper in enumerate(papers):
            paper.score = float(scores[i])

        ranked_papers = sorted(papers, key=lambda p:p.score, reverse=True)
        logger.info(f"Ranked {len(papers)} papers using embeddings")
        return ranked_papers
    except Exception as e:
        logger.error(f"Error in embedding ranking: {str(e)}")
        return rank_with_heuristics(papers, query)
    
def rank_with_heuristics(papers: List[Paper], query: str) -> List[Paper]:
    """
    Rank papers using simple heuristics

    Args:
        papers: List of Paper objects
        query: Search query string

    Returns:
        List of ranked Paper objects with scores
    """
    query_terms = set(query.lower().split())
    
    for paper in papers:
        title_terms = set(paper.title.lower().split())
        abstract_terms = set(paper.abstract.lower().split()) if paper.abstract else set()

        title_matches = len(query_terms.intersection(title_terms))
        abstract_matches = len(query_terms.intersection(abstract_terms))

        paper.score = (title_matches * 2 + abstract_matches) / (len(query_terms) + 1)

    ranked_papers = sorted(papers, key=lambda p:p.score, reverse=True)
    logger.info(f"Ranked {len(papers)} papers using heuristics")
    return ranked_papers

def rank_papers(papers: List[Paper], query: str, use_embeddings: bool) -> List[Paper]:
    """
    Rank papers using embeddings or fallback to heuristics

    Args:
        papers: List of Paper objects
        query: Search query string

    Returns:
        List of ranked Paper objects
    """
    if not papers:
        return []
    
    if use_embeddings:
        return rank_with_embeddings(papers, query)
    else:
        return rank_with_heuristics(papers, query)