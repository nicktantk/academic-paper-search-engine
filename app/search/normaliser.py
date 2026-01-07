"""
Paper normalisation and deduplication
"""
import logging
from typing import List, Dict
from difflib import SequenceMatcher
from app.core.schemas import Paper

logger = logging.getLogger(__name__)

def normalise_paper(raw_paper: Dict) -> Paper:
    """
    Normalise a raw paper dictionary into a Paper object

    Args:
        raw_paper: Dictionary with raw paper data

    Returns:
        Normalised Paper object
    """
    return Paper(
        title=raw_paper.get("title", ""),
        authors=raw_paper.get("authors", []),
        abstract=raw_paper.get("abstract", "").strip(),
        published_date=raw_paper.get("published_date"),
        arxiv_id=raw_paper.get("arxiv_id"),
        doi=raw_paper.get("doi"),
        pdf_url=raw_paper.get("pdf_url"),
        source=raw_paper.get("source", "unknown"),
    )

def title_similarity(title1: str, title2: str) -> float:
    """
    Compute similarity between two titles using SequenceMatcher

    Args:
        title1: First title string
        title2: Second title string

    Returns:
        Similarity ratio between 0 and 1
    """
    return SequenceMatcher(None, title1.lower(), title2.lower()).ratio()

def deduplicate_papers(papers: List[Paper], similarity_threshold: float = 0.9) -> List[Paper]:
    """
    Remove duplicate papers based on title similarity

    Args:
        papers: List of Paper objects
        similarity_threshold: Threshold above which papers are considered duplicates

    Returns:
        List of deduplicated Paper objects
    """
    if not papers:
        return []
    unique_papers = []
    seen_titles = []

    for paper in papers:
        is_duplicate = False
        for seen_title in seen_titles:
            if title_similarity(paper.title, seen_title) >= similarity_threshold:
                is_duplicate = True
                logger.debug(f"Duplicate found: '{paper.title}' is similar to '{seen_title}'")
                break
        if not is_duplicate:
            unique_papers.append(paper)
            seen_titles.append(paper.title)

    logger.info(f"Deduplicated papers: {len(papers)} -> {len(unique_papers)}")
    return unique_papers

def normalise_papers(raw_papers: List[Dict]) -> List[Paper]:
    """
    Normalise and deduplicate a list of raw paper dictionaries

    Args:
        raw_papers: List of dictionaries with raw paper data

    Returns:
        List of normalised and deduplicated Paper objects
    """
    normalised_papers = [normalise_paper(rp) for rp in raw_papers]
    return deduplicate_papers(normalised_papers)
