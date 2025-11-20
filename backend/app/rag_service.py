from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
from sentence_transformers import SentenceTransformer

from .config import get_settings
from .schemas import QueryResponse, SourceChunk
from .text_utils import clean_sentence, curated_sentence_split, is_advice_query


class RagService:
    """Lightweight retrieval augmented generation layer."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self._model: Optional[SentenceTransformer] = None
        self._documents: List[SourceChunk] = []
        self._embeddings: Optional[np.ndarray] = None

    def _load_model(self) -> SentenceTransformer:
        if self._model is None:
            self._model = SentenceTransformer(self.settings.embeddings_model)
        return self._model

    def ingest_documents(self, documents_path: Path) -> int:
        with documents_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        self._documents = [SourceChunk(**item) for item in data]
        model = self._load_model()
        texts = [doc.text for doc in self._documents]
        self._embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        self._persist_embeddings()
        return len(self._documents)

    def load_index(self) -> None:
        documents_path = self.settings.data_dir / "documents.json"
        embeddings_path = self.settings.data_dir / "embeddings.npy"
        if not documents_path.exists() or not embeddings_path.exists():
            raise FileNotFoundError(
                "Vector store not found. Run `python -m app.ingest` from the backend directory."
            )
        with documents_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        self._documents = [SourceChunk(**item) for item in data]
        self._embeddings = np.load(embeddings_path)
        if len(self._documents) != self._embeddings.shape[0]:
            raise ValueError("Mismatch between embeddings and documents length.")

    def _persist_embeddings(self) -> None:
        embeddings_path = self.settings.data_dir / "embeddings.npy"
        embeddings_path.parent.mkdir(parents=True, exist_ok=True)
        if self._embeddings is None:
            raise RuntimeError("No embeddings to persist.")
        np.save(embeddings_path, self._embeddings)
        documents_path = self.settings.data_dir / "documents.json"
        serializable = [doc.dict() for doc in self._documents]
        with documents_path.open("w", encoding="utf-8") as f:
            json.dump(serializable, f, indent=2, default=str)

    def answer(self, question: str) -> QueryResponse:
        if is_advice_query(question):
            return QueryResponse(
                answer=(
                    "I can only share factual details from official sources. "
                    "Please consult a SEBI-registered advisor for personalised guidance. "
                    "Facts-only. No investment advice."
                ),
                citation=self.settings.investor_education_link,
                last_updated=datetime.utcnow().date(),
                matched_fund=None,
                metadata={
                    "reason": "advice_request",
                    "note": "Forward user to investor education resources.",
                },
            )

        documents, scores = self._retrieve(question)
        if not documents:
            return QueryResponse(
                answer="I could not find an official answer for that scheme. Facts-only. No investment advice.",
                citation=self.settings.allowed_sources[0],
                last_updated=datetime.utcnow().date(),
                matched_fund=None,
                metadata={"reason": "no_match"},
            )

        top_doc = documents[0]
        sentences = curated_sentence_split(top_doc.text)
        trimmed = " ".join(sentences[: self.settings.max_answer_sentences])
        answer_text = f"{trimmed} Facts-only. No investment advice. Last updated from sources: {top_doc.captured_at}."

        return QueryResponse(
            answer=answer_text,
            citation=top_doc.source,
            last_updated=top_doc.captured_at,
            matched_fund=top_doc.fund_name,
            metadata={"score": scores[0]},
        )

    def _retrieve(self, question: str) -> Tuple[List[SourceChunk], List[float]]:
        if self._embeddings is None or not len(self._documents):
            self.load_index()
        assert self._embeddings is not None
        model = self._load_model()
        query_vec = model.encode([question], convert_to_numpy=True, normalize_embeddings=True)[0]
        scores = np.dot(self._embeddings, query_vec)
        top_indices = np.argsort(scores)[::-1][: self.settings.top_k]
        documents: List[SourceChunk] = []
        selected_scores: List[float] = []
        for idx in top_indices:
            if scores[idx] <= 0:
                continue
            documents.append(self._documents[idx])
            selected_scores.append(float(scores[idx]))
        return documents, selected_scores


rag_service = RagService()


