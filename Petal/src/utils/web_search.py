# src/utils/web_search.py

# ✅ New
from ddgs import DDGS
import re


def sanitize_input(text: str) -> str:
    """
    Basic prompt injection protection by removing unsafe patterns.
    """
    banned_phrases = [
        "ignore previous instructions",
        "act as", 
        "disregard above", 
        "you are now",
        "forget all previous instructions",
        "pretend you are",
        "override system message",
        "system prompt"
    ]

    for phrase in banned_phrases:
        if phrase.lower() in text.lower():
            text = text.lower().replace(phrase.lower(), "")

    return text.strip()



def search_duckduckgo(query: str) -> str:
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=5)
        summaries = [r["body"] for r in results if "body" in r]
        return "\n".join(summaries)


