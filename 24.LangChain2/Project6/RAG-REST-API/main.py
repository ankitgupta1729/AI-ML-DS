#!/usr/bin/env python
import os

from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langserve import add_routes
from langchain.schema.runnable import RunnableLambda
from dotenv import load_dotenv
from langchain.schema import AIMessage

load_dotenv()

# Use a harmless placeholder so the app can boot even if OPENAI_API_KEY
# is added after deploy creation; actual API calls will still require a real key.
model = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY", "missing-key"))
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")


def parseResponse(response: AIMessage) -> str:
    """Sample function that expects a Response type which is a pydantic model"""
    return response.content

# create server
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

# create runnable
chain = prompt | model | RunnableLambda(parseResponse)

# create routes
add_routes(
    app,
    model,
    path="/openai",
)

add_routes(
    app,
    chain,
    path="/joke",
)

# run server
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
