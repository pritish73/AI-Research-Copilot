# ==================================================
# INTENT ROUTER
# Detects what the user wants to do
# ==================================================

def detect_intent(query):

    query = query.lower()

    # Compare papers
    if "compare" in query or "difference" in query or "vs" in query:
        return "comparison"

    # Summarize
    elif "summarize" in query or "summary" in query:
        return "summary"

    # Literature review
    elif "literature review" in query or "review" in query:
        return "literature_review"

    # Research gaps
    elif "research gap" in query or "limitations" in query or "future work" in query:
        return "research_gap"

    # Default
    else:
        return "question"