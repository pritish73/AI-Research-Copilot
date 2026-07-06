import re


class ConversationManager:

    FOLLOW_UP_WORDS = [
        "it",
        "its",
        "this",
        "that",
        "those",
        "these",
        "they",
        "them",
        "previous",
        "above",
        "former",
        "latter"
    ]

    def __init__(self):

        self.last_topics = []

    # ==========================================
    # CHECK IF FOLLOW-UP QUESTION
    # ==========================================

    def is_follow_up(self, query):

        words = re.findall(
            r"\b\w+\b",
            query.lower()
        )

        return any(
            word in self.FOLLOW_UP_WORDS
            for word in words
        )

    # ==========================================
    # UPDATE DISCUSSION TOPICS
    # ==========================================

    def update_topics_from_chunks(self, retrieved_results):

        self.last_topics = []

        pattern = r"\b(?:[A-Z][a-zA-Z0-9\-]+|[A-Z]{2,}[0-9\-]*)\b"

        for result in retrieved_results:

            text = result["text"]

            matches = re.findall(pattern, text)

            for match in matches:

                if len(match) < 3:
                    continue

                if match not in self.last_topics:
                    self.last_topics.append(match)

        self.last_topics = self.last_topics[:20]

    # ==========================================
    # RESOLVE FOLLOW-UP QUESTIONS
    # ==========================================

    def resolve_query(self, query):

        if len(self.last_topics) == 0:
            return query

        # --------------------------------------
        # it
        # --------------------------------------

        query = re.sub(
            r"\bit\b",
            self.last_topics[-1],
            query,
            flags=re.IGNORECASE
        )

        # --------------------------------------
        # its
        # --------------------------------------

        query = re.sub(
            r"\bits\b",
            self.last_topics[-1] + "'s",
            query,
            flags=re.IGNORECASE
        )

        # --------------------------------------
        # this paper
        # --------------------------------------

        query = re.sub(
            r"\bthis paper\b",
            self.last_topics[-1],
            query,
            flags=re.IGNORECASE
        )

        # --------------------------------------
        # previous paper
        # --------------------------------------

        query = re.sub(
            r"\bprevious paper\b",
            self.last_topics[-1],
            query,
            flags=re.IGNORECASE
        )

        # --------------------------------------
        # which one
        # --------------------------------------

        if len(self.last_topics) >= 2:

            query = re.sub(
                r"\bwhich one\b",
                f"{self.last_topics[-2]} or {self.last_topics[-1]}",
                query,
                flags=re.IGNORECASE
            )

        return query