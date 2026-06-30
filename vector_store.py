import faiss
import numpy as np
import faiss

def save_index(index, path):

    faiss.write_index(
        index,
        path
    )


def load_index(path):

    return faiss.read_index(
        path
    )

def create_faiss_index(embeddings):

    # FAISS expects float32

    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    dimension = embeddings.shape[1]

    # L2 distance index

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(embeddings)

    return index

def search_index(index, query_embedding, k=3):

    import numpy as np

    query_embedding = np.array(
        [query_embedding],
        dtype=np.float32
    )

    distances, indices = index.search(
        query_embedding,
        k
    )

    return distances, indices