# ---- Knowledge base ----

# ---- Prompts ----

from langchain_core.prompts import ChatPromptTemplate

CHATBOT_SCOPE = "Helping users with i) electricity billing, and ii) electricity plan recommendations."

primary_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            f"You are a helpful customer support assistant for an electricity "
            f"company. Your task is to identify the user's intent and redirect "
            f"the user to one of your specialized assistants, namely the "
            f"Spending Assistant and the Recommendation Assistant. The Spending "
            f"Assistant can resolve inquiries related to billing, whereas the "
            f"Recommendation Assistant can help the user find a better "
            f"electricity plan based on their requirements. Always answer "
            f"concisely to the user, with a human friendly tone. Never mention "
            f"the other assistants, the user must not know about them. Do not "
            f"answer to out of scope questions. Your scope is {CHATBOT_SCOPE}.",
        ),
        ("placeholder", "{messages}"),
    ]
).partial(scope=CHATBOT_SCOPE)


spending_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            f"You are a helpful customer support assistant specializing in "
            f"resolving customer inquiries related to their electricity bills. "
            f"You have the `fetch_spending_events` tool which you can use to "
            f"fetch billing events from the database. You must infer which "
            f"billing events to fetch. If the customer's inquiry is out of "
            f"your scope, or if the problem is resolved, call the `leave_skill` "
            f"tool to delegate back to the primary assistant. You must never "
            f"mention tools to the customer, so call them silently.",
        ),
        ("placeholder", "{messages}"),
    ]
)


recommendation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            f"You are a helpful customer support assistant specializing in "
            f"electricity plan recommendations. You have the "
            f"`list_supported_plans` tool to see which plans are offered by the "
            f"electricity company. You can see additional information about a "
            f"plan by calling the `fetch_plan_information` tool. You must not "
            f"make up your own plan descriptions etc. Only use the available "
            f"data that you get through your tools. If it's not clear, you may "
            f"ask the user additional questions that help you understand their "
            f"requirements before suggesting a plan. If the customer's inquiry "
            f"is out of your scope, or if the problem is resolved, call the "
            f"`leave_skill` tool to delegate back to the primary assistant. You "
            f"must never mention tools to the customer, so call them silently.",
        ),
        ("placeholder", "{messages}"),
    ]
)


# ---- Tools ----

import sqlite3
from langchain_core.tools import tool
from pydantic import BaseModel, ConfigDict, Field


class ToSpendingAssistant(BaseModel):
    """Transfers work to a specialized assistant to handle billing inquiries."""

    request: str = Field(
        description="Any necessary followup questions the spending assistant should clarify before proceeding."
    )


class ToRecommendationAssistant(BaseModel):
    """Transfers work to a specialized assistant to handle electricity plan recommendations."""

    request: str = Field(
        description="Any necessary followup questions the recommendation assistant should clarify before proceeding."
    )


@tool
def fetch_spending_events(sql_query: str) -> str:
    """
    Fetches the spending events for a given user from an SQL database.
    The SQL table is called spending_events. The table schema is given below:

    {
        event_id: INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id: INTEGER,
        plan_name: TEXT NOT NULL,
        billing_start: DATE NOT NULL,
        billing_end: DATE NOT NULL,
        amount_due: REAL
    }

    In our case, customer_id is always 1, so you can simply ignore this field.
    """

    conn = sqlite3.connect("demo.db")
    cursor = conn.cursor()

    cursor.execute(sql_query)
    result = cursor.fetchall()

    message = ""
    for entry in result:
        message += f"\n{entry}"

    conn.close()

    return message


@tool
def list_supported_plans() -> str:
    """
    Lists the electricity plans supported by the electricity company.
    """

    conn = sqlite3.connect("demo.db")
    cursor = conn.cursor()

    cursor.execute("SELECT plan_name FROM electricity_plans")
    plans = cursor.fetchall()

    message = ""
    for plan in plans:
        message += f"\n{plan}"

    conn.close()

    return message


@tool
def fetch_plan_description(sql_query: str) -> str:
    """
    Fetches the electricity plan description from the database.
    The SQL table is called electricity_plans.
    """

    conn = sqlite3.connect("demo.db")
    cursor = conn.cursor()

    cursor.execute(sql_query)
    charging_events = cursor.fetchall()

    message = ""
    for event in charging_events:
        message += f"\n{event}"

    conn.close()

    return message


class CompleteOrEscalate(BaseModel):
    """A tool to mark the current task as completed and/or to escalate control
    of the dialog to the primary assistant, who can re-route the dialog based
    on the user's needs.
    """

    cancel: bool = True
    reason: str
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "cancel": True,
                    "reason": "User changed their mind about the current task.",
                },
                {
                    "cancel": True,
                    "reason": "I have fully completed the task.",
                },
            ]
        }
    )


# ---- State ----

from typing import Annotated, Callable, Dict, Literal, Optional, TypedDict

from langgraph.graph.message import AnyMessage, add_messages


def update_dialog_stack(left: list[str], right: Optional[str]) -> list[str]:
    """Push or pop the state."""
    if right is None:
        return left
    if right == "pop":
        return left[:-1]
    return left + [right]


class ChatbotState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    user_info: str
    dialog_state: Annotated[
        list[Literal["primary", "spending", "recommendation"]],
        update_dialog_stack,
    ]


# ---- Assistants ----

from langchain_core.runnables import Runnable, RunnableConfig
from langgraph.prebuilt import tools_condition
from langgraph.graph import END


class Assistant:
    """Base assistant class which will be inherited by other assistants."""

    def __init__(self, runnable: Runnable, name: str, tools: list):
        self.runnable = runnable
        self.name = name
        self.tools = tools

    def __call__(self, state: ChatbotState, config: RunnableConfig):
        while True:
            result = self.runnable.invoke(state, config=config)

            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break

        return {"messages": result}

    def route_non_primary_assistants(self, state: ChatbotState):
        route = tools_condition(state)

        if route == END:
            return END

        tool_calls = state["messages"][-1].tool_calls

        did_cancel = any(
            tc["name"] == CompleteOrEscalate.__name__ for tc in tool_calls
        )

        if did_cancel:
            return "leave_skill"

        return f"{self.name}_tools"


class SpendingAssistant(Assistant):
    """Spending/billing assistant class."""

    def __init__(self, llm: Runnable, name="spending_assistant"):
        tools = [fetch_spending_events, CompleteOrEscalate]
        runnable = spending_prompt | llm.bind_tools(tools)
        super().__init__(runnable=runnable, name=name, tools=tools)


class RecommendationAssistant(Assistant):
    """Plan recommendation assistant class."""

    def __init__(self, llm: Runnable, name="recommendation_assistant"):
        tools = [list_supported_plans, fetch_plan_description, CompleteOrEscalate]
        runnable = recommendation_prompt | llm.bind_tools(tools)
        super().__init__(runnable=runnable, name=name, tools=tools)


class PrimaryAssistant(Assistant):
    """Primary assistant class."""

    def __init__(self, llm: Runnable, name="primary_assistant"):
        tools = [ToSpendingAssistant, ToRecommendationAssistant]
        runnable = primary_prompt | llm.bind_tools(tools)
        super().__init__(runnable=runnable, name=name, tools=tools)

    def route_primary_assistant(self, state: ChatbotState):
        route = tools_condition(state)

        if route == END:
            return END

        tool_calls = state["messages"][-1].tool_calls

        if tool_calls:
            if tool_calls[0]["name"] == ToSpendingAssistant.__name__:
                return "enter_spending"

            if tool_calls[0]["name"] == ToRecommendationAssistant.__name__:
                return "enter_recommendation"

            return "primary_assistant_tools"

        raise ValueError("Invalid route")


# ---- Graph helpers ----

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI

import os
import json
from copy import deepcopy
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.base import BaseCheckpointSaver


def handle_tool_error(state) -> dict:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls

    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }


def create_tool_node_with_fallback(tools: list) -> dict:
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)],
        exception_key="error",
    )


def pop_dialog_state(state) -> dict:
    """
    Pop the dialog stack and return to the main assistant.

    This lets the full graph explicitly track the dialog flow and delegate
    control to specific sub-graphs.
    """

    messages = []

    if state["messages"][-1].tool_calls:
        messages.append(
            ToolMessage(
                content="Resuming dialog with the primary assistant.",
                tool_call_id=state["messages"][-1].tool_calls[0]["id"],
            )
        )

    return {
        "dialog_state": "pop",
        "messages": messages,
    }


def create_entry_node(assistant_name: str, new_dialog_state: str) -> Callable:
    def entry_node(state: TypedDict) -> dict:  # type: ignore
        tool_call_id = state["messages"][-1].tool_calls[0]["id"]

        return {
            "messages": [
                ToolMessage(
                    content=(
                        f"The assistant is now the {assistant_name}. "
                        f"Reflect on the above conversation between the host assistant and the user. "
                        f"The user's intent is unsatisfied. Use the provided tools to assist the user. "
                        f"Remember, you are {assistant_name}, and the identification, resolution, "
                        f"or any other action is not complete until after you have successfully invoked "
                        f"the appropriate tool. If the user changes their mind or needs help for other "
                        f"tasks, call the CompleteOrEscalate function to let the primary assistant take "
                        f"control. Do not mention who you are - just act as the proxy for the assistant."
                    ),
                    tool_call_id=tool_call_id,
                )
            ],
            "dialog_state": new_dialog_state,
        }

    return entry_node


def route_to_workflow(
    state: TypedDict,  # type: ignore
) -> Literal["primary_assistant", "spending_assistant", "recommendation_assistant"]:
    """If we are in a delegated state, route directly to the appropriate assistant."""

    dialog_state = state.get("dialog_state")

    if not dialog_state:
        return "primary_assistant"

    if dialog_state[-1] == "spending":
        return "spending_assistant"

    if dialog_state[-1] == "recommendation":
        return "recommendation_assistant"

    return "primary_assistant"


def ckpnt_to_dict(checkpoint: BaseCheckpointSaver) -> Dict:
    checkpoint_dict = deepcopy(checkpoint)

    def convert(obj):
        if hasattr(obj, "model_dump"):
            return obj.model_dump()
        if isinstance(obj, dict):
            return {k: convert(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [convert(v) for v in obj]
        return obj

    return convert(checkpoint_dict)


# ---- Chatbot ----

class ChatBot:
    def __init__(self):
        load_dotenv()

        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.checkpoint_saver = MemorySaver()
        self.checkpoint_file = None
        self.config = {"configurable": {"thread_id": 0}}

        if not os.path.exists("checkpoints"):
            os.makedirs("checkpoints")

    def build_graph(self):
        # ---- Define the various assistants of the chatbot ----
        primary_assistant = PrimaryAssistant(self.llm)
        spending_assistant = SpendingAssistant(self.llm)
        recommendation_assistant = RecommendationAssistant(self.llm)

        # ---- Specify the state of the LangGraph graph. ----
        builder = StateGraph(ChatbotState)

        # ============================================================================
        # Primary assistant nodes and edges
        # ============================================================================

        builder.add_node("primary_assistant", primary_assistant)

        builder.add_node(
            "primary_assistant_tools",
            create_tool_node_with_fallback(primary_assistant.tools),
        )

        builder.add_conditional_edges(
            "primary_assistant",
            primary_assistant.route_primary_assistant,
            [
                "enter_spending",
                "enter_recommendation",
                "primary_assistant_tools",
                END,
            ],
        )

        builder.add_edge("primary_assistant_tools", "primary_assistant")

        # ============================================================================
        # Spending assistant nodes and edges
        # ============================================================================

        builder.add_node(
            "enter_spending",
            create_entry_node("Spending Assistant", "spending"),
        )

        builder.add_node("spending_assistant", spending_assistant)

        builder.add_edge("enter_spending", "spending_assistant")

        builder.add_node(
            "spending_assistant_tools",
            create_tool_node_with_fallback(spending_assistant.tools),
        )

        builder.add_edge("spending_assistant_tools", "spending_assistant")

        builder.add_conditional_edges(
            "spending_assistant",
            spending_assistant.route_non_primary_assistants,
            [
                "spending_assistant_tools",
                "leave_skill",
                END,
            ],
        )

        # ============================================================================
        # Recommendation assistant nodes and edges
        # ============================================================================

        builder.add_node(
            "enter_recommendation",
            create_entry_node("Recommendation Assistant", "recommendation"),
        )

        builder.add_node("recommendation_assistant", recommendation_assistant)

        builder.add_edge("enter_recommendation", "recommendation_assistant")

        builder.add_node(
            "recommendation_assistant_tools",
            create_tool_node_with_fallback(recommendation_assistant.tools),
        )

        builder.add_edge("recommendation_assistant_tools", "recommendation_assistant")

        builder.add_conditional_edges(
            "recommendation_assistant",
            recommendation_assistant.route_non_primary_assistants,
            [
                "recommendation_assistant_tools",
                "leave_skill",
                END,
            ],
        )

        # ---- From secondary assistant to `leave_skill` then to primary. ----
        builder.add_node("leave_skill", pop_dialog_state)
        builder.add_edge("leave_skill", "primary_assistant")

        # ---- Allow persistence in specialized assistants. ----
        builder.add_conditional_edges(
            START,
            route_to_workflow,
            [
                "primary_assistant",
                "spending_assistant",
                "recommendation_assistant",
            ],
        )

        # ---- Compile the graph. ----
        self.graph = builder.compile(checkpointer=self.checkpoint_saver)

        # Draw the graph and inspect if it seems correct.
        self.graph.get_graph().draw_mermaid_png(
            output_file_path="chatbot_graph.png"
        )


if __name__ == "__main__":
    from colorama import Fore, init

    init(autoreset=True)

    chatbot = ChatBot()
    chatbot.build_graph()

    print("Chatbot initialized. Type `exit` to end the chat.")

    while True:
        user_input = input("User: ")

        if user_input.lower() == "exit":
            print("Chatbot session ended.")
            break

        bot_reply = None

        for s in chatbot.graph.stream(
            {"messages": [HumanMessage(content=user_input, name="user")]},
            config=chatbot.config,
        ):
            if "__end__" not in s:
                print("-" * 50)
                print(Fore.LIGHTMAGENTA_EX + f"Internal graph message: {s}")
                for node_update in s.values():
                    messages = node_update.get("messages") if isinstance(node_update, dict) else None
                    if messages:
                        latest_message = messages[-1] if isinstance(messages, list) else messages
                        if getattr(latest_message, "content", None):
                            bot_reply = latest_message.content

        checkpoint = chatbot.checkpoint_saver.get(chatbot.config)

        id = checkpoint["ts"].split(".")[0]
        id = id.replace(":", "-")

        chatbot.checkpoint_file = os.path.join("checkpoints", f"{id}.json")

        checkpoint_dict = ckpnt_to_dict(checkpoint)

        with open(chatbot.checkpoint_file, "w", encoding="utf-8") as f:
            json.dump(checkpoint_dict, f, ensure_ascii=False)

        if bot_reply is None:
            state_values = chatbot.graph.get_state(config=chatbot.config).values
            messages = state_values.get("messages", [])
            if messages:
                bot_reply = messages[-1].content
            else:
                bot_reply = "I processed your request, but no response message was returned."

        print("\n")
        print("-" * 50)
        print(Fore.CYAN + f"Chatbot: {bot_reply}")
        print("-" * 50)
        print("\n")
