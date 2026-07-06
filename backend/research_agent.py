from pdf_loader import add_new_paper
import os
import numpy as np


import re
from pathlib import Path
from agent import ResearchAgent
from chat_service import ask_question

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

while True:

    query = input(
        "\nAsk a question (or type 'exit'): "
    )
    if query.lower() == "exit":
        break

    # ==============================================
    # ADD NEW PAPER
    # ==============================================

    if query.lower() == "/add":

        pdf_name = input(
            "\nEnter PDF name (inside papers folder): "
        )

        pdf_path = os.path.join(
            "papers",
            pdf_name
        )

        if not os.path.exists(pdf_path):

            print("\nPDF not found.")

            continue

        try:

            paper_name, new_chunks = add_new_paper(pdf_path)

            print("\n✅ Paper indexed successfully.")
            print("Restart the assistant to start querying it.")

        except Exception as e:

            print(f"\n❌ Error: {e}")

        continue


    result = ask_question(query)

    print("\n")
    print("=" * 100)
    print("ANSWER")
    print("=" * 100)

    print(result["answer"])

    print("\n")
    print("=" * 100)
    print("SOURCES")
    print("=" * 100)

    for source in result["sources"]:
        print(source)