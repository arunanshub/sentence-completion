from __future__ import annotations

from pydantic import BaseModel


class CompletionIn(BaseModel):
    sentence: str


class CompletionConfig(BaseModel):
    top_k: int = 50
    top_p: float = 0.7
    # temperature: float = 0.7
    early_stopping: bool = True
    num_return_sequences: int = 5
    num_beams: int = 10
    no_repeat_ngram_size: int = 2
    max_new_tokens: int = 5
