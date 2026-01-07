"""
Semantic Scholar API client
"""
import logging
from typing import List, Dict
from semanticscholar import SemanticScholar

logger = logging.getLogger(__name__)

async def search_ss(query: str, max_results: int, api_key: str = None) -> List[Dict]:
    """
    Search Semantic Scholar for papers matching the query

    Args:
        query: Search query string
        max_results: Maximum number of results to return
        api_key: Semantic Scholar API key
    
    Returns:
        List of dictionaries representing papers
    """
    try:
        client = SemanticScholar(api_key=api_key) if api_key else SemanticScholar()
        search_results = client.search_paper(query, limit=max_results, fields=[
            "title", "authors", "abstract", "year", "publicationDate", "paperId", "externalIds", "openAccessPdf", "citationCount"
        ])

        results = []
        for i, paper in enumerate(search_results):
            if i >= max_results:
                break

            pdf_url = None
            if paper.openAccessPdf:
                pdf_url = paper.openAccessPdf.get("url") if hasattr(paper.openAccessPdf, 'get') else paper.openAccessPdf.url
            doi = None
            arxiv_id = None
            if paper.externalIds:
                doi = paper.externalIds.get("DOI")
                arxiv_id = paper.externalIds.get("ArXiv")
            results.append({
                "title": paper.title or "",
                "authors": [author.get("name", "") if hasattr(author, 'get') else author.name for author in paper.authors] if paper.authors else [],
                "abstract": paper.abstract or "Abstract unavailable (publisher restriction).",
                "published_date": paper.publicationDate or None,
                "arxiv_id": arxiv_id,
                "doi": doi,
                "pdf_url": pdf_url,
                "source": "semantic_scholar",
                "citation_count": paper.citationCount if hasattr(paper, 'citationCount') else None
            })
        logger.info(f"Retrieved {len(results)} papers from Semantic Scholar")
        return results
    except Exception as e:
        logger.error(f"Error searching Semantic Scholar: {str(e)}")
        return []