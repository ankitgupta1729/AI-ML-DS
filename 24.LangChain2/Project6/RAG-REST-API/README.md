## 💻  Project : Deploy Application as a Web Service with Render

server deploying an OpenAI chat model and a chain to tell a joke about a topic.

## 🛠️ Requirements : PYTHON Installation & Setup

### Python 3.11

`brew install pyenv`
`pyenv install 3.11.11`

switch to Python 3.11

`pyenv local 3.11.11`

### 🌐 Create a virtual environment & activate the virtual environment :

**MacOS/Linux**:

```
python3 -m venv env
source env/bin/activate
```

**Windows**:

```
python -m venv env
.\env\Scripts\activate
```


### 🏗️ Installation:

#### Install Python 3.11

use pip3 on a Mac or Linux and pip on Windows

```
pip install -r requirements.txt
```

### [Get an API key](https://platform.openai.com/account/api-keys)

### Set OpenAI API Key as an environment variable:

`export OPENAI_API_KEY='sk-brHeh...A39v5iXsM2'`

.env file:

```
OPENAI_API_KEY=sk-brHeh...A39v5iXsM2
```

### Start the server:
`uvicorn main:app --reload`

### Test the RESTAPI 

joke/invoke
```
curl --location --request POST 'http://localhost:8000/joke/invoke' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "input": {
            "topic": "cats"
        }
    }'

```
joke/batch

```
curl --location --request POST 'http://localhost:8000/joke/batch' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "inputs": [
            {"topic": "cats"},
            {"topic": "dogs"}
        ]
    }'
```

### Try the Playground & Docs :

`http://localhost:8000/joke/playground/`
`http://localhost:8000/openai/playground/`


### Display a [documentation](https://python.langchain.com/docs/langserve#docss)

`http://localhost:8000/docs`

### Deploy Live to [Render](https://docs.render.com/deploy-fastapi)

For Render, make sure the service root is `24.LangChain2/Project6/RAG-REST-API` and use:

- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

This project includes a `.python-version` file that pins Render to Python `3.11`, which avoids `tiktoken==0.6.0` being built from source on Render's default Python `3.14`.

Do not install additional deployment packages outside `requirements.txt`. Keeping Render on the pinned dependency set prevents resolver drift and avoids incompatibilities such as `langserve==0.2.2` with newer `httpx` releases.
