from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")
ATLAS_CONNECTION_STRING = os.getenv("ATLAS_CONNECTION_STRING")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
ATLAS_VECTOR_SEARCH_INDEX_NAME = os.getenv("ATLAS_VECTOR_SEARCH_INDEX_NAME")

# Connect to your Atlas cluster
client = MongoClient(ATLAS_CONNECTION_STRING)

# Define collection and index name
collection = client[DB_NAME][COLLECTION_NAME]

if client:
    print("Connected to MongoDB Atlas successfully!")
    print(client.list_database_names())

# Load the sample data
loader = TextLoader("./atlas_security_notes.txt", encoding="utf-8")
data = loader.load()

# Split PDF into smaller documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
docs = text_splitter.split_documents(data)

# Print the first document
print(docs[0].page_content)

# Instantiate the vector store

# create the vector store
vector_search = MongoDBAtlasVectorSearch.from_documents(

documents = docs,
embedding = OpenAIEmbeddings(disallowed_special=()),
collection = collection,
index_name = ATLAS_VECTOR_SEARCH_INDEX_NAME
)

qa_retriever = vector_search.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

qa = RetrievalQA.from_chain_type(
    llm=model,
    retriever=qa_retriever,
    chain_type="stuff",
)

def query_data(query):
    """run vector search queries"""
    results = vector_search.similarity_search(query)
    print(results[0].page_content)

def ask_question(question):
    """ask a question from the indexed document and print the answer"""
    answer = qa.invoke({"query": question})["result"]
    print(f"Question: {question}")
    print(f"Answer: {answer}")

query_data("MongoDB Atlas Security Best Practices")
ask_question("What are the security best practices for MongoDB Atlas?")
