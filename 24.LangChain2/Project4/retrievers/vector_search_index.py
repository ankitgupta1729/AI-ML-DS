from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import StrOutputParser
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pymongo import MongoClient
import certifi
import os

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")
ATLAS_CONNECTION_STRING = os.getenv("ATLAS_CONNECTION_STRING")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
ATLAS_VECTOR_SEARCH_INDEX_NAME = os.getenv("ATLAS_VECTOR_SEARCH_INDEX_NAME")


def require_env(name: str, value: str | None) -> str:
    if value:
        return value
    raise ValueError(f"Missing required environment variable: {name}")


def get_collection():
    connection_string = require_env("ATLAS_CONNECTION_STRING", ATLAS_CONNECTION_STRING)
    db_name = require_env("DB_NAME", DB_NAME)
    collection_name = require_env("COLLECTION_NAME", COLLECTION_NAME)

    client = MongoClient(
        connection_string,
        tls=True,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=10000,
    )
    collection = client[db_name][collection_name]

    try:
        client.admin.command("ping")
        print("Connected to MongoDB Atlas")
    except Exception as exc:
        raise ConnectionError(
            "Could not connect to MongoDB Atlas. Check ATLAS_CONNECTION_STRING, "
            "Atlas IP access list, cluster status, and local TLS certificates."
        ) from exc

    return collection


def build_rag_chain():
    collection = get_collection()
    index_name = require_env(
        "ATLAS_VECTOR_SEARCH_INDEX_NAME",
        ATLAS_VECTOR_SEARCH_INDEX_NAME,
    )

    loader = TextLoader("./atlas_security_notes.txt", encoding="utf-8")
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    docs = text_splitter.split_documents(data)

    print(docs[0])

    vector_store = MongoDBAtlasVectorSearch(
        collection=collection,
        embedding=OpenAIEmbeddings(disallowed_special=()),
        index_name=index_name,
    )

    if collection.count_documents({}) == 0:
        vector_store.add_documents(docs)

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 1},
    )

    template = """
Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
{context}
Question: {question}
"""
    custom_rag_prompt = PromptTemplate.from_template(template)

    return (
        {"context": retriever, "question": RunnablePassthrough()}
        | custom_rag_prompt
        | model
        | StrOutputParser()
    )


rag_chain = build_rag_chain()
