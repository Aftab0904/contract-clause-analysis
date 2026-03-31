# Contract AI Engine

An AI-powered system to analyze legal contracts using Retrieval-Augmented Generation (RAG).
The system can extract clauses, answer questions, and detect risks from real-world legal contracts.

---
## Tech Stack

<p align="center">
  <img src="https://img.shields.io/badge/Python-Backend-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Streamlit-Frontend-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/LangChain-RAG-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/ChromaDB-VectorDB-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Groq-LLM-orange?style=for-the-badge" />
</p>

## Project Status

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Type-Production%20Project-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Focus-RAG%20Systems-orange?style=for-the-badge" />
</p>

---
## Features

| Feature | Description |
|--------|------------|
| Clause Extraction | Extract 10+ legal clause categories |
| Q&A | Ask natural language questions |
| Risk Detection | Identify legal red flags |
| Source Tracking | Exact paragraph reference |
| Interactive UI | Streamlit-based interface |

---

## Problem Statement

Legal contracts are long and complex documents. Important clauses are often buried inside large text and expressed in different ways. Manual analysis is time-consuming and error-prone. 

This system solves that by automating the extraction and analysis process, allowing legal professionals to focus on high-level decision-making.

---

## Architecture Overview

```mermaid
flowchart TD

    %% ----------------------
    %% DATA LAYER
    %% ----------------------
    subgraph DATA_LAYER
        A[CUAD Dataset]
    end

    %% ----------------------
    %% INGESTION LAYER
    %% ----------------------
    subgraph INGESTION_LAYER
        B[Load JSON<br>ingest.py]
        C[Convert to Documents<br>ingest.py]
    end

    %% ----------------------
    %% PROCESSING LAYER
    %% ----------------------
    subgraph PROCESSING_LAYER
        D[Chunking Engine<br>chunk.py]
    end

    %% ----------------------
    %% EMBEDDING + STORAGE
    %% ----------------------
    subgraph VECTOR_LAYER
        E[Embedding Model<br>HuggingFace]
        F[Vector Store<br>vectorstore.py]
    end

    %% ----------------------
    %% RETRIEVAL LAYER
    %% ----------------------
    subgraph RETRIEVAL_LAYER
        G[Similarity Search<br>Chroma Retriever]
    end

    %% ----------------------
    %% REASONING LAYER
    %% ----------------------
    subgraph LLM_LAYER
        H[LLM Engine<br>Groq - LLaMA]
    end

    %% ----------------------
    %% APPLICATION LOGIC
    %% ----------------------
    subgraph APPLICATION_LAYER
        I[Clause Extraction<br>extract.py]
        J[Question Answering<br>ui.py]
        K[Risk Detection<br>ui.py]
    end

    %% ----------------------
    %% UI LAYER
    %% ----------------------
    subgraph UI_LAYER
        L[Streamlit UI<br>ui.py]
    end

    %% FLOW
    A --> B --> C --> D --> E --> F --> G --> H
    H --> I
    H --> J
    H --> K
    I --> L
    J --> L
    K --> L

    %% ----------------------
    %% STYLING
    %% ----------------------
    style A fill:#1f77b4,color:#fff

    style B fill:#2ca02c,color:#fff
    style C fill:#2ca02c,color:#fff
    style D fill:#2ca02c,color:#fff

    style E fill:#9467bd,color:#fff
    style F fill:#9467bd,color:#fff

    style G fill:#ff7f0e,color:#fff

    style H fill:#d62728,color:#fff

    style I fill:#17becf,color:#000
    style J fill:#17becf,color:#000
    style K fill:#17becf,color:#000

    style L fill:#000000,color:#fff
```


### How to Run

### 1. Clone the repository

git clone https://github.com/Aftab0904/contract-clause-analysis.git
cd contract-ai-engine  



### 2. Create virtual environment

python -m venv venv  
venv\Scripts\activate  


### 3. Install dependencies

pip install -r requirements.txt  


### 4. Setup environment variables

Create a `.env` file in the root directory:

GROQ_API_KEY=your_api_key_here  
LANGCHAIN_API_KEY=your_langsmith_key  
LANGCHAIN_TRACING_V2=true  

### 5. Run the application

streamlit run app/ui.py  

## Key Design Decisions

1. RAG Architecture  
Used Retrieval-Augmented Generation to ensure answers are grounded in contract data instead of hallucination.

2. Chunking Strategy  
Contracts are split into smaller chunks to handle long documents and improve retrieval accuracy.

3. Embedding-based Retrieval  
Semantic search is used instead of keyword matching to handle variation in legal language.

4. Contract-level Filtering  
Metadata-based filtering ensures queries are answered for a selected contract only.

5. Few-shot Prompting  
Examples are added in prompts to improve clause extraction accuracy.

6. Source Tracking  
Each output includes source location (contract and paragraph) for explainability.

## Limitations and Failure Modes

- Retrieval quality depends on chunking and embeddings
- Some clauses may not be detected if phrasing is highly different
- Performance may slow down with larger datasets
- LLM responses may vary slightly due to non-deterministic behavior


## Future Improvements

- Add re-ranking for better retrieval accuracy
- Support full dataset (510 contracts) with optimized indexing
- Add evaluation metrics such as precision and recall
- Improve UI with highlighted clauses
- Add multi-contract comparison

## Tech Stack

- Python  
- Streamlit  
- LangChain  
- ChromaDB  
- HuggingFace Embeddings  
- Groq LLM  

---

## Dataset

CUAD (Contract Understanding Atticus Dataset)

- 510 real contracts  
- 41 clause categories  
- Sourced from SEC EDGAR filings  

---
## Key Learnings

- RAG system design  
- Prompt engineering  
- Retrieval optimization  
- LLM evaluation techniques  

---
## Conclusion

This project demonstrates how AI can simplify legal document analysis using RAG pipelines, enabling faster and more accurate contract understanding.

---
## Demo

<p align="center">
  <img src="assets/question.png" width="45%" />
  <img src="assets/extract.png" width="45%" />
</p>

<p align="center">
  <img src="assets/liability.png" width="45%" />
  <img src="assets/riskdetection.png" width="45%" />
</p>

