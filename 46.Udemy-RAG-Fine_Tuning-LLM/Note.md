1. RAG is a powerful framework for retrieving and generating natural languages with LLMs. It contains both retrieval and generation based approaches.

Retrieval based approaches use large collection of documents or knowledge sources to find relevant information for a given query or context. 

Generative approaches use large neural networks or language models to generate natural languages.

2. RAG helps LLM to avoid repetition or hallucinations which is a common problem with generative models to produce low quality and inaccurate answers. 

3. Challenges and Limitations of RAG:

- How to choose and prepare a suitable knowledge source for RAG ?
- How to fine-tune a RAG model on a particular task  or domain ?
- How to evaluate the performance and quality of RAG models ?
- How to optimize the RAG model for speed and efficiency ?
- How to scale and serve a RAG model in a production environment ?
- How to use RAG with other techniques such as prompt engineering, lexical search and re-ranking etc ?

4. RAG framework consists of 3 main components:

- A query encoder
- A retriever 
- A generator

A. Query Encoder:

It is a neural network that encodes the input query or context into a vector representation. It can be any pre-trained language model such as BERT, T5 etc. Query encoder is responsible for capturing meaning and intent from the input and providing a compact and representation that can be used for retriever and generation. 

B. Retriever:

A retriever is a system that uses the query vector to search for and retrieve relevant documents from the knowledge source. 

Retriever can be based on different methods such as:

- Exact match
- TF-IDF
- BM25
- Dense Vector Similarity etc.

Retriever is responsible for finding and ranking the most informative and relevant document that can provide the additional knowledge and facts for input query or context.

C. Generator:

It is a neural network that decodes the query vector and the retrieved documents to the natural language output. The generator can be any sequence-to-sequence model such as GPT-3, BERT, T5 etc. Generator is responsible for generating natural language output based on the input query and retrieved documents.

5. The RAG framework can be implemented in different ways depending on how the retriever and generator interact with each other. There are 2 main variants of RAG as:

- RAG token
- RAG Sequence

[See the attached pdfs for more details]