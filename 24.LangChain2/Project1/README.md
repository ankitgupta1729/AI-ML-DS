## Project : Create a streamlit application
....
>  
This is a Python application that uses the OpenAI API to generate text based on a user's input.

## **Install Python** ![Python](img/python_65.png)

A [Quick Guide for Installing](https://github.com/PackeTsar/Install-Python/blob/master/README.md#install-python-) Python on Common Operating Systems

....

## Create a virtual environment :

**MacOS/Linux**:
```
python3 -m venv env
```
**Windows**:
```
python -m venv env
```

## Activate the virtual environment :
**MacOS/Linux**:
```
source env/bin/activate
```
**Windows**:
```
.\env\Scripts\activate
```

## Installation: Install the necessary dependencies by running the following command:
**MacOS/Linux**:
```
pip3 install -r requirements.txt
pip3 install -U langchain-community
pip3 install -U langchain-openai
```
**Windows**:
```
pip install -r requirements.txt
pip install -U langchain-community
pip install -U langchain-openai
```

## [Get an API key](https://platform.openai.com/account/api-keys)

### Set the key as an environment variable:
Additionally, you need to obtain an OpenAI API key and add it to the `.env` file.

`export OPENAI_API_KEY='sk-brHeh...A39v5iXsM2'`

```
OPENAI_API_KEY=sk-brHeh...A39v5iXsM2
```

## Run the script:

Run the CLI version:
**MacOS/Linux**:
```
python3 main.py
```
**Windows**:
```
python main.py
```

Run the Streamlit web app (opens in your browser at http://localhost:8501):
```
streamlit run app.py
```
Note: do not run `python app.py` directly — Streamlit apps must be launched
through the `streamlit` CLI so the script-runner context is initialized.

## Contributing
This repository is intended for educational purposes only and is not designed to accept external contributions. It serves as supplemental material for the YouTube tutorial, demonstrating how to build the project.

For any suggestions or improvements related to the tutorial content, please feel free to reach out through the YouTube channel's comment section.
