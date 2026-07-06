# Research Copilot

An AI-powered Research Assistant that helps users interact with research papers using **Retrieval-Augmented Generation (RAG)**. Upload research papers, ask questions in natural language, generate summaries, compare papers, identify research gaps, and create literature reviews.

Built with **FastAPI**, **React**, **FAISS**, **Sentence Transformers**, **Cross-Encoder Reranking**, and **Llama 3 (Ollama)**.

---

## Features

- Upload research papers (PDF)
- Delete uploaded papers
- Ask questions about uploaded papers
- Generate paper summaries
- Compare multiple research papers
- Generate literature reviews
- Identify research gaps
- Conversational memory for follow-up questions
- Intent-based routing
- Semantic search using FAISS
- Cross-Encoder reranking for improved retrieval
- Modern React frontend
- FastAPI backend

---

# Architecture

```
                 User
                  │
                  ▼
          React Frontend
                  │
                  ▼
           FastAPI Backend
                  │
     ┌────────────┼────────────┐
     ▼            ▼            ▼
Intent Router   Memory     Paper Manager
     │
     ▼
 Vector Search (FAISS)
     │
     ▼
 Cross Encoder Reranker
     │
     ▼
  Llama 3 (Ollama)
     │
     ▼
 Generated Answer
```

---

# Tech Stack

### Frontend

- React
- Axios
- CSS

### Backend

- FastAPI
- Uvicorn
- PyMuPDF
- FAISS
- NumPy

### AI / ML

- Sentence Transformers
- Cross Encoder
- BAAI/bge-base-en-v1.5
- ms-marco-MiniLM-L-6-v2
- Ollama
- Llama 3

---

# Project Structure

```
Research-Copilot/

│
├── backend/
│   ├── data/
│   ├── papers/
│   ├── chunks/
│   ├── main.py
│   ├── database.py
│   ├── vector_store.py
│   ├── embedder.py
│   ├── chunker.py
│   ├── reranker.py
│   ├── chat_service.py
│   ├── conversation_manager.py
│   ├── intent_router.py
│   ├── prompts.py
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   └── ...
│
└── README.md
```

---

# RAG Pipeline

```
PDF Upload
     │
     ▼
Extract Text
     │
     ▼
Chunk Documents
     │
     ▼
Generate Embeddings
     │
     ▼
Store in FAISS
     │
     ▼
User Question
     │
     ▼
Embedding
     │
     ▼
FAISS Retrieval
     │
     ▼
Cross Encoder Reranking
     │
     ▼
Context Selection
     │
     ▼
Llama 3
     │
     ▼
Final Response
```

---

# Installation

## Clone the repository

```bash
git clone https://github.com/pritish73/autonomous-research-agent.git

cd autonomous-research-agent
```

---

## Backend

Create the environment:

```bash
conda create -n research_agent python=3.11

conda activate research_agent
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start Ollama:

```bash
ollama serve
```

Download the Llama 3 model:

```bash
ollama pull llama3
```

Run the backend:

```bash
uvicorn main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# Usage

1. Upload one or more research papers.
2. Wait for indexing to complete.
3. Ask questions in natural language.
4. Generate summaries, comparisons, literature reviews, or research gap analyses.

---

# Example Questions

```
Summarize this paper.

Explain the methodology.

Compare the uploaded papers.

What are the key contributions?

Identify research gaps.

Explain the Transformer architecture.

How does BERT differ from GPT?

Generate a literature review on attention mechanisms.
```

---

# Future Improvements

- Multiple chat sessions
- Chat history
- Streaming responses
- Export chat to PDF
- PDF viewer
- Citation highlighting
- OCR support for scanned PDFs
- Cloud deployment
- User authentication
- Multi-user support

---

# Author

**Pritish Dutta**

GitHub: https://github.com/pritish73

LinkedIn: https://www.linkedin.com/in/pritish-dutta-06aa43247/

---

# License

This project is intended for educational and research purposes.
