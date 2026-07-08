# This is the basic building block code for an agent. 
from typing import TypedDict, Annotated

from langchain_core.messages import AnyMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages

from dotenv import load_dotenv

from agent.tools import (
    get_n_random_words
)

load_dotenv()

#### Step 1 #####
# The agent state: this is like the short-term memory(working memory) of the agent which allows th agent to
# keep track of its progress as it completes each task. Most importantly what actions it has actually taken and outcome 
# of each of these. This is what the reasoning model is observing in thought-action-observation cycle. And the main sort of thing that 
# it needs to get from that observation is working out whether the step it took was successful and it can move on to the next action, 
# whether it needs to retry the current step. And you can see that the only field that we have in the agent state so far is the messages.
# Now this is the very important field in the agent state in LangGraph because it essentially allows the agent to keep a running
# conversation history of everything that's gone through the agent so far. So, everything that has been passed in, including by the user and
# everything that has been output in each step that the agent has taken. So, the next thing that our React agent of course needs is
# some tools.    
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

#### Step 2 #####
# At the moment, I have one custom built-in tool that I have created called get_n_random_words. First we import it as above and then we
# assign that to this local_tools list below. Next thing that our agent needs is an LLM.   


# Tools: these are additional capabilities the agent can use to achieve a goal
local_tools = [
    get_n_random_words,
]

#### Step 3 #####
# Now, we are going to start by using a model from OpenAI, called GPT-4o (a powerful reasoning model and also it is a multi-modal model, 
# so it can take both text and image inputs and it is very fast also and while using local model, things become slow down).

# Now, the final and most important component is the assistant function. This is the heart of the agent. It's basically the infrastructure
# that allows our reasoning model to act as the reasoning engine in the agent. So, basically the job of this function is to take the
# information contained in the agent state, that's basically the argument that it takes. And then it passes this information to 
# the LLM for processing and call any available tools to complete the next plan step that the agent wants to do. And then update the 
# agent state following this action. And there's a few important components that this function has to accomplish that. 

# The first is the system message. So, basically this is going to be input as part of the initial prompt to the LLM when we start 
# the entire process. And it's exactly the same as if you are using a chat LLM like GPT or Claude and you give it a lot of context or
# instructions to allow it to understand a task you want to do. So, here, we have very basic instructions so far. We will expand this 
# prompt later.

# Next thing we need to do is to bind the tools to assistant so that they are available to it when the agent is running. Naturally, 
# we have talked about the core components which is the reasoning LLM. 

# What is returned from this function is a dictionary which contains all of the necessary information to update the agent state. 

############################################### 

# The assistant function: this acts like the central planner of the agent,
# allowing the LLM to decompose a problem, evaluate the steps already carried
# out, and select which tools to use.

def assistant(state: AgentState):
    textual_description_of_tools = """
    def get_n_random_words(language: str,
                       n: int, ) -> list:
    Selects a specified number of random words from a language-specific word list.

    The function reads a JSON file containing words for the specified language from
    a predefined directory. It then selects `n` random words from the file and
    returns them in a list.

    :param language: A string representing the language for which to fetch the word list.
    :param n: An integer specifying the number of random words to retrieve.
    :return: A list containing `n` randomly selected words.
    """
    sys_msg = SystemMessage(content=f""" You are a helpful language learning assistant. You have access to the following tools: {textual_description_of_tools}
        The user is going to give you a command.
        
        Your job is to check:
        1. Which source language the user wants words from.
        2. How many words they want.
        
        Here are some example workflows:
        input: Get 20 random words in Spanish.
        Source Language: Spanish
        Number of words: 20
        
        input: Get 10 random words in German.
        Source Language: German
        Number of words: 10
        """
    )

    # The LLM: the model that will act as the reasoning engine at the centre of the agent.
    # Reasoning LLMs work best in this role.
    tools = assistant.tools if hasattr(assistant, 'tools') else []

    llm = ChatOpenAI(model="gpt-4o")

    llm_with_tools = llm.bind_tools(
        tools,
        parallel_tool_calls=False
    )
    return {
        "messages": [llm_with_tools.invoke([sys_msg]+state["messages"])],
    }

