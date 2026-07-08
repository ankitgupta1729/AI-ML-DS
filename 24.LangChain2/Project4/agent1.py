from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.agents import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor
from retrievers.vector_search_index import rag_chain
from retrievers.web_search import web_search_chain

load_dotenv()

# load the LLM

llm = ChatOpenAI(model="gpt-4o-mini")

# define the tool

@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)

get_word_length.invoke("abc")

@tool 
def vector_search_query(query: str):
    """Use this tool only for questions about the local indexed Atlas security notes document."""
    return rag_chain.invoke(query)

@tool
def web_search_query(query: str):
    """Use this tool for questions that need web documentation, such as how to create a vector store, setup steps, or MongoDB Atlas Vector Search guides."""
    return web_search_chain.invoke(query)


tools = [get_word_length, vector_search_query, web_search_query]

# create the prompt

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system", 
            "You are a helpful assistant. "
            "Use `vector_search_query` only for questions about the local indexed Atlas security notes. "
            "Use `web_search_query` for web/documentation questions such as how to create a vector store, setup instructions, or MongoDB Atlas Vector Search guidance. "
            "Do not ask the user whether they want you to search. "
            "Always use the most relevant tool before answering. "
            "If a tool returns useful information, answer directly and concisely."
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# bind the tool to the LLM
llm_with_tools = llm.bind_tools(tools)

# create the agent

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)

# run the agent

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def run_agent(query):
    response = agent_executor.invoke({"input": query})
    return response["output"]

answer = run_agent("How to create a vector store ?")
#answer = run_agent("What is vector search ?")
print(f"Answer: {answer}")
