from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID  # noqa: TCH003

from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, MappedColumn, mapped_column, relationship
from uuid_utils import uuid7

from .base import Base

if TYPE_CHECKING:
    from .user_input import UserInput


class CompletionConfig(Base):
    """
    Configuration for the completion model used during sentence generation.
    """

    __tablename__ = "completion_configs"

    id: MappedColumn[UUID] = mapped_column(
        primary_key=True,
        default_factory=lambda: str(uuid7()),
        init=False,
    )
    #: number of most probable words to return.
    top_k: MappedColumn[int] = mapped_column(default=50)
    #: the nucleus sampling probability.
    top_p: MappedColumn[float] = mapped_column(default=0.7)
    #: whether to stop generation when the model reaches a high enough likelihood.
    early_stopping: MappedColumn[bool] = mapped_column(default=True)
    #: the number of generated sentences to return.
    num_return_sequences: MappedColumn[int] = mapped_column(default=5)
    #: the number of beams to use during generation.
    num_beams: MappedColumn[int] = mapped_column(default=5)
    #: size of ngrams to avoid repeating during generation.
    no_repeat_ngram_size: MappedColumn[int] = mapped_column(default=2)
    #: the maximum number of tokens to generate.
    max_new_tokens: MappedColumn[int] = mapped_column(default=5)
    #: The id of the user input that this completion config is associated with.
    user_input_id: MappedColumn[UUID] | None = mapped_column(
        ForeignKey("user_inputs.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=True,
        init=False,
    )
    #: The user input that this completion config is associated with.
    user_input: Mapped[UserInput] = relationship(
        back_populates="completion_config",
        init=False,
    )


class CompletionConfigIn(BaseModel):
    """
    The model for completion configuration that is used by FastAPI. For info on
    the fields, see `CompletionConfig`.
    """

    top_k: int = 50
    top_p: float = 0.7
    early_stopping: bool = True
    num_return_sequences: int = 5
    num_beams: int = 10
    no_repeat_ngram_size: int = 2
    max_new_tokens: int = 5
