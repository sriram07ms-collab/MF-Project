from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List

import requests
from bs4 import BeautifulSoup

from .config import get_settings
from .rag_service import RagService


@dataclass
class FundSource:
    fund_id: str
    fund_name: str
    url: str


FUND_SOURCES = [
    FundSource(
        fund_id="nippon_large_cap",
        fund_name="Nippon India Large Cap Fund",
        url="https://mf.nipponindiaim.com/FundsAndPerformance/Pages/NipponIndia-Large-Cap-Fund.aspx",
    ),
    FundSource(
        fund_id="nippon_growth_midcap",
        fund_name="Nippon India Growth Mid Cap Fund",
        url="https://mf.nipponindiaim.com/FundsAndPerformance/Pages/NipponIndia-Growth-Mid-Cap-Fund.aspx",
    ),
    FundSource(
        fund_id="nippon_small_cap",
        fund_name="Nippon India Small Cap Fund",
        url="https://mf.nipponindiaim.com/FundsAndPerformance/Pages/NipponIndia-Small-Cap-Fund.aspx",
    ),
]


KEYWORDS = [
    "investment objective",
    "exit load",
    "entry load",
    "minimum investment",
    "sip",
    "riskometer",
    "benchmark",
    "fund manager",
    "load details",
    "account statements",
    "downloads",
    "capital gain",
    "statement",
    "portfolio",
    "factsheet",
]


def fetch_html(source: FundSource) -> str:
    response = requests.get(source.url, timeout=30)
    response.raise_for_status()
    return response.text


def extract_chunks(html: str) -> List[str]:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    text = soup.get_text("\n")
    lines = [line.strip() for line in text.splitlines()]
    filtered: List[str] = []
    include_next = 0
    for idx, line in enumerate(lines):
        lower_line = line.lower()
        match = any(keyword in lower_line for keyword in KEYWORDS)
        if match:
            filtered.append(line)
            for step in range(1, 3):
                if idx + step < len(lines):
                    filtered.append(lines[idx + step])
            include_next = 0
        elif include_next > 0:
            filtered.append(line)
            include_next -= 1
        elif lower_line.startswith(("₹", "rs", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9")):
            filtered.append(line)
    filtered = [line for line in filtered if len(line.split()) >= 1]
    chunks: List[str] = []
    current: List[str] = []
    char_limit = 600
    for line in filtered:
        current.append(line)
        if sum(len(segment) for segment in current) >= char_limit:
            chunks.append(" ".join(current))
            current = []
    if current:
        chunks.append(" ".join(current))
    return chunks


def build_documents() -> List[dict]:
    documents: List[dict] = []
    captured_at = datetime.utcnow().date()
    for source in FUND_SOURCES:
        html = fetch_html(source)
        for idx, chunk in enumerate(extract_chunks(html)):
            section = chunk.split(".")[0][:80]
            documents.append(
                {
                    "id": f"{source.fund_id}_{idx}",
                    "fund_id": source.fund_id,
                    "fund_name": source.fund_name,
                    "section": section,
                    "text": chunk,
                    "source": source.url,
                    "captured_at": captured_at.isoformat(),
                }
            )
    return documents


def write_documents(documents: Iterable[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(list(documents), f, indent=2)


def run_ingestion() -> None:
    settings = get_settings()
    documents_path = settings.data_dir / "documents.json"
    documents = build_documents()
    write_documents(documents, documents_path)
    rag = RagService()
    count = rag.ingest_documents(documents_path)
    print(f"Ingested {count} documents into the local vector store.")


if __name__ == "__main__":
    run_ingestion()


