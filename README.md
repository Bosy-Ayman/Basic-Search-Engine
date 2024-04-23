# Basic Search Engine

## Overview

This project aims to design and implement a basic search engine for a collection of text documents. The search engine will allow users to input queries and retrieve relevant documents from the corpus. The project will involve data collection, preprocessing, indexing, query processing, query expansion, user interface development, and evaluation of the search engine's performance.

## Project Procedures

### 1. Data Collection

- Gather a set of text documents to serve as the corpus. This could include articles, web pages, or any other textual content.
- Ensure the documents are in a format that can be easily parsed and indexed.

### 2. Preprocessing

- **Tokenization**: Split documents into individual words or tokens.
- **Lowercasing**: Convert all text to lowercase for case insensitivity.
- **Stopword Removal**: Eliminate common words (e.g., "and", "the", "is") that do not contribute much to the meaning of the document.
- **Stemming or Lemmatization**: Reduce words to their base or root form (e.g., "running" to "run").

### 3. Indexing

- Build an inverted index.
- Create a data structure that maps each unique word (or term) to the documents that contain that word.
- Maintain a list of document IDs for each term along with the frequency of occurrence.

### 4. Query Processing

- Implement a simple query processing with expanded capabilities.
- Parse user queries and apply preprocessing steps (tokenization, lowercase, etc.).
- Identify relevant documents using the inverted index.
- Retrieve documents that contain all terms from the query.
- Rank retrieved documents based on a ranking algorithm (e.g., TF-IDF).

### 5. Query Expansion

- Apply relevance feedback by analyzing top-ranked documents for initial queries.
- Incorporate synonyms or related terms using pre-built mappings or embeddings (e.g., ELMo and BERT).

### 6. User Interface

- Develop a basic user interface to interact with the search engine.
- Accept user queries.
- Display relevant search results.

### 7. Evaluation

- Evaluate the performance of the search engine:
  - Test with various queries to assess retrieval accuracy and speed.

## Usage

To use the search engine:
1. Ensure the corpus is collected and stored in a suitable format.
2. Run the preprocessing steps to tokenize, lowercase, remove stopwords, and perform stemming/lemmatization.
3. Build the inverted index based on the preprocessed documents.
4. Implement query processing to handle user queries and retrieve relevant documents.
5. Incorporate query expansion techniques for enhanced search results.
6. Develop a user interface for easy interaction with the search engine.
7. Evaluate the performance by testing with diverse queries and measuring retrieval accuracy and speed.


## Acknowledgments

- [Pyterrier](https://pyterrier.readthedocs.io/en/latest/terrier-index-api.html)
- [NLTK](https://www.nltk.org/)
