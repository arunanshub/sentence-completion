from __future__ import annotations

from pydantic import BaseModel

from .completion_config import CompletionConfig as CompletionConfig1
from .user_input import UserInput


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


__all__ = ["CompletionConfig1", "UserInput"]
