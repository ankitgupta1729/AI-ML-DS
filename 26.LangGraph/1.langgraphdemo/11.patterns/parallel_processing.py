from typing import TypedDict,Annotated
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).with_name(".env"))

# Define State

class MarketResearchState(TypedDict):
    query: str
    trends: str
    competitors: str
    sentiment: str
    summary: str
    
llm = ChatOpenAI()

def fetch_trends(state: MarketResearchState):
    response = llm.invoke(f"What are the latest market trends for {state['query']}")
    return {"trends": response.content}

def analyze_competitors(state: MarketResearchState):
    response = llm.invoke(f"List top competitors in {state['query']} market")
    return {"competitors": response.content}

def extract_sentiment(state: MarketResearchState):
    response = llm.invoke(f"What do customers feel about products in {state['query']} category")
    return {"sentiment": response.content}

def summarize(state: MarketResearchState):
    summary_prompt = f"""
    Product Research Summary:
    - Trends: {state['trends']}
    - Competitors: {state['competitors']}
    - Customer Sentiment: {state['sentiment']}

    Provide strategic insights for entering the {state['query']} market.
    """
    response = llm.invoke(summary_prompt)
    return {"summary": response.content}
    
    
# The above three nodes are not dependent on each other and so they can be executed in parallel

graph_builder = StateGraph(MarketResearchState)

# Add nodes
graph_builder.add_node("fetch_trends", fetch_trends)
graph_builder.add_node("analyze_competitors", analyze_competitors)
graph_builder.add_node("extract_sentiment", extract_sentiment)
graph_builder.add_node("summarize", summarize)

# TODO: Add edges for parallel execution
graph_builder.add_edge(START, "fetch_trends")
graph_builder.add_edge(START, "analyze_competitors")
graph_builder.add_edge(START, "extract_sentiment")

graph_builder.add_edge("fetch_trends", "summarize")
graph_builder.add_edge("analyze_competitors", "summarize")
graph_builder.add_edge("extract_sentiment", "summarize")

# compile the graph
graph = graph_builder.compile()

# Run it

inputs = {"query": "Smart Water Bottle"}
result = graph.invoke(inputs)

# Output

print("\n--- Market Research Summary ---")
print(result["summary"])