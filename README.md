# RAG Provenance System

A lightweight, governed **RAG (Retrieval-Augmented Generation)** pipeline with full provenance tracking — every answer is traceable to its source document with audit trails and lifecycle management.

## What This Does

Most RAG systems return answers but can't tell you *why* they picked a particular source or *where* the answer came from. This system bakes provenance metadata into every retrieval step:

- **Source attribution** — every result links back to its original document, chunk, and position
- **Provenance metadata** — agent, session, timestamp, retrieval score, and ranking explanation
- **Lifecycle management** — artifacts move through Draft → Verified → Trusted → Canonical with full audit logging
- **Recency fallback** — graceful degradation when vector search is unavailable
- **Authorization boundaries** — who can read, write, and verify what

## Tech Stack

- **Python** — core retrieval and embedding pipeline
- **PostgreSQL + pgvector** — vector storage and hybrid search
- **Sentence Transformers** — embedding generation
- **FastAPI** — REST API for query and ingestion
- **Docker** — containerized deployment

## Quick Start

```bash
# Clone and install
git clone https://github.com/ruffine41/rag-provenance-system.git
cd rag-provenance-system
pip install -r requirements.txt

# Set up PostgreSQL with pgvector
# (requires PostgreSQL 16+ with pgvector extension)

# Run the ingestion pipeline
python src/ingest.py --source ./documents

# Start the API
uvicorn src.api:app --reload

# Query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is a RAG pipeline?"}'
```

## Architecture

```
┌──────────┐    ┌──────────────┐    ┌─────────────┐
│ Documents │ → │  Ingestion   │ → │  Embeddings  │
│  (PDF/    │    │  Pipeline    │    │  + pgvector  │
│   MD/TXT) │    │              │    │              │
└──────────┘    └──────────────┘    └──────┬──────┘
                                          │
                                          ▼
┌──────────┐    ┌──────────────┐    ┌─────────────┐
│  Answer  │ ← │   LLM Gen    │ ← │   Retrieval  │
│ + Source │    │  (OpenAI/)  │    │  + Reranking │
│  Cites   │    │   Claude    │    │  + Provenance│
└──────────┘    └──────────────┘    └─────────────┘
                                          │
                                          ▼
                                   ┌─────────────┐
                                   │  Provenance  │
                                   │   Metadata   │
                                   │   (audit log)│
                                   └─────────────┘
```

## Project Structure

```
rag-provenance-system/
├── src/
│   ├── api.py              # FastAPI query/ingestion endpoints
│   ├── ingest.py           # Document ingestion pipeline
│   ├── embedder.py         # Embedding generation
│   ├── retriever.py        # Vector + hybrid retrieval
│   ├── provenance.py       # Provenance metadata tracking
│   ├── lifecycle.py        # Document lifecycle management
│   └── models.py           # Pydantic data models
├── tests/
│   ├── test_retrieval.py
│   └── test_provenance.py
├── documents/              # Sample documents
├── requirements.txt
├── Dockerfile
└── README.md
```

## Why Provenance Matters

Without provenance, a RAG system is a black box. With it:

- **Auditors** can verify exactly where information came from
- **Developers** can debug retrieval failures by inspecting scores and ranks
- **End users** see confidence levels and source links alongside answers
- **The system** can explain *why* it ranked one result above another

## Roadmap

- [ ] Hybrid search (dense + sparse embeddings)
- [ ] Cross-encoder reranking
- [ ] Streaming response support
- [ ] Document versioning and diff tracking
- [ ] Web UI for document management

## License

MIT
