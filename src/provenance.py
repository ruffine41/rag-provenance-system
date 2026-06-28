"""Provenance tracking and lifecycle management for RAG."""
from datetime import datetime, timezone
from src.models import ProvenanceEntry, ArtifactLifecycle


class ProvenanceTracker:
    """Records and manages provenance metadata for every retrieval."""

    def __init__(self, agent_id: str, session_id: str):
        self.agent_id = agent_id
        self.session_id = session_id
        self._entries: list[ProvenanceEntry] = []

    def record(
        self,
        document_id: str,
        chunk_index: int,
        source_path: str,
        retrieval_score: float,
        rank_explanation: str,
    ) -> ProvenanceEntry:
        entry = ProvenanceEntry(
            document_id=document_id,
            chunk_index=chunk_index,
            source_path=source_path,
            ingested_at=datetime.now(timezone.utc),
            retrieved_at=datetime.now(timezone.utc),
            retrieval_score=retrieval_score,
            rank_explanation=rank_explanation,
            agent_id=self.agent_id,
            session_id=self.session_id,
            lifecycle=ArtifactLifecycle.DRAFT,
        )
        self._entries.append(entry)
        return entry

    def promote(self, document_id: str) -> ProvenanceEntry | None:
        """Move a document to the next lifecycle stage."""
        for entry in self._entries:
            if entry.document_id == document_id:
                stages = list(ArtifactLifecycle)
                idx = stages.index(entry.lifecycle)
                if idx < len(stages) - 1:
                    entry.lifecycle = stages[idx + 1]
                return entry
        return None

    def audit_log(self) -> list[dict]:
        """Return a human-readable audit trail."""
        return [
            {
                "document_id": e.document_id,
                "source": e.source_path,
                "score": e.retrieval_score,
                "lifecycle": e.lifecycle.value,
                "retrieved_by": e.agent_id,
                "at": e.retrieved_at.isoformat(),
            }
            for e in self._entries
        ]
