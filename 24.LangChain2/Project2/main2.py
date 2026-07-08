from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.runnables import chain
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
    
    """Search for information about a person."""
    
    query: str = Field(
        ...,
        description="Query to look up",
        )
    person: str = Field(
        ...,
        description="Person to look things up for. Should be `Harrison` or `Ankush`.",
        ) 

system = """ You have the ability to issue search queries to get information to help answer user information."""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)
structured_llm = llm_function_calling.with_structured_output(Search, method="function_calling")
query_analyzer = {"question": RunnablePassthrough()} | prompt | structured_llm

structured_output = query_analyzer.invoke({"question": "Where did Harrison work?"})
print(structured_output)

# Create Index and connect to datasource
embeddings = OpenAIEmbeddings(model = "text-embedding-3-small")

texts = ["Harrison worked at Kensho"]
vectorstore = Chroma.from_texts(texts, embeddings, collection_name="harrison")
retriever_harrison = vectorstore.as_retriever(search_kwargs={"k": 1})

texts = ["Ankush worked at Facebook"]
vectorstore = Chroma.from_texts(texts, embeddings, collection_name="ankush")
retriever_ankush = vectorstore.as_retriever(search_kwargs={"k": 1})

docs=vectorstore.similarity_search("Who worked at Facebook?")
#print(docs[0].page_content)

# Retrieval with query analysis

retrievers = {
    "HARRISON": retriever_harrison,
    "ANKUSH": retriever_ankush,
}

@chain 
def custom_chain(question):
    structured_output = query_analyzer.invoke({"question": question})
    # LLM may return different casing (e.g., "Ankush" vs "ANKUSH").
    person_key = structured_output.person.strip().upper()
    retriever = retrievers.get(person_key)
    if retriever is None:
        raise KeyError(
            f"Unknown person={structured_output.person!r}. Expected one of: {', '.join(sorted(retrievers))}"
        )
    return retriever.invoke(structured_output.query)

response = custom_chain.invoke("Where did Ankush work?") 
print(response[0].page_content)
