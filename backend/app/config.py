from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "Facts-Only MF Assistant API"
    allowed_sources: List[AnyHttpUrl] = Field(
        default=[
            "https://mf.nipponindiaim.com/FundsAndPerformance/Pages/NipponIndia-Large-Cap-Fund.aspx",
            "https://mf.nipponindiaim.com/FundsAndPerformance/Pages/NipponIndia-Growth-Mid-Cap-Fund.aspx",
            "https://mf.nipponindiaim.com/FundsAndPerformance/Pages/NipponIndia-Small-Cap-Fund.aspx",
        ]
    )
    investor_education_link: AnyHttpUrl = Field(
        default="https://mf.nipponindiaim.com/InvestorEducation"
    )
    data_dir: Path = Path(__file__).resolve().parent.parent / "data"
    embeddings_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="SentenceTransformer model name.",
    )
    top_k: int = 4
    max_answer_sentences: int = 3

    class Config:
        env_file = (Path(__file__).resolve().parent.parent / ".env",)
        env_file_encoding = "utf-8"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


