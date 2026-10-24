import os
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.types import interrupt
from langgraph.types import Command

class CodingStateAssistant(TypedDict):
    task: str
    code: str
    tests: str


def load_local_env() -> None:
    env_path = Path(__file__).with_name(".env")
    if not env_path.exists():
        return

    for raw_line in env_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


load_local_env()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY is not set. Add it to 7.hitl/.env or export it before running the script."
    )

model = ChatOpenAI(api_key=api_key)

code_prompt = ChatPromptTemplate.from_template("Generate Python Code for {task}")
test_prompt = ChatPromptTemplate.from_template("Write unit tests for this code: \n{code}")

code_chain = code_prompt | model | StrOutputParser()
test_chain = test_prompt | model | StrOutputParser()

def generate_code(state):
    print("Generating code")
    code = code_chain.invoke({"task": state["task"]})
    return Command(goto="human_review", update={"code": code})
    
# TODO

def human_review(state):
    value = interrupt({
        "question": "Are you okay with the code ? Type: (yes/no)"
    })
    if value == "yes":
        return Command(goto="create_tests")
    else:
        return Command(goto=END)

def create_tests(state):
    tests = test_chain.invoke({"code": state["code"]})
    return Command(goto=END, update={"tests": tests})

def create_coding_assistant_workflow():
    workflow = StateGraph(CodingStateAssistant)
    workflow.add_node("generate_code", generate_code)
    workflow.add_node("human_review", human_review)
    workflow.add_node("create_tests", create_tests)
    # here we don't have to create edges because using `Command`, we are navigating dynamically between nodes
    workflow.set_entry_point("generate_code")
    
    return workflow.compile(checkpointer=MemorySaver() )

# Run the workflow

coding_assistant = create_coding_assistant_workflow()
inputs = {"task": "Create a function to reverse a string in python"}
thread = {"configurable": {"thread_id": "1"}}
result = coding_assistant.invoke(inputs, config=thread)

# TODO: Handle Interrupt

print("\n--- Generated Code ---")
print(result["code"])
tasks = coding_assistant.get_state(config=thread).tasks
print(tasks)
task = tasks[0]
question = task.interrupts[0].value.get("question")
user_input = input(question)
result = coding_assistant.invoke(Command(resume=user_input),config=thread)

print("\n--- Generate Tests ---")
print(result.get("tests", "No code or tests generated"))
