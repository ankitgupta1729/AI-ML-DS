import asyncio
from typing import TypedDict
from langgraph.graph import END, START, StateGraph
from langgraph.types import StreamWriter

class HelloWorldState(TypedDict):
    message: str
    
async def hello(state: HelloWorldState, writer: StreamWriter) -> HelloWorldState:
    print(f"Hello Node: {state['message']}")
    # TODO: Write custom key
    writer({"custom_key": "Custom Value"})
    return {"message": "Hello "+ state['message']}

async def bye(state: HelloWorldState) -> HelloWorldState:
    return {"message": "Bye " + state['message']}

graph = StateGraph(HelloWorldState)
graph.add_node("hello", hello)
graph.add_node("bye", bye)

graph.add_edge(START, "hello")
graph.add_edge("hello", "bye")
graph.add_edge("bye", END)

runnable=graph.compile()

# TODO: Streaming invocation
async def main() -> None:
    # async for chunk in runnable.astream({"message": "Ankit"}, stream_mode="values"):
    #     print(chunk)
    # async for chunk in runnable.astream({"message": "Ankit"}, stream_mode="updates"):
    #     print(chunk)
    # async for chunk in runnable.astream({"message": "Ankit"}, stream_mode="custom"):
    #     print(chunk)
    # async for chunk in runnable.astream({"message": "Ankit"}, stream_mode="messages"):
    #     print(chunk) # will see later when we use LLM.
    async for chunk in runnable.astream({"message": "Ankit"}, stream_mode="debug"):
        print(chunk)
    


asyncio.run(main())
    
