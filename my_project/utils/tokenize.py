from __future__ import annotations
def estimate_tokens_from_words(words: int) -> int:
    return int(words * 1.3)
def estimate_tokens_from_text(text: str) -> int:
    words = max(1, len(text.split()))
    return estimate_tokens_from_words(words)
