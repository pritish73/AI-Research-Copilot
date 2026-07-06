from conversation_manager import ConversationManager
from database import get_database

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

def initialize():

    (
        all_chunks,
        chunk_texts,
        embeddings,
        index
    ) = get_database()

    return (
        all_chunks,
        chunk_texts,
        index,
        conversation,
        conversation_history,
        conversation_state
    )