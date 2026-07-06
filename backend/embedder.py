from sentence_transformers import SentenceTransformer

# WHY EMBEDDINGS?
#
# Computers do not understand text directly.
#
# We convert each chunk into a numerical vector.
#
# Example:
#
# "Attention is all you need"
#
# becomes
#
# [0.123, -0.555, 0.918, ...]
#
# Similar chunks produce similar vectors.
#
# Later:
#
# Question
#    ↓
# Embedding
#    ↓
# Similarity Search
#    ↓
# Relevant Chunks
#
# This is the foundation of Semantic Search and RAG.

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

def generate_embeddings(chunks):

    embeddings = model.encode(
        chunks,
        show_progress_bar=True
    )

    return embeddings