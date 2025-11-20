from datetime import date
from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class QueryRequest(BaseModel):
    question: str
    context: Optional[str] = None


class SourceChunk(BaseModel):
    id: str
    fund_id: str
    fund_name: str
    section: str
    text: str
    source: HttpUrl
    captured_at: date


class QueryResponse(BaseModel):
    answer: str
    citation: HttpUrl
    last_updated: date
    matched_fund: Optional[str] = None
    metadata: Optional[dict] = None


class ReindexResponse(BaseModel):
    documents_indexed: int
    message: str


class ChunkList(BaseModel):
    items: List[SourceChunk]


