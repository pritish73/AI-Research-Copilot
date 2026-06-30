import os
import numpy as np
from prompts import *
from intent_router import detect_intent
from ollama import chat
from embedder import generate_embeddings
from conversation_manager import ConversationManager
from vector_store import (
    create_faiss_index,
    search_index,
    save_index,
    load_index
)
import re

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

print("\nLoading research papers...\n")

# ==================================================
# LOAD ALL CHUNKS
# ==================================================

all_chunks = []
chunk_texts = []

chunk_folder = "data/chunks"

for file in os.listdir(chunk_folder):

    path = os.path.join(
        chunk_folder,
        file
    )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        text = f.read()

    chunks = text.split(
        "===== CHUNK"
    )

    for chunk in chunks:

        chunk = chunk.strip()

        if len(chunk) > 50:

            all_chunks.append(
                {
                    "paper": file,
                    "text": chunk
                }
            )

            chunk_texts.append(
                chunk
            )

print(
    f"Total Chunks Loaded: {len(all_chunks)}"
)
# ==================================================
# GENERATE OR LOAD EMBEDDINGS
# ==================================================

embedding_file = "data/embeddings.npy"

if os.path.exists(embedding_file):

    try:

        print("\nLoading saved embeddings...")

        embeddings = np.load(
            embedding_file
        )

    except Exception:

        print(
            "\nSaved embeddings are corrupted."
        )

        print(
            "Regenerating embeddings..."
        )

        embeddings = generate_embeddings(
            chunk_texts
        )

        np.save(
            embedding_file,
            embeddings
        )

        print(
            "\nEmbeddings saved."
        )

else:

    print(
        "\nGenerating embeddings..."
    )

    embeddings = generate_embeddings(
        chunk_texts
    )

    np.save(
        embedding_file,
        embeddings
    )

    print(
        "\nEmbeddings saved."
    )

print(
    f"Embedding Shape: {embeddings.shape}"
)

# ==================================================
# CREATE FAISS INDEX
# ==================================================

index_file = "data/faiss.index"

if os.path.exists(index_file):

    print(
        "\nLoading saved FAISS index..."
    )

    index = load_index(
        index_file
    )

else:

    print(
        "\nCreating FAISS Index..."
    )

    index = create_faiss_index(
        embeddings
    )

    save_index(
        index,
        index_file
    )

    print(
        "\nFAISS index saved."
    )

print(
    f"Vectors Stored: {index.ntotal}"
)

# ==================================================
# CHAT MEMORY
# ==================================================

conversation_history = []
# ==================================================
# CONVERSATION MANAGER
# ==================================================

conversation = ConversationManager()
# ==================================================
# QUESTION LOOP
# ==================================================
conversation_state = {
    "last_chunks": [],
    "last_sources": [],
    "last_intent": ""
}

while True:

    query = input(
        "\nAsk a question (or type 'exit'): "
    )
    if query.lower() == "exit":
        break
    conversation_history.append(
        {
            "role": "user",
            "content": query
        }
    )
    

    # ==============================================
    # DETECT USER INTENT
    # ==============================================

    intent = detect_intent(query)
    use_previous_context = conversation.is_follow_up(query)

    query = conversation.resolve_query(query)

    print(f"\nMode Selected : {intent}")
    print(f"\nResolved Query : {query}")  

    

    # ==============================================
    # SEARCH FAISS
    # ==============================================

    if intent == "literature_review":
        k = 20
    else:
        k = 3

    if use_previous_context and conversation_state["last_chunks"]:

        print("\nUsing previous retrieved papers...")

        retrieved_results = conversation_state["last_chunks"]

    else:
        # ==============================================
        # CONVERT QUESTION TO EMBEDDING
        # ==============================================
        
            
        query_embedding = generate_embeddings(
            [query]
        )[0]

        conversation_state["last_chunks"] = []

        distances, indices = search_index(
            index,
            query_embedding,
            k=k
        )

        retrieved_results = []

        conversation_state["last_chunks"] = []

        for idx in indices[0]:

            result = all_chunks[idx]

            retrieved_results.append(result)

            conversation_state["last_chunks"].append(result)    

    # ==============================================
    # BUILD CONTEXT
    # ==============================================

    context = ""

    sources = []
    for result in retrieved_results:

        sources.append(
            result["paper"]
        )

    context += f"""

        ==========================
        Paper
        ==========================

        {result['paper']}

        Content

        {result['text']}

        """
    conversation.update_topics_from_chunks(
        retrieved_results
    )
    conversation_state["last_sources"] = list(set(sources))
    conversation_state["last_intent"] = intent
    # ==============================================
    # BUILD CONVERSATION MEMORY
    # ==============================================

    memory = ""

    for msg in conversation_history[-6:]:

        memory += f"""
    {msg['role'].upper()}:
    {msg['content']}
    """
    
    if intent == "comparison":
      
        prompt = COMPARE_PROMPT.format(
            memory=memory,
            context=context,
            query=query
        )

    elif intent == "summary":

        prompt = SUMMARY_PROMPT.format(
            memory=memory,
            context=context,
            query=query
        )

    elif intent == "literature_review":

        prompt = REVIEW_PROMPT.format(
            memory=memory,
            context=context,
            query=query
        )

    elif intent == "research_gap":

        prompt = GAP_PROMPT.format(
            memory=memory,
            context=context,
            query=query
        )

    else:

        prompt = QA_PROMPT.format(
            memory=memory,
            context=context,
            query=query
        )

    # ==============================================
    # GENERATE ANSWER
    # ==============================================

    response = chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response["message"]["content"]
    conversation_history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
    # ==============================================
    # DISPLAY RESULTS
    # ==============================================

    print("\n")
    print("=" * 100)
    print("ANSWER")
    print("=" * 100)

    print(answer)

    print("\n")
    print("=" * 100)
    print("SOURCES")
    print("=" * 100)

    for source in set(sources):
        print(source)