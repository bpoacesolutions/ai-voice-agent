class AgentBrain:
    def __init__(self, memory_store):
        self.memory_store = memory_store

    # -------------------------
    # MEMORY RETRIEVAL
    # -------------------------
    def retrieve_memory(self, query):
        raw_memory = self.memory_store.search(query, k=10)

        filtered = []

        for memory in raw_memory:

            if memory["distance"] < 1.5:
                filtered.append(memory["text"])

        return filtered[:6]

    # -------------------------
    # REFLECTION VALIDATION
    # -------------------------
    def validate_reflection(self, reflection):
        reflection = reflection.lower()

        banned_patterns = [
            "work-life balance",
            "likely",
            "probably",
            "maybe",
            "possibly"
        ]

        for pattern in banned_patterns:
            if pattern in reflection:
                return False

        if len(reflection) > 120:
            return False

        return True

    # -------------------------
    # PROMPT BUILDER
    # -------------------------
    def build_prompt(self, query, memory, history):
        memory_text = "\n".join(memory)

        history_text = "\n".join(history[-4:])

        return f"""
You are a helpful AI assistant.

Use the memory and conversation history
to answer accurately and consistently.

Memory:
{memory_text}

Conversation History:
{history_text}

User:
{query}

Assistant:
"""