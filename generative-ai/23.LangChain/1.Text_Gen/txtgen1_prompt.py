import contextlib
import os

from langchain_community.llms import LlamaCpp
from langchain_core.prompts import PromptTemplate


@contextlib.contextmanager
def _suppress_stderr_fd():
    devnull_fd = os.open(os.devnull, os.O_WRONLY)
    saved_stderr_fd = os.dup(2)
    try:
        os.dup2(devnull_fd, 2)
        yield
    finally:
        os.dup2(saved_stderr_fd, 2)
        os.close(saved_stderr_fd)
        os.close(devnull_fd)


with _suppress_stderr_fd():
    llm = LlamaCpp(

    model_path=r"/Users/ankit/Workspace/Projects/ankit-github/AI-ML-DS/23.LangChain/Text_Gen/mistral-7b-v0.1.Q8_0.gguf",

    temperature=0.75,

    max_tokens=128,

    top_p=1,

    verbose=False,
)

question = "What is the capital of France?"
prompt = PromptTemplate.from_template(
    "Answer the question with ONLY the final answer (no extra text).\n"
    "Question: {question}\n"
    "Answer:"
)
response = llm.invoke(prompt.format(question=question), stop=["\nQuestion:"])
print(response)
