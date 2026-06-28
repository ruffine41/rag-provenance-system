"""Provenance metadata models for RAG retrieval tracking."""
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional


class ArtifactLifecycle(str, Enum):
    DRAFT = "draft"
    VERIFIED = "verified"
    TRUSTED = "trusted"
    CANONICAL = "canonical"


class ProvenanceEntry(BaseModel):
    """Tracks the origin and chain of custody for a retrieved document."""
    document_id: str
    chunk_index: int
    source_path: str
    ingested_at: datetime
    retrieved_at: datetime
    retrieval_score: float
    rank_explanation: str
    agent_id: str
    session_id: str
    lifecycle: ArtifactLifecycle = ArtifactLifecycle.DRAFT


class RetrievalResult(BaseModel):
    """A single retrieved document chunk with full provenance."""
    content: str
    provenance: ProvenanceEntry
    similarity_score: float


class QueryRequest(BaseModel):
    query: str
    top_k: int = Field(default=5, ge=1, le=20)
    threshold: float = Field(default=0.0, ge=0.0, le=1.0)


class QueryResponse(BaseModel):
    query: str
    results: list[RetrievalResult]
    total_results: int
    query_time_ms: float
