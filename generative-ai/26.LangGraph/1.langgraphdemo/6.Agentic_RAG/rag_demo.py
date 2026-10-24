import os
from pathlib import Path
from typing import List, TypedDict
import warnings

os.environ.setdefault(
    "USER_AGENT",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X) LangGraph-RAG-Demo/1.0",
)

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core._api.deprecation import LangChainPendingDeprecationWarning
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

warnings.simplefilter("ignore", LangChainPendingDeprecationWarning)
warnings.filterwarnings(
    "ignore",
    message="The default value of `allowed_objects` will change in a future version.*",
)

from langgraph.graph import END, START, StateGraph

load_dotenv(Path(__file__).with_name(".env"))

os.environ.setdefault(
    "USER_AGENT",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X) LangGraph-RAG-Demo/1.0",
)

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError(
        "OPENAI_API_KEY is missing. Add it to 6.Agentic_RAG/.env before running this script."
    )

news_urls = [
    "https://www.bbc.com/news",
    "https://www.cnn.com/world",
    "https://www.nytimes.com/section/world",
    "https://apnews.com/world-news",
    "https://www.aljazeera.com/news/",
]

loader = WebBaseLoader(
    web_paths=news_urls,
    header_template={"User-Agent": os.environ["USER_AGENT"]},
    requests_kwargs={"timeout": 30},
    continue_on_failure=True,
    raise_for_status=False,
    show_progress=False,
)


def load_news_documents() -> List[Document]:
    documents = loader.load()
    if not documents:
        raise RuntimeError(
            "Unable to load any news sources. Check your internet connection and try again."
        )
    return documents


def build_retriever():
    docs_list = load_news_documents()
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=300,
        chunk_overlap=20,
    )
    doc_splits = text_splitter.split_documents(docs_list)

    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name="current-affairs-news",
        embedding=OpenAIEmbeddings(),
    )
    return vectorstore.as_retriever(search_kwargs={"k": 4})


retriever = build_retriever()

prompt = ChatPromptTemplate.from_template(
    """
    You are a news analyst summarizing the latest current affairs.
    Use only the retrieved articles to provide a concise summary.
    Highlight key global events and developments.
    Return the answer as short bullet points only.
    Each bullet should contain one headline or development.
    Do not write any introductory sentence before the bullets.

    Question: {question}
    News Articles:
    {context}

    Summary:
    """
)

model = ChatOpenAI()
current_affairs_chain = prompt | model | StrOutputParser()


class CurrentAffairsGraphState(TypedDict):
    question: str
    retrieved_news: List[Document]
    generation: str


def format_retrieved_news(retrieved_news: List[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in retrieved_news)


def retrieve_current_affairs(state: CurrentAffairsGraphState):
    print("--- Retrieving Current Affairs ---")
    question = state["question"]
    retrieved_news = retriever.invoke(question)
    return {"question": question, "retrieved_news": retrieved_news}


def generate_current_affairs_summary(state: CurrentAffairsGraphState):
    print("--- Generating Current Affairs Summary ---")
    question = state["question"]
    retrieved_news = state["retrieved_news"]
    generation = current_affairs_chain.invoke(
        {
            "question": question,
            "context": format_retrieved_news(retrieved_news),
        }
    )
    return {
        "question": question,
        "retrieved_news": retrieved_news,
        "generation": generation,
    }


def create_current_affairs_workflow():
    workflow = StateGraph(CurrentAffairsGraphState)
    workflow.add_node("retrieve_current_affairs", retrieve_current_affairs)
    workflow.add_node(
        "generate_current_affairs_summary",
        generate_current_affairs_summary,
    )
    workflow.add_edge(START, "retrieve_current_affairs")
    workflow.add_edge("retrieve_current_affairs", "generate_current_affairs_summary")
    workflow.add_edge("generate_current_affairs_summary", END)
    return workflow.compile()


current_affairs_graph = create_current_affairs_workflow()

inputs = {"question": "What are the top global headlines today?"}
response = current_affairs_graph.invoke(inputs)

print("\n--- Current Affairs Summary ---")
print(response["generation"])
