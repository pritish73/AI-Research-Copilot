from prompts import *
from intent_router import detect_intent
from ollama import chat
from embedder import generate_embeddings
from vector_store import search_index
import time
from core import initialize
from reranker import rerank

def ask_question(query):

    start_time = time.time()

    (
        all_chunks,
        chunk_texts,
        index,
        conversation,
        conversation_history,
        conversation_state
    ) = initialize()

    conversation_history.append(
        {
            "role": "user",
            "content": query
        }
    )

    intent = detect_intent(query)

    use_previous_context = conversation.is_follow_up(query)

    query = conversation.resolve_query(query) 


    # ==============================================
    # SEARCH FAISS
    # ==============================================

    if intent == "literature_review":
        k = 30

    elif intent == "summary":
        k = 20

    elif intent == "comparison":
        k = 20

    elif intent == "research_gap":
        k = 20

    else:
        k = 20

    if use_previous_context and conversation_state["last_chunks"]:

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

        for idx in indices[0]:

            if idx == -1:
                continue

            retrieved_results.append(all_chunks[idx])

        retrieved_results = rerank(
            query,
            retrieved_results,
            top_k=8
        )

        conversation_state["last_chunks"] = retrieved_results   

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
    processing_time = round(time.time() - start_time, 2)
    
    unique_sources = list(set(sources))

    if "information not found" in answer.lower():
        unique_sources = []

    return {
        "success": True,
        "query": query,
        "intent": intent,
        "answer": answer,
        "sources": unique_sources,
        "processing_time": processing_time
    }