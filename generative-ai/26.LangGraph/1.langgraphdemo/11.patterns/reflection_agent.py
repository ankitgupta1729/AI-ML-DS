from pathlib import Path
from typing import TypedDict

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.types import Command


load_dotenv(Path(__file__).with_name(".env"))

# Initialize OpenAI model after loading environment variables.
llm = ChatOpenAI()


class CodeState(TypedDict, total=False):
    problem_statement: str
    generated_code: str
    review_feedback: str
    refined_code: str
    iteration: int
    review_score: float


def generate_code(state: CodeState):
    print("Generating code")
    prompt = f"""
    Write a clean, efficient and well-commented python solution for following problem:
    {state['problem_statement']}
    """
    response = llm.invoke(
        [
            SystemMessage(content="You are an expert python developer."),
            HumanMessage(content=prompt),
        ]
    )
    state["generated_code"] = response.content
    state["iteration"] = 1
    state["review_score"] = 0.0
    return Command(goto="review_code", update=state)


def review_code(state: CodeState):
    print("Reviewing code")
    prompt = f"""
    Review the following Python code for correctness, readability, efficiency and best practices:
    {state['generated_code']}

    Provide a list of improvements and necessary changes.
    Also, give a review score (1-10) for:
    - correctness
    - readability
    - efficiency
    - maintainability

    Provide the average score out of 10 at the end.
    The last line should contain just the final score in the format:
    final_score:<score>
    """
    response = llm.invoke(
        [
            SystemMessage(content="You are a senior software engineer reviewing code."),
            HumanMessage(content=prompt),
        ]
    )
    state["review_feedback"] = response.content

    try:
        last_line = response.content.strip().splitlines()[-1]
        state["review_score"] = float(last_line.split(":", 1)[1].strip())
    except Exception:
        state["review_score"] = 5.0

    return Command(goto="improve_code", update=state)


def improve_code(state: CodeState):
    print("Improving code")
    print("Review Score:", state["review_score"], "Iteration:", state["iteration"])

    if state["review_score"] >= 9 or state["iteration"] >= 3:
        state["refined_code"] = state["generated_code"]
        return Command(goto=END, update=state)

    prompt = f"""
    Here is the initial Python code:
    {state['generated_code']}

    Here is the review feedback:
    {state['review_feedback']}

    Apply the suggested improvements and rewrite the code with better efficiency, readability and maintainability.
    """
    response = llm.invoke(
        [
            SystemMessage(content="You are an AI code refiner."),
            HumanMessage(content=prompt),
        ]
    )
    state["generated_code"] = response.content
    state["iteration"] = state["iteration"] + 1
    return Command(goto="review_code", update=state)


workflow = StateGraph(CodeState)
workflow.add_node("generate_code", generate_code)
workflow.add_node("review_code", review_code)
workflow.add_node("improve_code", improve_code)
workflow.set_entry_point("generate_code")
graph = workflow.compile()


if __name__ == "__main__":
    input_data: CodeState = {
        "problem_statement": "Write a python function to find the factorial of a number."
    }

    result = graph.invoke(input_data)
    print("Final Code after Reflection:\n", result["generated_code"])
    print("\nFinal Review Feedback:\n", result["review_feedback"])
