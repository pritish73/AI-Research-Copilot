import faiss
import numpy as np


# ==============================================
# SAVE FAISS INDEX
# ==============================================

def save_index(index, path):

    faiss.write_index(
        index,
        str(path)
    )


# ==============================================
# LOAD FAISS INDEX
# ==============================================

def load_index(path):

    return faiss.read_index(
        str(path)
    )


# ==============================================
# CREATE NEW FAISS INDEX
# ==============================================

def create_faiss_index(embeddings):

    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(embeddings)

    return index


# ==============================================
# SEARCH INDEX
# ==============================================

def search_index(index, query_embedding, k=3):

    query_embedding = np.array(
        [query_embedding],
        dtype=np.float32
    )

    distances, indices = index.search(
        query_embedding,
        k
    )

    return distances, indices