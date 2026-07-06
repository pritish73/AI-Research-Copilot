from pdf_loader import add_new_paper
import os
import numpy as np
from prompts import *
from intent_router import detect_intent
from ollama import chat
from embedder import generate_embeddings
from conversation_manager import ConversationManager
from vector_store import (
    create_faiss_index,
    search_index,
    save_index,
    load_index
)
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

PAPER_DIR = BASE_DIR / "papers"
# ==================================================
# AUTONOMOUS RESEARCH AGENT
# ==================================================
#
# Workflow:
#
# Research Papers
#        ↓
# Chunk Loading
#        ↓
# Embedding Generation
#        ↓
# FAISS Vector Database
#        ↓
# User Question
#        ↓
# Semantic Retrieval
#        ↓
# Llama 3
#        ↓
# Final Answer
#
# ==================================================

from core import initialize

(
    all_chunks,
    chunk_texts,
    index,
    conversation,
    conversation_history,
    conversation_state
) = initialize()

def ask_question(query):

    global conversation_history
    global conversation_state
    global all_chunks
    global chunk_texts
    global conversation
    global index

    # Everything from inside the while loop

def test():
    return "Research Engine Loaded!"