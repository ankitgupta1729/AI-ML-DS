from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain_community.document_loaders import TextLoader
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

from dotenv import load_dotenv
import os
import warnings
warnings.filterwarnings("ignore")

# Load environment variables from .env file
load_dotenv()

llm = ChatOpenAI()
chat_history = []

contextualize_q_system_prompt = """ Given a chat history and the latest user question {input} \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history, Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is. 
    """
    
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

# build the full QA chain
qa_system_prompt = """ You are an assistant for question-answering tasks. \
Use the following pieces of retrieved context to answer the question {input}. \
based on context {context}.
If you don't know the answer, just say that you don't know. \
Use three sentences maximum and keep the answer concise. \ 
"""

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

# Indexing
documents = TextLoader("docs/faq.txt").load()
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=0, separator="\n")
splits = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings()
db = Chroma.from_documents(splits, embeddings)
retriever = db.as_retriever()


# Retrieve Chat History
history_aware_retriever = create_history_aware_retriever(
    llm,retriever,contextualize_q_prompt,
)

# Retrieve and Generate
question_answering_chain = create_stuff_documents_chain(llm=llm, prompt=qa_prompt)

def generate_response(query):
    """Generate a response to a user query"""
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answering_chain)
    return rag_chain.invoke({"input": query, "chat_history": chat_history})


def query(query):
    """Query and generate a response"""
    response = generate_response(query)
    chat_history.append(HumanMessage(content=query))
    chat_history.append(AIMessage(content=response["answer"]))
    return response["answer"]
