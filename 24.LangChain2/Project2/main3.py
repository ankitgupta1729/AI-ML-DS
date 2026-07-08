from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.runnables import chain
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma
from typing import List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(temperature=0)
llm_function_calling = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

class Search(BaseModel):
    
    """Search for information about a clothing category."""
    
    query: str = Field(
        ...,
        description="Query to look up",
        )
    category: str = Field(
        ...,
        description="Category to look things up for. Should be `SHOES` or `SHIRTS`.",
        ) 

system = """ You have the ability to issue search queries to get information to help answer user information.
If you answer the general inquiries, refer to the company name only without the clothes category (shirts, shoes ...).
"""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)
structured_llm = llm_function_calling.with_structured_output(Search, method="function_calling")
query_analyzer = {"question": RunnablePassthrough()} | prompt | structured_llm

# Prompt for Generation and retrieval tasks

template: str = """/
You are a customer support specialist/
who answers question: {question}.
You assist users with general inqueries based on {context} /
and technical issues. /
"""

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        ("human", "{question}"),
    ]
)

# Create Index and connect to datasource
embeddings = OpenAIEmbeddings(model = "text-embedding-3-small")

raw_text_shoes = TextLoader('./docs/faq_shoes.txt').load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
documents = text_splitter.split_documents(raw_text_shoes)
vector_store = Chroma.from_documents(documents, embeddings, collection_name="shoes_collection")
retriever_shoes = vector_store.as_retriever()

raw_text_shirts = TextLoader('./docs/faq_shirts.txt').load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
documents = text_splitter.split_documents(raw_text_shirts)
vector_store = Chroma.from_documents(documents, embeddings, collection_name="shirts_collection")
retriever_shirts = vector_store.as_retriever()

# Retrieval with query analysis

retrievers = {
    "SHOES": retriever_shoes,
    "SHIRTS": retriever_shirts,
}

def select_retriever_query_anaysis(question):
    """Select a retriever based on the query analysis."""
    structured_output = query_analyzer.invoke({"question": question})
    category_key = structured_output.category.strip().upper()
    retriever = retrievers.get(category_key)
    if retriever is None:
        raise KeyError(
            f"Unknown category={structured_output.category!r}. Expected one of: {', '.join(sorted(retrievers))}"
        )
    return retriever

def query(user_query: str):
    """Final chain to query, retrieve information and generate augmented response."""
    retriever = select_retriever_query_anaysis(user_query)
    return (
        {"context": retriever, "question": RunnablePassthrough()}
        | chat_prompt_template
        | llm
        | StrOutputParser()
    ).invoke(user_query)
    
response = query("How long do we have to return shirts?")
#response = query("What type of shoes you sell?")
print(response)
