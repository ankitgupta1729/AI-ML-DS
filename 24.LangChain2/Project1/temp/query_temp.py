from langchain_classic.chains import create_retrieval_chain, create_history_aware_retriever
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")

load_dotenv()

llm = ChatOpenAI()
_default_chat_history = []


contextualize_q_system_prompt = (
    "Given a chat history and the latest user question which might reference "
    "context in the chat history, formulate a standalone question which can be "
    "understood without the chat history. Do NOT answer the question, just "
    "reformulate it if needed and otherwise return it as is."
)
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

qa_system_prompt = (
    "You are an assistant for question-answering tasks. Use the following "
    "pieces of retrieved context to answer the question.\n\n{context}\n\n"
    "If you don't know the answer, just say that you don't know. Use three "
    "sentences maximum and keep the answer concise."
)
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

documents = TextLoader("./docs/faq.txt").load()
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0, separator="\n")
splits = text_splitter.split_documents(documents)
db = Chroma.from_documents(splits, OpenAIEmbeddings())
retriever = db.as_retriever()

history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


def query(user_query, chat_history=None):
    """Answer a user question using the RAG chain.

    If chat_history is provided, it is used for context and mutated in place
    with the new exchange. Otherwise a module-level list is used (CLI mode).
    """
    if chat_history is None:
        chat_history = _default_chat_history
    response = rag_chain.invoke({
        "chat_history": chat_history,
        "input": user_query,
    })
    chat_history.extend([
        HumanMessage(content=user_query),
        AIMessage(content=response["answer"]),
    ])
    return response
