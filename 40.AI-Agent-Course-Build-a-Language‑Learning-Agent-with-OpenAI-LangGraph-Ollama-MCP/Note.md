1. First create a virtual environment with python 3.13 using `uv python install 3.13` and `uv init`.

2. Use the `https://github.com/eymenefealtun/all-words-in-all-languages` repo for data.  You can use the kaggle datasets or UC Irvine datasets(https://archive.ics.uci.edu/datasets) also. 

3. Create a folder `intelligent-learning-agent` and in that run `mkdir raw-word-lists` to create the folder.

Run the following code to copy the data.

```
cd "40.AI-Agent-Course-Build-a-Language‑Learning-Agent-with-OpenAI-LangGraph-Ollama-MCP/language-learning-agent"
mkdir -p raw-word-lists
cp -r ../all-words-in-all-languages/{Catalan,Croatian,Danish,Dutch,English,Finnish,French,German,Greek,Italian,Polish,Portuguese,Romanian,Russian,Slovenian,Spanish,Swedish,Ukranian} raw-word-lists/
```

4. Install packages using `uv add pandas ipywidgets spacy spacy-transformers wordfreq python-dotenv typing-extensions langchain langchain_core langgraph langchain-openai langchain-ollama langchain-mcp-adapters matplotlib` in terminal under the `language-learning-agent` folder.

5.  

First, run the code from clean-word-lists.ipynb to clean the data. Spacy is a family of libraries to process text data in natural languages like english. Here we use lemmatization. Spacy supports some languages which can be checked here `https://spacy.io/models` that's why we use some languages in above `cp` command.

Select the accurate model instead of efficient from here `https://spacy.io/models` because here accuracy matters.

We use zipf's law to find rare words and use wordfreq library to find rare words.