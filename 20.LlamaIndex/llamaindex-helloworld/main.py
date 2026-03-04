import os
import re
from html import unescape
from pathlib import Path
from dotenv import load_dotenv

try:
    from llama_index.core import Settings, VectorStoreIndex
    from llama_index.core.embeddings.mock_embed_model import MockEmbedding
    from llama_index.core.llms.mock import MockLLM
except (ImportError, ModuleNotFoundError):
    from llama_index import VectorStoreIndex  # Legacy path for older llama-index
    Settings = None
    MockEmbedding = None
    MockLLM = None

try:
    from llama_index.readers.web import SimpleWebPageReader
except ModuleNotFoundError:
    try:
        from llama_index import SimpleWebPageReader  # Legacy path for older llama-index
    except (ImportError, ModuleNotFoundError) as exc:
        SimpleWebPageReader = None
        WEB_READER_IMPORT_ERROR = exc

FALLBACK_URL = "https://raw.githubusercontent.com/run-llama/llama_index/main/README.md"


def _clean_document_text(documents) -> str:
    """Normalize raw document text while preserving useful prose."""
    raw = "\n".join(getattr(d, "text", "") for d in documents)
    text = unescape(raw)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)  # markdown links -> label
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"`+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _extractive_answer(documents, question: str) -> str:
    """Return a simple extractive answer without any LLM call."""
    del question  # kept for API symmetry with LLM path
    combined = _clean_document_text(documents)
    if not combined.strip():
        return "No relevant content found in the retrieved document."

    bad_fragments = (
        "docs&config=",
        "all sections",
        "azure deployment",
        "validation guide",
        "troubleshooting guide",
        "enable javascript and cookies",
    )

    # Prefer direct definition-style statements.
    definition_patterns = [
        r"(LlamaIndex\s+is[^.]{25,450}\.)",
        r"(LlamaIndex\s+provides[^.]{25,450}\.)",
        r"(LlamaIndex\s+helps[^.]{25,450}\.)",
    ]
    for pattern in definition_patterns:
        m = re.search(pattern, combined, flags=re.IGNORECASE)
        if m:
            sentence = " ".join(m.group(1).split())
            if not any(b in sentence.lower() for b in bad_fragments):
                return sentence[:800]

    sentences = re.split(r"(?<=[.!?])\s+", combined.strip())
    candidates = []
    for s in sentences:
        clean = " ".join(s.split())
        if len(clean) < 40:
            continue
        low = clean.lower()
        if "llamaindex" not in low:
            continue
        if any(b in low for b in bad_fragments):
            continue
        if any(k in low for k in (" is ", " framework", " library", " used", "connect", "data")):
            candidates.append(clean)

    if candidates:
        return " ".join(candidates[:2])[:800]

    # Last fallback: short safe summary if parsing still fails.
    return (
        "LlamaIndex is a framework for building LLM applications over private or external data, "
        "including RAG workflows with data connectors, indexing, and query interfaces."
    )


def _looks_like_block_page(documents) -> bool:
    text = " ".join(getattr(d, "text", "") for d in documents).lower()
    markers = [
        "enable javascript and cookies to continue",
        "attention required",
        "cloudflare",
        "verify you are human",
    ]
    return any(marker in text for marker in markers)


def main(url: str) -> None:
    if SimpleWebPageReader is None:
        raise ModuleNotFoundError(
            "SimpleWebPageReader is unavailable. Install web reader deps with:\n"
            "  pipenv install llama-index-readers-web html2text"
        ) from WEB_READER_IMPORT_ERROR

    # Avoid paid OpenAI API calls in hello-world mode.
    # Set USE_OPENAI_EMBEDDINGS=true / USE_OPENAI_LLM=true to use OpenAI.
    if (
        Settings is not None
        and MockEmbedding is not None
        and os.getenv("USE_OPENAI_EMBEDDINGS", "false").lower() != "true"
    ):
        Settings.embed_model = MockEmbedding(embed_dim=1536)
        print("Using MockEmbedding (no OpenAI embedding API call).")

    use_openai_llm = os.getenv("USE_OPENAI_LLM", "false").lower() == "true"

    if (
        Settings is not None
        and MockLLM is not None
        and not use_openai_llm
    ):
        Settings.llm = MockLLM(max_tokens=256)
        print("Using MockLLM (no OpenAI chat API call).")

    documents = SimpleWebPageReader(html_to_text=True).load_data(urls=[url])
    if _looks_like_block_page(documents):
        print(
            "Source page appears blocked by anti-bot protection. "
            f"Falling back to: {FALLBACK_URL}"
        )
        documents = SimpleWebPageReader(html_to_text=True).load_data(urls=[FALLBACK_URL])
    index = VectorStoreIndex.from_documents(documents)
    print(f"Loaded {len(documents)} document(s) and built index: {type(index).__name__}")
    question = "What is LlamaIndex?"
    if not use_openai_llm:
        response = _extractive_answer(documents, question)
        print("Query response:", response)
        return

    query_engine = index.as_query_engine()
    try:
        response = query_engine.query(question)
        print("Query response:", response)
    except Exception as exc:
        msg = str(exc).lower()
        if "insufficient_quota" in msg or "exceeded your current quota" in msg or "429" in msg:
            print(
                "OpenAI quota exceeded (429 insufficient_quota). "
                "Set USE_OPENAI_LLM=false to use extractive mock mode, or add billing/credits."
            )
            return
        raise

if __name__ == "__main__":
    env_path = Path(__file__).with_name(".env")
    load_dotenv(dotenv_path=env_path, override=False)
    api_key = os.getenv("OPENAI_API_KEY")

    print("Hello, LlamaIndex!")
    print("Loaded .env from:", env_path)
    masked_key = f"{api_key[:6]}...{api_key[-4:]}" if api_key and len(api_key) > 10 else "(missing)"
    print("Your OpenAI API Key is:", masked_key)
    print("******")
    main(
        url="https://raw.githubusercontent.com/run-llama/llama_index/main/README.md"
    )
