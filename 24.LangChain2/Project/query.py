import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import (
    CharacterTextSplitter,
)
from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain_community.vectorstores import Chroma
from openai import OpenAI
import warnings
warnings.filterwarnings("ignore")

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text_to_embed):
    response = client.embeddings.create(input=[text_to_embed], model="text-embedding-ada-002")
    print(response.data[0].embedding)

template: str = """/
    You are a customer support specialist /
    question: . 
    You assist users with general inquiries based on  /
    and  technical issues. /
    """

# define prompt
system_message_prompt_template = SystemMessagePromptTemplate.from_template(template)
chat_prompt_template = ChatPromptTemplate.from_messages([system_message_prompt_template, 
                                                         HumanMessagePromptTemplate.from_template("{user_query}")])


# init model

model = ChatOpenAI()

# indexing
def load_split_documents():
    """Load a file from path, split it into chunks, embed each chunk and load it into the vector store."""
    raw_text = TextLoader("docs/faq.txt").load()
    text_splitter = CharacterTextSplitter(chunk_size=30, chunk_overlap=0, separator=".") # maximum 30 characters in each chunk 
    # and last 0 characters of previous chunk are overlapping with first 0 characters of next chunk and break the text into chunks at the period character
    # we can also use "\n" as separator to break the text into chunks at the newline character
    chunks = text_splitter.split_documents(raw_text)
    print(f"Number of chunks: {len(chunks)}")
    print(f"First chunk: {chunks[0].page_content}")
    print(f"Second chunk: {chunks[1].page_content}")
    print("--------------------------------------------------------------")
    return chunks


# convert to embeddings
def load_embeddings(documents, user_query):
    """Create a vector store from a set of documents."""
    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(documents,embeddings)
    docs = db.similarity_search(user_query,k=5) # here we are retrieving the top 5 most similar/relevant documents to the user query
    print(docs)
    print("--------------------------------------------------------------")
    get_embedding(user_query)
    _ =[get_embedding(doc.page_content) for doc in docs] # here we are getting the embeddings for the user query and the retrieved documents to see how similar they are in the vector space
    
def generate_response(query):
    """Generate a response to a user query."""
    chain = chat_prompt_template | model | StrOutputParser() # here we are creating a chain that takes the user query as input, passes it through the prompt template and then generates a response using the model and finally parses the output to a string
    return chain.invoke({"user_query": query}) # here we are invoking the chain with the user query as input

def query(query):
    """Query the model with a user query."""
    documents = load_split_documents()
    load_embeddings(documents, query)
    return generate_response(query) # here we are generating a response to the user query using the generate_response function

query("what is your return policy?")
