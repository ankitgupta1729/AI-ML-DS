from typing import TypedDict
from langgraph.graph import END, START, StateGraph

# Define the structure of the input state (customer support request)

class SupportRequest(TypedDict):
    message: str
    priority: int # 1 (high), 2 (medium), 3 (low)
    

# Function to categorize the support request based on its priority
def categorize_request(request: SupportRequest) -> str:
    print(f"Received request: {request['message']} with priority {request['priority']}")
    # TODO: Implement Conditional Routing Logic
    if 'urgent' in request['message'].lower() or request['priority'] == 1:
        return "high"
    else:        
        return "low"
    
def handle_urgent(request: SupportRequest) -> str:
    print(f"Routing to Urgent Support Team: {request}")
    return request

def handle_standard(request: SupportRequest) -> str:
    print(f"Routing to Standard Support Queue: {request}")
    return request

# Create the state graph

graph = StateGraph(SupportRequest)
graph.add_node("urgent", handle_urgent)
graph.add_node("standard", handle_standard)

graph.add_conditional_edges(START,categorize_request,{"high":"urgent","low":"standard"})
graph.add_edge("urgent", END)
graph.add_edge("standard", END)

runnable = graph.compile()

# Simulate a customer support request

print(runnable.invoke({
    "message": "My account was hacked! Urgent help needed.",
    "priority": 1}))

print(runnable.invoke({
    "message": "I need help with password reset.",
    "priority": 3}))