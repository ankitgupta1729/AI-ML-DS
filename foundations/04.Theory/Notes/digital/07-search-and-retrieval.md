# LLM University: Search & Retrieval

## Semantic Search: Lexical Search vs Embeddings
<!-- pages: 276-280 -->

![Keyword search finds only documents that share the query's words; semantic search finds all documents that are close in meaning](figures/keyword-vs-semantic.svg)

- Here you'll learn how to use embeddings and similarity in order to build a **semantic search** model.
- Semantic search is a powerful way to search in large databases using the **context of the query**.

### What Is Not Semantic Search? (Lexical Search)

**Lexical search** is word matching.

*Example* — query: *"Where was the last world cup?"* Sentences in the dataset:

| Sentences |
| --- |
| The last world cup was in Qatar |
| The sky is blue |
| The bear lives in the woods |
| An apple is a fruit |

- It is basically **word matching**. The idea is to search in the dataset for the answer, or at least the closest things to an answer. So let's say that the possible answers are: "The last world cup was in Qatar", "The sky is blue", "The bear lives in the woods", "An apple is a fruit".
- The way lexical search works is by word matching: it looks at which words from the query appear in the answer, and counts them. So:

| Sentence | Matching words | Count |
| --- | --- | ---: |
| 1st: The last world cup was in Qatar | The, last, world, cup, was | **5** |
| 2nd: The sky is blue | The | 1 |
| 3rd: The bear lives in the woods | The … the | 1 |
| 4th: An apple is a fruit | nothing is matching | 0 |

The count is highest for the first sentence, so this time it did okay and actually found the answer.
