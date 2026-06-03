"""Vector store factory (Chroma + OpenAI embeddings)."""

from __future__ import annotations

import shutil

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from .config import Settings, get_settings


def get_embeddings(settings: Settings | None = None) -> OpenAIEmbeddings:
    settings = settings or get_settings()
    return OpenAIEmbeddings(
        model=settings.embedding_model,
        api_key=settings.openai_api_key,
    )


def get_vectorstore(
    settings: Settings | None = None, *, reset: bool = False
) -> Chroma:
    """Return a persistent Chroma collection.

    If ``reset`` is True, the on-disk collection is wiped first — useful for a
    clean re-index after changing the embedding model or chunking strategy.
    """
    settings = settings or get_settings()
    settings.ensure_dirs()

    if reset and settings.vector_dir.exists():
        shutil.rmtree(settings.vector_dir)
        settings.vector_dir.mkdir(parents=True, exist_ok=True)

    return Chroma(
        collection_name=settings.collection_name,
        embedding_function=get_embeddings(settings),
        persist_directory=str(settings.vector_dir),
    )


def collection_size(settings: Settings | None = None) -> int:
    """Number of indexed chunks (0 if the store is empty / missing)."""
    settings = settings or get_settings()
    try:
        return get_vectorstore(settings)._collection.count()
    except Exception:  # noqa: BLE001
        return 0
