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

- Check `Guide` folder to understand all the code.

9. Fine-Tuning:

- Fine-Tuning Prompts: Evaluate different prompt engineering strategies
- Fine-Tuning Tools: refine tool arguments and tool scope
- Fine-Tuning graph structure: explore more reliable graph alternatives

Prompt Engineering Strategies:

- Zero-shot prompting
- Few-shot prompting
- Chain-of-thought prompting
- ...

Prompt engineering is all about designing effective inputs to get best possible responses from LLMs. Different strategies improve accuracy, coherence and relevance. 

- Zero-shot prompting: This means asking model to perform a task without giving any prior example. The model entirely relies on its pre-trained knowledge to generate a response. For example, if we ask to summarize a paragraph then model will generate a summary based on its pre-trained knowledge. It works well when task is clear. It falls under models' general capabilities.

Example: 

! [Zero-shot prompting](./images/4.png)

- Few-shot prompting: Here, instead of just asking a question, we provide few examples to guide the model. If you want to classify a movie review as positive or negative, then you can give few labeled examples to guide the model before asking about a new review. This helps the model to understand the format and expected response. 

Example:

! [Few-shot prompting](./images/5.png)

- Chain-of-thought prompting: It is useful for reasoning based tasks. Instead of asking for an answer directly, we encourage the model to break the problem in steps. If we give a math problem then instead of asking the final answer, we can prompt it for its reasoning step-by-step. This often leads more structured and more accurate responses particularly for complex and multi-step problems. 

Example:

! [Chain-of-thought prompting](./images/6.png)

Experimenting with different approaches is the key to get best results but make sure answers are correct. 

! [Experimenting with different approaches](./images/7.png)

Tools and Graph fine-tuning:

! [Tools and Graph fine-tuning](./images/8.png)
! [Tools and Graph fine-tuning](./images/9.png)
! [Tools and Graph fine-tuning](./images/10.png)
! [Tools and Graph fine-tuning](./images/11.png)

10. Production Safeguards:

- Guardrails: set of actions to ensure safe, ethical and contextually appropriate responses. This can include filtering mechanisms, response moderation and bias mediation techniques.
- Performance Optimization: techniques like caching to improve performance (e.g. latency)
- Performance Profiling: It means understanding of how our application behaves under different hardware configurations and loads i.e. mapping of hardware configurations/load to performance levels. It helps in selecting right resources and optimizing inference time.
- LLM Infrastructure: capabilities of your LLM servers
- Handling long context: techniques like context compression maintains relevant context and without using unwanted token uses.So, it is used to compare the LLM context

11. Guardrails:

It is defined as a set of actions to ensure safe, ethical and contextually appropriate responses by enforcing constraints on content, behavior and decision-making.

In principles, for chatbot, Apply guardrails across 3 levels:

- Input
- Tool calling
- Output

A. Input Guardrails:

! [Input Guardrails](./images/12.png)
! [Input Guardrails](./images/13.png)
! [Input Guardrails](./images/14.png)
! [Input Guardrails](./images/15.png)
! [Input Guardrails](./images/16.png)
! [Input Guardrails](./images/17.png)
! [Input Guardrails](./images/18.png)
! [Input Guardrails](./images/19.png)

B. Tool Calling Guardrails:

! [Tool Calling Guardrails](./images/20.png)
! [Tool Calling Guardrails](./images/21.png)

C. Output Guardrails:

! [Output Guardrails](./images/22.png)
! [Output Guardrails](./images/23.png)
! [Output Guardrails](./images/24.png)

General Remarks:

! [General Remarks](./images/25.png)

12. Performance Optimization points:

- LLM Heterogeneity
- Infrastructure
- Context Window
- Output Tokens
- Caching
- LangGraph graph
- Minimize LLM Processing

! [Performance Optimization points](./images/26.png)
! [Performance Optimization points](./images/27.png)
! [Performance Optimization points](./images/28.png)
! [Performance Optimization points](./images/29.png)
! [Performance Optimization points](./images/30.png)
! [Performance Optimization points](./images/31.png)
! [Performance Optimization points](./images/32.png)
! [Performance Optimization points](./images/33.png)
! [Performance Optimization points](./images/34.png)   


13. Performance Profiling:

Performance profiling is a process that helps us understand the performance behavior of our app w.r.t. varying load levels and resource configurations. Among others, it facilitates:

- Resource optimization
- Load handling
- Cost efficiency

! [Performance Profiling](./images/35.png)
! [Performance Profiling](./images/36.png)
! [Performance Profiling](./images/37.png)
! [Performance Profiling](./images/38.png) 
! [Performance Profiling](./images/39.png)
! [Performance Profiling](./images/40.png)


14. LLM Infrastructure:

! [LLM Infrastructure](./images/41.png)
! [LLM Infrastructure](./images/42.png)
! [LLM Infrastructure](./images/43.png) 
! [LLM Infrastructure](./images/44.png)
! [LLM Infrastructure](./images/45.png)

15. Handling long context:

! [Handling long context](./images/46.png)
! [Handling long context](./images/47.png)
! [Handling long context](./images/48.png)
! [Handling long context](./images/49.png)  
! [Handling long context](./images/50.png)

16. Demo to Client:

! [Demo to Client](./images/51.png)
! [Demo to Client](./images/52.png)
! [Demo to Client](./images/53.png)
! [Demo to Client](./images/54.png)
! [Demo to Client](./images/55.png)
! [Demo to Client](./images/56.png)

17. Key takeaways:

! [Key takeaways](./images/57.png)

18. 