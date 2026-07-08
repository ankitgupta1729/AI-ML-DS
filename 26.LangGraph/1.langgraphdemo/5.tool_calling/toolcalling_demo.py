import os
from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool


def load_local_env() -> None:
    env_path = Path(__file__).with_name(".env")
    if not env_path.exists():
        return

    for raw_line in env_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_local_env()


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
llm = ChatOpenAI()
llm_with_tools = llm.bind_tools(tools)

messages = [
    HumanMessage(content="Can you recommend some good restaurants in Munich?")
]

# TODO: Invoke the llm

llm_output = llm_with_tools.invoke(messages)
print(llm_output)
