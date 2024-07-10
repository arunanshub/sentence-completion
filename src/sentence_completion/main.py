from __future__ import annotations

import typing
from functools import lru_cache

import sqlalchemy as sa
from fastapi import Depends, FastAPI
from fastapi.concurrency import run_in_threadpool

from .completion import ModelCompletion, SentenceCompletion
from .database import AsyncSessionDep  # noqa: TCH001
from .models import CompletionConfigIn, completion, completion_config
from .models.user_input import UserInput

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


@app.get("/_health")
async def health(db: AsyncSessionDep):
    """Check the health of the application.

    This route executes a simple SQL select query to check the health of the
    database connection.
    """
    await db.execute(sa.text("SELECT 1"))


@app.post("/completion")
async def complete_sentence(
    model: ModelDep,
    sentence: str,
    db: AsyncSessionDep,
    config: CompletionConfigIn | None = None,
) -> list[ModelCompletion]:
    if config is None:
        config = CompletionConfigIn()

    model_completion = await run_in_threadpool(
        model.complete_with_scores,
        sentence,
        config,
    )

    model_config = completion_config.CompletionConfig(**config.model_dump())
    user_input = UserInput(sentence, model_config)
    comp = completion.Completion(model_completion, user_input)
    db.add_all([model_config, user_input, comp])

    return model_completion
