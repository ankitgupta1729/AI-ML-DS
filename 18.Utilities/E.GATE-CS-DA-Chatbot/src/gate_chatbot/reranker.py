"""Optional cross-encoder reranking via FlashRank (lightweight, ONNX, no torch).

Reranking re-orders the over-fetched retrieval candidates by true query–passage
relevance, giving sharper top-k citations than vector similarity alone. It is
**optional** and disabled unless ``RERANK=true`` *and* ``flashrank`` is
installed (``pip install flashrank``). If anything is missing it degrades
gracefully to the original order.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

_ranker = None
_unavailable = False


def rerank(query: str, texts: list[str], top_k: int) -> list[int] | None:
    """Return indices of the top-``top_k`` passages after reranking.

    Returns ``None`` if reranking is unavailable, so the caller keeps the
    original order.
    """
    global _ranker, _unavailable
    if _unavailable or not texts:
        return None
    try:
        from flashrank import Ranker, RerankRequest  # type: ignore
    except Exception:  # noqa: BLE001
        _unavailable = True
        logger.info("flashrank not installed — reranking disabled.")
        return None

    if _ranker is None:
        try:
            _ranker = Ranker()  # downloads a small model on first use
        except Exception as exc:  # noqa: BLE001
            _unavailable = True
            logger.warning("Could not init reranker: %s", exc)
            return None

    passages = [{"id": i, "text": t} for i, t in enumerate(texts)]
    try:
        results = _ranker.rerank(RerankRequest(query=query, passages=passages))
    except Exception as exc:  # noqa: BLE001
        logger.warning("Rerank failed, using original order: %s", exc)
        return None
    return [int(r["id"]) for r in results][:top_k]
