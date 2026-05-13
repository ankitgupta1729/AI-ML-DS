import os
import sys
from pydantic import BaseModel, Field
from langgraph.graph import END, START, StateGraph

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from util.langgraph_util import display

class HelloWorldState(BaseModel): # this is a state definition from where langgraph workflow starts.
    message: str = Field(min_length=3,max_length=100) # message is a key of string type which is actually a state and we can have many states.
    id: int = Field(default=0) # this is another state which is of integer type and has a default value of 0.

# Here, we have two nodes i.e. "hello" and "bye" which are actually functions.
    
def hello(state: HelloWorldState): # this hello node takes the state as HelloWorldState
    print(f"Hello Node: {state.message}") # this will print the state
    return {"message": "Hello " + state.message} # it will update the message state, so here langgraph is updating the state 

def bye(state: HelloWorldState):
    print(f"Bye Node: {state.message}")
    return {"message": "Bye " + state.message}

# Now, once we have the nodes, we create the state graph. 

graph = StateGraph(HelloWorldState)
graph.add_node("hello", hello) # we add the hello node to the graph
graph.add_node("bye", bye) # we add the bye node to the graph


graph.add_edge("hello", "bye") # we add an edge from hello node to bye node
graph.add_edge("bye", END) # we add an edge from bye node to END
graph.set_entry_point("hello") # we set the entry point of the graph to hello node

runnable = graph.compile() # we compile the graph to make it runnable
display(runnable) # we display the compiled graph
output = runnable.invoke(HelloWorldState(message="Ankit", id=123)) # we invoke the graph with the initial state
print(f"Final Output: {output}") # we print the final output
