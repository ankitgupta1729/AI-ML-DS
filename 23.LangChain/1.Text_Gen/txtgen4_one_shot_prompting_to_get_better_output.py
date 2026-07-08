from langchain_community.llms import LlamaCpp
from langchain_core.prompts import PromptTemplate

llm = LlamaCpp(
    model_path=r"/Users/ankit/Workspace/Projects/ankit-github/AI-ML-DS/23.LangChain/Text_Gen/mistral-7b-v0.1.Q8_0.gguf",
    temperature=0.75,
    max_tokens=2000,
    top_p=1,
    verbose=False,
)

question = PromptTemplate.from_template(template=
                                        '''
                                        Q: How to cook Boiled Egg?
                                        A: - Choose Fresh Egs
                                           - Bring Eggs to room temperature
                                           - Boil the water
                                           - Add eggs to boiling water
                                           - Cool Eggs
                                        
                                        Q: "How to cook {recipe}?''')

chain = question | llm.bind(stop=["Q:"])

for chunk in chain.stream({"recipe": "French Fries"}):
    print(chunk, end="", flush=True)

# Now, we get the answer in the given structured way as mentioned in the example.