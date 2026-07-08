from typing import TypedDict
from langgraph.graph import END, START, StateGraph
import asyncio

class HelloWorldState(TypedDict):
    message: str
    
async def hello(state: HelloWorldState) -> HelloWorldState:
    print(f"Hello Node: {state['message']}")
    # TODO: Simulate Async processing
    await asyncio.sleep(1)  # Simulate async delay
    return {"message": "Hello "+ state['message']}

async def bye(state: HelloWorldState) -> HelloWorldState:
    print(f"Bye Node: {state['message']}")
    # TODO: Simulate Async processing
    await asyncio.sleep(1)  # Simulate async delay
    return {"message": "Bye " + state['message']}

graph = StateGraph(HelloWorldState)
graph.add_node("hello", hello)
graph.add_node("bye", bye)

graph.add_edge(START, "hello")
graph.add_edge("hello", "bye")
graph.add_edge("bye", END)

runnable=graph.compile()

# TODO: Async invocation
async def main():
    output = await runnable.ainvoke({"message": "Ankit"})
    print(f"Final Result: {output}")    
    
asyncio.run(main())