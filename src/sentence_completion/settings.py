from __future__ import annotations

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings related to the application.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    #: The URL of the database to use.
    database_url: PostgresDsn = Field(default=...)


settings = Settings()
