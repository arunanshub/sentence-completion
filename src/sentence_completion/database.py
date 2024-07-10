from __future__ import annotations

import typing
from typing import TYPE_CHECKING

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from .settings import settings

if TYPE_CHECKING:
    from collections.abc import AsyncIterable


async def get_db() -> AsyncIterable[AsyncSession]:
    """
    Get an instance of the database session suitable for use with FastAPI.
    """
    engine = create_async_engine(settings.database_url.unicode_string())
    async with AsyncSession(engine) as session:
        yield session


#: A dependency type for use with FastAPI.
AsyncSessionDep = typing.Annotated[AsyncSession, Depends(get_db)]
