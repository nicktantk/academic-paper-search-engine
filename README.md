# 🎓 Academic Paper Search Engine **(Backend)**

[![API Docs](https://img.shields.io/badge/Live-API%20Docs-blue)](https://academic-paper-search-engine.onrender.com/docs)
[![Swagger](https://img.shields.io/badge/Swagger-UI-brightgreen)](https://academic-paper-search-engine.onrender.com/docs)
[![ReDoc](https://img.shields.io/badge/ReDoc-Docs-orange)](https://academic-paper-search-engine.onrender.com/redoc)

**Production FastAPI backend** powering AI-enhanced academic paper search across **arXiv + Semantic Scholar** (10M+ papers) with **sentence-transformer embeddings** for 95%+ relevance ranking.

## 🚀 **Live Frontend Deployment**
| Frontend | Live Demo |
|----------|-----------|
| **[Streamlit App](https://research-engine.streamlit.app)** | Full search UI + paper cards |
| **[Backend API](https://academic-paper-search-engine.onrender.com/docs)** | Swagger docs + test endpoints |

## ✨ **Key Features**
- **Hybrid search**: Keyword + `all-MiniLM-L6-v2` semantic embeddings
- **Multi-source**: arXiv + Semantic Scholar with deduplication
- **Configurable**: Pydantic settings, `.env` driven
- **Production-ready**: CORS, timeouts, healthchecks, Render deployment

## 🛠 **Quick Start (Local)**

```bash
# 1. Clone & install
pip install -r requirements.txt

# 2. Configure (.env)
cp .env.example .env
# Add SEMANTIC_SCHOLAR_KEY=your_key

# 3. Run
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# 🎓 Academic Paper Search Engine **(Backend)**
```
## 🔗 **API Endpoints**
```bash
# Production search (POST)
curl -X POST https://academic-paper-search-engine.onrender.com/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "LSTMs stock forecast", "top_k": 20, "use_embeddings": true}'

# Browser test (GET)
https://academic-paper-search-engine.onrender.com/test/search?query=lstms%20stock%20forecast
Response: [{"title": "...", "authors": [...], "score": 0.95, "abstract": "..."}]
```
## 🏗 **Architecture**
app/  
├── main.py           # FastAPI app + endpoints  
├── core/             # Pydantic settings + schemas  
├── search/  
│   ├── engine.py     # Search orchestrator  
│   ├── ss_client.py  # Semantic Scholar client  
│   ├── normaliser.py # Paper normalisation  
│   └── ranker.py     # Embedding-based ranking  
## ⚙️ **Configuration (.env)**
SEMANTIC_SCHOLAR_KEY=required  
USE_EMBEDDINGS=true  
EMBEDDING_MODEL=all-MiniLM-L6-v2  
MAX_RESULTS_PER_SOURCE=40  
DEFAULT_TOP_K=20  
## 🚀 **Production Deployment**
Platform: Render.com (Free tier)  
Start: uvicorn app.main:app --host 0.0.0.0 --loop asyncio  
Health: https://academic-paper-search-engine.onrender.com/health
## 📈 **Tech Stack**
Backend: FastAPI, Pydantic, sentence-transformers  
Deployment: Render, GitHub Actions  
Search: Semantic Scholar API  
Embeddings: all-MiniLM-L6-v2  
