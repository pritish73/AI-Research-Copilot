from pathlib import Path
import os
import shutil
import numpy as np

from pdf_reader import extract_text
from chunker import create_chunks
from embedder import generate_embeddings

from vector_store import (
    create_faiss_index,
    save_index,
    load_index
)

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
PAPER_DIR = BASE_DIR / "papers"

CHUNK_DIR = DATA_DIR / "chunks"

EMBEDDING_FILE = DATA_DIR / "embeddings.npy"
INDEX_FILE = DATA_DIR / "faiss.index"

all_chunks = []
chunk_texts = []
embeddings = None
index = None

def build_database():

    global all_chunks
    global chunk_texts
    global embeddings
    global index

    print("\nBuilding Database...\n")

    all_chunks = []
    chunk_texts = []

    # -----------------------------------------
    # Read every chunk file
    # -----------------------------------------

    for file in CHUNK_DIR.glob("*.txt"):

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

        chunks = text.split("===== CHUNK")

        for chunk in chunks:

            chunk = chunk.strip()

            if len(chunk) > 50:

                all_chunks.append(
                    {
                        "paper": file.name,
                        "text": chunk
                    }
                )

                chunk_texts.append(chunk)

    print(f"Chunks Loaded : {len(all_chunks)}")

    # -----------------------------------------
    # Generate embeddings
    # -----------------------------------------

    print("\nGenerating Embeddings...")

    embeddings = generate_embeddings(
        chunk_texts
    )

    np.save(
        EMBEDDING_FILE,
        embeddings
    )

    print("Embeddings Saved")

    # -----------------------------------------
    # Create FAISS
    # -----------------------------------------

    print("\nCreating FAISS Index...")

    index = create_faiss_index(
        embeddings
    )

    save_index(
        index,
        INDEX_FILE
    )

    print("FAISS Saved")

    print(f"""

--------------------------------
Chunks      : {len(all_chunks)}
Embeddings  : {len(embeddings)}
Vectors     : {index.ntotal}
--------------------------------

""")

def load_database():

    global all_chunks
    global chunk_texts
    global embeddings
    global index

    print("\nLoading Database...\n")

    all_chunks = []
    chunk_texts = []

    # -----------------------------------------
    # Read all chunk files
    # -----------------------------------------

    for file in CHUNK_DIR.glob("*.txt"):

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

        chunks = text.split("===== CHUNK")

        for chunk in chunks:

            chunk = chunk.strip()

            if len(chunk) > 50:

                all_chunks.append(
                    {
                        "paper": file.name,
                        "text": chunk
                    }
                )

                chunk_texts.append(chunk)

    # -----------------------------------------
    # Load embeddings
    # -----------------------------------------

    embeddings = np.load(
        EMBEDDING_FILE
    )

    # -----------------------------------------
    # Load FAISS
    # -----------------------------------------

    index = load_index(
        INDEX_FILE
    )

    # -----------------------------------------
    # Verify database integrity
    # -----------------------------------------

    if not (
        len(all_chunks)
        ==
        len(embeddings)
        ==
        index.ntotal
    ):

        raise RuntimeError(
            f"""
Database Corrupted

Chunks      : {len(all_chunks)}
Embeddings  : {len(embeddings)}
Vectors     : {index.ntotal}

Run build_database().
"""
        )

    print(f"""

------------------------------
Database Loaded

Chunks      : {len(all_chunks)}
Embeddings  : {len(embeddings)}
Vectors     : {index.ntotal}
------------------------------

""")

def get_database():

    return (
        all_chunks,
        chunk_texts,
        embeddings,
        index
    )

def reload_database():

    build_database()

    load_database()

    print("\nDatabase Reloaded Successfully.\n")

def add_paper(pdf_file):

    # -----------------------------------------
    # Save PDF
    # -----------------------------------------

    destination = Path(pdf_file)

    print(f"\nProcessing: {destination.name}")

    # -----------------------------------------
    # Extract text
    # -----------------------------------------

    print("\nExtracting text...")

    text = extract_text(destination)

    # -----------------------------------------
    # Chunk
    # -----------------------------------------

    print("Creating chunks...")

    chunks = create_chunks(text)

    # -----------------------------------------
    # Save chunk file
    # -----------------------------------------

    chunk_file = CHUNK_DIR / f"{destination.stem}.txt"

    with open(
        chunk_file,
        "w",
        encoding="utf-8"
    ) as f:

        for i, chunk in enumerate(chunks):

            f.write(
                f"===== CHUNK {i+1} =====\n"
            )

            f.write(chunk)

            f.write("\n\n")

    print(f"Saved {len(chunks)} chunks")

    # -----------------------------------------
    # Rebuild database
    # -----------------------------------------

    reload_database()

    return {
        "success": True,
        "paper": destination.name,
        "chunks": len(chunks)
    }

if EMBEDDING_FILE.exists() and INDEX_FILE.exists():
    load_database()