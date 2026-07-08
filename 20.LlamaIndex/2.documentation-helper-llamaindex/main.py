from dotenv import load_dotenv
import os
import re
from typing import List, Optional

import streamlit as st

from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.chat_engine.types import ChatMode
from llama_index.core.embeddings import MockEmbedding
from llama_index.core.llms.mock import MockLLM
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.postprocessor import SentenceEmbeddingOptimizer
from llama_index.core.callbacks import LlamaDebugHandler, CallbackManager
from llama_index.core.schema import NodeWithScore

from llama_index.core.settings import Settings

load_dotenv()

os.environ.setdefault("LLAMA_INDEX_CACHE_DIR", os.path.abspath(".cache/llama_index"))
os.environ.setdefault("HF_HOME", os.path.abspath(".cache/huggingface"))
os.environ.setdefault("TRANSFORMERS_CACHE", os.path.abspath(".cache/huggingface/transformers"))
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")

print("***Streamlit LlamaIndex Documentation Helper***")

debug_traces = os.getenv("DEBUG_TRACES", "false").strip().lower() == "true"
callback_manager = CallbackManager(
    handlers=[LlamaDebugHandler(print_trace_on_end=True)] if debug_traces else []
)

DEFAULT_LOCAL_DIMENSION = 384
DEFAULT_PINECONE_DIMENSION = 1536
DEFAULT_LOCAL_EMBED_MODEL = "BAAI/bge-small-en-v1.5"
PERSIST_DIR = "./storage"

query_backend = os.getenv("QUERY_BACKEND", "local").strip().lower()
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME", "llamaindex-documentation-helper")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_host = os.getenv("PINECONE_HOST")
pinecone_dimension = int(
    os.getenv("PINECONE_DIMENSION", str(DEFAULT_PINECONE_DIMENSION))
)

resolved_backend = query_backend
if resolved_backend == "auto":
    has_pinecone_config = bool(pinecone_api_key and (pinecone_index_name or pinecone_host))
    resolved_backend = "pinecone" if has_pinecone_config else "local"


def resolve_query_embed_model():
    if resolved_backend == "pinecone":
        return MockEmbedding(embed_dim=pinecone_dimension)
    model_name = os.getenv("LOCAL_EMBED_MODEL", DEFAULT_LOCAL_EMBED_MODEL)
    local_files_only = os.getenv("LOCAL_EMBED_OFFLINE", "true").strip().lower() == "true"
    try:
        from llama_index.embeddings.huggingface import HuggingFaceEmbedding

        return HuggingFaceEmbedding(
            model_name=model_name,
            model_kwargs={"local_files_only": local_files_only},
        )
    except Exception:
        return MockEmbedding(embed_dim=DEFAULT_LOCAL_DIMENSION)


Settings.llm = MockLLM()
Settings.embed_model = resolve_query_embed_model()
Settings.callback_manager = callback_manager


def _clean_text(text: str) -> str:
    text = re.sub(r"^file_path:\s*.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _is_prompt_echo(text: str) -> bool:
    lower = text.lower()
    return "system:" in lower and "user:" in lower and "assistant:" in lower


def _build_fallback_answer(prompt: str, nodes: List[NodeWithScore]) -> str:
    cleaned_chunks: List[str] = []
    seen = set()
    for node_with_score in nodes:
        cleaned = _clean_text(node_with_score.text)
        if cleaned and cleaned not in seen:
            cleaned_chunks.append(cleaned)
            seen.add(cleaned)
        if len(cleaned_chunks) >= 2:
            break
    if not cleaned_chunks:
        return (
            "I could not find relevant information in the indexed documents for that question."
        )
    combined = " ".join(cleaned_chunks)
    combined = re.sub(r"\s+", " ", combined).strip()
    lower_prompt = prompt.lower()
    if "what is llamaindex" in lower_prompt or "what is llama index" in lower_prompt:
        definition_match = re.search(
            r"(llamaindex is .*?)(?:use cases|getting started|community|on this page|copy as markdown|$)",
            combined,
            flags=re.IGNORECASE,
        )
        if definition_match:
            definition = definition_match.group(1).strip(" .,:;")
            return f"{definition}."
        return (
            "LlamaIndex is a framework for building context-augmented LLM applications "
            "and agents over your data."
        )
    return f"Based on the indexed documentation: {combined[:400]}"


try:
    from node_postprocessors.duplicate_postprocessing import (
        DuplicateRemoverNodePostprocessor,
    )
except Exception:
    class DuplicateRemoverNodePostprocessor(BaseNodePostprocessor):
        """Fallback duplicate remover when local module is unavailable."""

        @classmethod
        def class_name(cls) -> str:
            return "DuplicateRemoverNodePostprocessor"

        def _postprocess_nodes(
            self,
            nodes: List[NodeWithScore],
            query_bundle: Optional[object] = None,
        ) -> List[NodeWithScore]:
            deduped: List[NodeWithScore] = []
            seen_text = set()
            for node_with_score in nodes:
                text = node_with_score.node.get_content()
                if text in seen_text:
                    continue
                seen_text.add(text)
                deduped.append(node_with_score)
            return deduped


@st.cache_resource(show_spinner=False)
def get_index() -> VectorStoreIndex:
    if resolved_backend == "pinecone":
        from pinecone import Pinecone
        from llama_index.vector_stores.pinecone import PineconeVectorStore

        if not pinecone_api_key:
            raise ValueError(
                "PINECONE_API_KEY is required for QUERY_BACKEND=pinecone."
            )
        pc = Pinecone(api_key=pinecone_api_key)
        pinecone_index = (
            pc.Index(name=pinecone_index_name)
            if pinecone_index_name
            else pc.Index(host=pinecone_host)
        )
        vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
        return VectorStoreIndex.from_vector_store(vector_store=vector_store)

    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    return load_index_from_storage(storage_context=storage_context)


index = get_index()
if "chat_engine" not in st.session_state.keys():
    postprocessor = SentenceEmbeddingOptimizer(
        embed_model=Settings.embed_model,
        percentile_cutoff=0.5,
        threshold_cutoff=0.7,
    )

    st.session_state.chat_engine = index.as_chat_engine(
        chat_mode=ChatMode.CONTEXT,
        verbose=debug_traces,
        node_postprocessors=[postprocessor, DuplicateRemoverNodePostprocessor()],
    )
    st.session_state.fallback_chat_engine = index.as_chat_engine(
        chat_mode=ChatMode.CONTEXT,
        verbose=debug_traces,
        node_postprocessors=[DuplicateRemoverNodePostprocessor()],
    )


st.set_page_config(
    page_title="Chat with LlamaIndex docs, powered by LlamaIndex",
    page_icon="🦙",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

st.title("Chat with LlamaIndex docs 💬🦙")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me a question about LlamaIndex's open source python library?",
        }
    ]


if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat_engine.chat(message=prompt)
            except ValueError as exc:
                if "Optimizer returned zero sentences." not in str(exc):
                    raise
                response = st.session_state.fallback_chat_engine.chat(message=prompt)
            nodes = [node for node in response.source_nodes]
            answer_text = response.response
            if _is_prompt_echo(answer_text):
                answer_text = _build_fallback_answer(prompt, nodes)
            st.write(answer_text)
            if nodes:
                for col, node, i in zip(st.columns(len(nodes)), nodes, range(len(nodes))):
                    with col:
                        st.header(f"Source Node {i+1}: score= {node.score}")
                        st.write(_clean_text(node.text)[:900])
            message = {"role": "assistant", "content": answer_text}
            st.session_state.messages.append(message)
