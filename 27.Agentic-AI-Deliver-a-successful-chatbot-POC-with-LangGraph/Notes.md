1. LLM orchestration frameworks (that provides behavior structure) includes LangChain and LangGraph etc.

LangChain provides many useful abstractions for integrating LLMs with tools and memory following more chain based execution models. It is quite useful for several use cases. This chain-based approach can sometimes lead to rigid conversation flows and performance inefficiency while handling complex multistep interactions. LangGraph inspires to overcome this limitation. LangGraph is a framework designed for managing complex AI workflows using graph based executions. Unlike traditional sequential pipeline, LanggGraph allows to define interaction flows as nodes in the graph and making them easier to manage multi-turn conversations in dynamic agent behavior. 

Some key advantages of using LangGraph:

- Stateful Conversation: It maintains memory across different turns which is crucial for contextual interactions. 
- Flexible Execution Pass: We can define multiple routes based on user inputs that enables adaptive behavior. 
- Better Performance: Graph based execution helps avoiding unnecessary preprocessing 

2. LLM (good next-word prediction skills for general tasks) includes OpenAI'S GPT, Google's Gemini, Meta's Llama etc.

3. 

#### Key chatbot capabilities

A. Respond to billing inquiries

- "Tell me my bills over the past three months"

- "How much did I pay for electricity in January?"

- "Why is my bill higher this month?"

B. Recommend electricity plans

- "Which plan do you recommend for a household of three people?"

4.

#### Outline of how we will build this

- LLMs for natural language understanding

- LangGraph to manage complex interaction flows

- Integration with database for billing history analysis and plan recommendations

5. Our chatbot should ask the clarifying questions as:

! [Clarifying questions](./images/1.png)


6. Requirements and Architecture:

! [Requirements and Architecture](./images/2.png)

! [Requirements and Architecture](./images/3.png)

7. Create Virtual Environment with Python 3.12.13 and use .env file or some other LLM server like ollama here.

Follow commands in terminal on mac:

- brew install python@3.12
- ls /opt/homebrew/bin/python3.12
- /opt/homebrew/bin/python3.12 --version
- /opt/homebrew/bin/python3.12 -m venv .venv
- source .venv/bin/activate
- python --version
- pip install -r requirements.txt

8. First run the script from the folder `27.Agentic-AI-Deliver-a-successful-chatbot-POC-with-LangGraph` as `python3 populate_db.py`.

Now, run the script `python3 main.py` and in terminal, ask "hi" and then ask "can you get me all of my billing events ?" and then ask "I want to know which month was the most expensive and which month was the least expensive ?"

For recommendations, ask "Hi, I want information about the standard plan."

For non-existing electricity plan, ask "Hi, I want information about Harry Potter electricity plan."

For recommendation based on preference, ask "Hi, can you recommend a plan that is environmentally sustainable ?" and then ask "thanks, bye".

For out-of-scope questions, ask "Hi, what is the recipe of spaghetti bolognese?".

9. 

