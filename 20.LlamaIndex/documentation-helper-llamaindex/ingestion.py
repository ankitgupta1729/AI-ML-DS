from pathlib import Path
import sys
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from llama_index.core import (
    SimpleDirectoryReader,
    Settings,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.core import MockEmbedding
from llama_index.core.node_parser import SimpleNodeParser

load_dotenv()

os.environ.setdefault("LLAMA_INDEX_CACHE_DIR", str(Path(".cache/llama_index").resolve()))
os.environ.setdefault("HF_HOME", str(Path(".cache/huggingface").resolve()))
os.environ.setdefault("TRANSFORMERS_CACHE", str(Path(".cache/huggingface/transformers").resolve()))

DOCS_DIR_CANDIDATES = ["./llamaindex-docs", "./llamindex-docs"]
PERSIST_DIR = "./storage"
DEFAULT_PINECONE_DIMENSION = 1536
DEFAULT_LOCAL_EMBED_MODEL = "BAAI/bge-small-en-v1.5"


def resolve_docs_dir() -> Path | None:
    for candidate in DOCS_DIR_CANDIDATES:
        path = Path(candidate)
        if path.exists() and path.is_dir():
            return path
    return None


def has_only_placeholder_docs(docs_dir: Path) -> bool:
    html_files = list(docs_dir.rglob("*.html"))
    if len(html_files) != 1:
        return False
    return html_files[0].name == "sample.html"


def clean_html_documents(documents) -> None:
    for document in documents:
        file_path = str(document.metadata.get("file_path", ""))
        if not file_path.endswith(".html"):
            continue
        soup = BeautifulSoup(document.get_content(), "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        cleaned_text = soup.get_text(separator=" ", strip=True)
        if cleaned_text:
            document.set_content(cleaned_text)


def resolve_local_embed_model():
    model_name = os.getenv("LOCAL_EMBED_MODEL", DEFAULT_LOCAL_EMBED_MODEL)
    try:
        from llama_index.embeddings.huggingface import HuggingFaceEmbedding

        print(f"Using local embedding model: {model_name}")
        return HuggingFaceEmbedding(model_name=model_name)
    except Exception as exc:
        print(f"Falling back to MockEmbedding because local model failed: {exc}")
        return MockEmbedding(embed_dim=384)


def resolve_pinecone_dimension(pc, index_name: str | None, fallback_dim: int) -> int:
    if not index_name:
        return fallback_dim
    try:
        desc = pc.describe_index(index_name)
        if isinstance(desc, dict):
            return int(desc.get("dimension", fallback_dim))
        return int(getattr(desc, "dimension", fallback_dim))
    except Exception:
        return fallback_dim


if __name__ == "__main__":
    ingest_backend = os.getenv("INGEST_BACKEND", "local").strip().lower()
    print(f"Starting ingestion with backend: {ingest_backend}")
    file_extractor = {}
    try:
        from llama_index.readers.file import UnstructuredReader

        file_extractor[".html"] = UnstructuredReader()
    except Exception:
        # Fallback keeps ingestion fully local without extra optional deps.
        print("Unstructured not available; using default HTML reader.")

    docs_dir = resolve_docs_dir()
    if docs_dir is None:
        print(
            "No docs folder found. Expected one of: "
            f"{', '.join(DOCS_DIR_CANDIDATES)}.\n"
            "Run `python download_docs.py` first."
        )
        sys.exit(1)
    if has_only_placeholder_docs(docs_dir):
        print(
            "Only placeholder docs found (sample.html). "
            "Run `python download_docs.py` to fetch real LlamaIndex docs before ingestion."
        )
        sys.exit(1)

    dir_reader = SimpleDirectoryReader(
        input_dir=str(docs_dir),
        file_extractor=file_extractor,
        recursive=True,
        required_exts=[".html"],
    )
    documents = dir_reader.load_data()
    if not documents:
        print(f"No documents found in {docs_dir}. Nothing to ingest.")
        sys.exit(1)
    clean_html_documents(documents)

    node_parser = SimpleNodeParser.from_defaults(chunk_size=500, chunk_overlap=20)
    Settings.node_parser = node_parser
    nodes = node_parser.get_nodes_from_documents(documents)
    if not nodes:
        print("No nodes created from documents after chunking. Nothing to ingest.")
        sys.exit(1)

    if ingest_backend == "pinecone":
        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")
        pinecone_host = os.getenv("PINECONE_HOST")
        fallback_dim = int(
            os.getenv("PINECONE_DIMENSION", str(DEFAULT_PINECONE_DIMENSION))
        )

        missing_vars = []
        if not pinecone_api_key:
            missing_vars.append("PINECONE_API_KEY")
        if not pinecone_index_name and not pinecone_host:
            missing_vars.append("PINECONE_INDEX_NAME or PINECONE_HOST")
        if missing_vars:
            print(
                "Missing required environment variables for pinecone backend: "
                f"{', '.join(missing_vars)}"
            )
            sys.exit(1)

        from llama_index.vector_stores.pinecone import PineconeVectorStore
        from pinecone import Pinecone

        pc = Pinecone(api_key=pinecone_api_key)
        embed_dim = resolve_pinecone_dimension(pc, pinecone_index_name, fallback_dim)
        # Free/local embeddings for Pinecone ingestion (no paid API usage).
        Settings.embed_model = MockEmbedding(embed_dim=embed_dim)

        # Prefer index-name resolution because copied host URLs are commonly malformed.
        pinecone_index = (
            pc.Index(name=pinecone_index_name)
            if pinecone_index_name
            else pc.Index(host=pinecone_host)
        )
        vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        VectorStoreIndex(nodes=nodes, storage_context=storage_context, show_progress=True)
        print(
            f"Finished ingesting {len(nodes)} chunks from {len(documents)} docs into "
            f"Pinecone index '{pinecone_index_name or pinecone_host}' with embedding dim {embed_dim}."
        )
    else:
        # Fully local ingestion path: no API keys and no paid services.
        Settings.embed_model = resolve_local_embed_model()
        persist_dir = Path(PERSIST_DIR)
        # Rebuild local index from current docs to keep storage consistent with source files.
        index = VectorStoreIndex(nodes=nodes, show_progress=True)
        index.storage_context.persist(persist_dir=str(persist_dir))
        print(
            f"Finished ingesting {len(nodes)} chunks from {len(documents)} docs into local storage: {persist_dir}"
        )
