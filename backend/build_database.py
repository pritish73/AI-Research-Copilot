from pathlib import Path
import numpy as np

from embedder import generate_embeddings
from vector_store import (
    create_faiss_index,
    save_index
)

# ==========================================
# PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

CHUNK_DIR = DATA_DIR / "chunks"

EMBEDDING_FILE = DATA_DIR / "embeddings.npy"

INDEX_FILE = DATA_DIR / "faiss.index"

# ==========================================
# LOAD CHUNKS
# ==========================================

all_chunks = []

for file in CHUNK_DIR.glob("*.txt"):

    with open(file, "r", encoding="utf-8") as f:

        text = f.read()

    chunks = text.split("===== CHUNK")

    for chunk in chunks:

        chunk = chunk.strip()

        if len(chunk) > 50:

            all_chunks.append(chunk)

print(f"\nChunks Loaded : {len(all_chunks)}")

# ==========================================
# GENERATE EMBEDDINGS
# ==========================================

print("\nGenerating embeddings...")

embeddings = generate_embeddings(all_chunks)

print(f"\nEmbeddings : {len(embeddings)}")

# ==========================================
# SAVE EMBEDDINGS
# ==========================================

np.save(
    EMBEDDING_FILE,
    embeddings
)

print("\nEmbeddings Saved")

# ==========================================
# CREATE FAISS
# ==========================================

print("\nCreating FAISS...")

index = create_faiss_index(
    embeddings
)

save_index(
    index,
    INDEX_FILE
)

print("\nFAISS Saved")

print("\nDatabase Rebuilt Successfully!")

print(f"""
------------------------------
Chunks      : {len(all_chunks)}
Embeddings  : {len(embeddings)}
Vectors      : {index.ntotal}
------------------------------
""")