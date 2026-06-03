"""The RAG chat engine.

Orchestrates: history-aware query reformulation → similarity retrieval →
topic guardrail → grounded, streaming answer with source citations.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Iterator

from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from .config import Settings, get_settings
from .prompts import (
    ANSWER_PROMPT,
    CAPABILITIES_REPLY,
    CONDENSE_PROMPT,
    FAREWELL_REPLY,
    GREETING_REPLY,
    SYSTEM_PROMPT,
    THANKS_REPLY,
)
from .vectorstore import get_vectorstore

logger = logging.getLogger(__name__)

# Conservative small-talk detection: only fires when the *whole* message is a
# greeting / thanks / farewell / capability question, so real questions that
# merely start with "hi" aren't swallowed.
_GREETING_RE = re.compile(
    r"^(hi+|hey+|hello+|yo|hiya|namaste|greetings|good\s*(morning|afternoon|evening|day))"
    r"(\s+(there|buddy|bot|go))?[\s!.,]*$",
    re.IGNORECASE,
)
_THANKS_RE = re.compile(
    r"^(thanks|thank\s*you|thx|ty|thank\s*u|much\s*appreciated|great|awesome|cool|nice|ok|okay|👍)[\s!.,]*$",
    re.IGNORECASE,
)
_FAREWELL_RE = re.compile(
    r"^(bye+|goodbye|good\s*night|see\s*(you|ya)|cya|take\s*care)[\s!.,]*$",
    re.IGNORECASE,
)
_CAPABILITY_RE = re.compile(
    r"^(who\s*are\s*you|what\s*(can|do)\s*you\s*(do|help)|what\s*is\s*this|"
    r"how\s*do\s*you\s*work|help|what\s*are\s*you)[\s?!.]*$",
    re.IGNORECASE,
)


def smalltalk_reply(text: str) -> str | None:
    """Return a canned reply for greetings/small talk, else ``None``."""
    t = (text or "").strip()
    if not t or len(t) > 60:
        return None
    if _GREETING_RE.match(t):
        return GREETING_REPLY
    if _THANKS_RE.match(t):
        return THANKS_REPLY
    if _FAREWELL_RE.match(t):
        return FAREWELL_REPLY
    if _CAPABILITY_RE.match(t):
        return CAPABILITIES_REPLY
    return None


@dataclass
class Source:
    """A retrieved chunk surfaced to the user as a citation."""

    source: str
    subject: str
    score: float
    locator: str  # e.g. "p. 12" or "slide 4"
    snippet: str


@dataclass
class ChatResult:
    answer: str
    sources: list[Source] = field(default_factory=list)
    in_scope: bool = True


def _format_locator(meta: dict) -> str:
    if "page" in meta:
        return f"p. {meta['page']}"
    if "slide" in meta:
        return f"slide {meta['slide']}"
    return ""


class ChatEngine:
    """Stateless engine — conversation history is passed in per call."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._store = None
        self._llm = ChatOpenAI(
            model=self.settings.chat_model,
            temperature=self.settings.temperature,
            max_tokens=self.settings.max_tokens,
            api_key=self.settings.openai_api_key,
            streaming=True,
        )
        # A cheap, deterministic model for query reformulation.
        self._condenser = ChatOpenAI(
            model=self.settings.chat_model,
            temperature=0.0,
            api_key=self.settings.openai_api_key,
        )

    @property
    def store(self):
        if self._store is None:
            self._store = get_vectorstore(self.settings)
        return self._store

    # ------------------------------------------------------------------ #
    # Retrieval                                                          #
    # ------------------------------------------------------------------ #
    def _condense(self, question: str, history: list[dict]) -> str:
        """Rewrite a follow-up into a standalone question using recent turns."""
        if not history:
            return question
        recent = history[-6:]  # last 3 exchanges
        transcript = "\n".join(
            f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
            for m in recent
        )
        prompt = CONDENSE_PROMPT.format(history=transcript, question=question)
        try:
            return self._condenser.invoke(prompt).content.strip() or question
        except Exception as exc:  # noqa: BLE001
            logger.warning("Condense failed, using raw question: %s", exc)
            return question

    def _retrieve(self, query: str) -> tuple[list[Document], list[float]]:
        k = self.settings.retriever_k
        try:
            scored = self.store.similarity_search_with_relevance_scores(query, k=k)
        except Exception as exc:  # noqa: BLE001
            logger.error("Retrieval failed: %s", exc)
            return [], []
        docs = [d for d, _ in scored]
        scores = [s for _, s in scored]
        return docs, scores

    def _build_sources(
        self, docs: list[Document], scores: list[float]
    ) -> list[Source]:
        sources: list[Source] = []
        seen: set[tuple[str, str]] = set()
        for d, score in zip(docs, scores):
            meta = d.metadata
            key = (meta.get("source", "?"), _format_locator(meta))
            if key in seen:
                continue
            seen.add(key)
            snippet = d.page_content.strip().replace("\n", " ")
            sources.append(
                Source(
                    source=meta.get("source", "unknown"),
                    subject=meta.get("subject", "general"),
                    score=round(float(score), 3),
                    locator=_format_locator(meta),
                    snippet=(snippet[:240] + "…") if len(snippet) > 240 else snippet,
                )
            )
        return sources

    # ------------------------------------------------------------------ #
    # Public API                                                         #
    # ------------------------------------------------------------------ #
    def _messages(
        self,
        question: str,
        history: list[dict],
        context: str,
        feedback_hint: str | None = None,
        image_parts: list[str] | None = None,
    ) -> list:
        msgs: list = [SystemMessage(content=SYSTEM_PROMPT)]
        for m in history[-8:]:
            if m["role"] == "user":
                msgs.append(HumanMessage(content=m["content"]))
            else:
                msgs.append(AIMessage(content=m["content"]))
        prompt = ANSWER_PROMPT.format(
            context=context or "(no relevant material found)",
            question=question,
        )
        if feedback_hint:
            # The previous answer was thumbed-down; steer the regeneration.
            prompt += (
                "\n\n----- REVIEWER FEEDBACK ON YOUR PREVIOUS ANSWER -----\n"
                f"{feedback_hint}\n"
                "Please write an improved answer that directly addresses this "
                "feedback while staying accurate and grounded in the context."
            )
        if image_parts:
            # Multimodal turn: text + one or more images (vision models).
            content: list[dict] = [{"type": "text", "text": prompt}]
            for url in image_parts:
                content.append({"type": "image_url", "image_url": {"url": url}})
            msgs.append(HumanMessage(content=content))
        else:
            msgs.append(HumanMessage(content=prompt))
        return msgs

    def stream(
        self,
        question: str,
        history: list[dict] | None = None,
        feedback_hint: str | None = None,
        attachments: dict | None = None,
    ) -> Iterator[str | ChatResult]:
        """Yield answer tokens as they arrive, then a final :class:`ChatResult`.

        ``attachments`` (optional) is ``{"images": [data_url, ...],
        "docs": [{"name": str, "text": str}, ...]}``.
        """
        history = history or []
        attachments = attachments or {}
        image_parts: list[str] = attachments.get("images", []) or []
        doc_files: list[dict] = attachments.get("docs", []) or []

        # Greetings / small talk → friendly, retrieval-free reply (only when
        # there are no attachments and it isn't a regeneration).
        if not image_parts and not doc_files and not feedback_hint:
            canned = smalltalk_reply(question)
            if canned is not None:
                for word in canned.split(" "):
                    yield word + " "
                yield ChatResult(answer=canned, sources=[], in_scope=True)
                return

        standalone = self._condense(question, history)
        docs, scores = self._retrieve(standalone) if standalone else ([], [])

        best = max(scores) if scores else 0.0
        in_scope = best >= self.settings.relevance_threshold

        context_parts = [
            f"[{d.metadata.get('source', '?')}{' ' + _format_locator(d.metadata) if _format_locator(d.metadata) else ''}]\n{d.page_content}"
            for d in docs
        ]
        # Prepend any uploaded document text as high-priority context.
        for f in doc_files:
            text = (f.get("text") or "").strip()
            if text:
                context_parts.insert(
                    0, f"[Uploaded file: {f.get('name', 'attachment')}]\n{text}"
                )
        context = "\n\n---\n\n".join(context_parts)

        messages = self._messages(
            standalone or question, history, context, feedback_hint, image_parts
        )
        parts: list[str] = []
        try:
            for chunk in self._llm.stream(messages):
                token = chunk.content or ""
                if token:
                    parts.append(token)
                    yield token
        except Exception as exc:  # noqa: BLE001
            err = f"\n\n⚠️ Sorry, I hit an error talking to the model: {exc}"
            parts.append(err)
            yield err

        answer = "".join(parts).strip()
        sources = self._build_sources(docs, scores) if in_scope else []
        yield ChatResult(answer=answer, sources=sources, in_scope=in_scope)

    def chat(
        self,
        question: str,
        history: list[dict] | None = None,
        attachments: dict | None = None,
    ) -> ChatResult:
        """Non-streaming convenience wrapper."""
        result: ChatResult | None = None
        for item in self.stream(question, history, attachments=attachments):
            if isinstance(item, ChatResult):
                result = item
        assert result is not None
        return result


_ENGINE: ChatEngine | None = None


def get_engine(settings: Settings | None = None) -> ChatEngine:
    """Return a process-wide singleton engine."""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = ChatEngine(settings)
    return _ENGINE
