from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
import shutil
import os
from remove_paper import remove_paper
from database import add_paper
from chat_service import ask_question
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from pathlib import Path
from database import get_database

app = FastAPI(
    title="Research Copilot API",
    description="AI-powered Research Paper Assistant using RAG, FAISS and Llama 3",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# REQUEST MODEL
# ==========================================

class ChatRequest(BaseModel):
    question: str


# ==========================================
# HOME
# ==========================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.get("/")
def home():

    return {
        "status": "running",
        "project": "Research Copilot",
        "version": "1.0.0"
    }


# ==========================================
# CHAT
# ==========================================

@app.post("/chat")
def chat(request: ChatRequest):
    return ask_question(request.question)

@app.get("/stats")
def stats():

    all_chunks, _, _, index = get_database()

    return {
        "papers": len(set(chunk["paper"] for chunk in all_chunks)),
        "chunks": len(all_chunks),
        "vectors": index.ntotal if index else 0
    }

import os

@app.get("/papers")
def get_papers():

    paper_folder = "papers"

    papers = []

    for file in os.listdir(paper_folder):

        if file.endswith(".pdf"):

            papers.append(file)

    return {
        "papers": sorted(papers)
    }

@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):

    # Only allow PDFs
    if not file.filename.endswith(".pdf"):
        return {
            "success": False,
            "message": "Only PDF files are allowed."
        }

    # Save uploaded file
    from pathlib import Path

    save_path = Path("papers") / file.filename

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Index the paper
    result = add_paper(save_path)

    return result

    return {
        "success": True,
        "message": "Paper uploaded successfully.",
        "filename": file.filename
    }

@app.delete("/paper/{paper_name}")
def delete_paper(paper_name: str):

    return remove_paper(paper_name)
    
BASE_DIR = Path(__file__).resolve().parent
PAPER_DIR = BASE_DIR / "papers"


@app.get("/pdf/{paper_name}")
def get_pdf(paper_name: str):

    pdf_path = PAPER_DIR / paper_name

    if not pdf_path.exists():
        return {
            "error": "PDF not found"
        }

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=paper_name
    )