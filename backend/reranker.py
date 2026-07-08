from sentence_transformers import CrossEncoder

print("Loading CrossEncoder...")

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank(query, retrieved_chunks, top_k=4):

    if not retrieved_chunks:
        return []

    pairs = [
        (query, chunk["text"])
        for chunk in retrieved_chunks
    ]

    scores = reranker.predict(pairs)

    ranked = sorted(
        zip(scores, retrieved_chunks),
        key=lambda x: x[0],
        reverse=True
    )

    return [
        chunk
        for _, chunk in ranked[:top_k]
    ]