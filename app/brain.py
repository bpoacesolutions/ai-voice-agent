class AgentBrain:
    def __init__(self, memory_store):
        self.memory_store = memory_store

    # -------------------------
    # MEMORY RETRIEVAL
    # -------------------------
    def retrieve_memory(self, query):
        raw_memory = self.memory_store.search(query, k=6)

        filtered_memory = [
            text for text, score in raw_memory
            if score < 1.5
        ]

        # fallback
        if len(filtered_memory) == 0 and len(raw_memory) > 0:
            filtered_memory = [raw_memory[0][0]]

        return filtered_memory

    # -------------------------
    # BUILD PROMPT
    # -------------------------
    def build_prompt(
        self,
        query,
        memory,
        history
    ):
        memory_text = "\n".join(memory)

        history_text = "\n".join(history[-4:])

        prompt = f"""
You are a helpful AI assistant.

You must use memory when relevant.

Memory:
{memory_text}

Conversation history:
{history_text}

User question:
{query}

Answer:
"""

        return prompt