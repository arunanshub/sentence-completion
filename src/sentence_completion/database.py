from __future__ import annotations

import typing
from functools import cache
from typing import TYPE_CHECKING

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from .settings import settings

if TYPE_CHECKING:
    from collections.abc import AsyncIterable


@cache
def get_engine() -> AsyncEngine:
    """
    Get a cached instance of the database async engine.
    """
    return create_async_engine(
        settings.database_url.unicode_string(),
        pool_pre_ping=True,
    )


async def get_db() -> AsyncIterable[AsyncSession]:
    """
    Get an instance of the database session suitable for use with FastAPI.
    """
    async with AsyncSession(get_engine(), expire_on_commit=False) as session:
        yield session


#: A dependency type for use with FastAPI.
AsyncSessionDep = typing.Annotated[AsyncSession, Depends(get_db)]
