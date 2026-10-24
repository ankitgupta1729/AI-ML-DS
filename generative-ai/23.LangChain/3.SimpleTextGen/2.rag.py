# Updated imports for LangChain v0.3+
from langchain_community.llms import LlamaCpp
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
import os

# Get the script directory for correct path resolution
script_dir = os.path.dirname(os.path.abspath(__file__))
persist_dir = os.path.join(script_dir, "data")
model_path = os.path.join(script_dir, "llama-2-7b-chat.Q8_0.gguf")

# Check if model file exists
if not os.path.exists(model_path):
    print(f"Error: Model not found at {model_path}")
    print("Please download the Llama 2 model or update the path")
    exit(1)

# Initialize LlamaCpp
llm = LlamaCpp(
    model_path=model_path,
    temperature=0.75,
    max_tokens=2000,
    top_p=1,
    n_ctx=2048,
    n_batch=512,
    verbose=False,
)

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load the existing vectorstore
vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embeddings)

# Create retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

# Function to extract question from dict
def get_question(input_dict):
    """Extract the question string from the input dictionary"""
    return input_dict["question"]

# Function to format docs
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Create the prompt template
template = """
Answer the question based only on the following context:
{context}   

Question: {question}
Answer:
"""

prompt = ChatPromptTemplate.from_template(template)

# Create the chain - FIXED: extract question before passing to retriever
chain = (
    {
        "context": RunnableLambda(get_question) | retriever | RunnableLambda(format_docs),
        "question": RunnableLambda(get_question)
    }
    | prompt
    | llm
)

# Stream the response
print("Question: What is the chat model?\n")
print("Answer: ", end="", flush=True)
for chunk in chain.stream({"question": "What is the chat model?"}):
    print(chunk, end="", flush=True)
print("\n")