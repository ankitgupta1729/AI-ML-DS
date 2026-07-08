from langchain.chains import RetrievalQA
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import ChatOpenAI, OpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from pymongo import MongoClient
from dotenv import load_dotenv
import certifi
import os

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")

DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
ATLAS_VECTOR_SEARCH_INDEX_NAME = os.getenv("ATLAS_VECTOR_SEARCH_INDEX_NAME")
ATLAS_CONNECTION_STRING = os.getenv("ATLAS_CONNECTION_STRING")

# initialize MongoDB python client
client = MongoClient(
    ATLAS_CONNECTION_STRING,
    tls=True,
    tlsCAFile=certifi.where(),
)

MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

# Create an Atlas-backed vector store from the project documents.
vector_search = MongoDBAtlasVectorSearch(
    collection=MONGODB_COLLECTION,
    embedding=OpenAIEmbeddings(disallowed_special=()),
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
)

# Sanity-check that Atlas retrieval works against the existing ingested corpus.
query = "What are the security best practices for MongoDB Atlas?"
results = vector_search.similarity_search(query)

# Instantiate Atlas Vector Search as a retriever
qa_retriever = vector_search.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4, "score_threshold": 0.7}
)

# Define a basic question-answering prompt template
prompt_template = """

Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
"""

prompt = ChatPromptTemplate.from_template(prompt_template)


def format_result(output):
    return output["result"]


def format_docs(docs):
    """Limit retrieved context so the prompt stays within the model context window."""
    trimmed_docs = []
    for doc in docs[:4]:
        trimmed_docs.append(doc.page_content[:1200])
    return "\n\n".join(trimmed_docs)


# Create the question-answering model
qa = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    retriever=qa_retriever,
    return_source_documents=True,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt},
)

retrieval_chain = (
    {"context": qa_retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)
