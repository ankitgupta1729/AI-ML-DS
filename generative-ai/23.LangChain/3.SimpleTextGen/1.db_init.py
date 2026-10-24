from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "sample.txt")

# Verify the file exists
print(f"Looking for file at: {file_path}")
print(f"File exists: {os.path.exists(file_path)}")

# Load the document
loader = TextLoader(file_path)

# Text splitter
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=400, 
    chunk_overlap=100
)

# Load and split documents
docs = loader.load_and_split(text_splitter=text_splitter)

# Create embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Create and persist the Chroma database
db = Chroma.from_documents(
    docs, 
    embedding=embeddings, 
    collection_name="my_collection", 
    persist_directory=os.path.join(script_dir, "data")  # Also save data in script directory
)

print(f"Successfully created Chroma database with {len(docs)} documents")