1. When we create AI agents using LangChain then these AI agents are LLMs with access to external tools. They operate in a loop acting as a reasoning engine that decides which tool they should use at each step to make given work done. 

! [LangChain](./images/1.png)

But as this agentic workflow becomes complex this linear flow of langchain is not good enough that's where LangGraph comes into play.

2. LangGraph is built on top of LangChain allows us to create graph-based workflow to orchestrate the behavior of AI agents. 

A LangGraph contains 3 important components:

- Nodes: A node represents the specific task ranging simple processing logic to a complex self-contained agent. Each node itself can be agent of its own. 
- Edges: Each node can be connected with an edge. Edge represents the transition between different nodes in the workflow or graph.
- State: It represents the state of the workflow and as the workflow happens then the state gets updated at each node. 

LangGraph comes with the following in-built features:

- Memory/state sharing
- Conditional Routing
- Tool Calling
- Human in the loop
- Persistence
- Async and Streaming

! [LangGraph](./images/2.png)

3. Hello World LangGraph workflow:

Every LangGraph workflow starts with the state definition. 

please check the code in `hello_world.py` in `1.basics` folder and see the comments.

4. For setup of this tutorial, go to `1.langgraphdemo` folder and run `python3 -m venv .venv` and then  `source .venv/bin/activate` and `pip3 install -r requirements.txt`.

5. Now go to `1.basics` folder and run `python3 1.basics/hello_world.py` and see the output as:

```
 ankit@MacBook-Air 💻  …/AI-ML-DS/26.LangGraph/1.langgraphdemo on  main [ ✱1 ?102  ] 🐍 (.venv) 🐍  v3.14.2 
╰─ python3 1.basics/hello_world.py
/Users/ankit/Workspace/Projects/ankit-github/AI-ML-DS/26.LangGraph/1.langgraphdemo/.venv/lib/python3.14/site-packages/langgraph/cache/base/__init__.py:8: LangChainPendingDeprecationWarning: The default value of `allowed_objects` will change in a future version. Pass an explicit value (e.g., allowed_objects='messages' or allowed_objects='core') to suppress this warning.
  from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
Hello Node: Ankit
Bye Node: Hello Ankit
Final Output: {'message': 'Bye Hello Ankit'}
```

6. Graph must have an entrypoint: add at least one edge from START to another node.

You can just delete `graph.add_edge(START, "hello") # we add an edge from START to hello node` from `hello_world.py` and run the script `python3 1.basics/hello_world1.py` and see the error.

To resolve this error, we can also add `graph.set_entry_point("hello") # we set the entry point of the graph to hello node` in the code and then run the script `python3 1.basics/hello_world2.py` and see the output as:

7. Now, to see the workflow an image, run the script as `python3 1.basics/hello_world3.py` and see the image.

8. We use the `Pydantic` library to validate the state of the graph.

To restricting the length of the message, we can use `Field` method.

Run the script as `python3 1.basics/hello_world4.py` and see the output.

9. You can make the "id" field option by importing `Optional` from `typing` library.

Run the script as `python3 1.basics/hello_world5.py` and see the output.

10. When we launch a langgraph workflow using the `invoke` method everything happens in a synchronous fashion that is the main thread in which the main thread happens is blocked until all the nodes are done with their work. When any new requests come then they have to wait until this blocked thread completes. That is where Asynchronous invocation comes into the picture and we use `ainvoke` method to do everything in asynchronous manner. 

Asynchronous method is simple. Use `async` keyword before any node functions and then we use `runnable.ainvoke()` method in async context of main thread to run the workflow for its working.  

Run the script as `python3 2.asyncandstreaming/async_demo.py` and see the output with delay of 1 second.

11. Langgraph also supports streaming. 

Streaming Types: values, updates, messages, custom, debug.

Run the script as `python3 2.asyncandstreaming/streaming_demo.py` and see the output.

12. Conditional Routing:

Here, we take the example of customer service use case. Here, user send the 2 things: request and the priority.

Now, we can run the script as `python3 3.conditional_routing/customer_service.py` and see the output.

13. Reducers:

Using reducers, we can override messages.

Run the script as `python3 4.reducers/reducer_demo.py` and see the output with `add` function is working as reducer and will add the discount.

For messgaes state, run the script as `python3 4.reducers/reducers_messagesstate_demo.py` and see the output.

14. Tool Calling:

Run the script as `python3 5.tool_calling/toolcalling_demo.py` and see the output.

Run the script as `python3 5.tool_calling/toolnode_manual.py` and see the output.

Run the script as `python3 5.tool_calling/toolnode_auto.py` and see the output.

15. Agentic RAG:

Run the script as `python3 6.agentic_rag/rag_demo.py` and see the output.

16. Human in the loop:


