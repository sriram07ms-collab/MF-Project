import re
from typing import List

ADVICE_KEYWORDS = {
    "buy",
    "sell",
    "hold",
    "switch",
    "recommend",
    "recommendation",
    "invest now",
    "should i",
    "better fund",
    "beat",
    "versus",
    "vs",
    "compare returns",
}


def is_advice_query(question: str) -> bool:
    normalized = question.lower()
    return any(keyword in normalized for keyword in ADVICE_KEYWORDS)


def clean_sentence(sentence: str) -> str:
    sentence = re.sub(r"\s+", " ", sentence).strip()
    return sentence


def curated_sentence_split(text: str) -> List[str]:
    raw_sentences = re.split(r"(?<=[.!?])\s+", text)
    cleaned = [clean_sentence(sentence) for sentence in raw_sentences if sentence.strip()]
    return cleaned


