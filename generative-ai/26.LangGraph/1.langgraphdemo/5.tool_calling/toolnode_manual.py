from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langgraph._internal._constants import CONF, CONFIG_KEY_RUNTIME
from langgraph.prebuilt import ToolNode
from langgraph.runtime import DEFAULT_RUNTIME

@tool
def get_restaurant_recommendations(location:str):
    """Provide a list of top restaurant recommendations for a given location."""
    recommendations ={
        "munich": ["Hofbräuhaus", "Augustiner-Keller", "Tantris"],
        "new york": ["Le Bernardin", "Per Se", "Eleven Madison Park"],
        "paris": ["Le Meurice", "L'Arpège", "Septime"],
        }
    return recommendations.get(location.lower(), ["Sorry, I don't have recommendations for that location."]) 

# TODO: Bind the tool to the model

tools = [get_restaurant_recommendations]
tool_node = ToolNode(tools)


# TODO: Create an AIMessage for the tool call

message_with_tool_call = AIMessage(content="",
                                   tool_calls=[{'name': 'get_restaurant_recommendations', 
                                                'args': {'location': 'Munich'}, 
                                                'id': 'call_8A9RxBVLcY12ZA1RU5Xex0tP', # unique id
                                                'type': 'tool_call'}])

# tool_calls parameter that is mentioned above comes from the output of the execution of toolcalling_demo.py

# TODO: Invoke the ToolNode with the state and get the result

result = tool_node.invoke(
    {"messages":[message_with_tool_call]},
    config={CONF: {CONFIG_KEY_RUNTIME: DEFAULT_RUNTIME}},
)


# TODO: Output the result
  
print(result)  
