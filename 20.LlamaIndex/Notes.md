[LlamaIndex Udemy Course by Eden Marco]

1. Large Language Models are powerful however they have some limitations.

For example, if I ask questions like "How much did I pay in Serpapi in June ?" to ChatGPT with GPT-3.5, it will
not answer because it was not trained on this data but if I use GPT-4 and ask the question by attaching the invoice file, I will get the answer. 


2. LlamaIndex is a powerful framework for developing LLM based applications. It is open source and very intuitive to use. On github, it has more popularity (based number of stars) than langchain(a framework to develop LLM based applications)

LlamaIndex is used to connect with our private data in pdf,ppt,doc,image,audio,video etc as well as various data 
connectors API like notion, salesforce data, discord etc as well as various databases like snowflake,mongodb, postgresql etc.

LlamaIndex can also interact with vectorstores like milvus etc.

If we have a very large document then we have to do chunking and make various chunks because LLMs have token limits, also for a question, we also might not need all the documents, so we may get answer from a one specific
chunk or 2-3 chunks etc and we only send these specific chunks as context to LLM then LLM will answer it.

We store these chunks into a vector store/vector db and we can retrieve relevant chunks based on the query/question.

3. We have different data connectors (LlamaHub). A data connector(i.e. reader) ingest data from different data sources and data formats into a simple `Document` representation (text and simple data).

Once you have ingested your data, you can build an `index` on top, ask question using a `Query Engine` and 
have a conversation using `Chat Engine`.

4. Our data connectors are offered through `LlamaHub`. LlamaHub is an open source repository containing data loaders that you can easily plug and play into any LlamaIndex application.

5. Documents/Nodes:
   
Document and Node objects are core abstractions within LlamaIndex.

A `Document` is a generic container around any data source - for instance a PDF, an API output or retrieved data from a database. They can be constructed manually or created automatically via data loaders. By default, a Document stores text along with some other attributes like metadata (a dictionary of annotations that can be appended to the text) or relationships(a dictionary containing relationships to other Documents/Nodes).

A `Node` represents a "chunk" of a source document whether it is a text chunk or an image or other. Similar to Documents they contain metadata and relationship information to other nodes.

Node and chunk are same.

Nodes are a first-class citizen in LlamaIndex. You can choose to define Nodes and its attributes directly. You may
also choose to "parse" source documents into Nodes through our `NodeParser` classes. By default, every Node 
derived from a Document will inherit the same metadata from that Document (e.g. a "file_name" filed in the Document is propagated to every Node.)

6. Node Parser:

Node parsers are a simple abstraction that take a list of documents and chunk them into a Node objects, such that each node is a specific size. 

A node parser can configure the chunk size (in tokens) as well as any overlap between chunked nodes. The chunking is done by `TokenTextSplitter` which default to a chunk size of 1024 and a default chunk overlap of 20 tokens.


7. Indexes:

An `Index` is a data structure that allows us to quickly retrieve relevant context for a user query.

For LlamaIndex, it's the core foundation for RAG use-cases.

At a high level, `indices` are built from `Documents`. They are used to build `Query Engines` and `Chat Engines`.
which enables question and answer and chat over your data.

Under the hood, `Indices` store data in `Node` objects and expose a `Retrieval` interface that supports additional 
automation and configuration.

8. Query Engine:

Query engine is a generic interface that allows you to ask questions over your data.

A query engine takes a natural language query and returns a rich response. It is most often built on one or many indices via Retrievals. You can compose multiple query engines to achieve more advanced capability.

9. LlamaIndex is the leading framework for building LLM-powered agents over your data with [LLMs](https://en.wikipedia.org/wiki/Large_language_model) and [workflows](/python/llamaagents/workflows).

<div class="grid cards" markdown>

- <span style="font-size: 200%">[Introduction](#introduction)</span>

  What is context augmentation? What are agents and workflows? How does LlamaIndex help build them?

- <span style="font-size: 200%">[Use cases](#use-cases)</span>

  What kind of apps can you build with LlamaIndex? Who should use it?

- <span style="font-size: 200%">[Getting started](#getting-started)</span>

  Get started in Python or TypeScript in just 5 lines of code!

- <span style="font-size: 200%">[LlamaCloud](https://docs.cloud.llamaindex.ai/)</span>

  Managed services for LlamaIndex including [LlamaParse](https://developers.llamaindex.ai/python/cloud/llamaparse/), the world's best document parser.

- <span style="font-size: 200%">[Community](#community)</span>

  Get help and meet collaborators on Discord, Twitter, LinkedIn, and learn how to contribute to the project.

- <span style="font-size: 200%">[Related projects](#related-projects)</span>

  Check out our library of connectors, readers, and other integrations at [LlamaHub](https://llamahub.ai) as well as demos and starter apps like [create-llama](https://www.npmjs.com/package/create-llama).

</div>

## Introduction

### What are agents?

[Agents](/python/framework/understanding/agent) are LLM-powered knowledge assistants that use tools to perform tasks like research, data extraction, and more. Agents range from simple question-answering to being able to sense, decide and take actions in order to complete tasks.

LlamaIndex provides a framework for building agents including the ability to use RAG pipelines as one of many tools to complete a task.

### What are workflows?

[Workflows](/python/llamaagents/workflows) are multi-step processes that combine one or more agents, data connectors, and other tools to complete a task. They are event-driven software that allows you to combine RAG data sources and multiple agents to create a complex application that can perform a wide variety of tasks with reflection, error-correction, and other hallmarks of advanced LLM applications. You can then [deploy these agentic workflows](/python/workflows/deployment/) as production microservices.

### What is context augmentation?

LLMs offer a natural language interface between humans and data. LLMs come pre-trained on huge amounts of publicly available data, but they are not trained on **your** data. Your data may be private or specific to the problem you're trying to solve. It's behind APIs, in SQL databases, or trapped in PDFs and slide decks.

Context augmentation makes your data available to the LLM to solve the problem at hand. LlamaIndex provides the tools to build any of context-augmentation use case, from prototype to production. Our tools allow you to ingest, parse, index and process your data and quickly implement complex query workflows combining data access with LLM prompting.

The most popular example of context-augmentation is [Retrieval-Augmented Generation or RAG](/python/framework/getting_started/concepts), which combines context with LLMs at inference time.

### LlamaIndex is the framework for Context-Augmented LLM Applications

LlamaIndex imposes no restriction on how you use LLMs. You can use LLMs as auto-complete, chatbots, agents, and more. It just makes using them easier. We provide tools like:

- **Data connectors** ingest your existing data from their native source and format. These could be APIs, PDFs, SQL, and (much) more.
- **Data indexes** structure your data in intermediate representations that are easy and performant for LLMs to consume.
- **Engines** provide natural language access to your data. For example:
  - Query engines are powerful interfaces for question-answering (e.g. a RAG flow).
  - Chat engines are conversational interfaces for multi-message, "back and forth" interactions with your data.
- **Agents** are LLM-powered knowledge workers augmented by tools, from simple helper functions to API integrations and more.
- **Observability/Evaluation** integrations that enable you to rigorously experiment, evaluate, and monitor your app in a virtuous cycle.
- **Workflows** allow you to combine all of the above into an event-driven system far more flexible than other, graph-based approaches.

## Use cases

Some popular use cases for LlamaIndex and context augmentation in general include:

- [Question-Answering](/python/framework/use_cases/q_and_a) (Retrieval-Augmented Generation aka RAG)
- [Chatbots](/python/framework/use_cases/chatbots)
- [Document Understanding and Data Extraction](/python/framework/use_cases/extraction)
- [Autonomous Agents](/python/framework/use_cases/agents) that can perform research and take actions
- [Multi-modal applications](/python/framework/use_cases/multimodal) that combine text, images, and other data types
- [Fine-tuning](/python/framework/use_cases/fine_tuning) models on data to improve performance

Check out our [use cases](/python/framework/use_cases) documentation for more examples and links to tutorials.

### 👨‍👩‍👧‍👦 Who is LlamaIndex for?

LlamaIndex provides tools for beginners, advanced users, and everyone in between.

Our high-level API allows beginner users to use LlamaIndex to ingest and query their data in 5 lines of code.

For more complex applications, our lower-level APIs allow advanced users to customize and extend any module -- data connectors, indices, retrievers, query engines, and reranking modules -- to fit their needs.

## Getting Started

LlamaIndex is available in Python (these docs) and [Typescript](https://ts.llamaindex.ai/). If you're not sure where to start, we recommend reading [how to read these docs](/python/framework/getting_started/reading) which will point you to the right place based on your experience level.

### 30 second quickstart

Set an environment variable called `OPENAI_API_KEY` with an [OpenAI API key](https://platform.openai.com/api-keys). Install the Python library:

```bash
pip install llama-index
```

Put some documents in a folder called `data`, then ask questions about them with our famous 5-line starter:

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("Some question about the data should go here")
print(response)
```

If any part of this trips you up, don't worry! Check out our more comprehensive starter tutorials using [remote APIs like OpenAI](/python/framework/getting_started/starter_example) or [any model that runs on your laptop](/python/framework/getting_started/starter_example_local).

## LlamaCloud

If you're an enterprise developer, check out [**LlamaCloud**](https://llamaindex.ai/enterprise). It is an end-to-end managed service for document parsing, extraction, indexing, and retrieval - allowing you to get production-quality data for your AI agent. You can [sign up](https://cloud.llamaindex.ai/) and get 10,000 free credits per month, sign up for one of our [plans](https://www.llamaindex.ai/pricing), or [come talk to us](https://www.llamaindex.ai/contact) if you're interested in an enterprise solution. We offer both SaaS and self-hosted plans.

You can also check out the [LlamaCloud documentation](https://docs.cloud.llamaindex.ai/) for more details.

- **Document Parsing (LlamaParse)**: LlamaParse is the best-in-class document parsing solution. It's powered by VLMs and perfect for even the most complex documents (nested tables, embedded charts/images, and more). [Learn more](https://www.llamaindex.ai/llamaparse) or check out the [docs](https://docs.cloud.llamaindex.ai/llamaparse).
- **Document Extraction (LlamaExtract)**: Given a human-defined or inferred schema, extract structured data from any document. [Learn more](https://www.llamaindex.ai/llamaextract) or check out the [docs](https://docs.cloud.llamaindex.ai/llamaextract/getting_started).
- **Indexing/Retrieval**: Set up an e2e pipeline to index a collection of documents for retrieval. Connect your data source (e.g. Sharepoint, Google Drive, S3), your vector DB data sink, and we automatically handle the document processing and syncing. [Learn more](https://www.llamaindex.ai/enterprise) or check out the [docs](https://docs.cloud.llamaindex.ai/llamacloud/getting_started).

## Community

Need help? Have a feature suggestion? Join the LlamaIndex community:

- [Twitter](https://twitter.com/llama_index)
- [Discord](https://discord.gg/dGcwcsnxhU)
- [LinkedIn](https://www.linkedin.com/company/llamaindex/)

### Getting the library

- LlamaIndex Python
  - [LlamaIndex Python Github](https://github.com/run-llama/llama_index)
  - [Python Docs](https://docs.llamaindex.ai/) (what you're reading now)
  - [LlamaIndex on PyPi](https://pypi.org/project/llama-index/)
- LlamaIndex.TS (Typescript/Javascript package):
  - [LlamaIndex.TS Github](https://github.com/run-llama/LlamaIndexTS)
  - [TypeScript Docs](https://ts.llamaindex.ai/)
  - [LlamaIndex.TS on npm](https://www.npmjs.com/package/llamaindex)

### Contributing

We are open-source and always welcome contributions to the project! Check out our [contributing guide](https://github.com/run-llama/llama_index/blob/main/CONTRIBUTING.md) for full details on how to extend the core library or add an integration to a third party like an LLM, a vector store, an agent tool and more.

## LlamaIndex Ecosystem

There's more to the LlamaIndex universe! Check out some of our other projects:

- [llama_deploy](https://github.com/run-llama/llama_deploy) | Deploy your agentic workflows as production microservices
- [LlamaHub](https://llamahub.ai) | A large (and growing!) collection of custom data connectors
- [SEC Insights](https://secinsights.ai) | A LlamaIndex-powered application for financial research
- [create-llama](https://www.npmjs.com/package/create-llama) | A CLI tool to quickly scaffold LlamaIndex projects


10. documentation: https://github.com/run-llama/llama_index

python-dotenv: https://github.com/theskumar/python-dotenv and https://www.youtube.com/watch?v=8dlQ_nDE7dQ&t=210s

11. Project:

Use Python 3.11, since it's the most stable for LlamaIndex.



Go to VSCode Terminal and follow:

- create a project directory using `mkdir llamaindex-helloworld` and then go in it using `cd llamaindex-helloworld `
- Install pipenv using `pip3 install pipenv` [pipenv is a package manager that handle all the dependencies], check version using `pipenv --version`
- Type `ls` to see virtual environment 
- Now, you have to create vurtual environment using `pipenv shell` (type `exit` to go outside)

[If you don't have requirements.txt file and wants to create virtual environment using pipenv and python 3.11 then follow the following steps:

rm -f Pipfile Pipfile.lock

# Clear pipenv cache and tell it NOT to look for requirements.txt
export PIPENV_NO_INHERIT=true
export PIPENV_IGNORE_REQUIREMENTS=true

# Create a new pipenv environment with Python 3.11
pipenv --python 3.11

# Now install your packages
pipenv install llama-index python-dotenv

# Activate the environment
pipenv shell



]

- Now, install packages using `pipenv install llama-index python-dotenv` and `pipenv install llama-index-readers-web html2text`
- Now, create 2 files using `touch main.py .env`    
- run the code using `pipenv run python main.py `
- 

12.  