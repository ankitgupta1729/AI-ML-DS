"""Central configuration.

All settings are read from environment variables (optionally via a ``.env``
file). This keeps secrets out of the code and makes the app portable across
local, staging and production environments.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Repository root (…/E.GATE-CS-DA-Chatbot)
ROOT_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Application settings loaded from the environment / ``.env``."""

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- OpenAI ---------------------------------------------------------
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    chat_model: str = Field(default="gpt-4o-mini", alias="CHAT_MODEL")
    embedding_model: str = Field(
        default="text-embedding-3-small", alias="EMBEDDING_MODEL"
    )
    temperature: float = Field(default=0.2, alias="TEMPERATURE")
    max_tokens: int = Field(default=1024, alias="MAX_TOKENS")

    # --- Retrieval ------------------------------------------------------
    chunk_size: int = Field(default=1000, alias="CHUNK_SIZE")
    chunk_overlap: int = Field(default=150, alias="CHUNK_OVERLAP")
    retriever_k: int = Field(default=5, alias="RETRIEVER_K")
    # Minimum cosine similarity (0–1) for a chunk to be considered relevant.
    # Used by the topic guardrail to decide whether the question is in scope.
    relevance_threshold: float = Field(default=0.25, alias="RELEVANCE_THRESHOLD")

    # --- Storage paths --------------------------------------------------
    data_dir: Path = Field(default=ROOT_DIR / "data", alias="DATA_DIR")
    vector_dir: Path = Field(
        default=ROOT_DIR / "storage" / "chroma", alias="VECTOR_DIR"
    )
    collection_name: str = Field(default="gate_cs_da", alias="COLLECTION_NAME")

    # --- Application database (conversations, messages, feedback, RLHF) -
    # SQLite by default; point at Postgres in production, e.g.
    # postgresql+psycopg://user:pass@host:5432/gateoverflow
    database_url: str = Field(
        default=f"sqlite:///{ROOT_DIR / 'storage' / 'app.db'}",
        alias="DATABASE_URL",
    )

    # --- API ------------------------------------------------------------
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")

    def ensure_dirs(self) -> None:
        """Create storage directories if they do not yet exist."""
        self.vector_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    """Return a cached :class:`Settings` instance."""
    return Settings()
