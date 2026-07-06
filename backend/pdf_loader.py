import os
import numpy as np

from pdf_reader import extract_text
from chunker import create_chunks
from embedder import generate_embeddings

from vector_store import (
    load_index,
    save_index
)


# ============================================
# PATHS
# ============================================

CHUNK_FOLDER = "data/chunks"

EMBEDDING_FILE = "data/embeddings.npy"

FAISS_FILE = "data/faiss.index"


# ============================================
# ADD NEW PAPER
# ============================================

def add_new_paper(pdf_path):

    print("\nReading PDF...")

    text = extract_text(pdf_path)

    print("Creating chunks...")

    chunks = create_chunks(text)

    # ----------------------------------------

    filename = os.path.basename(pdf_path)

    chunk_filename = os.path.splitext(filename)[0] + ".txt"

    chunk_path = os.path.join(
        CHUNK_FOLDER,
        chunk_filename
    )

    print("Saving chunks...")

    with open(
        chunk_path,
        "w",
        encoding="utf-8"
    ) as f:

        for i, chunk in enumerate(chunks):

            f.write(
                f"===== CHUNK {i+1} =====\n"
            )

            f.write(chunk)

            f.write("\n\n")

    # ----------------------------------------

    print("Generating embeddings...")

    new_embeddings = generate_embeddings(
        chunks
    )

    # ----------------------------------------

    print("Loading old embeddings...")

    old_embeddings = np.load(
        EMBEDDING_FILE
    )

    embeddings = np.vstack(
        (
            old_embeddings,
            new_embeddings
        )
    )

    np.save(
        EMBEDDING_FILE,
        embeddings
    )

    # ----------------------------------------

    print("Updating FAISS index...")

    index = load_index(
        FAISS_FILE
    )

    index.add(
        np.array(
            new_embeddings,
            dtype=np.float32
        )
    )

    save_index(
        index,
        FAISS_FILE
    )

    print("\nDone!")

    print(f"Chunks Added : {len(chunks)}")
    print(f"Vectors Added : {len(new_embeddings)}")

    return chunk_filename, chunks