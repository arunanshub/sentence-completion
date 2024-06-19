from __future__ import annotations

import typing
from functools import lru_cache

from fastapi import Depends, FastAPI
from fastapi.concurrency import run_in_threadpool

from .completion import Completion, SentenceCompletion
from .models import CompletionConfig

app = FastAPI()


@lru_cache
def _get_cached_model() -> SentenceCompletion:
    return SentenceCompletion()


def get_model() -> typing.Iterable[SentenceCompletion]:
    yield _get_cached_model()


ModelDep = typing.Annotated[SentenceCompletion, Depends(get_model)]


@app.get("/")
def read_root():
    return "working"


@app.post("/completion")
async def complete_sentence(
    model: ModelDep,
    sentence: str,
    config: CompletionConfig | None = None,
) -> list[Completion]:
    if config is None:
        config = CompletionConfig()

    return await run_in_threadpool(model.complete_with_scores, sentence, config)
