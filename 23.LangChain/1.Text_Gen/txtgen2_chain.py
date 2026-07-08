from langchain_community.llms import LlamaCpp
from langchain_core.prompts import PromptTemplate

llm = LlamaCpp(
    model_path=r"/Users/ankit/Workspace/Projects/ankit-github/AI-ML-DS/23.LangChain/Text_Gen/mistral-7b-v0.1.Q8_0.gguf",
    temperature=0.75,
    max_tokens=256,
    top_p=1,
    verbose=False,
)

question = PromptTemplate.from_template(template="How to cook {recipe}?")

chain = question | llm

response = chain.invoke({"recipe": "boiled egg"})

print(response)
