from langchain_community.llms import LlamaCpp
from langchain_core.prompts import ChatPromptTemplate

llm = LlamaCpp(
    model_path=r"/Users/ankit/Workspace/Projects/ankit-github/AI-ML-DS/23.LangChain/2.Chat_Models/llama-2-7b-chat.Q8_0.gguf",
    temperature=0.75,
    max_tokens=2000,
    top_p=1,
    verbose=False,
)

question = ChatPromptTemplate.from_messages([
    ("system","answer in 5 sentences only"),
    ("human","{question}")
])
 
chain = question | llm.bind(stop=["Human:"]) # we stop here when we see the "Human" string

while True:
    question = input("Human: ")
    for chunk in chain.stream({"question": question}):
        print(chunk, end="", flush=True)
