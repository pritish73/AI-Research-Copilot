    # WHY CHUNKING?
    #
    # Research papers are very large (often 5,000–30,000 words).
    # LLMs and vector databases do not work efficiently on entire papers.
    #
    # Example:
    # User asks:
    # "What is Multi-Head Attention?"
    #
    # If we store the entire paper as one embedding,
    # retrieval quality becomes poor because the embedding
    # represents the whole document.
    #
    # Instead we split the paper into smaller chunks:
    #
    # Paper
    #   ↓
    # Chunk 1
    # Chunk 2
    # Chunk 3
    # ...
    #
    # Each chunk gets its own embedding later.
    #
    # When a user asks a question:
    #
    # Question
    #   ↓
    # Find most relevant chunk
    #   ↓
    # Send chunk to LLM
    #   ↓
    # Generate answer
    #
    # This is the foundation of RAG
    # (Retrieval-Augmented Generation).
    #
    # chunk_size = maximum characters per chunk
    # chunk_overlap = repeated characters between chunks
    # to avoid losing context at boundaries
def create_chunks(text, chunk_size=1000, overlap=200):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks