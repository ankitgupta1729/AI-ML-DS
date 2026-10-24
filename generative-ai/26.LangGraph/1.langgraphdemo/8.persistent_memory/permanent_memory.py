import os
from pathlib import Path
import sys
from typing import Literal, TypedDict
import warnings

from dotenv import load_dotenv
from langchain_core._api.deprecation import LangChainPendingDeprecationWarning

os.environ.setdefault("LANGGRAPH_STRICT_MSGPACK", "true")
warnings.filterwarnings("ignore", category=LangChainPendingDeprecationWarning)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from psycopg import connect
from psycopg.rows import dict_row
from langgraph.graph import END, START, StateGraph, MessagesState
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.postgres import PostgresSaver
from util.langgraph_util import display

load_dotenv(Path(__file__).with_name(".env"))

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError(
        "OPENAI_API_KEY is missing. Add it to 8.persistent_memory/.env before running this script."
    )

DB_CONNECTION_STRING = os.getenv(
    "DB_CONNECTION_STRING",
    "postgresql://postgres:ankit%40135@localhost:5432/langgraph_memory",
)

class ChatState(TypedDict):
    messages: list
    
@tool
def get_restaurant_recommendations(location:str):
    """Provide a single top restaurant recommendations for a given location."""
    recommendations ={
        "munich": ["Hofbräuhaus", "Augustiner-Keller", "Tantris"],
        "new york": ["Le Bernardin", "Per Se", "Eleven Madison Park"],
        "paris": ["Le Meurice", "L'Arpège", "Septime"],
        }
    return recommendations.get(location.lower(), ["Sorry, I don't have recommendations for that location."])

@tool
def book_table(restaurant:str, time: str):
    """Book a table at a specific restaurant and time."""
    return f"Table booked at {restaurant} at {time}"



# Bind the tool to the model
tools = [get_restaurant_recommendations, book_table]
model = ChatOpenAI().bind_tools(tools)
tool_node = ToolNode(tools)

# TODO: Define functions for the workflow

def call_model(state: MessagesState):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}

# TODO: Define conditional routing

def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return "__end__"

# Establish a database connection

with connect(DB_CONNECTION_STRING, autocommit=True, prepare_threshold=0, row_factory=dict_row) as conn:
    # TODO: Initialize postgres-backed memory
    checkpointer = PostgresSaver(conn)
    checkpointer.setup() # will create the required tables in the database

    # TODO: Define the workflow

    workflow = StateGraph(MessagesState)
    workflow.add_node("agent",call_model)
    workflow.add_node("tools",tool_node)

    workflow.add_edge(START,"agent")
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "__end__": END,
        },
    )
    workflow.add_edge("tools","agent")

    # Compile the graph with postgres-backed memory
    graph = workflow.compile(checkpointer=checkpointer)
    display(graph, Path(__file__).with_name("toolnode_auto_graph.png"))

    config = {"configurable": {"thread_id":"1"}}

    # First invoke - Get one restaurant recommendation

    response = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content=(
                        "Can you recommend just one top restaurant in paris? "
                        "The Response should contain just the restaurant name."
                    )
                )
            ]
        },
        config,
    )


    # TODO: Extract the recommended restaurant

    recommended_restaurant = response["messages"][-1].content
    print(recommended_restaurant)

    response = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content=("Book a table at this restaurant.")
                )
            ]
        },
        config,)

    final_response = response["messages"][-1].content
    print(final_response)
