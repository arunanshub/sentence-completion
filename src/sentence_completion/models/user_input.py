from __future__ import annotations

from datetime import datetime  # noqa: TCH003
from typing import TYPE_CHECKING
from uuid import UUID  # noqa: TCH003

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, MappedColumn, mapped_column, relationship
from uuid_utils import uuid7

from .base import Base

if TYPE_CHECKING:
    from .completion_config import CompletionConfig


class UserInput(Base):
    """
    User input for sentence completion.
    """

    __tablename__ = "user_inputs"

    id: MappedColumn[UUID] = mapped_column(
        primary_key=True,
        default_factory=lambda: str(uuid7()),
        init=False,
    )
    #: The user input sentence.
    sentence: MappedColumn[str]
    #: The time user input was created.
    created_at: MappedColumn[datetime] = mapped_column(
        init=False,
        server_default=sa.func.now(),
    )
    #: The completion config used for this user input.
    completion_config: Mapped[CompletionConfig] = relationship(
        back_populates="user_input"
    )
