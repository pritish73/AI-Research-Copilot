# Autonomous Research Agent

An AI-powered research assistant that processes academic research papers and enables semantic search using transformer-based embeddings and vector databases. The system converts research documents into searchable knowledge representations, forming the foundation for Retrieval-Augmented Generation (RAG), literature review automation, and research gap detection.

## Features

- PDF text extraction using PyMuPDF
- Automatic document chunking
- Transformer-based embedding generation
- FAISS vector database integration
- Semantic search over research papers
- Multi-paper knowledge retrieval
- Scalable architecture for future RAG and agentic workflows

## Tech Stack

- Python
- PyMuPDF
- Sentence Transformers
- PyTorch
- FAISS
- Hugging Face Transformers
- NumPy

## System Architecture

```text
Research Papers (PDFs)
            ↓
      Text Extraction
            ↓
        Chunking
            ↓
 Embedding Generation
            ↓
      FAISS Index
            ↓
     Semantic Search
            ↓
 Autonomous Research Agent
```

## Current Pipeline

```text
PDF
 ↓
Text
 ↓
Chunks
 ↓
Embeddings
 ↓
FAISS Vector Database
 ↓
Semantic Retrieval
```

## Implemented Components

### PDF Reader
Extracts textual content from academic research papers.

### Chunking Engine
Splits large research papers into overlapping chunks for efficient retrieval.

### Embedding Engine
Generates dense semantic vector representations using transformer-based embedding models.

### Vector Database
Stores embeddings using FAISS for high-performance similarity search.

### Semantic Search
Retrieves the most relevant research paper chunks based on meaning rather than keyword matching.

## Example Queries

- What is ReAct?
- How does self-attention work?
- What are the limitations of Retrieval-Augmented Generation?
- What is Toolformer?

## Example Workflow

```text
User Question
      ↓
Question Embedding
      ↓
FAISS Similarity Search
      ↓
Top Relevant Chunks
      ↓
Research Insights
```

## Project Structure

```text
Autonomous Research Agent/
│
├── papers/
├── data/
│   └── chunks/
│
├── pdf_reader.py
├── chunker.py
├── embedder.py
├── vector_store.py
├── paper_search.py
├── test_embed.py
├── test_faiss.py
├── search_test.py
├── README.md
└── .gitignore
```

## Future Roadmap

- Research Paper Question Answering
- Retrieval-Augmented Generation (RAG)
- Multi-Paper Comparison
- Literature Review Generation
- Research Gap Detection
- Multi-Agent Research Workflows
- Autonomous Research Report Generation

## Author

**Pritish Dutta**