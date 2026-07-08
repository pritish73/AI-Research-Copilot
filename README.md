# AI Research Copilot

AI Research Copilot is a Retrieval-Augmented Generation (RAG) application that enables users to upload research papers, search across multiple documents, and receive context-aware answers using Large Language Models.

The system combines semantic search, FAISS vector retrieval, CrossEncoder reranking, and Groq's Llama 3.3 model to provide accurate responses grounded in uploaded research papers.

---

## Features

- Upload and manage multiple PDF research papers
- Automatic PDF text extraction and intelligent chunking
- Semantic search using Sentence Transformers embeddings
- Fast similarity search with FAISS
- CrossEncoder reranking for improved retrieval quality
- Intent-aware prompting for different research tasks
- Conversational follow-up questions
- Multi-document Retrieval-Augmented Generation (RAG)
- Source citation for every response
- Modern React frontend
- FastAPI backend
- Groq Llama 3.3 integration for high-speed inference

---

## Supported Queries

The assistant can answer questions such as:

- Summarize this paper
- Explain the methodology
- Compare uploaded papers
- Find research gaps
- List the key contributions
- Suggest future work
- Answer technical questions about uploaded papers

---

## Architecture

```
User
   │
   ▼
React Frontend
   │
   ▼
FastAPI Backend
   │
   ▼
Intent Detection
   │
   ▼
Sentence Transformer Embeddings
   │
   ▼
FAISS Vector Search
   │
   ▼
CrossEncoder Re-ranking
   │
   ▼
Groq Llama 3.3
   │
   ▼
Grounded Response + Sources
```

---

## Tech Stack

### Frontend

- React
- Vite
- Axios
- React Markdown
- CSS

### Backend

- FastAPI
- Python
- Groq API
- Sentence Transformers
- FAISS
- PyMuPDF
- NumPy
- Scikit-learn

---

## Project Structure

```
AI-Research-Copilot
│
├── backend
│   ├── data
│   ├── papers
│   ├── main.py
│   ├── chat_service.py
│   ├── database.py
│   ├── reranker.py
│   ├── vector_store.py
│   ├── conversation_manager.py
│   └── ...
│
├── frontend
│   ├── src
│   ├── public
│   └── ...
│
├── requirements.txt
└── README.md
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/pritish73/AI-Research-Copilot.git

cd AI-Research-Copilot
```

---

### Backend

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r ../requirements.txt

uvicorn main:app --reload
```

---

### Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## Environment Variables

Create a `.env` file inside the `backend` directory.

```env
GROQ_API_KEY=your_groq_api_key
```

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/upload` | Upload PDF |
| DELETE | `/paper/{paper}` | Delete paper |
| GET | `/papers` | List uploaded papers |
| GET | `/stats` | Database statistics |
| POST | `/chat` | Ask a question |
| GET | `/pdf/{paper}` | Retrieve PDF |

---

## How It Works

1. Upload one or more research papers.
2. PDFs are converted into text.
3. Text is split into semantic chunks.
4. Embeddings are generated using Sentence Transformers.
5. FAISS indexes all vectors.
6. User questions are embedded.
7. Relevant chunks are retrieved.
8. CrossEncoder reranks retrieved passages.
9. Groq Llama 3.3 generates a grounded answer.
10. Sources are returned with every response.

---

## Future Improvements

- User authentication
- Persistent chat history
- Hybrid keyword + semantic search
- Streaming responses
- Support for DOCX and TXT files
- Research paper metadata extraction
- Citation export
- Cloud storage integration

---

## Author

**Pritish Dutta**

GitHub: https://github.com/pritish73

LinkedIn: https://www.linkedin.com/in/pritish-dutta-06aa43247

---

## License

This project is licensed under the MIT License.
