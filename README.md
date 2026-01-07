# Academic Paper Search Engine

Minimal FastAPI backend for searching academic papers from arXiv and Semantic Scholar.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env and add your Semantic Scholar API key
```

3. Run the server:
```bash
uvicorn app.main:app --reload
```

## Usage

### POST /api/search
```bash
curl -X POST http://localhost:8000/api/search -H "Content-Type: application/json" -d '{"query": "lstms stock forecast", "top_k": 20}'
```

### GET /test/search
```bash
curl "http://localhost:8000/test/search?query=lstms%20stock%20forecast&top_k=20"
```

### Browser test
```
http://localhost:8000/test/search?query=lstms%20stock%20forecast
```

## API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Configuration

All settings in `.env`:
- `SEMANTIC_SCHOLAR_KEY`: Required API key
- `USE_EMBEDDINGS`: Enable semantic ranking (default: true)
- `EMBEDDING_MODEL`: Model name (default: all-MiniLM-L6-v2)
- `MAX_RESULTS_PER_SOURCE`: Papers per source (default: 40)
- `DEFAULT_TOP_K`: Default results returned (default: 20)

## Architecture

- `app/main.py`: FastAPI app and endpoints
- `app/core/`: Configuration and schemas
- `app/search/engine.py`: Search orchestrator
- `app/search/sources/`: arXiv and Semantic Scholar clients
- `app/search/normalizer.py`: Paper normalisation and deduplication
- `app/search/ranker.py`: Embedding-based ranking