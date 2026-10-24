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
#from retrievers.web_search import search_engine_chain

load_dotenv()

# load the LLM

llm = ChatOpenAI()

# define the tool

@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)

get_word_length.invoke("abc")

@tool 
def vector_search_query(query: str):
    """Use this tool to answer questions about MongoDB Atlas security and the indexed document content."""
    return rag_chain.invoke(query)

tools = [get_word_length, vector_search_query]

# create the prompt

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system", 
            "You are a helpful assistant. "
            "For any question about MongoDB Atlas, security best practices, or document content, "
            "you must use the `vector_search_query` tool before answering. "
            "Do not ask the user whether they want you to search. "
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

answer = run_agent("What are the security best practices for MongoDB Atlas?")
print(f"Answer: {answer}")
