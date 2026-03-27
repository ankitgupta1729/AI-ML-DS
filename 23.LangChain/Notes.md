[Udemy Course]

1. In this course, we would discuss about LLMs, Chains, Prompts, Memory, RAG, Agents, tools and much more.

2. Here, we use Mistral and Llama2 models as LLMs and libraries we use as LlamaCpp for loading GGUF Quantized models and HuggingFace Transformers library for loading Original models.

3. LangChain was launched in October 2022 as an open source project by Haris and Chase. It is framework tailored to developing applications leveraging large language models (LLMs). It provides python and javascript libraries serving as a central hub for large language models (LLM) development. It is integrated with the external data sources like Pinecone, Chromadb and also it is integrated with various workflows. 

4. It is launched in October 2022 and became the fastest growing open source project on github (https://github.com/langchain-ai/langchain). By June 2023, it is playing a vital role in popularizing Generative AI alongside release of OpenAI's ChatGPT. LangChain supports various LLM use cases like grom chatbot to intelligent search and summarization services. 

5. How to Generate Text using an LLM:

here, we will be downloading open source GGUF models from HuggingFace and to load the models we will be using LlamaCpp. The reason to use GGUF models is that we can run the models on CPU.  

![How to Generate Text using an LLM](images/img1.png)

6. Now, go to 23.LangChain folder using `cd 23.LangChain` and then create and activate virtual environment using `pipenv install` and `pipenv shell`.

Now, install 2 libraries `pipenv install langchain llama-cpp-python`.

Here, we are using `Mistral-7B-v0.1-GGUF` model. There are various quantized models are there of this category in HF(HuggingFace) Hub.

Download one of the these models from HuggingFace Hub. 

7. 