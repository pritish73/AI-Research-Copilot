def create_chunks(text, chunk_size=1000, overlap=200):

    # WHY CHUNKING?
    #
    # Research papers are very large.
    # LLMs and vector databases do not work efficiently
    # with entire papers.
    #
    # We split papers into smaller chunks.
    #
    # Later:
    # Chunk -> Embedding -> Vector DB
    #
    # When a user asks a question:
    #
    # Question
    #    ↓
    # Find relevant chunk
    #    ↓
    # Send chunk to LLM
    #    ↓
    # Generate answer
    #
    # This is the foundation of RAG.

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks