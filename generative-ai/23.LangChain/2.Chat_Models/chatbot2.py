from langchain_community.llms import LlamaCpp
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_classic.memory import ConversationBufferMemory  # Changed this line
from operator import itemgetter

# Rest of your code remains exactly the same
llm = LlamaCpp(
    model_path=r"/Users/ankit/Workspace/Projects/ankit-github/AI-ML-DS/23.LangChain/2.Chat_Models/llama-2-7b-chat.Q8_0.gguf",
    temperature=0.75,
    max_tokens=2000,
    top_p=1,
    verbose=False,
)

prompt = ChatPromptTemplate.from_messages([
    ("system","answer in 5 sentences only"),
    MessagesPlaceholder(variable_name = "chat_history"),
    ("human","{question}")
])

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    input_key="question",
    output_key="output",
)
 
chain = RunnablePassthrough.assign(
    chat_history = RunnableLambda(lambda x: memory.load_memory_variables(x)["chat_history"])
) | prompt | llm.bind(stop=["Human:"])

while True:
    try:
        text = ""
        question = input("Human: ").strip()
        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            break

        for chunk in chain.stream({"question": question}):
            print(chunk, end="", flush=True)
            text += chunk
        print()

        memory.save_context({"question": question}, {"output": text})
    except (EOFError, KeyboardInterrupt):
        print()
        break